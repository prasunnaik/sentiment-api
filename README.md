package com.insurewise.policy.service;

import com.insurewise.policy.dto.CategoryRequest;
import com.insurewise.policy.dto.CategoryResponse;
import com.insurewise.policy.entity.Category;
import com.insurewise.policy.repository.CategoryRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@Transactional
public class CategoryService {

    private final CategoryRepository repository;

    public CategoryService(CategoryRepository repository) {
        this.repository = repository;
    }

    @Transactional(readOnly = true)
    public List<CategoryResponse> getAll() {

        return repository.findAll()
                .stream()
                .map(CategoryResponse::from)
                .toList();
    }

    public CategoryResponse create(
            CategoryRequest request
    ) {

        String name = request.name().trim();

        if (repository.existsByNameIgnoreCase(name)) {
            throw new IllegalArgumentException(
                    "Category already exists"
            );
        }

        Category category = new Category();

        category.setName(name);
        category.setDescription(
                request.description().trim()
        );
        category.setStatus(
                request.status().trim().toUpperCase()
        );

        validateStatus(category.getStatus());

        return CategoryResponse.from(
                repository.save(category)
        );
    }

    public CategoryResponse update(
            UUID id,
            CategoryRequest request
    ) {

        Category category = repository.findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Category not found"
                        )
                );

        String name = request.name().trim();

        if (repository.existsByNameIgnoreCaseAndIdNot(
                name,
                id
        )) {
            throw new IllegalArgumentException(
                    "Category already exists"
            );
        }

        category.setName(name);
        category.setDescription(
                request.description().trim()
        );

        String status =
                request.status().trim().toUpperCase();

        validateStatus(status);

        category.setStatus(status);

        return CategoryResponse.from(
                repository.save(category)
        );
    }

    private void validateStatus(String status) {

        if (!status.equals("ACTIVE")
                && !status.equals("INACTIVE")) {

            throw new IllegalArgumentException(
                    "Category status must be ACTIVE or INACTIVE"
            );
        }
    }
}




package com.insurewise.policy.dto;

import com.insurewise.policy.entity.Category;

import java.time.LocalDateTime;
import java.util.UUID;

public record CategoryResponse(
        UUID id,
        String name,
        String description,
        String status,
        LocalDateTime createdAt
) {

    public static CategoryResponse from(Category category) {

        return new CategoryResponse(
                category.getId(),
                category.getName(),
                category.getDescription(),
                category.getStatus(),
                category.getCreatedAt()
        );
    }
}





package com.insurewise.policy.service;

import com.insurewise.policy.dto.PolicyRequest;
import com.insurewise.policy.dto.PolicyResponse;
import com.insurewise.policy.entity.Category;
import com.insurewise.policy.entity.Policy;
import com.insurewise.policy.repository.CategoryRepository;
import com.insurewise.policy.repository.PolicyApplicationRepository;
import com.insurewise.policy.repository.PolicyRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@Transactional
public class PolicyService {

    private final PolicyRepository policyRepository;
    private final CategoryRepository categoryRepository;
    private final PolicyApplicationRepository applicationRepository;

    public PolicyService(
            PolicyRepository policyRepository,
            CategoryRepository categoryRepository,
            PolicyApplicationRepository applicationRepository
    ) {
        this.policyRepository = policyRepository;
        this.categoryRepository = categoryRepository;
        this.applicationRepository = applicationRepository;
    }

    @Transactional(readOnly = true)
    public List<PolicyResponse> getAllPolicies() {

        return policyRepository.findAll()
                .stream()
                .map(PolicyResponse::from)
                .toList();
    }

    @Transactional(readOnly = true)
    public List<PolicyResponse> getActivePolicies() {

        return policyRepository
                .findByStatusOrderByCreatedAtDesc("ACTIVE")
                .stream()
                .map(PolicyResponse::from)
                .toList();
    }

    @Transactional(readOnly = true)
    public PolicyResponse getPolicy(UUID id) {

        return PolicyResponse.from(findPolicy(id));
    }

    public PolicyResponse create(
            PolicyRequest request
    ) {

        validateAmounts(request);

        Category category =
                findCategory(request.categoryId());

        Policy policy = new Policy();

        policy.setName(request.name().trim());
        policy.setCategory(category);
        policy.setCoverageAmount(
                request.coverageAmount()
        );
        policy.setPremiumAmount(
                request.premiumAmount()
        );
        policy.setDurationLabel(
                request.durationLabel().trim()
        );

        String status =
                request.status().trim().toUpperCase();

        validateStatus(status);

        policy.setStatus(status);

        return PolicyResponse.from(
                policyRepository.save(policy)
        );
    }

