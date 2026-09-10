package com.insurewise.auth.controller;

import com.insurewise.auth.dto.request.StaffCreateRequest;
import com.insurewise.auth.dto.request.StaffUpdateRequest;
import com.insurewise.auth.dto.response.StaffProfileResponse;
import com.insurewise.auth.service.StaffUserService;
import jakarta.validation.Valid;
import java.util.List;
import java.util.UUID;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/staff/users")
@PreAuthorize("hasRole('STAFF')")
public class StaffUserManagementController {

    private final StaffUserService staffUserService;

    public StaffUserManagementController(
            StaffUserService staffUserService) {

        this.staffUserService = staffUserService;
    }

    @PostMapping
    public ResponseEntity<StaffProfileResponse> create(
            @Valid @RequestBody StaffCreateRequest request) {

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(staffUserService.create(request));
    }

    @GetMapping
    public List<StaffProfileResponse> list() {

        return staffUserService.list();
    }

    @GetMapping("/{id}")
    public StaffProfileResponse get(
            @PathVariable UUID id) {

        return staffUserService.get(id);
    }

    @PutMapping("/{id}")
    public StaffProfileResponse update(
            @PathVariable UUID id,
            @Valid @RequestBody StaffUpdateRequest request) {

        return staffUserService.update(id, request);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID id) {

        staffUserService.delete(id);

        return ResponseEntity.noContent().build();
    }
}
package com.insurewise.auth.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record StaffCreateRequest(

        @NotBlank
        @Size(max = 120)
        String fullName,

        @NotBlank
        @Email
        @Size(max = 160)
        String email,

        @NotBlank
        @Size(max = 240)
        String address,

        @NotBlank
        @Size(min = 8, max = 100)
        String password
) {
}
package com.insurewise.auth.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record StaffUpdateRequest(

        @NotBlank
        @Size(max = 120)
        String fullName,

        @NotBlank
        @Email
        @Size(max = 160)
        String email,

        @NotBlank
        @Size(max = 240)
        String address,

        @Size(min = 8, max = 100)
        String password
) {
}
package com.insurewise.auth.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.UUID;

public record StaffProfileResponse(
        UUID id,

        @JsonProperty("full_name")
        String fullName,

        String email,
        String address
) {
}
package com.insurewise.auth.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.PrePersist;
import jakarta.persistence.Table;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "staff_users")
public class StaffUser {
    @Id
    private UUID id;

    @Column(name = "full_name", nullable = false, length = 120)
    private String fullName;

    @Column(nullable = false, unique = true, length = 160)
    private String email;

    @Column(nullable = false, length = 240)
    private String address;

    @Column(name = "password_hash", nullable = false, length = 100)
    private String passwordHash;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    protected StaffUser() {
    }

    public StaffUser(
            String fullName,
            String email,
            String address,
            String passwordHash) {
        this.id = UUID.randomUUID();
        this.fullName = fullName;
        this.email = email.toLowerCase();
        this.address = address;
        this.passwordHash = passwordHash;
    }

    @PrePersist
    void prePersist() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
    }

    public UUID getId() {
        return id;
    }

    public String getFullName() {
        return fullName;
    }

    public String getEmail() {
        return email;
    }

    public String getAddress() {
        return address;
    }

    public String getPasswordHash() {
        return passwordHash;
    }

    public void update(
            String fullName,
            String email,
            String address,
            String passwordHash) {

        this.fullName = fullName;
        this.email = email.toLowerCase();
        this.address = address;

        if (passwordHash != null && !passwordHash.isBlank()) {
            this.passwordHash = passwordHash;
        }
    }
}
package com.insurewise.auth.exception;

import java.util.UUID;

public class StaffUserNotFoundException extends RuntimeException {

    public StaffUserNotFoundException(UUID id) {
        super("Staff user not found: " + id);
    }
}
package com.insurewise.auth.repository;

import com.insurewise.auth.entity.StaffUser;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StaffUserRepository extends JpaRepository<StaffUser, UUID> {
    boolean existsByEmailIgnoreCase(String email);

    Optional<StaffUser> findByEmailIgnoreCase(String email);
}
package com.insurewise.auth.service;

import com.insurewise.auth.dto.request.StaffCreateRequest;
import com.insurewise.auth.dto.request.StaffUpdateRequest;
import com.insurewise.auth.dto.response.StaffProfileResponse;
import com.insurewise.auth.entity.StaffUser;
import com.insurewise.auth.exception.DuplicateEmailException;
import com.insurewise.auth.repository.CustomerRepository;
import com.insurewise.auth.repository.StaffUserRepository;
import java.util.List;
import java.util.UUID;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.insurewise.auth.exception.StaffUserNotFoundException;

@Service
@Transactional
public class StaffUserService {

    private final StaffUserRepository staffUserRepository;
    private final CustomerRepository customerRepository;
    private final PasswordEncoder passwordEncoder;

