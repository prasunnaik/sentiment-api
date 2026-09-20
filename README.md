package com.insurewise.policy.controller;

import com.insurewise.common.security.JwtPrincipal;
import com.insurewise.policy.dto.response.ApplicationDocumentResponse;
import com.insurewise.policy.service.ApplicationDocumentService;
import java.util.List;
import java.util.UUID;
import org.springframework.http.MediaType;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/applications/{id}/documents")
@PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
public class ApplicationDocumentController {

    private final ApplicationDocumentService service;

    /**
     * Creates the application document controller.
     *
     * @param service application document use cases
     */
    public ApplicationDocumentController(
            ApplicationDocumentService service) {
        this.service = service;
    }

    /**
     * Uploads a document for the current application.
     *
     * @param principal authenticated principal
     * @param id application identifier
     * @param file document file
     * @return uploaded document
     */
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ApplicationDocumentResponse upload(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id,
            @RequestPart("file") MultipartFile file) {

        return service.uploadDocument(
                principal,
                id,
                file);
    }

    /**
     * Lists documents for the current application.
     *
     * @param principal authenticated principal
     * @param id application identifier
     * @return document responses
     */
    @GetMapping
    public List<ApplicationDocumentResponse> list(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id) {

        return service.listDocuments(
                principal,
                id);
    }

    /**
     * Deletes a document from the current application.
     *
     * @param principal authenticated principal
     * @param id application identifier
     * @param documentId document identifier
     */
    @DeleteMapping("/{documentId}")
    public void delete(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id,
            @PathVariable UUID documentId) {

        service.deleteDocument(
                principal,
                id,
                documentId);
    }
}
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

    /**
     * Creates the category controller.
     *
     * @param service category use cases
     */
    public CategoryController(CategoryService service) {
        this.service = service;
    }

    /**
     * Creates a category record.
     *
     * @param request category payload
     * @return created category
     */
    @PostMapping
    @PreAuthorize("hasRole('STAFF')")
    public CategoryResponse create(
            @Valid @RequestBody CategoryCreateRequest request) {
        return service.create(request);
    }

    /**
     * Lists all categories.
     *
     * @return category responses
     */
    @GetMapping
    @PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
    public List<CategoryResponse> list() {
        return service.list();
    }

    /**
     * Updates a category record.
     *
     * @param id category identifier
     * @param request category update payload
     * @return updated category
     */
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('STAFF')")
    public CategoryResponse update(
            @PathVariable UUID id,
            @Valid @RequestBody CategoryUpdateRequest request) {
        return service.update(id, request);
    }

    /**
     * Deletes a category record.
     *
     * @param id category identifier
     */
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

    /**
     * Creates the dashboard controller.
     *
     * @param service dashboard metrics service
     */
    public DashboardController(DashboardService service) {
        this.service = service;
    }

    /**
     * Loads dashboard metrics.
     *
     * @return dashboard metrics
     */
    @GetMapping("/metrics")
    public DashboardMetricsResponse metrics() {
        return service.getMetrics();
    }
}
package com.insurewise.policy.controller;

import com.insurewise.common.security.JwtPrincipal;
import com.insurewise.policy.dto.request.PolicyApplicationCreateRequest;
import com.insurewise.policy.dto.response.*;
import com.insurewise.policy.entity.ApplicationStatus;
import com.insurewise.policy.service.PolicyApplicationService;
import jakarta.validation.Valid;
import java.util.List;
import java.util.UUID;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/applications")
public class PolicyApplicationController {
    private final PolicyApplicationService service;

    /**
     * Creates the policy application controller.
     *
     * @param service application use cases
     */
    public PolicyApplicationController(
            PolicyApplicationService service) {
        this.service = service;
    }

    /**
     * Creates a policy application for the authenticated customer.
     *
     * @param principal authenticated principal
     * @param request application payload
     * @return created application
     */
    @PostMapping
    @PreAuthorize("hasRole('CUSTOMER')")
    public PolicyApplicationResponse create(
            @AuthenticationPrincipal JwtPrincipal principal,
            @Valid @RequestBody PolicyApplicationCreateRequest request) {
        return service.createApplication(principal.userId(), request);
    }