    public PolicyResponse update(
            UUID id,
            PolicyRequest request
    ) {

        validateAmounts(request);

        Policy policy = findPolicy(id);

        Category category =
                findCategory(request.categoryId());

        String status =
                request.status().trim().toUpperCase();

        validateStatus(status);

        policy.setName(request.name().trim());
        policy.setCategory(category);
        policy.setCoverageAmount(
                request.coverageAmount()
        );
        policy.setPremiumAmount(
                request.premiumAmount()
        );
        policy.setDurationLabel(
                request.durationLabel().trim()
        );
        policy.setStatus(status);

        return PolicyResponse.from(
                policyRepository.save(policy)
        );
    }

    public void delete(UUID id) {

        Policy policy = findPolicy(id);

        boolean hasApplications =
                applicationRepository
                        .existsByPolicyIdAndStatusIn(
                                id,
                                List.of(
                                        "PENDING",
                                        "ACTIVE",
                                        "REJECTED",
                                        "EXPIRED"
                                )
                        );

        if (hasApplications) {

            throw new IllegalStateException(
                    "Policy cannot be deleted because a customer "
                    + "has a policy application against it"
            );
        }

        policyRepository.delete(policy);
    }

    private Policy findPolicy(UUID id) {

        return policyRepository.findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Policy not found"
                        )
                );
    }

    private Category findCategory(UUID id) {

        return categoryRepository.findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Category not found"
                        )
                );
    }

    private void validateAmounts(
            PolicyRequest request
    ) {

        if (request.coverageAmount() == null
                || request.coverageAmount().signum() <= 0) {

            throw new IllegalArgumentException(
                    "Coverage must be greater than zero"
            );
        }

        if (request.premiumAmount() == null
                || request.premiumAmount().signum() <= 0) {

            throw new IllegalArgumentException(
                    "Premium must be greater than zero"
            );
        }
    }

    private void validateStatus(String status) {

        if (!status.equals("DRAFT")
                && !status.equals("ACTIVE")
                && !status.equals("INACTIVE")) {

            throw new IllegalArgumentException(
                    "Invalid policy status"
            );
        }
    }
}






package com.insurewise.policy.controller;

import com.insurewise.policy.dto.PolicyRequest;
import com.insurewise.policy.dto.PolicyResponse;
import com.insurewise.policy.service.PolicyService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/policies")
public class PolicyController {

    private final PolicyService service;

    public PolicyController(PolicyService service) {
        this.service = service;
    }

    @GetMapping
    public List<PolicyResponse> getAll(
            Authentication authentication
    ) {

        requireAuthenticated(authentication);

        return service.getAllPolicies();
    }

    @GetMapping("/active")
    public List<PolicyResponse> getActivePolicies(
            Authentication authentication
    ) {

        requireAuthenticated(authentication);

        return service.getActivePolicies();
    }

    @GetMapping("/{id}")
    public PolicyResponse getById(
            @PathVariable UUID id,
            Authentication authentication
    ) {

        requireAuthenticated(authentication);

        return service.getPolicy(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public PolicyResponse create(
            @Valid @RequestBody PolicyRequest request,
            Authentication authentication
    ) {

        requireStaff(authentication);

        return service.create(request);
    }

    @PutMapping("/{id}")
    public PolicyResponse update(
            @PathVariable UUID id,
            @Valid @RequestBody PolicyRequest request,
            Authentication authentication
    ) {

        requireStaff(authentication);

        return service.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(
            @PathVariable UUID id,
            Authentication authentication
    ) {

        requireStaff(authentication);

        service.delete(id);
    }

    private void requireAuthenticated(
            Authentication authentication
    ) {

        if (authentication == null
                || !authentication.isAuthenticated()) {

            throw new SecurityException(
                    "Authentication required"
            );
        }
    }

    private void requireStaff(
            Authentication authentication
    ) {

        requireAuthenticated(authentication);

        boolean isStaff =
                authentication.getAuthorities()
                        .stream()
                        .anyMatch(a ->
                                a.getAuthority().equals("STAFF")
                                || a.getAuthority().equals("ROLE_STAFF")
                        );

        if (!isStaff) {

            throw new SecurityException(
                    "Only staff users can perform this operation"
            );
        }
    }
}