    public StaffUserService(
            StaffUserRepository staffUserRepository,
            CustomerRepository customerRepository,
            PasswordEncoder passwordEncoder) {

        this.staffUserRepository = staffUserRepository;
        this.customerRepository = customerRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public StaffProfileResponse create(
            StaffCreateRequest request) {

        try {
            String email = request.email().toLowerCase();

            validateEmailNotUsed(email);

            StaffUser staffUser = new StaffUser(
                    request.fullName(),
                    email,
                    request.address(),
                    passwordEncoder.encode(request.password()));

            return toResponse(
                    staffUserRepository.save(staffUser));

        } catch (Exception exception) {
            System.err.println(
                    "Error in StaffUserService.create: "
                            + exception.getMessage());

            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public List<StaffProfileResponse> list() {

        try {
            return staffUserRepository.findAll()
                    .stream()
                    .map(this::toResponse)
                    .toList();

        } catch (Exception exception) {
            System.err.println(
                    "Error in StaffUserService.list: "
                            + exception.getMessage());

            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public StaffProfileResponse get(UUID id) {

        try {
            return toResponse(find(id));

        } catch (Exception exception) {
            System.err.println(
                    "Error in StaffUserService.get: "
                            + exception.getMessage());

            throw exception;
        }
    }

    public StaffProfileResponse update(
            UUID id,
            StaffUpdateRequest request) {

        try {

            StaffUser staffUser = find(id);

            String email = request.email().toLowerCase();

            boolean emailUsedByAnotherStaff =
                    staffUserRepository
                            .findByEmailIgnoreCase(email)
                            .filter(existing ->
                                    !existing.getId().equals(id))
                            .isPresent();

            boolean emailUsedByCustomer =
                    customerRepository
                            .existsByEmailIgnoreCase(email);

            if (emailUsedByAnotherStaff
                    || emailUsedByCustomer) {
                throw new DuplicateEmailException(email);
            }

            String passwordHash = null;

            if (request.password() != null
                    && !request.password().isBlank()) {

                passwordHash =
                        passwordEncoder.encode(request.password());
            }

            staffUser.update(
                    request.fullName(),
                    email,
                    request.address(),
                    passwordHash);

            return toResponse(staffUser);

        } catch (Exception exception) {
            System.err.println(
                    "Error in StaffUserService.update: "
                            + exception.getMessage());

            throw exception;
        }
    }

    public void delete(UUID id) {

        try {
            StaffUser staffUser = find(id);

            staffUserRepository.delete(staffUser);

        } catch (Exception exception) {
            System.err.println(
                    "Error in StaffUserService.delete: "
                            + exception.getMessage());

            throw exception;
        }
    }

    private StaffUser find(UUID id) {

        return staffUserRepository.findById(id)
                .orElseThrow(() ->
                        new StaffUserNotFoundException(id));
    }

    private void validateEmailNotUsed(String email) {

        if (staffUserRepository.existsByEmailIgnoreCase(email)
                || customerRepository.existsByEmailIgnoreCase(email)) {

            throw new DuplicateEmailException(email);
        }
    }

    private StaffProfileResponse toResponse(
            StaffUser staffUser) {

        return new StaffProfileResponse(
                staffUser.getId(),
                staffUser.getFullName(),
                staffUser.getEmail(),
                staffUser.getAddress());
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

    public PolicyApplicationController(
            PolicyApplicationService service) {
        this.service = service;
    }

    @PostMapping
    @PreAuthorize("hasRole('CUSTOMER')")
    public PolicyApplicationResponse create(
            @AuthenticationPrincipal JwtPrincipal principal,
            @Valid @RequestBody PolicyApplicationCreateRequest request) {
        return service.createApplication(principal.userId(), request);
    }

    @GetMapping
    @PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
    public List<PolicyApplicationResponse> list(
            @AuthenticationPrincipal JwtPrincipal principal,
            @RequestParam(required = false) ApplicationStatus status) {
        return service.listApplications(principal, status);
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
    public PolicyApplicationResponse get(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id) {
        return service.getApplication(principal, id);
    }

    @PutMapping("/{id}/approve")
    @PreAuthorize("hasRole('STAFF')")
    public ApplicationDecisionResponse approve(
            @AuthenticationPrincipal JwtPrincipal principal,
            @PathVariable UUID id) {
        return service.approveApplication(principal.userId(), id);
    }

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

public enum ApplicationStatus {
    PENDING,
    ACTIVE,
    REJECTED,
    EXPIRED
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
package com.insurewise.policy.exception;

import java.util.UUID;

public class ApplicationNotFoundException extends RuntimeException {
    public ApplicationNotFoundException(UUID id) {
        super("Policy application not found: " + id);
    }
}
package com.insurewise.policy.exception;

public class ApplicationStateException extends RuntimeException {
    public ApplicationStateException(String message) {
        super(message);
    }
}
package com.insurewise.policy.exception;

public class DuplicatePendingApplicationException
        extends RuntimeException {

    public DuplicatePendingApplicationException() {
        super("A pending application already exists for this policy");
    }
}
package com.insurewise.policy.exception;

import java.util.UUID;

public class PolicyNotFoundException extends RuntimeException {

    public PolicyNotFoundException(UUID id) {
        super("Policy not found: " + id);
    }
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