    /**
     * Lists applications visible to the authenticated principal.
     *
     * @param principal authenticated principal
     * @param status optional status filter
     * @return application responses
     */
    @GetMapping
    @PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
    public List<PolicyApplicationResponse> list(
            @AuthenticationPrincipal JwtPrincipal principal,
            @RequestParam(required = false) ApplicationStatus status) {
        return service.listApplications(principal, status);
    }

    /**
     * Loads an application visible to the authenticated principal.
     *
     * @param principal authenticated principal
     * @param id application identifier
     * @return application details
     */
    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
    public PolicyApplicationResponse get(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id) {
        return service.getApplication(principal, id);
    }

    /**
     * Approves an application.
     *
     * @param principal authenticated principal
     * @param id application identifier
     * @return decision response
     */
    @PutMapping("/{id}/approve")
    @PreAuthorize("hasRole('STAFF')")
    public ApplicationDecisionResponse approve(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id) {
        return service.approveApplication(principal.userId(), id);
    }

    /**
     * Rejects an application.
     *
     * @param principal authenticated principal
     * @param id application identifier
     * @return decision response
     */
    @PutMapping("/{id}/reject")
    @PreAuthorize("hasRole('STAFF')")
    public ApplicationDecisionResponse reject(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id) {
        return service.rejectApplication(principal.userId(), id);
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

    /**
     * Creates the policy controller.
     *
     * @param service policy use cases
     */
    public PolicyController(PolicyService service) {
        this.service = service;
    }

    /**
     * Lists policies that are visible to customers and staff.
     *
     * @return active policies
     */
    @GetMapping
    @PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
    public List<PolicyResponse> listActive() {
        return service.listActive();
    }

    /**
     * Loads a policy by identifier.
     *
     * @param id policy identifier
     * @return policy details
     */
    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
    public PolicyResponse get(@PathVariable UUID id) {
        return service.get(id);
    }

    /**
     * Creates a policy record.
     *
     * @param request policy payload
     * @return created policy
     */
    @PostMapping
    @PreAuthorize("hasRole('STAFF')")
    public PolicyResponse create(
            @Valid @RequestBody PolicyCreateRequest request) {
        return service.create(request);
    }

    /**
     * Updates a policy record.
     *
     * @param id policy identifier
     * @param request policy update payload
     * @return updated policy
     */
    @PutMapping("/{id}")
    @PreAuthorize("hasRole('STAFF')")
    public PolicyResponse update(
            @PathVariable UUID id,
            @Valid @RequestBody PolicyUpdateRequest request) {
        return service.update(id, request);
    }

    /**
     * Deletes a policy record.
     *
     * @param id policy identifier
     */
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('STAFF')")
    public void delete(@PathVariable UUID id) {
        service.delete(id);
    }
}
package com.insurewise.policy.dto.request;

import com.insurewise.policy.entity.CategoryStatus;
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

import com.insurewise.policy.entity.CategoryStatus;
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

import com.fasterxml.jackson.annotation.JsonProperty;
import com.insurewise.policy.entity.CoverageType;
import com.insurewise.policy.entity.NomineeRelationship;
import jakarta.validation.constraints.*;
import java.time.LocalDate;
import java.util.UUID;

public record PolicyApplicationCreateRequest(
        @JsonProperty("policy_id")
        @NotNull
        UUID policyId,

        @JsonProperty("coverage_type")
        @NotNull
        CoverageType coverageType,

        @JsonProperty("date_of_birth")
        @NotNull
        @Past
        LocalDate dateOfBirth,

        @NotBlank
        @Size(max = 500)
        String address,

        @JsonProperty("preferred_start_date")
        @FutureOrPresent
        LocalDate preferredStartDate,

        @JsonProperty("nominee_name")
        @Size(max = 120)
        String nomineeName,

        @JsonProperty("nominee_relationship")
        NomineeRelationship nomineeRelationship
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

import com.insurewise.policy.entity.ApplicationStatus;
import java.time.LocalDate;
import java.util.UUID;

public record ApplicationDecisionResponse(
        UUID applicationId,
        String applicationCode,
        ApplicationStatus status,
        LocalDate startDate,
        LocalDate endDate,
        UUID decidedBy
) {
}
package com.insurewise.policy.dto.response;

import com.insurewise.common.dto.PresignedUrlResponse;
import java.util.UUID;

public record ApplicationDocumentResponse(
        UUID id,
        UUID applicationId,
        String fileName,
        String contentType,
        PresignedUrlResponse download,
        UUID uploadedBy
) {
}
package com.insurewise.policy.dto.response;

import com.insurewise.policy.entity.CategoryStatus;

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
        LocalDateTime decidedAt
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
import java.util.UUID;

@Entity
@Table(name = "application_documents")
public class ApplicationDocument {
    @Id
    @GeneratedValue
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "policy_application_id", nullable = false)
    private PolicyApplication policyApplication;

    @Column(name = "file_name", nullable = false, length = 255)
    private String fileName;

    @Column(name = "content_type", length = 100)
    private String contentType;

    @Column(name = "s3_key", nullable = false, length = 600)
    private String s3Key;

    @Column(name = "uploaded_by", nullable = false)
    private UUID uploadedBy;

    protected ApplicationDocument() {
    }

    public ApplicationDocument(
            PolicyApplication policyApplication,
            String fileName,
            String contentType,
            String s3Key,
            UUID uploadedBy) {
        this.policyApplication = policyApplication;
        this.fileName = fileName;
        this.contentType = contentType;
        this.s3Key = s3Key;
        this.uploadedBy = uploadedBy;
    }

    public UUID getId() {
        return id;
    }

    public PolicyApplication getPolicyApplication() {
        return policyApplication;
    }

    public String getFileName() {
        return fileName;
    }

    public String getContentType() {
        return contentType;
    }

    public String getS3Key() {
        return s3Key;
    }

    public UUID getUploadedBy() {
        return uploadedBy;
    }
}
package com.insurewise.policy.entity;

public enum ApplicationStatus {
    PENDING,
    ACTIVE,
    REJECTED,
    EXPIRED
}
package com.insurewise.policy.entity;

import jakarta.persistence.*;
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

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private CategoryStatus status;

