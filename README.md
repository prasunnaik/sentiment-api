package com.insurewise.policy.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CategoryRequest(

        @NotBlank(message = "Category name is required")
        @Size(max = 80)
        String name,

        @NotBlank(message = "Category description is required")
        @Size(max = 500)
        String description,

        @NotBlank(message = "Category status is required")
        String status
) {
}



package com.insurewise.policy.dto;

import jakarta.validation.constraints.*;

import java.math.BigDecimal;
import java.util.UUID;

public record PolicyRequest(

        @NotBlank(message = "Policy name is required")
        @Size(max = 120)
        String name,

        @NotNull(message = "Category is required")
        UUID categoryId,

        @NotNull(message = "Coverage amount is required")
        @DecimalMin(
                value = "0.01",
                message = "Coverage must be greater than zero"
        )
        BigDecimal coverageAmount,

        @NotNull(message = "Premium amount is required")
        @DecimalMin(
                value = "0.01",
                message = "Premium must be greater than zero"
        )
        BigDecimal premiumAmount,

        @NotBlank(message = "Duration is required")
        @Size(max = 40)
        String durationLabel,

        @NotBlank(message = "Status is required")
        String status
) {
}




package com.insurewise.policy.dto;

import com.insurewise.policy.entity.Policy;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

public record PolicyResponse(

        UUID id,
        String name,
        UUID categoryId,
        String categoryName,
        BigDecimal coverageAmount,
        BigDecimal premiumAmount,
        String durationLabel,
        String status,
        LocalDateTime createdAt
) {

    public static PolicyResponse from(Policy policy) {

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
