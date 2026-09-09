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