    protected Category() {
    }

    public Category(String name, String description, CategoryStatus status) {
        this.name = name;
        this.description = description;
        this.status = status;
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

public enum CoverageType {
    SINGLE,
    GROUP
}
package com.insurewise.policy.entity;

public enum NomineeRelationship {
    SPOUSE,
    PARENT,
    CHILD,
    SIBLING,
    OTHER
}
package com.insurewise.policy.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
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
}
package com.insurewise.policy.entity;

public enum PolicyStatus {
    DRAFT,
    ACTIVE,
    INACTIVE
}
package com.insurewise.policy.exception;

import com.insurewise.common.exception.ResourceNotFoundException;
import java.util.UUID;

public class ApplicationDocumentNotFoundException
        extends ResourceNotFoundException {

    public ApplicationDocumentNotFoundException(UUID id) {
        super(
                "APPLICATION_DOCUMENT_NOT_FOUND",
                "Application document not found: " + id);
    }

    public ApplicationDocumentNotFoundException(
            UUID id,
            Throwable cause) {
        super(
                "APPLICATION_DOCUMENT_NOT_FOUND",
                "Application document not found: " + id,
                cause);
    }
}
package com.insurewise.policy.exception;

import com.insurewise.common.exception.ResourceNotFoundException;
import java.util.UUID;

public class ApplicationNotFoundException extends ResourceNotFoundException {

    public ApplicationNotFoundException(UUID id) {
        super("APPLICATION_NOT_FOUND", "Policy application not found: " + id);
    }

