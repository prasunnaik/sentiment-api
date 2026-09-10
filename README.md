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

@Service
@Transactional
public class StaffUserService {

    private final StaffUserRepository staffUserRepository;
    private final CustomerRepository customerRepository;
    private final PasswordEncoder passwordEncoder;

    public StaffUserService(
            StaffUserRepository staffUserRepository,
            CustomerRepository customerRepository,
            PasswordEncoder passwordEncoder) {

        this.staffUserRepository = staffUserRepository;
        this.customerRepository = customerRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public StaffProfileResponse create(
            StaffCreateRequest request) {

        String email = request.email().toLowerCase();

        validateEmailNotUsed(email);

        StaffUser staffUser = new StaffUser(
                request.fullName(),
                email,
                request.address(),
                passwordEncoder.encode(request.password()));

        return toResponse(
                staffUserRepository.save(staffUser));
    }

    @Transactional(readOnly = true)
    public List<StaffProfileResponse> list() {

        return staffUserRepository.findAll()
                .stream()
                .map(this::toResponse)
                .toList();
    }

    @Transactional(readOnly = true)
    public StaffProfileResponse get(UUID id) {

        return toResponse(find(id));
    }

    public StaffProfileResponse update(
            UUID id,
            StaffUpdateRequest request) {

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

        if (emailUsedByAnotherStaff || emailUsedByCustomer) {
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
    }

    public void delete(UUID id) {

        StaffUser staffUser = find(id);

        staffUserRepository.delete(staffUser);
    }

    private StaffUser find(UUID id) {

        return staffUserRepository.findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Staff user not found: " + id));
    }

    private void validateEmailNotUsed(String email) {

        if (staffUserRepository.existsByEmailIgnoreCase(email)
                || customerRepository.existsByEmailIgnoreCase(email)) {

            throw new DuplicateEmailException(email);
        }
    }

    private StaffProfileResponse toResponse(
            StaffUser staffUser) {

        return new StaffProfileResponse(
                staffUser.getId(),
                staffUser.getFullName(),
                staffUser.getEmail(),
                staffUser.getAddress());
    }
}



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
}




