@Column(name = "password_hash", nullable = false, length = 100)
private String passwordHash;

@Column(name = "profile_picture_s3_key", length = 600)
private String profilePictureS3Key;

@Column(name = "created_at", nullable = false)
private LocalDateTime createdAt;




public String getProfilePictureS3Key() {
    return profilePictureS3Key;
}

public void updateProfilePictureS3Key(String s3Key) {
    this.profilePictureS3Key = s3Key;
}





package com.insurewise.auth.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.UUID;

public record StaffProfileResponse(
        UUID id,

        @JsonProperty("full_name")
        String fullName,

        String email,
        String address,

        String profilePictureUrl
) {
}





import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.service.S3StorageService;
import org.springframework.web.multipart.MultipartFile;



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





import org.springframework.http.MediaType;
import org.springframework.web.multipart.MultipartFile;



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






