package com.insurewise.policy.service;



import static org.junit.jupiter.api.Assertions.assertEquals;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import static org.junit.jupiter.api.Assertions.assertThrows;

import static org.junit.jupiter.api.Assertions.assertTrue;

import static org.mockito.ArgumentMatchers.any;

import static org.mockito.Mockito.never;

import static org.mockito.Mockito.verify;

import static org.mockito.Mockito.when;



import com.insurewise.common.exception.BusinessException;

import com.insurewise.policy.dto.request.PolicyCreateRequest;

import com.insurewise.policy.dto.request.PolicyUpdateRequest;

import com.insurewise.policy.dto.response.PolicyResponse;

import com.insurewise.policy.entity.Category;

import com.insurewise.policy.entity.CategoryStatus;

import com.insurewise.policy.entity.Policy;

import com.insurewise.policy.entity.PolicyStatus;

import com.insurewise.policy.exception.PolicyDeletionException;

import com.insurewise.policy.exception.PolicyNotFoundException;

import com.insurewise.policy.repository.PolicyApplicationRepository;

import com.insurewise.policy.repository.PolicyRepository;

import java.math.BigDecimal;

import java.util.List;

import java.util.Optional;

import java.util.UUID;

import org.junit.jupiter.api.BeforeEach;

import org.junit.jupiter.api.Test;

import org.junit.jupiter.api.extension.ExtendWith;

import org.mockito.InjectMocks;

import org.mockito.Mock;

import org.mockito.junit.jupiter.MockitoExtension;



@ExtendWith(MockitoExtension.class)

class PolicyServiceTest {



    @Mock

    private PolicyRepository policyRepository;



    @Mock

    private PolicyApplicationRepository applicationRepository;



    @Mock

    private CategoryService categoryService;



    @InjectMocks

    private PolicyService service;



    private Policy policy;



    @BeforeEach

    void setUp() {

        Category category = new Category("Health", "Health insurance plans", CategoryStatus.ACTIVE);

        policy = new Policy(

                "Standard Plan",

                category,

                BigDecimal.valueOf(250000),

                BigDecimal.valueOf(4999),

                "1 Year",

                PolicyStatus.ACTIVE);

    }



    @Test

    void listActiveShouldReturnOnlyCustomerVisiblePolicies() {

        when(policyRepository.findAllByStatusOrderByCreatedAtDesc(PolicyStatus.ACTIVE)).thenReturn(List.of(policy));



        List responses = service.listActivePolicies();



        assertEquals(1, responses.size());

        assertEquals("Standard Plan", responses.get(0).name());

        assertEquals(PolicyStatus.ACTIVE, responses.get(0).status());

    }



    @Test

    void createShouldSavePolicyAndReturnResponse() {

        UUID categoryId = UUID.randomUUID();

        PolicyCreateRequest request = new PolicyCreateRequest(

                "Standard Plan",

                categoryId,

                BigDecimal.valueOf(250000),

                BigDecimal.valueOf(4999),

                "1 Year",

                PolicyStatus.ACTIVE);

        when(categoryService.find(categoryId)).thenReturn(policy.getCategory());

        when(policyRepository.save(any(Policy.class))).thenReturn(policy);



        PolicyResponse response = service.createPolicy(request);



        assertEquals("Standard Plan", response.name());

        assertEquals(PolicyStatus.ACTIVE, response.status());

    }



    @Test

    void getShouldReturnMappedPolicyResponse() {

        UUID policyId = UUID.randomUUID();

        when(policyRepository.findById(policyId)).thenReturn(Optional.of(policy));



        PolicyResponse response = service.getPolicyById(policyId);



        assertNotNull(response);

        assertEquals("Standard Plan", response.name());

        assertEquals("Health", response.categoryName());

    }



    @Test

    void getShouldThrowWhenPolicyMissing() {

        UUID policyId = UUID.randomUUID();

        when(policyRepository.findById(policyId)).thenReturn(Optional.empty());



        PolicyNotFoundException exception =

                assertThrows(PolicyNotFoundException.class, () -> service.getPolicyById(policyId));



        assertTrue(exception.getMessage().contains(policyId.toString()));

    }



    @Test

    void deleteShouldBlockPoliciesWithApplications() {

        UUID policyId = UUID.randomUUID();

        when(policyRepository.findById(policyId)).thenReturn(Optional.of(policy));

        when(applicationRepository.existsByPolicyId(policyId)).thenReturn(true);



        assertThrows(PolicyDeletionException.class, () -> service.deletePolicy(policyId));



        verify(policyRepository, never()).delete(policy);

    }



    @Test

    void updateShouldModifyExistingPolicy() {

        UUID policyId = UUID.randomUUID();

        UUID categoryId = UUID.randomUUID();

        PolicyUpdateRequest request = new PolicyUpdateRequest(

                "Updated Plan",

                categoryId,

                BigDecimal.valueOf(500000),

                BigDecimal.valueOf(7999),

                "2 Years",

                PolicyStatus.INACTIVE);

        when(policyRepository.findById(policyId)).thenReturn(Optional.of(policy));

        when(categoryService.find(categoryId)).thenReturn(policy.getCategory());



        PolicyResponse response = service.updatePolicy(policyId, request);



        assertEquals("Updated Plan", response.name());

        assertEquals(BigDecimal.valueOf(500000), response.coverageAmount());

        assertEquals(PolicyStatus.INACTIVE, response.status());

    }



    @Test

    void deleteShouldRemovePolicyWhenNoApplicationsExist() {

        UUID policyId = UUID.randomUUID();

        when(policyRepository.findById(policyId)).thenReturn(Optional.of(policy));

        when(applicationRepository.existsByPolicyId(policyId)).thenReturn(false);



        service.deletePolicy(policyId);



        verify(policyRepository).delete(policy);

    }



    @Test

    void listActiveShouldWrapUnexpectedRepositoryFailure() {

        when(policyRepository.findAllByStatusOrderByCreatedAtDesc(PolicyStatus.ACTIVE))

                .thenThrow(new RuntimeException("db error"));



        BusinessException exception = assertThrows(BusinessException.class, () -> service.listActivePolicies());



        assertEquals("POLICY_LIST_FAILED", exception.getErrorCode());

    }

}

what does each annotation does and how does it does
