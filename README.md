package com.insurewise.auth.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "staff_users")
@Getter
@Setter
@NoArgsConstructor
public class StaffUser {

    @Id
    @Column(nullable = false)
    private UUID id;

    @Column(name = "full_name", nullable = false, length = 120)
    private String fullName;

    @Column(nullable = false, unique = true, length = 160)
    private String email;

    @Column(nullable = false, length = 240)
    private String address;

    @Column(name = "password_hash", nullable = false, length = 100)
    private String passwordHash;

    @Column(name = "profile_picture_s3_key", length = 600)
    private String profilePictureS3Key;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;
}



package com.insurewise.auth.repository;

import com.insurewise.auth.entity.StaffUser;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface StaffUserRepository extends JpaRepository<StaffUser, UUID> {

    Optional<StaffUser> findByEmail(String email);

    boolean existsByEmail(String email);
}