    public ApplicationNotFoundException(
            UUID id,
            Throwable cause) {
        super(
                "APPLICATION_NOT_FOUND",
                "Policy application not found: " + id,
                cause);
    }
}
package com.insurewise.policy.exception;

import com.insurewise.common.exception.BusinessException;

public class ApplicationStateException extends BusinessException {

    public ApplicationStateException(String message) {
        super("APPLICATION_STATE_INVALID", message);
    }

    public ApplicationStateException(
            String message,
            Throwable cause) {
        super("APPLICATION_STATE_INVALID", message, cause);
    }
}
package com.insurewise.policy.exception;

import com.insurewise.common.exception.ResourceNotFoundException;
import java.util.UUID;

public class CategoryNotFoundException extends ResourceNotFoundException {

    public CategoryNotFoundException(UUID id) {
        super("CATEGORY_NOT_FOUND", "Category not found: " + id);
    }

    public CategoryNotFoundException(
            UUID id,
            Throwable cause) {
        super("CATEGORY_NOT_FOUND", "Category not found: " + id, cause);
    }
}
package com.insurewise.policy.exception;

import com.insurewise.common.exception.BusinessException;

public class DuplicatePendingApplicationException
        extends BusinessException {

    public DuplicatePendingApplicationException() {
        super(
                "DUPLICATE_PENDING_APPLICATION",
                "A pending application already exists for this policy");
    }

    public DuplicatePendingApplicationException(Throwable cause) {
        super(
                "DUPLICATE_PENDING_APPLICATION",
                "A pending application already exists for this policy",
                cause);
    }
}
package com.insurewise.policy.exception;

import com.insurewise.common.exception.ResourceNotFoundException;
import java.util.UUID;

public class PolicyNotFoundException extends ResourceNotFoundException {

    public PolicyNotFoundException(UUID id) {
        super("POLICY_NOT_FOUND", "Policy not found: " + id);
    }

    public PolicyNotFoundException(
            UUID id,
            Throwable cause) {
        super("POLICY_NOT_FOUND", "Policy not found: " + id, cause);
    }
}
package com.insurewise.policy.repository;

import com.insurewise.policy.entity.ApplicationDocument;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ApplicationDocumentRepository
        extends JpaRepository<ApplicationDocument, UUID> {

    /**
     * Lists documents for an application in descending identifier order.
     *
     * @param policyApplicationId application identifier
     * @return document list
     */
    List<ApplicationDocument> findByPolicyApplicationIdOrderByIdDesc(
            UUID policyApplicationId);
}
package com.insurewise.policy.repository;

import com.insurewise.policy.entity.Category;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CategoryRepository extends JpaRepository<Category, UUID> {
}
package com.insurewise.policy.repository;

import com.insurewise.policy.entity.ApplicationStatus;
import com.insurewise.policy.entity.PolicyApplication;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface PolicyApplicationRepository
        extends JpaRepository<PolicyApplication, UUID> {

    /**
     * Lists applications for a customer in descending identifier order.
     *
     * @param customerId customer identifier
     * @return application list
     */
    List<PolicyApplication> findByCustomerIdOrderByIdDesc(
            UUID customerId);

    /**
     * Lists applications for a given status in descending identifier order.
     *
     * @param status application status
     * @return application list
     */
    List<PolicyApplication> findByStatusOrderByIdDesc(
            ApplicationStatus status);

    /**
     * Lists customer applications for a given status in descending identifier order.
     *
     * @param customerId customer identifier
     * @param status application status
     * @return application list
     */
    List<PolicyApplication> findByCustomerIdAndStatusOrderByIdDesc(
            UUID customerId,
            ApplicationStatus status);

    /**
     * Checks whether a pending application already exists for the customer and policy.
     *
     * @param customerId customer identifier
     * @param policyId policy identifier
     * @param status application status
     * @return true when a matching application exists
     */
    boolean existsByCustomerIdAndPolicyIdAndStatus(
            UUID customerId,
            UUID policyId,
            ApplicationStatus status);

    /**
     * Reads the next application code sequence value.
     *
     * @return next sequence value
     */
    @Query(
            value = "select nextval('application_code_seq')",
            nativeQuery = true)
    Long nextApplicationCodeSequence();

    /**
     * Counts applications by status.
     *
     * @param status application status
     * @return matching row count
     */
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
    /**
     * Lists policies by status in descending identifier order.
     *
     * @param status policy status
     * @return policy list
     */
    List<Policy> findAllByStatusOrderByIdDesc(PolicyStatus status);

    /**
     * Counts policies by status.
     *
     * @param status policy status
     * @return matching row count
     */
    long countByStatus(
            com.insurewise.policy.entity.PolicyStatus status);
}
package com.insurewise.policy.service;

import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.exception.InfrastructureException;
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

