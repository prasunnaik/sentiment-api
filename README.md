package com.insurewise.policy.controller;

import com.insurewise.policy.dto.CategoryRequest;
import com.insurewise.policy.dto.CategoryResponse;
import com.insurewise.policy.service.CategoryService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/categories")
public class CategoryController {

    private final CategoryService categoryService;

    public CategoryController(CategoryService categoryService) {
        this.categoryService = categoryService;
    }

    @GetMapping
    public List<CategoryResponse> getAllCategories() {
        return categoryService.getAll();
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CategoryResponse createCategory(
            @Valid @RequestBody CategoryRequest request
    ) {
        return categoryService.create(request);
    }

    @PutMapping("/{id}")
    public CategoryResponse updateCategory(
            @PathVariable UUID id,
            @Valid @RequestBody CategoryRequest request
    ) {
        return categoryService.update(id, request);
    }
}



package com.insurewise.policy.controller;

import com.insurewise.policy.dto.PolicyRequest;
import com.insurewise.policy.dto.PolicyResponse;
import com.insurewise.policy.service.PolicyService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/policies")
public class PolicyController {

    private final PolicyService policyService;

    public PolicyController(PolicyService policyService) {
        this.policyService = policyService;
    }

    /*
     * Staff dashboard can use this endpoint.
     */
    @GetMapping
    public List<PolicyResponse> getAllPolicies() {
        return policyService.getAllPolicies();
    }

    /*
     * Customer-facing endpoint.
     *
     * IMPORTANT:
     * Only ACTIVE policies should be returned here.
     */
    @GetMapping("/active")
    public List<PolicyResponse> getActivePolicies() {
        return policyService.getActivePolicies();
    }

    @GetMapping("/{id}")
    public PolicyResponse getPolicy(
            @PathVariable UUID id
    ) {
        return policyService.getPolicy(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public PolicyResponse createPolicy(
            @Valid @RequestBody PolicyRequest request
    ) {
        return policyService.create(request);
    }

    @PutMapping("/{id}")
    public PolicyResponse updatePolicy(
            @PathVariable UUID id,
            @Valid @RequestBody PolicyRequest request
    ) {
        return policyService.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deletePolicy(
            @PathVariable UUID id
    ) {
        policyService.delete(id);
    }
}




package com.insurewise.policy.repository;

import com.insurewise.policy.entity.PolicyApplication;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface PolicyApplicationRepository
        extends JpaRepository<PolicyApplication, UUID> {

    List<PolicyApplication> findByStatusOrderByCreatedAtAsc(
            String status
    );

    boolean existsByPolicyId(UUID policyId);

    List<PolicyApplication> findByCustomerIdOrderByCreatedAtDesc(
            UUID customerId
    );
}



public void delete(UUID id) {

    findPolicy(id);

    boolean hasApplications =
            applicationRepository.existsByPolicyId(id);

    if (hasApplications) {
        throw new IllegalStateException(
                "Policy cannot be deleted because a customer "
                        + "has a policy application against it"
        );
    }

    policyRepository.deleteById(id);
}



