import com.insurewise.policy.exception.PolicyStateException;

@ExceptionHandler(PolicyStateException.class)
ResponseEntity<ApiErrorResponse> handlePolicyState(
        PolicyStateException exception,
        HttpServletRequest request) {

    return build(
            HttpStatus.CONFLICT,
            exception.getMessage(),
            request.getRequestURI());
}


package com.insurewise.policy.exception;

public class PolicyStateException
        extends RuntimeException {

    public PolicyStateException(String message) {
        super(message);
    }
}




package com.insurewise.policy.dto.request;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class CreateCategoryRequest {

    private String name;

    private String description;

    private String status;
}



package com.insurewise.policy.dto.request;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class UpdateCategoryRequest {

    private String name;

    private String description;

    private String status;
}




package com.insurewise.policy.dto.request;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class CreatePolicyRequest {

    private String name;

    private UUID categoryId;

    private BigDecimal coverageAmount;

    private BigDecimal premiumAmount;

    private String durationLabel;

    private String status;
}





package com.insurewise.policy.dto.request;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class UpdatePolicyRequest {

    private String name;

    private UUID categoryId;

    private BigDecimal coverageAmount;

    private BigDecimal premiumAmount;

    private String durationLabel;

    private String status;
}




package com.insurewise.policy.dto.response;

import com.insurewise.policy.entity.Category;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class CategoryResponse {

    private UUID id;

    private String name;

    private String description;

    private String status;

    private LocalDateTime createdAt;

    public static CategoryResponse from(
            Category category) {

        return new CategoryResponse(
                category.getId(),
                category.getName(),
                category.getDescription(),
                category.getStatus(),
                category.getCreatedAt()
        );
    }
}




package com.insurewise.policy.dto.response;

import com.insurewise.policy.entity.Policy;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class PolicyResponse {

    private UUID id;

    private String name;

    private UUID categoryId;

    private String categoryName;

    private BigDecimal coverageAmount;

    private BigDecimal premiumAmount;

    private String durationLabel;

    private String status;

    private LocalDateTime createdAt;

    public static PolicyResponse from(
            Policy policy) {

        return new PolicyResponse(
                policy.getId(),
                policy.getName(),
                policy.getCategory().getId(),
                policy.getCategory().getName(),
                policy.getCoverageAmount(),
                policy.getPremiumAmount(),
                policy.getDurationLabel(),
                policy.getStatus(),
                policy.getCreatedAt()
        );
    }
}




package com.insurewise.policy.repository;

import com.insurewise.policy.entity.Category;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface CategoryRepository
        extends JpaRepository<Category, UUID> {

    List<Category> findAllByOrderByCreatedAtDesc();

    boolean existsByNameIgnoreCase(String name);
}




package com.insurewise.policy.repository;

import com.insurewise.policy.entity.Policy;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface PolicyRepository
        extends JpaRepository<Policy, UUID> {

    List<Policy> findAllByOrderByCreatedAtDesc();

    List<Policy> findByStatusIgnoreCaseOrderByCreatedAtDesc(
            String status
    );

    boolean existsByCategoryId(UUID categoryId);
}