    /**
     * Creates the application document service.
     *
     * @param documentRepository document persistence access
     * @param applicationService application lookup service
     * @param storageService file storage service
     */
    public ApplicationDocumentService(
            ApplicationDocumentRepository documentRepository,
            PolicyApplicationService applicationService,
            S3StorageService storageService) {
        this.documentRepository = documentRepository;
        this.applicationService = applicationService;
        this.storageService = storageService;
    }

    /**
     * Uploads a document for an application.
     *
     * @param principal authenticated principal
     * @param applicationId application identifier
     * @param file document file
     * @return uploaded document response
     */
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
        } catch (ApplicationNotFoundException
                 | InvalidFileException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "APPLICATION_DOCUMENT_UPLOAD_FAILED",
                    "Unable to upload application document",
                    exception);
        }
    }

    /**
     * Lists documents attached to an application.
     *
     * @param principal authenticated principal
     * @param applicationId application identifier
     * @return document responses
     */
    @Transactional(readOnly = true)
    public List<ApplicationDocumentResponse> listDocuments(
            JwtPrincipal principal,
            UUID applicationId) {
        requireApplicationAccess(principal, applicationId);

        return documentRepository
                .findByPolicyApplicationIdOrderByIdDesc(applicationId)
                .stream()
                .map(this::toResponse)
                .toList();
    }

    /**
     * Deletes a document from an application.
     *
     * @param principal authenticated principal
     * @param applicationId application identifier
     * @param documentId document identifier
     */
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
        } catch (ApplicationNotFoundException
                 | ApplicationDocumentNotFoundException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "APPLICATION_DOCUMENT_DELETE_FAILED",
                    "Unable to delete application document",
                    exception);
        }
    }

    /**
     * Checks that the principal can access the target application.
     *
     * @param principal authenticated principal
     * @param applicationId application identifier
     * @return application entity
     */
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

    /**
     * Maps a document entity to its response payload.
     *
     * @param document document entity
     * @return document response
     */
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
                document.getUploadedBy());
    }
}
package com.insurewise.policy.service;

