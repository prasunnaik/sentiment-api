package com.insurewise.policy.repository;

import com.insurewise.policy.entity.Category;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface CategoryRepository
        extends JpaRepository<Category, UUID> {

    boolean existsByNameIgnoreCase(String name);

    boolean existsByNameIgnoreCaseAndIdNot(
            String name,
            UUID id
    );
}


package com.insurewise.policy.repository;

import com.insurewise.policy.entity.Policy;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface PolicyRepository
        extends JpaRepository<Policy, UUID> {

    List<Policy> findByStatusOrderByCreatedAtDesc(
            String status
    );

    boolean existsByCategoryId(UUID categoryId);

    boolean existsByCategoryIdAndStatus(
            UUID categoryId,
            String status
    );
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

    boolean existsByPolicyIdAndStatusIn(
            UUID policyId,
            List<String> statuses
    );

    List<PolicyApplication> findByCustomerIdOrderByCreatedAtDesc(
            UUID customerId
    );
}




package com.insurewise.policy.repository;

import com.insurewise.policy.entity.ApplicationDocument;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface ApplicationDocumentRepository
        extends JpaRepository<ApplicationDocument, UUID> {

    List<ApplicationDocument>
    findByPolicyApplicationIdOrderByCreatedAtDesc(
            UUID policyApplicationId
    );
}



package com.insurewise.policy.repository;

import com.insurewise.policy.entity.Dependent;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface DependentRepository
        extends JpaRepository<Dependent, UUID> {

    List<Dependent> findByPolicyApplicationId(
            UUID policyApplicationId
    );
}



