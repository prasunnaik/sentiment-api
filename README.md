package com.insurewise.policy.controller;

import com.insurewise.policy.dto.request.CategoryCreateRequest;
import com.insurewise.policy.dto.request.CategoryUpdateRequest;
import com.insurewise.policy.service.CategoryService;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/categories")
public class CategoryController {

    private final CategoryService categoryService;

    public CategoryController(
            CategoryService categoryService) {

        this.categoryService = categoryService;
    }

    @GetMapping
    public ResponseEntity<?> getAll() {

        try {

            return ResponseEntity.ok(
                    categoryService.getAll()
            );

        } catch (Exception e) {

            throw e;
        }
    }

    @GetMapping("/active")
    public ResponseEntity<?> getActive() {

        try {

            return ResponseEntity.ok(
                    categoryService.getActive()
            );

        } catch (Exception e) {

            throw e;
        }
    }

    @PostMapping
    @PreAuthorize("hasRole('STAFF')")
    public ResponseEntity<?> create(
            @RequestBody
            CategoryCreateRequest request) {

        try {

            return ResponseEntity
                    .status(HttpStatus.CREATED)
                    .body(
                            categoryService.create(request)
                    );

        } catch (Exception e) {

            throw e;
        }
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('STAFF')")
    public ResponseEntity<?> update(
            @PathVariable UUID id,
            @RequestBody
            CategoryUpdateRequest request) {

        try {

            return ResponseEntity.ok(
                    categoryService.update(
                            id,
                            request
                    )
            );

        } catch (Exception e) {

            throw e;
        }
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('STAFF')")
    public ResponseEntity<?> delete(
            @PathVariable UUID id) {

        try {

            categoryService.delete(id);

            return ResponseEntity
                    .noContent()
                    .build();

        } catch (Exception e) {

            throw e;
        }
    }
}

package com.insurewise.policy.service;

import com.insurewise.policy.dto.request.CategoryCreateRequest;
import com.insurewise.policy.dto.request.CategoryCreateRequest;
import com.insurewise.policy.dto.response.CategoryResponse;
import com.insurewise.policy.entity.Category;
import com.insurewise.policy.exception.CategoryNotFoundException;
import com.insurewise.policy.repository.CategoryRepository;
import com.insurewise.policy.repository.PolicyRepository;

import lombok.extern.slf4j.Slf4j;

import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Service
@Slf4j
public class CategoryService {

    private final CategoryRepository categoryRepository;

    private final PolicyRepository policyRepository;

    public CategoryService(
            CategoryRepository categoryRepository,
            PolicyRepository policyRepository) {

        this.categoryRepository = categoryRepository;
        this.policyRepository = policyRepository;
    }

    // =========================
    // GET ALL
    // =========================

    public List<CategoryResponse> getAll() {

        try {

            return categoryRepository
                    .findAllByOrderByCreatedAtDesc()
                    .stream()
                    .map(CategoryResponse::from)
                    .toList();

        } catch (Exception e) {

            log.error(
                    "Error fetching categories",
                    e
            );

            throw new RuntimeException(
                    "Unable to fetch categories: "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // GET ACTIVE
    // =========================

    public List<CategoryResponse> getActive() {

        try {

            return categoryRepository
                    .findAllByOrderByCreatedAtDesc()
                    .stream()
                    .filter(category ->
                            "ACTIVE".equalsIgnoreCase(
                                    category.getStatus()
                            ))
                    .map(CategoryResponse::from)
                    .toList();

        } catch (Exception e) {

            log.error(
                    "Error fetching active categories",
                    e
            );

            throw new RuntimeException(
                    "Unable to fetch active categories: "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // CREATE
    // =========================

    public CategoryResponse create(
            CategoryCreateRequest request) {

        try {

            validateRequest(request);

            String name =
                    request.getName().trim();

            if (categoryRepository
                    .existsByNameIgnoreCase(name)) {

                throw new IllegalArgumentException(
                        "Category already exists: "
                                + name
                );
            }

            Category category =
                    new Category();

            category.setName(name);

            category.setDescription(
                    request.getDescription().trim()
            );

            String status =
                    request.getStatus();

            if (status == null
                    || status.isBlank()) {

                status = "ACTIVE";
            }

            status = status.trim().toUpperCase();

            validateStatus(status);

            category.setStatus(status);

            Category saved =
                    categoryRepository.save(category);

            return CategoryResponse.from(saved);

        } catch (Exception e) {

            log.error(
                    "Error creating category",
                    e
            );

            /*
             * Preserve the original exception if it is
             * already meaningful.
             */
            if (e instanceof IllegalArgumentException) {
                throw e;
            }

            throw new RuntimeException(
                    "Unable to create category: "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // UPDATE
    // =========================

    public CategoryResponse update(
            UUID id,
            CategoryUpdateRequest request) {

        try {

            if (id == null) {

                throw new IllegalArgumentException(
                        "Category id is required."
                );
            }

            validateRequest(request);

            Category category =
                    categoryRepository
                            .findById(id)
                            .orElseThrow(() ->
                                    new CategoryNotFoundException(
                                            "Category not found: "
                                                    + id
                                    )
                            );

            category.setName(
                    request.getName().trim()
            );

            category.setDescription(
                    request.getDescription().trim()
            );

            String status =
                    request.getStatus()
                            .trim()
                            .toUpperCase();

            validateStatus(status);

            category.setStatus(status);

            Category updated =
                    categoryRepository.save(category);

            return CategoryResponse.from(updated);

        } catch (CategoryNotFoundException e) {

            throw e;

        } catch (Exception e) {

            log.error(
                    "Error updating category {}",
                    id,
                    e
            );

            throw new RuntimeException(
                    "Unable to update category "
                            + id + ": "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // DELETE
    // =========================

    public void delete(UUID id) {

        try {

            if (id == null) {

                throw new IllegalArgumentException(
                        "Category id is required."
                );
            }

            Category category =
                    categoryRepository
                            .findById(id)
                            .orElseThrow(() ->
                                    new CategoryNotFoundException(
                                            "Category not found: "
                                                    + id
                                    )
                            );

            if ("ACTIVE".equalsIgnoreCase(
                    category.getStatus())) {

                throw new IllegalStateException(
                        "Active category cannot be deleted. "
                                + "Set the category to INACTIVE first."
                );
            }

            if (policyRepository
                    .existsByCategoryId(id)) {

                throw new IllegalStateException(
                        "Category cannot be deleted because "
                                + "policies are associated with it."
                );
            }

            categoryRepository.delete(category);

        } catch (CategoryNotFoundException e) {

            throw e;

        } catch (Exception e) {

            log.error(
                    "Error deleting category {}",
                    id,
                    e
            );

            throw new RuntimeException(
                    "Unable to delete category "
                            + id + ": "
                            + rootMessage(e),
                    e
            );
        }
    }

    private void validateRequest(
            CategoryCreateRequest request) {

        if (request == null) {

            throw new IllegalArgumentException(
                    "Category request cannot be null."
            );
        }

        validateFields(
                request.getName(),
                request.getDescription()
        );
    }

    private void validateRequest(
            CategoryUpdateRequest request) {

        if (request == null) {

            throw new IllegalArgumentException(
                    "Category request cannot be null."
            );
        }

        validateFields(
                request.getName(),
                request.getDescription()
        );
    }

    private void validateFields(
            String name,
            String description) {

        if (name == null || name.isBlank()) {

            throw new IllegalArgumentException(
                    "Category name is required."
            );
        }

        if (description == null
                || description.isBlank()) {

            throw new IllegalArgumentException(
                    "Category description is required."
            );
        }

        if (name.trim().length() > 80) {

            throw new IllegalArgumentException(
                    "Category name cannot exceed 80 characters."
            );
        }

        if (description.trim().length() > 500) {

            throw new IllegalArgumentException(
                    "Category description cannot exceed 500 characters."
            );
        }
    }

    private void validateStatus(
            String status) {

        if (!"ACTIVE".equals(status)
                && !"INACTIVE".equals(status)) {

            throw new IllegalArgumentException(
                    "Category status must be ACTIVE or INACTIVE."
            );
        }
    }

    private String rootMessage(Exception e) {

        Throwable current = e;

        while (current.getCause() != null) {
            current = current.getCause();
        }

        return current.getMessage() == null
                ? current.getClass().getSimpleName()
                : current.getMessage();
    }
}
package com.insurewise.policy.service;

import com.insurewise.policy.dto.request.CreatePolicyRequest;
import com.insurewise.policy.dto.request.PolicyCreateRequest;
import com.insurewise.policy.dto.request.PolicyUpdateRequest;
import com.insurewise.policy.dto.request.UpdatePolicyRequest;
import com.insurewise.policy.dto.response.PolicyResponse;
import com.insurewise.policy.entity.Category;
import com.insurewise.policy.entity.Policy;
import com.insurewise.policy.exception.CategoryNotFoundException;
import com.insurewise.policy.exception.PolicyNotFoundException;
import com.insurewise.policy.exception.PolicyStateException;
import com.insurewise.policy.repository.CategoryRepository;
import com.insurewise.policy.repository.PolicyRepository;

import lombok.extern.slf4j.Slf4j;

import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Service
@Slf4j
public class PolicyService {

    private final PolicyRepository policyRepository;

    private final CategoryRepository categoryRepository;

    public PolicyService(
            PolicyRepository policyRepository,
            CategoryRepository categoryRepository) {

        this.policyRepository = policyRepository;
        this.categoryRepository = categoryRepository;
    }

    // =========================
    // GET ALL POLICIES
    // =========================

    public List<PolicyResponse> getAll() {

        try {

            return policyRepository
                    .findAllByOrderByCreatedAtDesc()
                    .stream()
                    .map(PolicyResponse::from)
                    .toList();

        } catch (Exception e) {

            log.error(
                    "Error fetching policies",
                    e
            );

            throw new RuntimeException(
                    "Unable to fetch policies: "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // GET ACTIVE
    // =========================

    public List<PolicyResponse> getActive() {

        try {

            return policyRepository
                    .findByStatusIgnoreCaseOrderByCreatedAtDesc(
                            "ACTIVE"
                    )
                    .stream()
                    .map(PolicyResponse::from)
                    .toList();

        } catch (Exception e) {

            log.error(
                    "Error fetching active policies",
                    e
            );

            throw new RuntimeException(
                    "Unable to fetch active policies: "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // GET PENDING
    // =========================

    public List<PolicyResponse> getPending() {

        try {

            return policyRepository
                    .findByStatusIgnoreCaseOrderByCreatedAtDesc(
                            "PENDING"
                    )
                    .stream()
                    .map(PolicyResponse::from)
                    .toList();

        } catch (Exception e) {

            log.error(
                    "Error fetching pending policies",
                    e
            );

            throw new RuntimeException(
                    "Unable to fetch pending policies: "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // GET REJECTED
    // =========================

    public List<PolicyResponse> getRejected() {

        try {

            return policyRepository
                    .findByStatusIgnoreCaseOrderByCreatedAtDesc(
                            "REJECTED"
                    )
                    .stream()
                    .map(PolicyResponse::from)
                    .toList();

        } catch (Exception e) {

            log.error(
                    "Error fetching rejected policies",
                    e
            );

            throw new RuntimeException(
                    "Unable to fetch rejected policies: "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // ADD POLICY
    // =========================

    public PolicyResponse create(
            PolicyCreateRequest request) {

        try {

            validateRequest(request);

            Category category =
                    categoryRepository
                            .findById(
                                    request.getCategoryId()
                            )
                            .orElseThrow(() ->
                                    new CategoryNotFoundException(
                                            "Category not found: "
                                                    + request.getCategoryId()
                                    )
                            );

            if (!"ACTIVE".equalsIgnoreCase(
                    category.getStatus())) {

                throw new PolicyStateException(
                        "Policy cannot be created under "
                                + "an INACTIVE category."
                );
            }

            /*
             * Always start with PENDING.
             */
            Policy policy =
                    new Policy();

            policy.setName(
                    request.getName().trim()
            );

            policy.setCategory(category);

            policy.setCoverageAmount(
                    request.getCoverageAmount()
            );

            policy.setPremiumAmount(
                    request.getPremiumAmount()
            );

            policy.setDurationLabel(
                    request.getDurationLabel().trim()
            );

            policy.setStatus("PENDING");

            Policy saved =
                    policyRepository.save(policy);

            return PolicyResponse.from(saved);

        } catch (CategoryNotFoundException e) {

            throw e;

        } catch (PolicyStateException e) {

            throw e;

        } catch (IllegalArgumentException e) {

            throw e;

        } catch (Exception e) {

            log.error(
                    "Error creating policy",
                    e
            );

            throw new RuntimeException(
                    "Unable to create policy: "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // UPDATE POLICY
    // =========================

    public PolicyResponse update(
            UUID id,
            PolicyUpdateRequest request) {

        try {

            validateId(id);

            validateRequest(request);

            Policy policy =
                    policyRepository
                            .findById(id)
                            .orElseThrow(() ->
                                    new PolicyNotFoundException(
                                            "Policy not found: "
                                                    + id
                                    )
                            );

            Category category =
                    categoryRepository
                            .findById(
                                    request.getCategoryId()
                            )
                            .orElseThrow(() ->
                                    new CategoryNotFoundException(
                                            "Category not found: "
                                                    + request.getCategoryId()
                                    )
                            );

            if (!"ACTIVE".equalsIgnoreCase(
                    category.getStatus())) {

                throw new PolicyStateException(
                        "Policy cannot use an INACTIVE category."
                );
            }

            policy.setName(
                    request.getName().trim()
            );

            policy.setCategory(category);

            policy.setCoverageAmount(
                    request.getCoverageAmount()
            );

            policy.setPremiumAmount(
                    request.getPremiumAmount()
            );

            policy.setDurationLabel(
                    request.getDurationLabel().trim()
            );

            /*
             * Editing requires approval again.
             */
            policy.setStatus("PENDING");

            Policy updated =
                    policyRepository.save(policy);

            return PolicyResponse.from(updated);

        } catch (PolicyNotFoundException e) {

            throw e;

        } catch (CategoryNotFoundException e) {

            throw e;

        } catch (PolicyStateException e) {

            throw e;

        } catch (IllegalArgumentException e) {

            throw e;

        } catch (Exception e) {

            log.error(
                    "Error updating policy {}",
                    id,
                    e
            );

            throw new RuntimeException(
                    "Unable to update policy "
                            + id + ": "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // APPROVE POLICY
    // =========================

    public PolicyResponse approve(UUID id) {

        try {

            validateId(id);

            Policy policy =
                    policyRepository
                            .findById(id)
                            .orElseThrow(() ->
                                    new PolicyNotFoundException(
                                            "Policy not found: "
                                                    + id
                                    )
                            );

            if (!"PENDING".equalsIgnoreCase(
                    policy.getStatus())) {

                throw new PolicyStateException(
                        "Only PENDING policies can be approved. "
                                + "Current status: "
                                + policy.getStatus()
                );
            }

            if (!"ACTIVE".equalsIgnoreCase(
                    policy.getCategory().getStatus())) {

                throw new PolicyStateException(
                        "Policy cannot be approved because "
                                + "its category is INACTIVE."
                );
            }

            policy.setStatus("ACTIVE");

            Policy approved =
                    policyRepository.save(policy);

            return PolicyResponse.from(approved);

        } catch (PolicyNotFoundException e) {

            throw e;

        } catch (PolicyStateException e) {

            throw e;

        } catch (Exception e) {

            log.error(
                    "Error approving policy {}",
                    id,
                    e
            );

            throw new RuntimeException(
                    "Unable to approve policy "
                            + id + ": "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // REJECT POLICY
    // =========================

    public PolicyResponse reject(UUID id) {

        try {

            validateId(id);

            Policy policy =
                    policyRepository
                            .findById(id)
                            .orElseThrow(() ->
                                    new PolicyNotFoundException(
                                            "Policy not found: "
                                                    + id
                                    )
                            );

            if (!"PENDING".equalsIgnoreCase(
                    policy.getStatus())) {

                throw new PolicyStateException(
                        "Only PENDING policies can be rejected. "
                                + "Current status: "
                                + policy.getStatus()
                );
            }

            policy.setStatus("REJECTED");

            Policy rejected =
                    policyRepository.save(policy);

            return PolicyResponse.from(rejected);

        } catch (PolicyNotFoundException e) {

            throw e;

        } catch (PolicyStateException e) {

            throw e;

        } catch (Exception e) {

            log.error(
                    "Error rejecting policy {}",
                    id,
                    e
            );

            throw new RuntimeException(
                    "Unable to reject policy "
                            + id + ": "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // DELETE POLICY
    // =========================

    public void delete(UUID id) {

        try {

            validateId(id);

            Policy policy =
                    policyRepository
                            .findById(id)
                            .orElseThrow(() ->
                                    new PolicyNotFoundException(
                                            "Policy not found: "
                                                    + id
                                    )
                            );

            policyRepository.delete(policy);

        } catch (PolicyNotFoundException e) {

            throw e;

        } catch (Exception e) {

            log.error(
                    "Error deleting policy {}",
                    id,
                    e
            );

            throw new RuntimeException(
                    "Unable to delete policy "
                            + id + ": "
                            + rootMessage(e),
                    e
            );
        }
    }

    // =========================
    // VALIDATION
    // =========================

    private void validateRequest(
            CreatePolicyRequest request) {

        if (request == null) {

            throw new IllegalArgumentException(
                    "Policy request cannot be null."
            );
        }

        validateFields(
                request.getName(),
                request.getCategoryId(),
                request.getCoverageAmount(),
                request.getPremiumAmount(),
                request.getDurationLabel()
        );
    }

    private void validateRequest(
            UpdatePolicyRequest request) {

        if (request == null) {

            throw new IllegalArgumentException(
                    "Policy request cannot be null."
            );
        }

        validateFields(
                request.getName(),
                request.getCategoryId(),
                request.getCoverageAmount(),
                request.getPremiumAmount(),
                request.getDurationLabel()
        );
    }

    private void validateFields(
            String name,
            UUID categoryId,
            BigDecimal coverage,
            BigDecimal premium,
            String duration) {

        if (name == null || name.isBlank()) {

            throw new IllegalArgumentException(
                    "Policy name is required."
            );
        }

        if (categoryId == null) {

            throw new IllegalArgumentException(
                    "Category id is required."
            );
        }

        if (coverage == null) {

            throw new IllegalArgumentException(
                    "Coverage amount is required."
            );
        }

        if (coverage.compareTo(
                BigDecimal.ZERO) <= 0) {

            throw new IllegalArgumentException(
                    "Coverage amount must be greater than zero."
            );
        }

        if (premium == null) {

            throw new IllegalArgumentException(
                    "Premium amount is required."
            );
        }

        if (premium.compareTo(
                BigDecimal.ZERO) <= 0) {

            throw new IllegalArgumentException(
                    "Premium amount must be greater than zero."
            );
        }

        if (duration == null
                || duration.isBlank()) {

            throw new IllegalArgumentException(
                    "Policy duration is required."
            );
        }
    }

    private void validateId(UUID id) {

        if (id == null) {

            throw new IllegalArgumentException(
                    "Policy id is required."
            );
        }
    }

    private String rootMessage(Exception e) {

        Throwable current = e;

        while (current.getCause() != null) {
            current = current.getCause();
        }

        return current.getMessage() == null
                ? current.getClass().getSimpleName()
                : current.getMessage();
    }
}
