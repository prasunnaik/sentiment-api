package com.insurewise.policy.controller;

import com.insurewise.policy.dto.request.CategoryCreateRequest;
import com.insurewise.policy.dto.request.CategoryUpdateRequest;
import com.insurewise.policy.dto.response.CategoryResponse;
import com.insurewise.policy.service.CategoryService;
import jakarta.validation.Valid;
import java.util.List;
import java.util.UUID;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/categories")
public class CategoryController {
    private final CategoryService service;

    public CategoryController(CategoryService service) {
        this.service = service;
    }

    @PostMapping
    @PreAuthorize("hasRole('STAFF')")
    public CategoryResponse create(
            @Valid @RequestBody CategoryCreateRequest request) {
        return service.create(request);
    }

    @GetMapping
    @PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
    public List<CategoryResponse> list() {
        return service.list();
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('STAFF')")
    public CategoryResponse update(
            @PathVariable UUID id,
            @Valid @RequestBody CategoryUpdateRequest request) {
        return service.update(id, request);
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('STAFF')")
    public void delete(@PathVariable UUID id) {
        service.delete(id);
    }
}

package com.insurewise.policy.controller;

import com.insurewise.policy.dto.response.DashboardMetricsResponse;
import com.insurewise.policy.service.DashboardService;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/dashboard")
@PreAuthorize("hasRole('STAFF')")
public class DashboardController {
    private final DashboardService service;

    public DashboardController(DashboardService service) {
        this.service = service;
    }

    @GetMapping("/metrics")
    public DashboardMetricsResponse metrics() {
        return service.getMetrics();
    }
}

package com.insurewise.policy.controller;

import com.insurewise.policy.dto.request.PolicyCreateRequest;
import com.insurewise.policy.dto.request.PolicyUpdateRequest;
import com.insurewise.policy.dto.response.PolicyResponse;
import com.insurewise.policy.service.PolicyService;
import jakarta.validation.Valid;
import java.util.List;
import java.util.UUID;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/policies")
public class PolicyController {
    private final PolicyService service;

    public PolicyController(PolicyService service) {
        this.service = service;
    }

    @GetMapping
    @PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
    public List<PolicyResponse> listActive() {
        return service.listActive();
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
    public PolicyResponse get(@PathVariable UUID id) {
        return service.get(id);
    }

    @PostMapping
    @PreAuthorize("hasRole('STAFF')")
    public PolicyResponse create(
            @Valid @RequestBody PolicyCreateRequest request) {
        return service.create(request);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('STAFF')")
    public PolicyResponse update(
            @PathVariable UUID id,
            @Valid @RequestBody PolicyUpdateRequest request) {
        return service.update(id, request);
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('STAFF')")
    public void delete(@PathVariable UUID id) {
        service.delete(id);
    }
}

package com.insurewise.policy.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record CategoryCreateRequest(
        @NotBlank
        @Size(max = 80)
        String name,

        @NotBlank
        @Size(max = 500)
        String description,

        @NotNull
        CategoryStatus status
) {
}

package com.insurewise.policy.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record CategoryUpdateRequest(
        @NotBlank
        @Size(max = 80)
        String name,

        @NotBlank
        @Size(max = 500)
        String description,

        @NotNull
        CategoryStatus status
) {
}

package com.insurewise.policy.dto.request;

import com.insurewise.policy.entity.PolicyStatus;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;
import java.util.UUID;

public record PolicyCreateRequest(
        @NotBlank
        @Size(max = 120)
        String name,

        @NotNull
        UUID categoryId,

        @NotNull
        @DecimalMin("0.01")
        BigDecimal coverageAmount,

        @NotNull
        @DecimalMin("0.01")
        BigDecimal premiumAmount,

        @NotBlank
        @Size(max = 40)
        String durationLabel,

        @NotNull
        PolicyStatus status
) {
}

package com.insurewise.policy.dto.request;

import com.insurewise.policy.entity.PolicyStatus;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;
import java.util.UUID;

public record PolicyUpdateRequest(
        @NotBlank
        @Size(max = 120)
        String name,

        @NotNull
        UUID categoryId,

        @NotNull
        @DecimalMin("0.01")
        BigDecimal coverageAmount,

        @NotNull
        @DecimalMin("0.01")
        BigDecimal premiumAmount,

        @NotBlank
        @Size(max = 40)
        String durationLabel,

        @NotNull
        PolicyStatus status
) {
}

package com.insurewise.policy.dto.response;

import java.util.UUID;

public record CategoryResponse(
        UUID id,
        String name,
        String description,
        CategoryStatus status
) {
}
package com.insurewise.policy.dto.response;

public record DashboardMetricsResponse(
        long totalCustomers,
        long totalStaff,
        long totalCategories,
        long totalPolicies,
        long activePolicies,
        long totalApplications,
        long pendingApplications,
        long activeApplications,
        long totalClaims,
        long pendingClaims,
        long totalPayments,
        long successfulPayments
) {
}
package com.insurewise.policy.dto.response;

import com.insurewise.policy.entity.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.UUID;

public record PolicyApplicationResponse(
        UUID id,
        String applicationCode,
        UUID customerId,
        UUID policyId,
        String policyName,
        CoverageType coverageType,
        BigDecimal coverageAmount,
        BigDecimal premiumAmount,
        LocalDate dateOfBirth,
        String address,
        LocalDate preferredStartDate,
        String nomineeName,
        NomineeRelationship nomineeRelationship,
        LocalDate startDate,
        LocalDate endDate,
        ApplicationStatus status,
        UUID decidedBy,
        LocalDateTime decidedAt,
        LocalDateTime createdAt
) {
}
package com.insurewise.policy.dto.response;

import com.insurewise.policy.entity.PolicyStatus;
import java.math.BigDecimal;
import java.util.UUID;

public record PolicyResponse(
        UUID id,
        String name,
        UUID categoryId,
        String categoryName,
        BigDecimal coverageAmount,
        BigDecimal premiumAmount,
        String durationLabel,
        PolicyStatus status
) {
}
package com.insurewise.policy.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "categories")
public class Category {
    @Id
    @GeneratedValue
    private UUID id;

    @Column(nullable = false, length = 80)
    private String name;

    @Column(nullable = false, length = 500)
    private String description;


    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    protected Category() {
    }

    public Category(String name, String description, CategoryStatus status) {
        this.name = name;
        this.description = description;
        this.status = status;
    }

    @PrePersist
    void initialize() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
    }

    public void update(
            String name,
            String description,
            CategoryStatus status) {
        this.name = name;
        this.description = description;
        this.status = status;
    }

    public UUID getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public CategoryStatus getStatus() {
        return status;
    }
}
package com.insurewise.policy.entity;

public enum CategoryStatus {
    ACTIVE,
    INACTIVE
}
package com.insurewise.policy.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "policies")
public class Policy {
    @Id
    @GeneratedValue
    private UUID id;

    @Column(nullable = false, length = 120)
    private String name;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "category_id", nullable = false)
    private Category category;

    @Column(name = "coverage_amount", nullable = false, precision = 14, scale = 2)
    private BigDecimal coverageAmount;

    @Column(name = "premium_amount", nullable = false, precision = 10, scale = 2)
    private BigDecimal premiumAmount;

    @Column(name = "duration_label", nullable = false, length = 40)
    private String durationLabel;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private PolicyStatus status;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    protected Policy() {
    }

    public Policy(
            String name,
            Category category,
            BigDecimal coverageAmount,
            BigDecimal premiumAmount,
            String durationLabel,
            PolicyStatus status) {
        this.name = name;
        this.category = category;
        this.coverageAmount = coverageAmount;
        this.premiumAmount = premiumAmount;
        this.durationLabel = durationLabel;
        this.status = status;
    }

    @PrePersist
    void initialize() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
    }

