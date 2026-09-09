package com.insurewise.auth.dto;

import com.insurewise.auth.entity.StaffUser;

import java.time.LocalDateTime;
import java.util.UUID;

public record StaffUserResponse(
        UUID id,
        String fullName,
        String email,
        String address,
        String profilePictureS3Key,
        LocalDateTime createdAt
) {

    public static StaffUserResponse from(StaffUser staffUser) {
        return new StaffUserResponse(
                staffUser.getId(),
                staffUser.getFullName(),
                staffUser.getEmail(),
                staffUser.getAddress(),
                staffUser.getProfilePictureS3Key(),
                staffUser.getCreatedAt()
        );
    }
}


package com.insurewise.auth.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CreateStaffUserRequest(

        @NotBlank(message = "Name is required")
        @Size(max = 120, message = "Name must not exceed 120 characters")
        String fullName,

        @NotBlank(message = "Email is required")
        @Email(message = "Invalid email format")
        @Size(max = 160, message = "Email must not exceed 160 characters")
        String email,

        @NotBlank(message = "Address is required")
        @Size(max = 240, message = "Address must not exceed 240 characters")
        String address,

        @NotBlank(message = "Password is required")
        @Size(
                min = 8,
                max = 72,
                message = "Password must be between 8 and 72 characters"
        )
        String password
) {
}

package com.insurewise.auth.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record UpdateStaffUserRequest(

        @NotBlank(message = "Name is required")
        @Size(max = 120, message = "Name must not exceed 120 characters")
        String fullName,

        @NotBlank(message = "Email is required")
        @Email(message = "Invalid email format")
        @Size(max = 160, message = "Email must not exceed 160 characters")
        String email,

        @NotBlank(message = "Address is required")
        @Size(max = 240, message = "Address must not exceed 240 characters")
        String address
) {
}
