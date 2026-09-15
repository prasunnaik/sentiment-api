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
}
