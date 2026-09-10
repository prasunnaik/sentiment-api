package com.insurewise.payments.service;

import com.insurewise.common.dto.*;
import com.insurewise.common.security.*;
import com.insurewise.payments.client.*;
import com.insurewise.payments.dto.request.PaymentCreateRequest;
import com.insurewise.payments.dto.response.PaymentResponse;
import com.insurewise.payments.entity.*;
import com.insurewise.payments.repository.PaymentRepository;
import java.math.BigDecimal;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;
import org.springframework.data.domain.*;
import org.springframework.security.core.parameters.P;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.insurewise.common.exception.IdempotencyKeyConflictException;
import com.insurewise.payments.exception.PaymentNotFoundException;


@Service
@Transactional
public class PaymentService {
    private static final DateTimeFormatter REF_TIME =
            DateTimeFormatter.ofPattern("yyyyMMddHHmmss");

    private final PaymentRepository paymentRepository;
    private final PaymentPolicyApplicationLookupClient applicationClient;
    private final PaymentDocumentService paymentDocumentService;

    public PaymentService(
            PaymentRepository paymentRepository,
            PaymentPolicyApplicationLookupClient applicationClient,
            PaymentDocumentService paymentDocumentService) {
        this.paymentRepository = paymentRepository;
        this.applicationClient = applicationClient;
        this.paymentDocumentService = paymentDocumentService;
    }