    public void update(
            String name,
            Category category,
            BigDecimal coverageAmount,
            BigDecimal premiumAmount,
            String durationLabel,
            PolicyStatus status) {
        this.name = name;
        this.category = category;
        this.coverageAmount = coverageAmount;
        this.premiumAmount = premiumAmount;
        this.durationLabel = durationLabel;
        this.status = status;
    }

    public boolean isActiveForCustomer() {
        return status == PolicyStatus.ACTIVE
                && category.getStatus() == CategoryStatus.ACTIVE;
    }

    public UUID getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Category getCategory() {
        return category;
    }

    public BigDecimal getCoverageAmount() {
        return coverageAmount;
    }

    public BigDecimal getPremiumAmount() {
        return premiumAmount;
    }

    public String getDurationLabel() {
        return durationLabel;
    }

    public PolicyStatus getStatus() {
        return status;
    }
}
package com.insurewise.policy.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "policy_applications")
public class PolicyApplication {
    @Id
    @GeneratedValue
    private UUID id;

    @Column(name = "application_code", nullable = false, unique = true, length = 40)
    private String applicationCode;

    @Column(name = "customer_id", nullable = false)
    private UUID customerId;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "policy_id", nullable = false)
    private Policy policy;

    @Enumerated(EnumType.STRING)
    @Column(name = "coverage_type", nullable = false, length = 20)
    private CoverageType coverageType;

    @Column(name = "coverage_amount", nullable = false, precision = 14, scale = 2)
    private BigDecimal coverageAmount;

    @Column(name = "premium_amount", nullable = false, precision = 10, scale = 2)
    private BigDecimal premiumAmount;

    @Column(name = "date_of_birth", nullable = false)
    private LocalDate dateOfBirth;

    @Column(nullable = false, length = 500)
    private String address;

    @Column(name = "preferred_start_date")
    private LocalDate preferredStartDate;

    @Column(name = "nominee_name", length = 120)
    private String nomineeName;

    @Enumerated(EnumType.STRING)
    @Column(name = "nominee_relationship", length = 20)
    private NomineeRelationship nomineeRelationship;

    @Column(name = "start_date")
    private LocalDate startDate;

    @Column(name = "end_date")
    private LocalDate endDate;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private ApplicationStatus status;

    @Column(name = "decided_by")
    private UUID decidedBy;

    @Column(name = "decided_at")
    private LocalDateTime decidedAt;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    protected PolicyApplication() {
    }

    public PolicyApplication(
            String applicationCode,
            UUID customerId,
            Policy policy,
            CoverageType coverageType,
            LocalDate dateOfBirth,
            String address,
            LocalDate preferredStartDate,
            String nomineeName,
            NomineeRelationship nomineeRelationship) {
        this.applicationCode = applicationCode;
        this.customerId = customerId;
        this.policy = policy;
        this.coverageType = coverageType;
        this.coverageAmount = policy.getCoverageAmount();
        this.premiumAmount = policy.getPremiumAmount();
        this.dateOfBirth = dateOfBirth;
        this.address = address;
        this.preferredStartDate = preferredStartDate;
        this.nomineeName = nomineeName;
        this.nomineeRelationship = nomineeRelationship;
        this.status = ApplicationStatus.PENDING;
    }

    @PrePersist
    void initialize() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
    }

    public void approve(
            UUID staffUserId,
            LocalDate startDate,
            LocalDate endDate) {
        ensurePending();
        this.status = ApplicationStatus.ACTIVE;
        this.decidedBy = staffUserId;
        this.decidedAt = LocalDateTime.now();
        this.startDate = startDate;
        this.endDate = endDate;
    }

    public void reject(UUID staffUserId) {
        ensurePending();
        this.status = ApplicationStatus.REJECTED;
        this.decidedBy = staffUserId;
        this.decidedAt = LocalDateTime.now();
    }

    private void ensurePending() {
        if (status != ApplicationStatus.PENDING) {
            throw new IllegalStateException(
                    "Only pending applications can be decided");
        }
    }

    public boolean isOwnedBy(UUID customerId) {
        return this.customerId.equals(customerId);
    }

    public boolean isActive() {
        return status == ApplicationStatus.ACTIVE;
    }

    public UUID getId() {
        return id;
    }

    public String getApplicationCode() {
        return applicationCode;
    }

    public UUID getCustomerId() {
        return customerId;
    }

    public Policy getPolicy() {
        return policy;
    }

    public CoverageType getCoverageType() {
        return coverageType;
    }

    public BigDecimal getCoverageAmount() {
        return coverageAmount;
    }

    public BigDecimal getPremiumAmount() {
        return premiumAmount;
    }

    public LocalDate getDateOfBirth() {
        return dateOfBirth;
    }

    public String getAddress() {
        return address;
    }

    public LocalDate getPreferredStartDate() {
        return preferredStartDate;
    }

    public String getNomineeName() {
        return nomineeName;
    }

    public NomineeRelationship getNomineeRelationship() {
        return nomineeRelationship;
    }

    public LocalDate getStartDate() {
        return startDate;
    }

    public LocalDate getEndDate() {
        return endDate;
    }

    public ApplicationStatus getStatus() {
        return status;
    }

    public UUID getDecidedBy() {
        return decidedBy;
    }

    public LocalDateTime getDecidedAt() {
        return decidedAt;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}
