<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
</dependency>


<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>software.amazon.awssdk</groupId>
            <artifactId>bom</artifactId>
            <version>2.54.17</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>



<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
</dependency>



package com.insurewise.framework.s3.config;

import java.time.Duration;
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "insurewise.s3")
public record S3Properties(
        boolean enabled,
        String bucket,
        String region,
        Duration presignedUrlDuration,
        long maxFileSize
) {
}




package com.insurewise.framework.s3.config;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.presigner.S3Presigner;

@Configuration
@EnableConfigurationProperties(S3Properties.class)
public class S3Config {

    @Bean
    public S3Client s3Client(S3Properties properties) {
        return S3Client.builder()
                .region(Region.of(properties.region()))
                .build();
    }

    @Bean
    public S3Presigner s3Presigner(S3Properties properties) {
        return S3Presigner.builder()
                .region(Region.of(properties.region()))
                .build();
    }
}





package com.insurewise.framework.s3.service;

import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.exception.InvalidFileException;
import com.insurewise.common.service.S3StorageService;
import com.insurewise.framework.s3.config.S3Properties;
import java.time.Duration;
import java.time.Instant;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.DeleteObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.model.S3Exception;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.presigner.S3Presigner;
import software.amazon.awssdk.services.s3.presigner.model.GetObjectPresignRequest;

@Service
public class AwsS3StorageService implements S3StorageService {

    private final S3Client s3Client;
    private final S3Presigner s3Presigner;
    private final S3Properties properties;

    public AwsS3StorageService(
            S3Client s3Client,
            S3Presigner s3Presigner,
            S3Properties properties) {

        this.s3Client = s3Client;
        this.s3Presigner = s3Presigner;
        this.properties = properties;
    }

    @Override
    public String upload(
            MultipartFile file,
            String folder,
            UUID ownerId) {

        if (file == null || file.isEmpty()) {
            throw new InvalidFileException("File cannot be empty");
        }

        if (file.getSize() > properties.maxFileSize()) {
            throw new InvalidFileException(
                    "File size exceeds the allowed limit");
        }

        String contentType = file.getContentType();

        if (contentType == null || contentType.isBlank()) {
            throw new InvalidFileException(
                    "File content type is required");
        }

        String originalName = file.getOriginalFilename();

        if (originalName == null || originalName.isBlank()) {
            originalName = "file";
        }

        String extension = "";

        int dot = originalName.lastIndexOf('.');

        if (dot >= 0) {
            extension = originalName.substring(dot);
        }

        String key = folder
                + "/"
                + ownerId
                + "/"
                + UUID.randomUUID()
                + extension;

        try {
            PutObjectRequest request = PutObjectRequest.builder()
                    .bucket(properties.bucket())
                    .key(key)
                    .contentType(contentType)
                    .build();

            s3Client.putObject(
                    request,
                    RequestBody.fromInputStream(
                            file.getInputStream(),
                            file.getSize()));

            return key;

        } catch (Exception exception) {
            throw new IllegalStateException(
                    "Failed to upload file to S3",
                    exception);
        }
    }

    @Override
    public String uploadGenerated(
            byte[] content,
            String fileName,
            String contentType,
            String folder,
            UUID ownerId) {

        if (content == null || content.length == 0) {
            throw new InvalidFileException(
                    "File content cannot be empty");
        }

        String key = folder
                + "/"
                + ownerId
                + "/"
                + UUID.randomUUID()
                + "-"
                + fileName;

        try {
            PutObjectRequest request = PutObjectRequest.builder()
                    .bucket(properties.bucket())
                    .key(key)
                    .contentType(contentType)
                    .build();

            s3Client.putObject(
                    request,
                    RequestBody.fromBytes(content));

            return key;

        } catch (Exception exception) {
            throw new IllegalStateException(
                    "Failed to upload generated file to S3",
                    exception);
        }
    }

