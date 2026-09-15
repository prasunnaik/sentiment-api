package com.insurewise.auth.controller;

import com.insurewise.auth.dto.request.StaffCreateRequest;
import com.insurewise.auth.dto.request.StaffUpdateRequest;
import com.insurewise.auth.dto.response.StaffProfileResponse;
import com.insurewise.auth.service.StaffUserService;
import jakarta.validation.Valid;
import java.util.List;
import java.util.UUID;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.MediaType;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/staff/users")
@PreAuthorize("hasRole('STAFF')")
public class StaffUserManagementController {

    private final StaffUserService staffUserService;

    public StaffUserManagementController(
            StaffUserService staffUserService) {

        this.staffUserService = staffUserService;
    }

    @PostMapping
    public ResponseEntity<StaffProfileResponse> create(
            @Valid @RequestBody StaffCreateRequest request) {

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(staffUserService.create(request));
    }

    @GetMapping
    public List<StaffProfileResponse> list() {

        return staffUserService.list();
    }

    @GetMapping("/{id}")
    public StaffProfileResponse get(
            @PathVariable UUID id) {

        return staffUserService.get(id);
    }

    @PutMapping("/{id}")
    public StaffProfileResponse update(
            @PathVariable UUID id,
            @Valid @RequestBody StaffUpdateRequest request) {

        return staffUserService.update(id, request);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable UUID id) {

        staffUserService.delete(id);

        return ResponseEntity.noContent().build();
    }