    public PaymentResponse makePayment(
            UUID customerId,
            PaymentCreateRequest request) {

        try {
            Optional<Payment> existing =
                    paymentRepository.findByIdempotencyKey(
                            request.idempotencyKey());

            if (existing.isPresent()) {
                Payment payment = existing.get();

                if (!payment.isOwnedBy(customerId)) {
                    throw new IdempotencyKeyConflictException(
                            "Idempotency key belongs to another customer");
                }

                return toResponse(payment);
            }

            PaymentPolicyApplicationSnapshot application =
                    applicationClient.getActiveApplicationForCustomer(
                            request.policyApplicationId(),
                            customerId);

            Payment payment = new Payment(
                    request.idempotencyKey(),
                    customerId,
                    application.applicationId(),
                    application.policyName(),
                    request.amount(),
                    request.method());

            Payment savedPayment = paymentRepository.save(payment);
            paymentDocumentService.createSystemReceipt(savedPayment.getId());

            return toResponse(savedPayment);

        } catch (Exception exception) {
            System.err.println(
                    "Error in PaymentService.makePayment: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public PageResponse<PaymentResponse> listPayments(
            JwtPrincipal principal,
            PaymentStatus status,
            int limit,
            int offset) {

        try {
            int safeLimit = Math.min(Math.max(limit, 1), 100);
            int safeOffset = Math.max(offset, 0);
            Pageable pageable = PageRequest.of(
                    safeOffset / safeLimit,
                    safeLimit,
                    Sort.by(Sort.Direction.DESC, "createdAt"));

            Page<Payment> page;

            if (principal.role() == JwtRole.CUSTOMER) {
                page = status == null
                        ? paymentRepository.findByCustomerId(
                        principal.userId(), pageable)
                        : paymentRepository.findByCustomerIdAndStatus(
                        principal.userId(), status, pageable);
            } else {
                page = status == null
                        ? paymentRepository.findAll(pageable)
                        : paymentRepository.findByStatus(status, pageable);
            }

            List<PaymentResponse> data = page.getContent()
                    .stream()
                    .map(this::toResponse)
                    .toList();

            return new PageResponse<>(
                    data,
                    new PaginationMetadata(
                            safeLimit,
                            safeOffset,
                            page.getTotalElements(),
                            safeOffset + data.size()
                                    < page.getTotalElements()));

        } catch (Exception exception) {
            System.err.println(
                    "Error in PaymentService.listPayments: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public PaymentResponse getPayment(
            JwtPrincipal principal,
            UUID paymentId) {

        try {
            Payment payment = paymentRepository.findById(paymentId)
                    .orElseThrow(() -> new PaymentNotFoundException(paymentId));

            if (principal.role() == JwtRole.CUSTOMER
                    && !payment.isOwnedBy(principal.userId())) {
                throw new PaymentNotFoundException();
            }

            return toResponse(payment);

        } catch (Exception exception) {
            System.err.println(
                    "Error in PaymentService.getPayment: "
                            + exception.getMessage());
            throw exception;
        }
    }

    private String generateTransactionRef() {
        int suffix = ThreadLocalRandom.current()
                .nextInt(100000, 1000000);

        return "TXN-"
                + LocalDateTime.now().format(REF_TIME)
                + suffix;
    }

    private PaymentResponse toResponse(Payment payment) {
        return new PaymentResponse(
                payment.getId(),
                payment.getIdempotencyKey(),
                payment.getCustomerId(),
                payment.getPolicyApplicationId(),
                payment.getPolicyNameSnapshot(),
                payment.getAmount(),
                payment.getMethod(),
                payment.getStatus(),
                payment.getTransactionRef(),
                payment.getPaidAt(),
                payment.getCreatedAt());
    }
}



package com.insurewise.payments.service;

import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.security.JwtPrincipal;
import com.insurewise.common.security.JwtRole;
import com.insurewise.common.service.S3StorageService;
import com.insurewise.payments.dto.response.PaymentDocumentResponse;
import com.insurewise.payments.entity.Payment;
import com.insurewise.payments.entity.PaymentDocument;
import com.insurewise.payments.entity.PaymentStatus;
import com.insurewise.payments.repository.PaymentDocumentRepository;
import com.insurewise.payments.repository.PaymentRepository;
import java.nio.charset.StandardCharsets;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import com.insurewise.common.exception.InvalidFileException;
import com.insurewise.common.exception.IdempotencyKeyConflictException;
import com.insurewise.payments.exception.PaymentDocumentNotFoundException;
import com.insurewise.payments.exception.PaymentDocumentStateException;
import com.insurewise.payments.exception.PaymentNotFoundException;
import com.insurewise.payments.exception.PaymentStateException;

@Service
@Transactional
public class PaymentDocumentService {
    private static final DateTimeFormatter RECEIPT_DATE_FORMAT =
            DateTimeFormatter.ISO_LOCAL_DATE_TIME;

    private final PaymentRepository paymentRepository;
    private final PaymentDocumentRepository documentRepository;
    private final S3StorageService storageService;

    public PaymentDocumentService(
            PaymentRepository paymentRepository,
            PaymentDocumentRepository documentRepository,
            S3StorageService storageService) {
        this.paymentRepository = paymentRepository;
        this.documentRepository = documentRepository;
        this.storageService = storageService;
    }

    public PaymentDocumentResponse uploadDocument(
            JwtPrincipal principal,
            UUID paymentId,
            MultipartFile file) {

        try {
            Payment payment = requirePaymentAccess(
                    principal,
                    paymentId);

            if (file == null || file.isEmpty()) {
                throw new InvalidFileException(
                        "A non-empty file is required");
            }

            String fileName = file.getOriginalFilename() == null
                    ? "payment-document"
                    : file.getOriginalFilename();

            String s3Key = storageService.upload(
                    file,
                    "payment-documents",
                    principal.userId());

            PaymentDocument document = documentRepository.save(
                    new PaymentDocument(
                            payment,
                            fileName,
                            file.getContentType(),
                            s3Key,
                            principal.userId(),
                            false));

            return toResponse(document);

        } catch (Exception exception) {
            System.err.println(
                    "Error in PaymentDocumentService.uploadDocument: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public List<PaymentDocumentResponse> listDocuments(
            JwtPrincipal principal,
            UUID paymentId) {

        try {
            requirePaymentAccess(principal, paymentId);

            return documentRepository
                    .findByPaymentIdOrderByCreatedAtDesc(paymentId)
                    .stream()
                    .map(this::toResponse)
                    .toList();

        } catch (Exception exception) {
            System.err.println(
                    "Error in PaymentDocumentService.listDocuments: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public void deleteDocument(
            JwtPrincipal principal,
            UUID paymentId,
            UUID documentId) {

        try {
            requirePaymentAccess(principal, paymentId);

            PaymentDocument document =
                    documentRepository.findById(documentId)
                            .filter(item -> item.getPayment().getId()
                                    .equals(paymentId))
                            .orElseThrow(() ->
                                    new PaymentDocumentNotFoundException(
                                            documentId));

            if (document.isSystemGenerated()) {
                throw new PaymentDocumentStateException(
                        "System-generated receipts cannot be deleted");
            }

            storageService.delete(document.getS3Key());
            documentRepository.delete(document);

        } catch (Exception exception) {
            System.err.println(
                    "Error in PaymentDocumentService.deleteDocument: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public PaymentDocumentResponse createSystemReceipt(
            UUID paymentId) {

        try {
            Payment payment = paymentRepository.findById(paymentId)
                    .orElseThrow(() ->
                            new PaymentNotFoundException(paymentId));

            if (payment.getStatus() != PaymentStatus.SUCCESS) {
                throw new PaymentStateException(
                        "Receipt requires a successful payment");
            }

            if (documentRepository.existsByPaymentIdAndSystemGenerated(
                    paymentId,
                    true)) {
                return documentRepository
                        .findByPaymentIdOrderByCreatedAtDesc(paymentId)
                        .stream()
                        .filter(PaymentDocument::isSystemGenerated)
                        .findFirst()
                        .map(this::toResponse)
                        .orElseThrow();
            }

            String receipt = """
                    InsureWise Payment Receipt
                    --------------------------
                    Transaction: %s
                    Payment ID: %s
                    Customer ID: %s
                    Policy: %s
                    Amount: %s
                    Method: %s
                    Status: %s
                    Paid At: %s
                    """.formatted(
                    payment.getTransactionRef(),
                    payment.getId(),
                    payment.getCustomerId(),
                    payment.getPolicyNameSnapshot(),
                    payment.getAmount(),
                    payment.getMethod(),
                    payment.getStatus(),
                    payment.getPaidAt()
                            .format(RECEIPT_DATE_FORMAT));

            String fileName = "receipt-"
                    + payment.getTransactionRef()
                    + ".txt";

            String s3Key = storageService.uploadGenerated(
                    receipt.getBytes(StandardCharsets.UTF_8),
                    fileName,
                    "text/plain",
                    "payment-receipts",
                    payment.getCustomerId());

            PaymentDocument document = documentRepository.save(
                    new PaymentDocument(
                            payment,
                            fileName,
                            "text/plain",
                            s3Key,
                            payment.getCustomerId(),
                            true));

            return toResponse(document);

        } catch (Exception exception) {
            System.err.println(
                    "Error in PaymentDocumentService.createSystemReceipt: "
                            + exception.getMessage());
            throw exception;
        }
    }

    private Payment requirePaymentAccess(
            JwtPrincipal principal,
            UUID paymentId) {

        Payment payment = paymentRepository.findById(paymentId)
                .orElseThrow(() ->
                        new PaymentNotFoundException(paymentId));

        if (principal.role() == JwtRole.CUSTOMER
                && !payment.isOwnedBy(principal.userId())) {
            throw new PaymentNotFoundException();
        }

        return payment;
    }

    private PaymentDocumentResponse toResponse(
            PaymentDocument document) {

        PresignedUrlResponse download =
                storageService.getPresignedDownloadUrl(
                        document.getS3Key());

        return new PaymentDocumentResponse(
                document.getId(),
                document.getPayment().getId(),
                document.getFileName(),
                document.getContentType(),
                download,
                document.getUploadedBy(),
                document.isSystemGenerated(),
                document.getCreatedAt());
    }
}





package com.insurewise.policy.service;

import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.security.JwtPrincipal;
import com.insurewise.common.security.JwtRole;
import com.insurewise.common.service.S3StorageService;
import com.insurewise.policy.dto.response.ApplicationDocumentResponse;
import com.insurewise.policy.entity.ApplicationDocument;
import com.insurewise.policy.entity.PolicyApplication;
import com.insurewise.policy.exception.ApplicationNotFoundException;
import com.insurewise.policy.repository.ApplicationDocumentRepository;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import com.insurewise.common.exception.InvalidFileException;
import com.insurewise.policy.exception.ApplicationDocumentNotFoundException;

@Service
@Transactional
public class ApplicationDocumentService {
    private final ApplicationDocumentRepository documentRepository;
    private final PolicyApplicationService applicationService;
    private final S3StorageService storageService;

    public ApplicationDocumentService(
            ApplicationDocumentRepository documentRepository,
            PolicyApplicationService applicationService,
            S3StorageService storageService) {
        this.documentRepository = documentRepository;
        this.applicationService = applicationService;
        this.storageService = storageService;
    }

    public ApplicationDocumentResponse uploadDocument(
            JwtPrincipal principal,
            UUID applicationId,
            MultipartFile file) {

        try {
            PolicyApplication application =
                    requireApplicationAccess(principal, applicationId);

            if (file == null || file.isEmpty()) {
                throw new InvalidFileException("A non-empty file is required");
            }

            String s3Key = storageService.upload(
                    file,
                    "application-documents",
                    principal.userId());

            ApplicationDocument document = documentRepository.save(
                    new ApplicationDocument(
                            application,
                            file.getOriginalFilename() == null
                                    ? "unnamed-file"
                                    : file.getOriginalFilename(),
                            file.getContentType(),
                            s3Key,
                            principal.userId()));

            return toResponse(document);

        } catch (Exception exception) {
            System.err.println(
                    "Error in ApplicationDocumentService.uploadDocument: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public List<ApplicationDocumentResponse> listDocuments(
            JwtPrincipal principal,
            UUID applicationId) {

        try {
            requireApplicationAccess(principal, applicationId);

            return documentRepository
                    .findByPolicyApplicationIdOrderByCreatedAtDesc(applicationId)
                    .stream()
                    .map(this::toResponse)
                    .toList();

        } catch (Exception exception) {
            System.err.println(
                    "Error in ApplicationDocumentService.listDocuments: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public void deleteDocument(
            JwtPrincipal principal,
            UUID applicationId,
            UUID documentId) {

        try {
            requireApplicationAccess(principal, applicationId);

            ApplicationDocument document =
                    documentRepository.findById(documentId)
                            .filter(item -> item
                                    .getPolicyApplication()
                                    .getId()
                                    .equals(applicationId))
                            .orElseThrow(() ->
                                    new ApplicationDocumentNotFoundException(
                                            documentId));

            storageService.delete(document.getS3Key());
            documentRepository.delete(document);

        } catch (Exception exception) {
            System.err.println(
                    "Error in ApplicationDocumentService.deleteDocument: "
                            + exception.getMessage());
            throw exception;
        }
    }

    private PolicyApplication requireApplicationAccess(
            JwtPrincipal principal,
            UUID applicationId) {

        PolicyApplication application =
                applicationService.getApplicationEntityForInternalUse(
                        applicationId);

        if (principal.role() == JwtRole.CUSTOMER
                && !application.isOwnedBy(principal.userId())) {
            throw new ApplicationNotFoundException(applicationId);
        }

        return application;
    }

    private ApplicationDocumentResponse toResponse(
            ApplicationDocument document) {

        PresignedUrlResponse download =
                storageService.getPresignedDownloadUrl(
                        document.getS3Key());

        return new ApplicationDocumentResponse(
                document.getId(),
                document.getPolicyApplication().getId(),
                document.getFileName(),
                document.getContentType(),
                download,
                document.getUploadedBy(),
                document.getCreatedAt());
    }
}




package com.insurewise.policy.service;

import com.insurewise.policy.dto.request.CategoryCreateRequest;
import com.insurewise.policy.dto.request.CategoryUpdateRequest;
import com.insurewise.policy.dto.response.CategoryResponse;
import com.insurewise.policy.entity.Category;
import com.insurewise.policy.repository.CategoryRepository;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.insurewise.policy.exception.CategoryNotFoundException;

@Service
@Transactional
public class CategoryService {
    private final CategoryRepository repository;

    public CategoryService(CategoryRepository repository) {
        this.repository = repository;
    }

    public CategoryResponse create(CategoryCreateRequest request) {

        try {
            Category category = repository.save(new Category(
                    request.name(),
                    request.description(),
                    request.status()));

            return toResponse(category);

        } catch (Exception exception) {
            System.err.println(
                    "Error in CategoryService.create: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public List<CategoryResponse> list() {

        try {
            return repository.findAll()
                    .stream()
                    .map(this::toResponse)
                    .toList();

        } catch (Exception exception) {
            System.err.println(
                    "Error in CategoryService.list: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public CategoryResponse update(
            UUID id,
            CategoryUpdateRequest request) {

        try {
            Category category = find(id);

            category.update(
                    request.name(),
                    request.description(),
                    request.status());

            return toResponse(category);

        } catch (Exception exception) {
            System.err.println(
                    "Error in CategoryService.update: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public void delete(UUID id) {

        try {
            repository.delete(find(id));

        } catch (Exception exception) {
            System.err.println(
                    "Error in CategoryService.delete: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public Category find(UUID id) {
        return repository.findById(id)
                .orElseThrow(() -> new CategoryNotFoundException(id));
    }

    private CategoryResponse toResponse(Category category) {
        return new CategoryResponse(
                category.getId(),
                category.getName(),
                category.getDescription(),
                category.getStatus());
    }
}




package com.insurewise.policy.service;

import com.insurewise.auth.repository.CustomerRepository;
import com.insurewise.auth.repository.StaffUserRepository;
import com.insurewise.policy.dto.response.DashboardMetricsResponse;
import com.insurewise.policy.entity.ApplicationStatus;
import com.insurewise.policy.entity.PolicyStatus;
import com.insurewise.policy.repository.CategoryRepository;
import com.insurewise.policy.repository.PolicyApplicationRepository;
import com.insurewise.policy.repository.PolicyRepository;
import jakarta.persistence.EntityManager;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
public class DashboardService {
    private final CustomerRepository customerRepository;
    private final StaffUserRepository staffUserRepository;
    private final CategoryRepository categoryRepository;
    private final PolicyRepository policyRepository;
    private final PolicyApplicationRepository applicationRepository;
    private final EntityManager entityManager;

    public DashboardService(
            CustomerRepository customerRepository,
            StaffUserRepository staffUserRepository,
            CategoryRepository categoryRepository,
            PolicyRepository policyRepository,
            PolicyApplicationRepository applicationRepository,
            EntityManager entityManager) {
        this.customerRepository = customerRepository;
        this.staffUserRepository = staffUserRepository;
        this.categoryRepository = categoryRepository;
        this.policyRepository = policyRepository;
        this.applicationRepository = applicationRepository;
        this.entityManager = entityManager;
    }

    public DashboardMetricsResponse getMetrics() {

        try {
            return new DashboardMetricsResponse(
                    customerRepository.count(),
                    staffUserRepository.count(),
                    categoryRepository.count(),
                    policyRepository.count(),
                    policyRepository.countByStatus(PolicyStatus.ACTIVE),
                    applicationRepository.count(),
                    applicationRepository.countByStatus(
                            ApplicationStatus.PENDING),
                    applicationRepository.countByStatus(
                            ApplicationStatus.ACTIVE),
                    countTable("claims"),
                    countByStatus("claims", "PENDING"),
                    countTable("payments"),
                    countByStatus("payments", "SUCCESS"));

        } catch (Exception exception) {
            System.err.println(
                    "Error in DashboardService.getMetrics: "
                            + exception.getMessage());
            throw exception;
        }
    }

    private long countTable(String tableName) {
        Number result = (Number) entityManager
                .createNativeQuery("select count(*) from " + tableName)
                .getSingleResult();

        return result.longValue();
    }

    private long countByStatus(String tableName, String status) {
        Number result = (Number) entityManager
                .createNativeQuery(
                        "select count(*) from " + tableName
                                + " where status = :status")
                .setParameter("status", status)
                .getSingleResult();

        return result.longValue();
    }
}




package com.insurewise.policy.service;

import com.insurewise.common.security.JwtPrincipal;
import com.insurewise.common.security.JwtRole;
import com.insurewise.policy.dto.request.DependentRequest;
import com.insurewise.policy.dto.response.DependentResponse;
import com.insurewise.policy.entity.Dependent;
import com.insurewise.policy.entity.PolicyApplication;
import com.insurewise.policy.exception.ApplicationNotFoundException;
import com.insurewise.policy.repository.DependentRepository;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.insurewise.policy.exception.DependentNotFoundException;

@Service
@Transactional
public class DependentService {
    private final DependentRepository dependentRepository;
    private final PolicyApplicationService applicationService;

    public DependentService(
            DependentRepository dependentRepository,
            PolicyApplicationService applicationService) {
        this.dependentRepository = dependentRepository;
        this.applicationService = applicationService;
    }

    public DependentResponse addDependent(
            JwtPrincipal principal,
            UUID applicationId,
            DependentRequest request) {

        try {
            PolicyApplication application =
                    requireApplicationAccess(principal, applicationId);

            Dependent dependent = dependentRepository.save(new Dependent(
                    application,
                    request.fullName(),
                    request.relationship(),
                    request.dateOfBirth(),
                    request.gender()));

            return toResponse(dependent);

        } catch (Exception exception) {
            System.err.println(
                    "Error in DependentService.addDependent: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public List<DependentResponse> listDependents(
            JwtPrincipal principal,
            UUID applicationId) {

        try {
            requireApplicationAccess(principal, applicationId);

            return dependentRepository
                    .findByPolicyApplicationIdOrderByCreatedAtAsc(applicationId)
                    .stream()
                    .map(this::toResponse)
                    .toList();

        } catch (Exception exception) {
            System.err.println(
                    "Error in DependentService.listDependents: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public DependentResponse updateDependent(
            JwtPrincipal principal,
            UUID applicationId,
            UUID dependentId,
            DependentRequest request) {

        try {
            requireApplicationAccess(principal, applicationId);

            Dependent dependent =
                    requireDependent(applicationId, dependentId);

            dependent.update(
                    request.fullName(),
                    request.relationship(),
                    request.dateOfBirth(),
                    request.gender());

            return toResponse(dependent);

        } catch (Exception exception) {
            System.err.println(
                    "Error in DependentService.updateDependent: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public void deleteDependent(
            JwtPrincipal principal,
            UUID applicationId,
            UUID dependentId) {

        try {
            requireApplicationAccess(principal, applicationId);
            dependentRepository.delete(
                    requireDependent(applicationId, dependentId));

        } catch (Exception exception) {
            System.err.println(
                    "Error in DependentService.deleteDependent: "
                            + exception.getMessage());
            throw exception;
        }
    }

    private PolicyApplication requireApplicationAccess(
            JwtPrincipal principal,
            UUID applicationId) {

        PolicyApplication application =
                applicationService.getApplicationEntityForInternalUse(
                        applicationId);

        if (principal.role() == JwtRole.CUSTOMER
                && !application.isOwnedBy(principal.userId())) {
            throw new ApplicationNotFoundException(applicationId);
        }

        return application;
    }

    private Dependent requireDependent(
            UUID applicationId,
            UUID dependentId) {

        return dependentRepository.findById(dependentId)
                .filter(dependent -> dependent
                        .getPolicyApplication()
                        .getId()
                        .equals(applicationId))
                .orElseThrow(() ->
                        new DependentNotFoundException(dependentId));
    }

    private DependentResponse toResponse(Dependent dependent) {
        return new DependentResponse(
                dependent.getId(),
                dependent.getPolicyApplication().getId(),
                dependent.getFullName(),
                dependent.getRelationship(),
                dependent.getDateOfBirth(),
                dependent.getGender(),
                dependent.getCreatedAt());
    }
}





package com.insurewise.policy.service;

import com.insurewise.common.security.JwtPrincipal;
import com.insurewise.policy.dto.request.PolicyApplicationCreateRequest;
import com.insurewise.policy.dto.response.*;
import com.insurewise.policy.entity.*;
import com.insurewise.policy.exception.*;
import com.insurewise.policy.repository.PolicyApplicationRepository;
import java.time.LocalDate;
import java.time.Period;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


@Service
@Transactional
public class PolicyApplicationService {
    private final PolicyApplicationRepository applicationRepository;
    private final PolicyService policyService;

    public PolicyApplicationService(
            PolicyApplicationRepository applicationRepository,
            PolicyService policyService) {
        this.applicationRepository = applicationRepository;
        this.policyService = policyService;
    }

    public PolicyApplicationResponse createApplication(
            UUID customerId,
            PolicyApplicationCreateRequest request) {

        try {
            Policy policy = policyService.find(request.policyId());

            if (!policy.isActiveForCustomer()) {
                throw new ApplicationStateException(
                        "Applications can only be created for active policies");
            }

            boolean duplicate = applicationRepository
                    .existsByCustomerIdAndPolicyIdAndStatus(
                            customerId,
                            request.policyId(),
                            ApplicationStatus.PENDING);

            if (duplicate) {
                throw new DuplicatePendingApplicationException();
            }

            Long sequence = applicationRepository.nextApplicationCodeSequence();

            PolicyApplication application = new PolicyApplication(
                    "APP-" + sequence,
                    customerId,
                    policy,
                    request.coverageType(),
                    request.dateOfBirth(),
                    request.address(),
                    request.preferredStartDate(),
                    request.nomineeName(),
                    request.nomineeRelationship());

            return toResponse(applicationRepository.save(application));

        } catch (Exception exception) {
            System.err.println(
                    "Error in PolicyApplicationService.createApplication: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public List<PolicyApplicationResponse> listApplications(
            JwtPrincipal principal,
            ApplicationStatus status) {

        try {
            List<PolicyApplication> applications;

            if (principal.role().name().equals("STAFF")) {
                applications = status == null
                        ? applicationRepository.findAll()
                        : applicationRepository.findByStatusOrderByCreatedAtDesc(
                        status);
            } else {
                applications = status == null
                        ? applicationRepository
                        .findByCustomerIdOrderByCreatedAtDesc(
                                principal.userId())
                        : applicationRepository
                        .findByCustomerIdAndStatusOrderByCreatedAtDesc(
                                principal.userId(),
                                status);
            }

            return applications.stream()
                    .map(this::toResponse)
                    .toList();

        } catch (Exception exception) {
            System.err.println(
                    "Error in PolicyApplicationService.listApplications: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public PolicyApplicationResponse getApplication(
            JwtPrincipal principal,
            UUID applicationId) {

        try {
            PolicyApplication application =
                    getApplicationEntity(applicationId);

            if (principal.role().name().equals("CUSTOMER")
                    && !application.isOwnedBy(principal.userId())) {
                throw new ApplicationNotFoundException(applicationId);
            }

            return toResponse(application);

        } catch (Exception exception) {
            System.err.println(
                    "Error in PolicyApplicationService.getApplication: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public ApplicationDecisionResponse approveApplication(
            UUID staffUserId,
            UUID applicationId) {

        try {
            PolicyApplication application =
                    getApplicationEntity(applicationId);

            LocalDate startDate =
                    application.getPreferredStartDate() == null
                            ? LocalDate.now()
                            : application.getPreferredStartDate();

            LocalDate endDate = calculateEndDate(
                    startDate,
                    application.getPolicy().getDurationLabel());

            application.approve(staffUserId, startDate, endDate);

            return toDecisionResponse(application);

        } catch (Exception exception) {
            System.err.println(
                    "Error in PolicyApplicationService.approveApplication: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public ApplicationDecisionResponse rejectApplication(
            UUID staffUserId,
            UUID applicationId) {

        try {
            PolicyApplication application =
                    getApplicationEntity(applicationId);

            application.reject(staffUserId);

            return toDecisionResponse(application);

        } catch (Exception exception) {
            System.err.println(
                    "Error in PolicyApplicationService.rejectApplication: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public PolicyApplication getApplicationEntityForInternalUse(
            UUID applicationId) {
        return getApplicationEntity(applicationId);
    }

    private PolicyApplication getApplicationEntity(UUID applicationId) {
        return applicationRepository.findById(applicationId)
                .orElseThrow(() ->
                        new ApplicationNotFoundException(applicationId));
    }

    private LocalDate calculateEndDate(
            LocalDate startDate,
            String durationLabel) {

        String digits = durationLabel.replaceAll("[^0-9]", "");

        if (!digits.isBlank()) {
            int years = Integer.parseInt(digits);
            return startDate.plusYears(Math.max(years, 1));
        }

        return startDate.plusYears(1);
    }

    private PolicyApplicationResponse toResponse(
            PolicyApplication application) {

        return new PolicyApplicationResponse(
                application.getId(),
                application.getApplicationCode(),
                application.getCustomerId(),
                application.getPolicy().getId(),
                application.getPolicy().getName(),
                application.getCoverageType(),
                application.getCoverageAmount(),
                application.getPremiumAmount(),
                application.getDateOfBirth(),
                application.getAddress(),
                application.getPreferredStartDate(),
                application.getNomineeName(),
                application.getNomineeRelationship(),
                application.getStartDate(),
                application.getEndDate(),
                application.getStatus(),
                application.getDecidedBy(),
                application.getDecidedAt(),
                application.getCreatedAt());
    }

    private ApplicationDecisionResponse toDecisionResponse(
            PolicyApplication application) {

        return new ApplicationDecisionResponse(
                application.getId(),
                application.getApplicationCode(),
                application.getStatus(),
                application.getStartDate(),
                application.getEndDate(),
                application.getDecidedBy());
    }
}





package com.insurewise.policy.service;

import com.insurewise.policy.dto.request.PolicyCreateRequest;
import com.insurewise.policy.dto.request.PolicyUpdateRequest;
import com.insurewise.policy.dto.response.PolicyResponse;
import com.insurewise.policy.entity.Policy;
import com.insurewise.policy.entity.PolicyStatus;
import com.insurewise.policy.repository.PolicyRepository;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.insurewise.policy.exception.PolicyNotFoundException;

@Service
@Transactional
public class PolicyService {
    private final PolicyRepository policyRepository;
    private final CategoryService categoryService;

    public PolicyService(
            PolicyRepository policyRepository,
            CategoryService categoryService) {
        this.policyRepository = policyRepository;
        this.categoryService = categoryService;
    }

    public PolicyResponse create(PolicyCreateRequest request) {

        try {
            Policy policy = policyRepository.save(new Policy(
                    request.name(),
                    categoryService.find(request.categoryId()),
                    request.coverageAmount(),
                    request.premiumAmount(),
                    request.durationLabel(),
                    request.status()));

            return toResponse(policy);

        } catch (Exception exception) {
            System.err.println(
                    "Error in PolicyService.create: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public List<PolicyResponse> listActive() {

        try {
            return policyRepository
                    .findAllByStatusOrderByCreatedAtDesc(PolicyStatus.ACTIVE)
                    .stream()
                    .filter(Policy::isActiveForCustomer)
                    .map(this::toResponse)
                    .toList();

        } catch (Exception exception) {
            System.err.println(
                    "Error in PolicyService.listActive: "
                            + exception.getMessage());
            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public PolicyResponse get(UUID id) {

        try {
            return toResponse(find(id));

        } catch (Exception exception) {
            System.err.println(
                    "Error in PolicyService.get: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public PolicyResponse update(
            UUID id,
            PolicyUpdateRequest request) {

        try {
            Policy policy = find(id);

            policy.update(
                    request.name(),
                    categoryService.find(request.categoryId()),
                    request.coverageAmount(),
                    request.premiumAmount(),
                    request.durationLabel(),
                    request.status());

            return toResponse(policy);

        } catch (Exception exception) {
            System.err.println(
                    "Error in PolicyService.update: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public void delete(UUID id) {

        try {
            policyRepository.delete(find(id));

        } catch (Exception exception) {
            System.err.println(
                    "Error in PolicyService.delete: "
                            + exception.getMessage());
            throw exception;
        }
    }

    public Policy find(UUID id) {
        return policyRepository.findById(id)
                .orElseThrow(() -> new PolicyNotFoundException(id));
    }

    private PolicyResponse toResponse(Policy policy) {
        return new PolicyResponse(
                policy.getId(),
                policy.getName(),
                policy.getCategory().getId(),
                policy.getCategory().getName(),
                policy.getCoverageAmount(),
                policy.getPremiumAmount(),
                policy.getDurationLabel(),
                policy.getStatus());
    }
}