    @Override
    public PresignedUrlResponse getPresignedDownloadUrl(
            String s3Key) {

        try {
            Duration duration =
                    properties.presignedUrlDuration();

            GetObjectRequest getObjectRequest =
                    GetObjectRequest.builder()
                            .bucket(properties.bucket())
                            .key(s3Key)
                            .build();

            GetObjectPresignRequest presignRequest =
                    GetObjectPresignRequest.builder()
                            .signatureDuration(duration)
                            .getObjectRequest(getObjectRequest)
                            .build();

            String url = s3Presigner
                    .presignGetObject(presignRequest)
                    .url()
                    .toString();

            return new PresignedUrlResponse(
                    url,
                    Instant.now().plus(duration));

        } catch (S3Exception exception) {
            throw new IllegalStateException(
                    "Failed to generate S3 download URL",
                    exception);
        }
    }

    @Override
    public void delete(String s3Key) {

        if (s3Key == null || s3Key.isBlank()) {
            return;
        }

        try {
            s3Client.deleteObject(
                    DeleteObjectRequest.builder()
                            .bucket(properties.bucket())
                            .key(s3Key)
                            .build());

        } catch (S3Exception exception) {
            throw new IllegalStateException(
                    "Failed to delete S3 object",
                    exception);
        }
    }
}





@Service
public class DisabledS3StorageService
        implements S3StorageService



@Service
public class AwsS3StorageService
        implements S3StorageService




insurewise:
  s3:
    enabled: true
    bucket: insurewise-documents
    region: ap-south-1
    presigned-url-duration: 15m
    max-file-size: 10485760

    

@Column(name = "profile_picture_s3_key", length = 500)
private String profilePictureS3Key;




public String getProfilePictureS3Key() {
    return profilePictureS3Key;
}



public void updateProfilePicture(String s3Key) {
    this.profilePictureS3Key = s3Key;
}




public void removeProfilePicture() {
    this.profilePictureS3Key = null;
}




public record StaffProfileResponse(
        UUID id,
        String fullName,
        String email,
        String address,
        String profilePictureUrl
) {
}





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




@PostMapping(consumes = "multipart/form-data")
public ResponseEntity<StaffProfileResponse> create(
        @Valid @RequestPart("data")
        StaffCreateRequest request,

        @RequestPart(value = "profilePicture", required = false)
        MultipartFile profilePicture) {

    return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(staffUserService.create(
                    request,
                    profilePicture));
}




public StaffProfileResponse create(
        StaffCreateRequest request)


public StaffProfileResponse create(
        StaffCreateRequest request,
        MultipartFile profilePicture)



StaffUser staffUser = new StaffUser(
        request.fullName(),
        email,
        request.address(),
        passwordEncoder.encode(request.password()));

staffUser = staffUserRepository.save(staffUser);

if (profilePicture != null && !profilePicture.isEmpty()) {

    String key = storageService.upload(
            profilePicture,
            "staff/profile-pictures",
            staffUser.getId());

    staffUser.updateProfilePicture(key);

    staffUser = staffUserRepository.save(staffUser);
}

return toResponse(staffUser);




@PutMapping(
        value = "/{id}",
        consumes = "multipart/form-data")
public StaffProfileResponse update(
        @PathVariable UUID id,

        @Valid @RequestPart("data")
        StaffUpdateRequest request,

        @RequestPart(
                value = "profilePicture",
                required = false)
        MultipartFile profilePicture) {

    return staffUserService.update(
            id,
            request,
            profilePicture);
}




public StaffProfileResponse update(
        UUID id,
        StaffUpdateRequest request,
        MultipartFile profilePicture) {



if (profilePicture != null
        && !profilePicture.isEmpty()) {

    String oldKey =
            staffUser.getProfilePictureS3Key();

    String newKey =
            storageService.upload(
                    profilePicture,
                    "staff/profile-pictures",
                    staffUser.getId());

    staffUser.updateProfilePicture(newKey);

    if (oldKey != null) {
        storageService.delete(oldKey);
    }
}





@DeleteMapping("/{id}/profile-picture")
public ResponseEntity<Void> removeProfilePicture(
        @PathVariable UUID id) {

    staffUserService.removeProfilePicture(id);

    return ResponseEntity.noContent().build();
}




public void removeProfilePicture(UUID id) {

    StaffUser staffUser = find(id);

    String key =
            staffUser.getProfilePictureS3Key();

    if (key != null) {
        storageService.delete(key);
        staffUser.removeProfilePicture();
    }
}






package com.insurewise.policy.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "policy_application_documents")
public class PolicyApplicationDocument {