import com.insurewise.policy.dto.request.CategoryCreateRequest;
import com.insurewise.policy.dto.request.CategoryUpdateRequest;
import com.insurewise.policy.dto.response.CategoryResponse;
import com.insurewise.policy.entity.Category;
import com.insurewise.common.exception.InfrastructureException;
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

    /**
     * Creates the category service.
     *
     * @param repository category persistence access
     */
    public CategoryService(CategoryRepository repository) {
        this.repository = repository;
    }

    /**
     * Creates a category.
     *
     * @param request category creation payload
     * @return created category response
     */
    public CategoryResponse create(CategoryCreateRequest request) {
        Category category = repository.save(new Category(
                request.name(),
                request.description(),
                request.status()));

        return toResponse(category);
    }

    /**
     * Lists all categories.
     *
     * @return category responses
     */
    @Transactional(readOnly = true)
    public List<CategoryResponse> list() {
        return repository.findAll()
                .stream()
                .map(this::toResponse)
                .toList();
    }

    /**
     * Updates a category.
     *
     * @param id category identifier
     * @param request category update payload
     * @return updated category response
     */
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
        } catch (CategoryNotFoundException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "CATEGORY_UPDATE_FAILED",
                    "Unable to update category",
                    exception);
        }
    }

    /**
     * Deletes a category by identifier.
     *
     * @param id category identifier
     */
    public void delete(UUID id) {
        try {
            repository.delete(find(id));
        } catch (CategoryNotFoundException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "CATEGORY_DELETE_FAILED",
                    "Unable to delete category",
                    exception);
        }
    }

    /**
     * Finds a category entity by identifier.
     *
     * @param id category identifier
     * @return category entity
     */
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
import com.insurewise.common.exception.InfrastructureException;
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

    /**
     * Creates the dashboard service.
     *
     * @param customerRepository customer persistence access
     * @param staffUserRepository staff user persistence access
     * @param categoryRepository category persistence access
     * @param policyRepository policy persistence access
     * @param applicationRepository application persistence access
     * @param entityManager entity manager for ad hoc counts
     */
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

    /**
     * Loads the dashboard metrics snapshot.
     *
     * @return dashboard metrics
     */
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
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "DASHBOARD_METRICS_FAILED",
                    "Unable to load dashboard metrics",
                    exception);
        }
    }

    /**
     * Counts rows in a table using a native query.
     *
     * @param tableName table name
     * @return row count
     */
    private long countTable(String tableName) {
        Number result = (Number) entityManager
                .createNativeQuery("select count(*) from " + tableName)
                .getSingleResult();

        return result.longValue();
    }

    /**
     * Counts rows by status in a table using a native query.
     *
     * @param tableName table name
     * @param status status value
     * @return row count
     */
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
import com.insurewise.common.exception.InfrastructureException;
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

    /**
     * Creates the policy application service.
     *
     * @param applicationRepository application persistence access
     * @param policyService policy lookup service
     */
    public PolicyApplicationService(
            PolicyApplicationRepository applicationRepository,
            PolicyService policyService) {
        this.applicationRepository = applicationRepository;
        this.policyService = policyService;
    }

    /**
     * Creates a policy application for a customer.
     *
     * @param customerId customer identifier
     * @param request application payload
     * @return created application response
     */
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
        } catch (ApplicationStateException
                 | DuplicatePendingApplicationException
                 | PolicyNotFoundException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "APPLICATION_CREATE_FAILED",
                    "Unable to create application",
                    exception);
        }
    }

    /**
     * Lists applications visible to the current principal.
     *
     * @param principal authenticated principal
     * @param status optional application status filter
     * @return application responses
     */
    @Transactional(readOnly = true)
    public List<PolicyApplicationResponse> listApplications(
            JwtPrincipal principal,
            ApplicationStatus status) {
        List<PolicyApplication> applications;

        if (principal.role().name().equals("STAFF")) {
            applications = status == null
                    ? applicationRepository.findAll()
                    : applicationRepository.findByStatusOrderByIdDesc(
                    status);
        } else {
            applications = status == null
                    ? applicationRepository
                    .findByCustomerIdOrderByIdDesc(
                            principal.userId())
                    : applicationRepository
                    .findByCustomerIdAndStatusOrderByIdDesc(
                            principal.userId(),
                            status);
        }

        return applications.stream()
                .map(this::toResponse)
                .toList();
    }

    /**
     * Loads an application visible to the current principal.
     *
     * @param principal authenticated principal
     * @param applicationId application identifier
     * @return application response
     */
    @Transactional(readOnly = true)
    public PolicyApplicationResponse getApplication(
            JwtPrincipal principal,
            UUID applicationId) {
        PolicyApplication application =
                getApplicationEntity(applicationId);

        if (principal.role().name().equals("CUSTOMER")
                && !application.isOwnedBy(principal.userId())) {
            throw new ApplicationNotFoundException(applicationId);
        }

        return toResponse(application);
    }

    /**
     * Approves an application on behalf of staff.
     *
     * @param staffUserId staff user identifier
     * @param applicationId application identifier
     * @return approval response
     */
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
        } catch (ApplicationNotFoundException
                 | ApplicationStateException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "APPLICATION_APPROVE_FAILED",
                    "Unable to approve application",
                    exception);
        }
    }

    /**
     * Rejects an application on behalf of staff.
     *
     * @param staffUserId staff user identifier
     * @param applicationId application identifier
     * @return rejection response
     */
    public ApplicationDecisionResponse rejectApplication(
            UUID staffUserId,
            UUID applicationId) {
        try {
            PolicyApplication application =
                    getApplicationEntity(applicationId);

            application.reject(staffUserId);

            return toDecisionResponse(application);
        } catch (ApplicationNotFoundException
                 | ApplicationStateException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "APPLICATION_REJECT_FAILED",
                    "Unable to reject application",
                    exception);
        }
    }

    /**
     * Loads an application entity for internal service use.
     *
     * @param applicationId application identifier
     * @return application entity
     */
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
                application.getDecidedAt());
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
import com.insurewise.common.exception.InfrastructureException;
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

    /**
     * Creates the policy service.
     *
     * @param policyRepository policy persistence access
     * @param categoryService category lookup service
     */
    public PolicyService(
            PolicyRepository policyRepository,
            CategoryService categoryService) {
        this.policyRepository = policyRepository;
        this.categoryService = categoryService;
    }

    /**
     * Persists a new policy.
     *
     * @param request policy creation payload
     * @return created policy response
     */
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
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "POLICY_CREATE_FAILED",
                    "Unable to create policy",
                    exception);
        }
    }

    /**
     * Lists policies that are active and available to customers.
     *
     * @return active policy responses
     */
    @Transactional(readOnly = true)
    public List<PolicyResponse> listActive() {
        return policyRepository
                .findAllByStatusOrderByIdDesc(PolicyStatus.ACTIVE)
                .stream()
                .filter(Policy::isActiveForCustomer)
                .map(this::toResponse)
                .toList();
    }

    /**
     * Loads a policy response by identifier.
     *
     * @param id policy identifier
     * @return policy response
     */
    @Transactional(readOnly = true)
    public PolicyResponse get(UUID id) {
        return toResponse(find(id));
    }

    /**
     * Updates an existing policy.
     *
     * @param id policy identifier
     * @param request policy update payload
     * @return updated policy response
     */
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
        } catch (PolicyNotFoundException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "POLICY_UPDATE_FAILED",
                    "Unable to update policy",
                    exception);
        }
    }

    /**
     * Deletes a policy by identifier.
     *
     * @param id policy identifier
     */
    public void delete(UUID id) {
        try {
            policyRepository.delete(find(id));
        } catch (PolicyNotFoundException exception) {
            throw exception;
        } catch (RuntimeException exception) {
            throw new InfrastructureException(
                    "POLICY_DELETE_FAILED",
                    "Unable to delete policy",
                    exception);
        }
    }

    /**
     * Finds a policy entity by identifier.
     *
     * @param id policy identifier
     * @return policy entity
     */
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
package com.insurewise.common.exception;