package com.insurewise.policy.entity;

public enum PolicyStatus {
    DRAFT,
    ACTIVE,
    INACTIVE
}
package com.insurewise.policy.repository;

import com.insurewise.policy.entity.Category;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CategoryRepository extends JpaRepository<Category, UUID> {
}
package com.insurewise.policy.repository;

import com.insurewise.policy.entity.PolicyApplicationResponse;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface PolicyApplicationRepository
        extends JpaRepository<PolicyApplicationResponse, UUID> {

    List<PolicyApplicationResponse> findByCustomerIdOrderByCreatedAtDesc(
            UUID customerId);

    List<PolicyApplicationResponse> findByStatusOrderByCreatedAtDesc(
            ApplicationStatus status);

    List<PolicyApplicationResponse> findByCustomerIdAndStatusOrderByCreatedAtDesc(
            UUID customerId,
            ApplicationStatus status);

    boolean existsByCustomerIdAndPolicyIdAndStatus(
            UUID customerId,
            UUID policyId,
            ApplicationStatus status);

    @Query(
            value = "select nextval('application_code_seq')",
            nativeQuery = true)
    Long nextApplicationCodeSequence();

    long countByStatus(
            com.insurewise.policy.entity.ApplicationStatus status);
}
package com.insurewise.policy.repository;