    @Id
    @GeneratedValue
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "application_id", nullable = false)
    private PolicyApplication application;

    @Column(name = "file_name", nullable = false, length = 255)
    private String fileName;

    @Column(name = "content_type", nullable = false, length = 120)
    private String contentType;

    @Column(name = "s3_key", nullable = false, length = 500)
    private String s3Key;

    @Column(name = "uploading_user", nullable = false)
    private UUID uploadingUser;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    protected PolicyApplicationDocument() {
    }

    public PolicyApplicationDocument(
            PolicyApplication application,
            String fileName,
            String contentType,
            String s3Key,
            UUID uploadingUser) {

        this.application = application;
        this.fileName = fileName;
        this.contentType = contentType;
        this.s3Key = s3Key;
        this.uploadingUser = uploadingUser;
    }

    @PrePersist
    void initialize() {
        if (createdAt == null) {
            createdAt = LocalDateTime.now();
        }
    }

    public UUID getId() {
        return id;
    }

    public PolicyApplication getApplication() {
        return application;
    }

    public String getFileName() {
        return fileName;
    }

    public String getContentType() {
        return contentType;
    }

    public String getS3Key() {
        return s3Key;
    }

    public UUID getUploadingUser() {
        return uploadingUser;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}




package com.insurewise.policy.repository;

import com.insurewise.policy.entity.PolicyApplicationDocument;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PolicyApplicationDocumentRepository
        extends JpaRepository<PolicyApplicationDocument, UUID> {

    List<PolicyApplicationDocument>
    findByApplicationIdOrderByCreatedAtDesc(
            UUID applicationId);
}




@Service
@Transactional
public class PolicyApplicationDocumentService {

    private final PolicyApplicationDocumentRepository repository;
    private final PolicyApplicationService applicationService;
    private final S3StorageService storageService;

    public PolicyApplicationDocumentService(
            PolicyApplicationDocumentRepository repository,
            PolicyApplicationService applicationService,
            S3StorageService storageService) {

        this.repository = repository;
        this.applicationService = applicationService;
        this.storageService = storageService;
    }

    public PolicyApplicationDocumentResponse upload(
            UUID applicationId,
            UUID staffUserId,
            MultipartFile file) {

        PolicyApplication application =
                applicationService
                        .getApplicationEntityForInternalUse(
                                applicationId);

        String key = storageService.upload(
                file,
                "policy-applications",
                applicationId);

        PolicyApplicationDocument document =
                new PolicyApplicationDocument(
                        application,
                        file.getOriginalFilename(),
                        file.getContentType(),
                        key,
                        staffUserId);

        return toResponse(repository.save(document));
    }

    @Transactional(readOnly = true)
    public List<PolicyApplicationDocumentResponse> list(
            UUID applicationId) {

        return repository
                .findByApplicationIdOrderByCreatedAtDesc(
                        applicationId)
                .stream()
                .map(this::toResponse)
                .toList();
    }

    private PolicyApplicationDocumentResponse toResponse(
            PolicyApplicationDocument document) {

        String url =
                storageService
                        .getPresignedDownloadUrl(
                                document.getS3Key())
                        .url();

        return new PolicyApplicationDocumentResponse(
                document.getId(),
                document.getApplication().getId(),
                document.getFileName(),
                document.getContentType(),
                url,
                document.getUploadingUser(),
                document.getCreatedAt());
    }
}




@RestController
@RequestMapping("/api/applications/{applicationId}/documents")
public class PolicyApplicationDocumentController {

    private final PolicyApplicationDocumentService service;

    public PolicyApplicationDocumentController(
            PolicyApplicationDocumentService service) {
        this.service = service;
    }

    @PostMapping(
            consumes = "multipart/form-data")
    @PreAuthorize("hasRole('STAFF')")
    public PolicyApplicationDocumentResponse upload(
            @PathVariable UUID applicationId,

            @AuthenticationPrincipal
            JwtPrincipal principal,

            @RequestPart("file")
            MultipartFile file) {

        return service.upload(
                applicationId,
                principal.userId(),
                file);
    }

    @GetMapping
    @PreAuthorize("hasRole('STAFF')")
    public List<PolicyApplicationDocumentResponse> list(
            @PathVariable UUID applicationId) {

        return service.list(applicationId);
    }
}




import com.insurewise.framework.s3.service.S3StorageService;