    @PostMapping(
            value = "/{id}/profile-picture",
            consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public StaffProfileResponse uploadProfilePicture(
            @PathVariable UUID id,
            @RequestPart("file") MultipartFile file) {

        return staffUserService.uploadProfilePicture(
                id,
                file);
    }

    @DeleteMapping("/{id}/profile-picture")
    public ResponseEntity<Void> deleteProfilePicture(
            @PathVariable UUID id) {

        staffUserService.deleteProfilePicture(id);

        return ResponseEntity.noContent().build();
    }

    package com.insurewise.auth.service;

import com.insurewise.auth.dto.request.StaffCreateRequest;
import com.insurewise.auth.dto.request.StaffUpdateRequest;
import com.insurewise.auth.dto.response.StaffProfileResponse;
import com.insurewise.auth.entity.StaffUser;
import com.insurewise.auth.exception.DuplicateEmailException;
import com.insurewise.auth.repository.CustomerRepository;
import com.insurewise.auth.repository.StaffUserRepository;
import java.util.List;
import java.util.UUID;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.insurewise.auth.exception.StaffUserNotFoundException;
import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.service.S3StorageService;
import org.springframework.web.multipart.MultipartFile;

@Service
@Transactional
public class StaffUserService {

    private final StaffUserRepository staffUserRepository;
    private final CustomerRepository customerRepository;
    private final PasswordEncoder passwordEncoder;
    private final S3StorageService storageService;

    public StaffUserService(
            StaffUserRepository staffUserRepository,
            CustomerRepository customerRepository,
            PasswordEncoder passwordEncoder,
            S3StorageService storageService) {

        this.staffUserRepository = staffUserRepository;
        this.customerRepository = customerRepository;
        this.passwordEncoder = passwordEncoder;
        this.storageService = storageService;
    }

    public StaffProfileResponse create(
            StaffCreateRequest request) {

        try {
            String email = request.email().toLowerCase();

            validateEmailNotUsed(email);

            StaffUser staffUser = new StaffUser(
                    request.fullName(),
                    email,
                    request.address(),
                    passwordEncoder.encode(request.password()));

            return toResponse(
                    staffUserRepository.save(staffUser));

        } catch (Exception exception) {
            System.err.println(
                    "Error in StaffUserService.create: "
                            + exception.getMessage());

            throw exception;
        }
    }

    public StaffProfileResponse uploadProfilePicture(
            UUID id,
            MultipartFile file) {

        StaffUser staffUser = find(id);

        String oldS3Key =
                staffUser.getProfilePictureS3Key();

        String newS3Key =
                storageService.upload(
                        file,
                        "profile-pictures",
                        staffUser.getId());

        staffUser.updateProfilePictureS3Key(newS3Key);

        if (oldS3Key != null && !oldS3Key.isBlank()) {
            storageService.delete(oldS3Key);
        }

        return toResponse(staffUser);
    }

    public void deleteProfilePicture(UUID id) {

        StaffUser staffUser = find(id);

        String s3Key =
                staffUser.getProfilePictureS3Key();

        if (s3Key != null && !s3Key.isBlank()) {
            storageService.delete(s3Key);
        }

        staffUser.updateProfilePictureS3Key(null);
    }

    @Transactional(readOnly = true)
    public List<StaffProfileResponse> list() {

        try {
            return staffUserRepository.findAll()
                    .stream()
                    .map(this::toResponse)
                    .toList();

        } catch (Exception exception) {
            System.err.println(
                    "Error in StaffUserService.list: "
                            + exception.getMessage());

            throw exception;
        }
    }

    @Transactional(readOnly = true)
    public StaffProfileResponse get(UUID id) {

        try {
            return toResponse(find(id));

        } catch (Exception exception) {
            System.err.println(
                    "Error in StaffUserService.get: "
                            + exception.getMessage());

            throw exception;
        }
    }

    public StaffProfileResponse update(
            UUID id,
            StaffUpdateRequest request) {

        try {

            StaffUser staffUser = find(id);

            String email = request.email().toLowerCase();

            boolean emailUsedByAnotherStaff =
                    staffUserRepository
                            .findByEmailIgnoreCase(email)
                            .filter(existing ->
                                    !existing.getId().equals(id))
                            .isPresent();

            boolean emailUsedByCustomer =
                    customerRepository
                            .existsByEmailIgnoreCase(email);

            if (emailUsedByAnotherStaff
                    || emailUsedByCustomer) {
                throw new DuplicateEmailException(email);
            }

            String passwordHash = null;

            if (request.password() != null
                    && !request.password().isBlank()) {

                passwordHash =
                        passwordEncoder.encode(request.password());
            }

            staffUser.update(
                    request.fullName(),
                    email,
                    request.address(),
                    passwordHash);

            return toResponse(staffUser);

        } catch (Exception exception) {
            System.err.println(
                    "Error in StaffUserService.update: "
                            + exception.getMessage());

            throw exception;
        }
    }

    public void delete(UUID id) {

        try {
            StaffUser staffUser = find(id);

            String s3Key =
                    staffUser.getProfilePictureS3Key();

            if (s3Key != null && !s3Key.isBlank()) {
                storageService.delete(s3Key);
            }

            staffUserRepository.delete(staffUser);

        } catch (Exception exception) {
            System.err.println(
                    "Error in StaffUserService.delete: "
                            + exception.getMessage());

            throw exception;
        }
    }

    private StaffUser find(UUID id) {

        return staffUserRepository.findById(id)
                .orElseThrow(() ->
                        new StaffUserNotFoundException(id));
    }

    private void validateEmailNotUsed(String email) {

        if (staffUserRepository.existsByEmailIgnoreCase(email)
                || customerRepository.existsByEmailIgnoreCase(email)) {

            throw new DuplicateEmailException(email);
        }
    }

    private StaffProfileResponse toResponse(
            StaffUser staffUser) {

        String profilePictureUrl = null;

        if (staffUser.getProfilePictureS3Key() != null
                && !staffUser.getProfilePictureS3Key().isBlank()) {

            PresignedUrlResponse download =
                    storageService.getPresignedDownloadUrl(
                            staffUser.getProfilePictureS3Key());

            profilePictureUrl = download.url();
        }

        return new StaffProfileResponse(
                staffUser.getId(),
                staffUser.getFullName(),
                staffUser.getEmail(),
                staffUser.getAddress(),
                profilePictureUrl);
    }
}

}