import com.insurewise.common.dto.ApiErrorResponse;
import com.insurewise.common.dto.FieldErrorResponse;
import com.insurewise.common.web.CorrelationIdFilter;
import jakarta.servlet.http.HttpServletRequest;
import java.time.OffsetDateTime;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.TransactionSystemException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.multipart.MaxUploadSizeExceededException;

@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger LOGGER =
            LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handleNotFound(
            ResourceNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getErrorCode(),
                exception.getMessage(),
                request,
                exception,
                null);
    }

    @ExceptionHandler(ValidationException.class)
    ResponseEntity<ApiErrorResponse> handleValidationException(
            ValidationException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.BAD_REQUEST,
                exception.getErrorCode(),
                exception.getMessage(),
                request,
                exception,
                null);
    }

    @ExceptionHandler(BusinessException.class)
    ResponseEntity<ApiErrorResponse> handleBusinessException(
            BusinessException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.CONFLICT,
                exception.getErrorCode(),
                exception.getMessage(),
                request,
                exception,
                null);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ResponseEntity<ApiErrorResponse> handleMethodArgumentNotValid(
            MethodArgumentNotValidException exception,
            HttpServletRequest request) {

        List<FieldErrorResponse> fieldErrors = exception.getBindingResult()
                .getFieldErrors()
                .stream()
                .map(error -> new FieldErrorResponse(
                        error.getField(),
                        error.getDefaultMessage()))
                .toList();

        String message = fieldErrors.isEmpty()
                ? "Request validation failed"
                : "Request validation failed";

        return build(
                HttpStatus.BAD_REQUEST,
                "VALIDATION_ERROR",
                message,
                request,
                exception,
                fieldErrors);
    }

    @ExceptionHandler(MaxUploadSizeExceededException.class)
    ResponseEntity<ApiErrorResponse> handleMaxUploadSizeExceeded(
            MaxUploadSizeExceededException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.BAD_REQUEST,
                "MAX_UPLOAD_SIZE_EXCEEDED",
                "Uploaded file exceeds the maximum allowed size",
                request,
                exception,
                null);
    }

    @ExceptionHandler({
            DataIntegrityViolationException.class,
            TransactionSystemException.class
    })
    ResponseEntity<ApiErrorResponse> handlePersistenceException(
            Exception exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.CONFLICT,
                "DATA_INTEGRITY_VIOLATION",
                "The request could not be completed because it conflicts with existing data",
                request,
                exception,
                null);
    }

    @ExceptionHandler(InfrastructureException.class)
    ResponseEntity<ApiErrorResponse> handleInfrastructureException(
            InfrastructureException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.INTERNAL_SERVER_ERROR,
                exception.getErrorCode(),
                exception.getMessage(),
                request,
                exception,
                null);
    }

    @ExceptionHandler(Exception.class)
    ResponseEntity<ApiErrorResponse> handleUnhandledException(
            Exception exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.INTERNAL_SERVER_ERROR,
                "INTERNAL_SERVER_ERROR",
                "An unexpected error occurred",
                request,
                exception,
                null);
    }

    private ResponseEntity<ApiErrorResponse> build(
            HttpStatus status,
            String errorCode,
            String message,
            HttpServletRequest request,
            Exception exception,
            List<FieldErrorResponse> fieldErrors) {

        String correlationId = resolveCorrelationId(request);
        logException(status, errorCode, request, correlationId, exception);

        return ResponseEntity.status(status).body(
                new ApiErrorResponse(
                        OffsetDateTime.now(),
                        status.value(),
                        errorCode,
                        message,
                        request.getRequestURI(),
                        correlationId,
                        fieldErrors));
    }

    private void logException(
            HttpStatus status,
            String errorCode,
            HttpServletRequest request,
            String correlationId,
            Exception exception) {

        Throwable rootCause = rootCauseOf(exception);
        LOGGER.error(
                "Request failed: status={}, errorCode={}, path={}, correlationId={}, exceptionType={}, rootCauseType={}, rootCauseMessage={}",
                status.value(),
                errorCode,
                request.getRequestURI(),
                correlationId,
                exception.getClass().getName(),
                rootCause.getClass().getName(),
                rootCause.getMessage(),
                exception);
    }

    private String resolveCorrelationId(HttpServletRequest request) {
        Object correlationId =
                request.getAttribute(CorrelationIdFilter.CORRELATION_ID_ATTRIBUTE);
        return correlationId == null
                ? "unavailable"
                : correlationId.toString();
    }

    private Throwable rootCauseOf(Throwable throwable) {
        Throwable current = throwable;
        while (current.getCause() != null && current.getCause() != current) {
            current = current.getCause();
        }
        return current;
    }
}
explain the codes how the flows works and how method calls service layers and how exception catches the error which tables from db are used are multiple tables connected with outeachother from these explain all also mainly the functions and codes i gave in detail
also explain how the annonations work all of it
also explain the code by code separately
