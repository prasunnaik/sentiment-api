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