import com.insurewise.policy.entity.Policy;
import com.insurewise.policy.entity.PolicyStatus;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PolicyRepository extends JpaRepository<Policy, UUID> {
    List<Policy> findAllByStatusOrderByCreatedAtDesc(PolicyStatus status);
    long countByStatus(
            com.insurewise.policy.entity.PolicyStatus status);
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
import com.insurewise.policy.entity.PolicyStatus;
import com.insurewise.policy.repository.CategoryRepository;
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

these files are showing this error dont add anything in codes if you want just deduct few lines from code but dont add anything because when we merge then it will create conflict individually it should run and when we merge also it should not show conflict also if you want can suggest to delete some class and deduct some lines but never add beacuse if we deduct while merging if other person has more code in same file along with my code it will overwrite it 

[ERROR] COMPILATION ERROR : 
[INFO] -------------------------------------------------------------
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/response/CategoryResponse.java:[9,9] cannot find symbol
  symbol:   class CategoryStatus
  location: class com.insurewise.policy.dto.response.CategoryResponse
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/common/exception/GlobalExceptionHandler.java:[78,13] cannot find symbol
  symbol:   class PolicyStateException
  location: class com.insurewise.common.exception.GlobalExceptionHandler
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/request/CategoryCreateRequest.java:[17,9] cannot find symbol
  symbol:   class CategoryStatus
  location: class com.insurewise.policy.dto.request.CategoryCreateRequest
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/request/CategoryUpdateRequest.java:[17,9] cannot find symbol
  symbol:   class CategoryStatus
  location: class com.insurewise.policy.dto.request.CategoryUpdateRequest
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[4,41] cannot find symbol
  symbol:   class PolicyApplicationCreateRequest
  location: package com.insurewise.policy.dto.request
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[3,36] cannot find symbol
  symbol:   class PolicyApplicationResponse
  location: package com.insurewise.policy.entity
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[10,31] cannot find symbol
  symbol: class PolicyApplicationResponse
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[32,13] cannot find symbol
  symbol:   class PolicyApplicationCreateRequest
  location: class com.insurewise.policy.service.PolicyApplicationService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/response/PolicyApplicationResponse.java:[15,9] cannot find symbol
  symbol:   class CoverageType
  location: class com.insurewise.policy.dto.response.PolicyApplicationResponse
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/response/PolicyApplicationResponse.java:[22,9] cannot find symbol
  symbol:   class NomineeRelationship
  location: class com.insurewise.policy.dto.response.PolicyApplicationResponse
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/response/PolicyApplicationResponse.java:[25,9] cannot find symbol
  symbol:   class ApplicationStatus
  location: class com.insurewise.policy.dto.response.PolicyApplicationResponse
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[78,13] cannot find symbol
  symbol:   class ApplicationStatus
  location: class com.insurewise.policy.service.PolicyApplicationService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[135,12] cannot find symbol
  symbol:   class ApplicationDecisionResponse
  location: class com.insurewise.policy.service.PolicyApplicationService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[164,12] cannot find symbol
  symbol:   class ApplicationDecisionResponse
  location: class com.insurewise.policy.service.PolicyApplicationService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[234,13] cannot find symbol
  symbol:   class ApplicationDecisionResponse
  location: class com.insurewise.policy.service.PolicyApplicationService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[28,13] cannot find symbol
  symbol:   class CoverageType
  location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[50,13] cannot find symbol
  symbol:   class NomineeRelationship
  location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[60,13] cannot find symbol
  symbol:   class ApplicationStatus
  location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[78,13] cannot find symbol
  symbol:   class CoverageType
  location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[83,13] cannot find symbol
  symbol:   class NomineeRelationship
  location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[155,12] cannot find symbol
  symbol:   class CoverageType
  location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[183,12] cannot find symbol
  symbol:   class NomineeRelationship
  location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[195,12] cannot find symbol
  symbol:   class ApplicationStatus
  location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[12,10] cannot find symbol
  symbol:   class PolicyApplicationResponse
  location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[16,13] cannot find symbol
  symbol:   class ApplicationStatus
  location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[15,10] cannot find symbol
  symbol:   class PolicyApplicationResponse
  location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[20,13] cannot find symbol
  symbol:   class ApplicationStatus
  location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[18,10] cannot find symbol
  symbol:   class PolicyApplicationResponse
  location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[25,13] cannot find symbol
  symbol:   class ApplicationStatus
  location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[33,41] cannot find symbol
  symbol:   class ApplicationStatus
  location: package com.insurewise.policy.entity
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/DashboardService.java:[20,19] cannot find symbol
  symbol:   class PolicyApplicationRepository
  location: class com.insurewise.policy.service.DashboardService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/DashboardService.java:[28,13] cannot find symbol
  symbol:   class PolicyApplicationRepository
  location: class com.insurewise.policy.service.DashboardService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/common/exception/GlobalExceptionHandler.java:[76,23] cannot find symbol
  symbol:   class PolicyStateException
  location: class com.insurewise.common.exception.GlobalExceptionHandler
[INFO] 33 errors 
[INFO] -------------------------------------------------------------
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  6.949 s
[INFO] Finished at: 2026-09-11T17:15:02+05:30
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.11.0:compile (default-compile) on project insurewise-service: Compilation failure: Compilation failure:                                                                                                                 
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/response/CategoryResponse.java:[9,9] cannot find symbol
[ERROR]   symbol:   class CategoryStatus
[ERROR]   location: class com.insurewise.policy.dto.response.CategoryResponse
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/common/exception/GlobalExceptionHandler.java:[78,13] cannot find symbol
[ERROR]   symbol:   class PolicyStateException
[ERROR]   location: class com.insurewise.common.exception.GlobalExceptionHandler
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/request/CategoryCreateRequest.java:[17,9] cannot find symbol
[ERROR]   symbol:   class CategoryStatus
[ERROR]   location: class com.insurewise.policy.dto.request.CategoryCreateRequest
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/request/CategoryUpdateRequest.java:[17,9] cannot find symbol
[ERROR]   symbol:   class CategoryStatus
[ERROR]   location: class com.insurewise.policy.dto.request.CategoryUpdateRequest
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[4,41] cannot find symbol
[ERROR]   symbol:   class PolicyApplicationCreateRequest
[ERROR]   location: package com.insurewise.policy.dto.request
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[3,36] cannot find symbol
[ERROR]   symbol:   class PolicyApplicationResponse
[ERROR]   location: package com.insurewise.policy.entity
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[10,31] cannot find symbol
[ERROR]   symbol: class PolicyApplicationResponse
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[32,13] cannot find symbol
[ERROR]   symbol:   class PolicyApplicationCreateRequest
[ERROR]   location: class com.insurewise.policy.service.PolicyApplicationService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/response/PolicyApplicationResponse.java:[15,9] cannot find symbol
[ERROR]   symbol:   class CoverageType
[ERROR]   location: class com.insurewise.policy.dto.response.PolicyApplicationResponse
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/response/PolicyApplicationResponse.java:[22,9] cannot find symbol
[ERROR]   symbol:   class NomineeRelationship
[ERROR]   location: class com.insurewise.policy.dto.response.PolicyApplicationResponse
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/dto/response/PolicyApplicationResponse.java:[25,9] cannot find symbol
[ERROR]   symbol:   class ApplicationStatus
[ERROR]   location: class com.insurewise.policy.dto.response.PolicyApplicationResponse
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[78,13] cannot find symbol
[ERROR]   symbol:   class ApplicationStatus
[ERROR]   location: class com.insurewise.policy.service.PolicyApplicationService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[135,12] cannot find symbol
[ERROR]   symbol:   class ApplicationDecisionResponse
[ERROR]   location: class com.insurewise.policy.service.PolicyApplicationService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[164,12] cannot find symbol
[ERROR]   symbol:   class ApplicationDecisionResponse
[ERROR]   location: class com.insurewise.policy.service.PolicyApplicationService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/PolicyApplicationService.java:[234,13] cannot find symbol
[ERROR]   symbol:   class ApplicationDecisionResponse
[ERROR]   location: class com.insurewise.policy.service.PolicyApplicationService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[28,13] cannot find symbol
[ERROR]   symbol:   class CoverageType
[ERROR]   location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[50,13] cannot find symbol
[ERROR]   symbol:   class NomineeRelationship
[ERROR]   location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[60,13] cannot find symbol
[ERROR]   symbol:   class ApplicationStatus
[ERROR]   location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[78,13] cannot find symbol
[ERROR]   symbol:   class CoverageType
[ERROR]   location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[83,13] cannot find symbol
[ERROR]   symbol:   class NomineeRelationship
[ERROR]   location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[155,12] cannot find symbol
[ERROR]   symbol:   class CoverageType
[ERROR]   location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[183,12] cannot find symbol
[ERROR]   symbol:   class NomineeRelationship
[ERROR]   location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/entity/PolicyApplication.java:[195,12] cannot find symbol
[ERROR]   symbol:   class ApplicationStatus
[ERROR]   location: class com.insurewise.policy.entity.PolicyApplication
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[12,10] cannot find symbol
[ERROR]   symbol:   class PolicyApplicationResponse
[ERROR]   location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[16,13] cannot find symbol
[ERROR]   symbol:   class ApplicationStatus
[ERROR]   location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[15,10] cannot find symbol
[ERROR]   symbol:   class PolicyApplicationResponse
[ERROR]   location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[20,13] cannot find symbol
[ERROR]   symbol:   class ApplicationStatus
[ERROR]   location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[18,10] cannot find symbol
[ERROR]   symbol:   class PolicyApplicationResponse
[ERROR]   location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[25,13] cannot find symbol
[ERROR]   symbol:   class ApplicationStatus
[ERROR]   location: interface com.insurewise.policy.repository.PolicyApplicationRepository
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/repository/PolicyApplicationRepository.java:[33,41] cannot find symbol
[ERROR]   symbol:   class ApplicationStatus
[ERROR]   location: package com.insurewise.policy.entity
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/DashboardService.java:[20,19] cannot find symbol
[ERROR]   symbol:   class PolicyApplicationRepository
[ERROR]   location: class com.insurewise.policy.service.DashboardService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/policy/service/DashboardService.java:[28,13] cannot find symbol
[ERROR]   symbol:   class PolicyApplicationRepository
[ERROR]   location: class com.insurewise.policy.service.DashboardService
[ERROR] /C:/Users/psumans/CAP-Code/insurewise-cap-angular-be/insurewise-service/src/main/java/com/insurewise/common/exception/GlobalExceptionHandler.java:[76,23] cannot find symbol
[ERROR]   symbol:   class PolicyStateException
[ERROR]   location: class com.insurewise.common.exception.GlobalExceptionHandler
[ERROR] -> [Help 1]
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException



