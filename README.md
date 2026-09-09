package com.insurewise.auth.repository;

import com.insurewise.auth.entity.StaffUser;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface StaffUserRepository extends JpaRepository<StaffUser, UUID> {

    Optional<StaffUser> findByEmail(String email);

    boolean existsByEmail(String email);

    boolean existsByEmailAndIdNot(String email, UUID id);
}

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

package com.insurewise.auth.service;

import com.insurewise.auth.dto.CreateStaffUserRequest;
import com.insurewise.auth.dto.StaffUserResponse;
import com.insurewise.auth.dto.UpdateStaffUserRequest;
import com.insurewise.auth.entity.StaffUser;
import com.insurewise.auth.repository.StaffUserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
@Transactional
public class StaffUserManagementService {

    private final StaffUserRepository staffUserRepository;
    private final PasswordEncoder passwordEncoder;

    public StaffUserManagementService(
            StaffUserRepository staffUserRepository,
            PasswordEncoder passwordEncoder
    ) {
        this.staffUserRepository = staffUserRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional(readOnly = true)
    public List<StaffUserResponse> getAllStaffUsers() {

        return staffUserRepository.findAll()
                .stream()
                .map(StaffUserResponse::from)
                .toList();
    }

    @Transactional(readOnly = true)
    public StaffUserResponse getStaffUser(UUID id) {

        StaffUser staffUser = findStaffUser(id);

        return StaffUserResponse.from(staffUser);
    }

    public StaffUserResponse createStaffUser(
            CreateStaffUserRequest request
    ) {

        String email = request.email().trim();

        if (staffUserRepository.existsByEmail(email)) {
            throw new IllegalArgumentException(
                    "A staff user with this email already exists"
            );
        }

        StaffUser staffUser = new StaffUser();

        staffUser.setId(UUID.randomUUID());
        staffUser.setFullName(request.fullName().trim());
        staffUser.setEmail(email);
        staffUser.setAddress(request.address().trim());

        // NEVER store raw password
        staffUser.setPasswordHash(
                passwordEncoder.encode(request.password())
        );

        StaffUser saved =
                staffUserRepository.save(staffUser);

        return StaffUserResponse.from(saved);
    }

    public StaffUserResponse updateStaffUser(
            UUID id,
            UpdateStaffUserRequest request
    ) {

        StaffUser staffUser = findStaffUser(id);

        String email = request.email().trim();

        if (staffUserRepository.existsByEmailAndIdNot(
                email,
                id
        )) {
            throw new IllegalArgumentException(
                    "A staff user with this email already exists"
            );
        }

        staffUser.setFullName(
                request.fullName().trim()
        );

        staffUser.setEmail(email);

        staffUser.setAddress(
                request.address().trim()
        );

        /*
         * Password intentionally NOT changed.
         */

        StaffUser saved =
                staffUserRepository.save(staffUser);

        return StaffUserResponse.from(saved);
    }

    public void deleteStaffUser(UUID id) {

        StaffUser staffUser = findStaffUser(id);

        staffUserRepository.delete(staffUser);
    }

    private StaffUser findStaffUser(UUID id) {

        return staffUserRepository.findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Staff user not found"
                        )
                );
    }
}

package com.insurewise.auth.controller;

import com.insurewise.auth.dto.CreateStaffUserRequest;
import com.insurewise.auth.dto.StaffUserResponse;
import com.insurewise.auth.dto.UpdateStaffUserRequest;
import com.insurewise.auth.service.StaffUserManagementService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/auth/staff-users")
public class StaffUserManagementController {

    private final StaffUserManagementService service;

    public StaffUserManagementController(
            StaffUserManagementService service
    ) {
        this.service = service;
    }

    @GetMapping
    public List<StaffUserResponse> getAll(
            Authentication authentication
    ) {

        requireStaff(authentication);

        return service.getAllStaffUsers();
    }

    @GetMapping("/{id}")
    public StaffUserResponse getById(
            @PathVariable UUID id,
            Authentication authentication
    ) {

        requireStaff(authentication);

        return service.getStaffUser(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public StaffUserResponse create(
            @Valid @RequestBody CreateStaffUserRequest request,
            Authentication authentication
    ) {

        requireStaff(authentication);

        return service.createStaffUser(request);
    }

    @PutMapping("/{id}")
    public StaffUserResponse update(
            @PathVariable UUID id,
            @Valid @RequestBody UpdateStaffUserRequest request,
            Authentication authentication
    ) {

        requireStaff(authentication);

        return service.updateStaffUser(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(
            @PathVariable UUID id,
            Authentication authentication
    ) {

        requireStaff(authentication);

        service.deleteStaffUser(id);
    }

    private void requireStaff(
            Authentication authentication
    ) {

        if (authentication == null
                || !authentication.isAuthenticated()) {

            throw new SecurityException(
                    "Authentication required"
            );
        }

        /*
         * Your application has STAFF and CUSTOMER.
         * There is NO ADMIN.
         */

        boolean staff = authentication.getAuthorities()
                .stream()
                .anyMatch(authority -> {

                    String value =
                            authority.getAuthority();

                    return value.equals("STAFF")
                            || value.equals("ROLE_STAFF");
                });

        if (!staff) {
            throw new SecurityException(
                    "Only staff users can perform this operation"
            );
        }
    }
}
