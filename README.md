package com.insurewise.framework.s3.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface EnableS3Delete {
}
package com.insurewise.framework.s3.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface EnableS3Upload {
    String folder() default "uploads";
}
package com.insurewise.framework.s3.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface S3FileField {
    String folder() default "uploads";
}
package com.insurewise.framework.s3.aspect;

import com.insurewise.framework.s3.annotation.EnableS3Delete;
import com.insurewise.framework.s3.annotation.S3FileField;
import com.insurewise.framework.s3.service.S3FileService;
import java.lang.reflect.Field;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class S3DeleteAspect {

    private final S3FileService fileService;

    public S3DeleteAspect(S3FileService fileService) {
        this.fileService = fileService;
    }

    @Around("@annotation(enableS3Delete)")
    public Object delete(
            ProceedingJoinPoint joinPoint,
            EnableS3Delete enableS3Delete) throws Throwable {

        for (Object argument : joinPoint.getArgs()) {
            if (argument == null) {
                continue;
            }

            String key = findS3FileField(argument);
            if (key != null && !key.isBlank()) {
                fileService.delete(key);
            }
        }

        return joinPoint.proceed();
    }

    private String findS3FileField(Object target)
            throws IllegalAccessException {

        for (Field field : target.getClass().getDeclaredFields()) {
            if (!field.isAnnotationPresent(S3FileField.class)
                    || field.getType() != String.class) {
                continue;
            }

            field.setAccessible(true);
            Object value = field.get(target);
            return value instanceof String string ? string : null;
        }

        return null;
    }
}
package com.insurewise.framework.s3.aspect;

import com.insurewise.framework.s3.annotation.EnableS3Upload;
import com.insurewise.framework.s3.annotation.S3FileField;
import com.insurewise.framework.s3.service.S3FileService;
import java.lang.reflect.Field;
import java.util.UUID;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

@Aspect
@Component
public class S3UploadAspect {

    private final S3FileService fileService;

    public S3UploadAspect(S3FileService fileService) {
        this.fileService = fileService;
    }

    @Around("@annotation(enableS3Upload)")
    public Object upload(
            ProceedingJoinPoint joinPoint,
            EnableS3Upload enableS3Upload) throws Throwable {

        MultipartFile file = null;
        UUID ownerId = null;
        Object targetFieldObject = null;

        for (Object argument : joinPoint.getArgs()) {
            if (argument instanceof MultipartFile multipartFile) {
                file = multipartFile;
            } else if (argument instanceof UUID uuid) {
                ownerId = uuid;
            } else if (argument != null) {
                targetFieldObject = argument;
            }
        }

        if (file != null && !file.isEmpty()) {
            String key = fileService.upload(
                    file,
                    enableS3Upload.folder(),
                    ownerId);

            if (targetFieldObject != null) {
                setS3FileField(targetFieldObject, key);
            }
        }

        return joinPoint.proceed();
    }

    private void setS3FileField(
            Object target,
            String key) throws IllegalAccessException {

        for (Field field : target.getClass().getDeclaredFields()) {
            if (!field.isAnnotationPresent(S3FileField.class)
                    || field.getType() != String.class) {
                continue;
            }

            field.setAccessible(true);
            field.set(target, key);
            return;
        }
    }
}
package com.insurewise.framework.s3.config;

import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.client.builder.AwsClientBuilder.EndpointConfiguration;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.insurewise.framework.s3.aspect.S3DeleteAspect;
import com.insurewise.framework.s3.aspect.S3UploadAspect;
import com.insurewise.framework.s3.controller.S3FileController;
import com.insurewise.framework.s3.service.AwsS3FileService;
import com.insurewise.framework.s3.service.DisabledS3FileService;
import com.insurewise.framework.s3.service.S3FileService;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;

@AutoConfiguration
@ConditionalOnClass({AmazonS3.class, S3FileService.class})
@Import({S3UploadAspect.class, S3DeleteAspect.class, S3FileController.class})
@EnableConfigurationProperties(S3Properties.class)
public class S3AutoConfiguration {

    @Bean
    @ConditionalOnProperty(
            prefix = "ng.file-upload.s3",
            name = "enabled",
            havingValue = "true")
    @ConditionalOnMissingBean
    AmazonS3 amazonS3(S3Properties properties) {

        AmazonS3ClientBuilder builder = AmazonS3ClientBuilder.standard()
                .withPathStyleAccessEnabled(properties.pathStyleAccessEnabled());

        if (properties.endpoint() != null && !properties.endpoint().isBlank()) {
            builder.withEndpointConfiguration(
                    new EndpointConfiguration(
                            properties.endpoint(),
                            properties.region()));
        } else {
            builder.withRegion(properties.region());
        }

        if (properties.accessKey() != null
                && !properties.accessKey().isBlank()
                && properties.secretKey() != null
                && !properties.secretKey().isBlank()) {
            builder.withCredentials(
                    new AWSStaticCredentialsProvider(
                            new BasicAWSCredentials(
                                    properties.accessKey(),
                                    properties.secretKey())));
        }

        return builder.build();
    }

    @Bean
    @ConditionalOnProperty(
            prefix = "ng.file-upload.s3",
            name = "enabled",
            havingValue = "true")
    @ConditionalOnMissingBean(S3FileService.class)
    S3FileService awsS3FileService(
            AmazonS3 amazonS3,
            S3Properties properties) {
        return new AwsS3FileService(amazonS3, properties);
    }

    @Bean
    @ConditionalOnProperty(
            prefix = "ng.file-upload.s3",
            name = "enabled",
            havingValue = "false",
            matchIfMissing = true)
    @ConditionalOnMissingBean(S3FileService.class)
    S3FileService disabledS3FileService() {
        return new DisabledS3FileService();
    }
}
package com.insurewise.framework.s3.config;

import java.time.Duration;
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "ng.file-upload.s3")
public record S3Properties(
        boolean enabled,
        String bucketName,
        String region,
        String accessKey,
        String secretKey,
        String endpoint,
        boolean pathStyleAccessEnabled,
        String keyPrefix,
        Download download) {

    public record Download(boolean enabled) {
    }

    public Duration presignedUrlTtl() {
        return Duration.ofMinutes(15);
    }
}
package com.insurewise.framework.s3.controller;

import com.insurewise.framework.s3.service.S3FileService;
import com.insurewise.framework.s3.service.S3PresignedUrl;
import java.util.Map;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/storage")
@ConditionalOnProperty(
        prefix = "ng.file-upload.s3.download",
        name = "enabled",
        havingValue = "true")
public class S3FileController {

    private final S3FileService fileService;

    /**
     * Creates the S3 file controller.
     *
     * @param fileService S3 file access service
     */
    public S3FileController(S3FileService fileService) {
        this.fileService = fileService;
    }

    /**
     * Generates a presigned download URL for the provided object key.
     *
     * @param key S3 object key
     * @return presigned download metadata
     */
    @GetMapping("/download-url")
    @PreAuthorize("hasRole('STAFF')")
    public ResponseEntity<Map<String, Object>> downloadUrl(
            @RequestParam String key) {

        S3PresignedUrl response =
                fileService.getPresignedDownloadUrl(key);

        return ResponseEntity.ok(Map.of(
                "url", response.url(),
                "expiresAt", response.expiresAt()));
    }
}
package com.insurewise.framework.s3.exception;

public class S3FileStorageException extends RuntimeException {
    public S3FileStorageException(String message) {
        super(message);
    }

    public S3FileStorageException(String message, Throwable cause) {
        super(message, cause);
    }
}
package com.insurewise.framework.s3.exception;

public class S3FileValidationException extends RuntimeException {
    public S3FileValidationException(String message) {
        super(message);
    }
}
package com.insurewise.framework.s3.service;

import com.amazonaws.HttpMethod;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.DeleteObjectRequest;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.amazonaws.services.s3.model.GeneratePresignedUrlRequest;
import com.insurewise.framework.s3.config.S3Properties;
import com.insurewise.framework.s3.exception.S3FileStorageException;
import com.insurewise.framework.s3.exception.S3FileValidationException;
import java.io.IOException;
import java.net.URL;
import java.time.Duration;
import java.time.Instant;
import java.util.Date;
import java.util.Set;
import java.util.UUID;
import org.springframework.web.multipart.MultipartFile;

public class AwsS3FileService implements S3FileService {

    private static final long MAX_FILE_SIZE = 10L * 1024L * 1024L;
    private static final Set<String> IMAGE_TYPES = Set.of(
            "image/jpeg",
            "image/png",
            "image/webp");
    private static final Set<String> DOCUMENT_TYPES = Set.of(
            "application/pdf",
            "image/jpeg",
            "image/png",
            "image/webp");

    private final AmazonS3 amazonS3;
    private final S3Properties properties;

    /**
     * Creates the AWS-backed S3 file service.
     *
     * @param amazonS3 S3 client
     * @param properties S3 configuration properties
     */
    public AwsS3FileService(
            AmazonS3 amazonS3,
            S3Properties properties) {
        this.amazonS3 = amazonS3;
        this.properties = properties;
    }

    /**
     * Uploads a multipart file to S3.
     *
     * @param file file content
     * @param folder destination folder
     * @param ownerId owner identifier
     * @return stored object key
     */
    @Override
    public String upload(
            MultipartFile file,
            String folder,
            UUID ownerId) {

        System.out.println("========== S3 DEBUG ==========");
        System.out.println("Bucket  = [" + properties.bucketName() + "]");
        System.out.println("Region  = [" + properties.region() + "]");
        System.out.println("Endpoint = [" + properties.endpoint() + "]");
        System.out.println("PathStyle = [" + properties.pathStyleAccessEnabled() + "]");
        System.out.println("===============================");

        validate(file, folder);

        String originalName = file.getOriginalFilename();
        if (originalName == null || originalName.isBlank()) {
            originalName = "file";
        }

        String extension = "";
        int dot = originalName.lastIndexOf('.');
        if (dot >= 0) {
            extension = originalName.substring(dot);
        }

        String key = buildKey(folder, ownerId, UUID.randomUUID() + extension);

        ObjectMetadata metadata = new ObjectMetadata();
        metadata.setContentLength(file.getSize());
        metadata.setContentType(file.getContentType());

        try {
            amazonS3.putObject(
                    new PutObjectRequest(
                            properties.bucketName(),
                            key,
                            file.getInputStream(),
                            metadata));
            return key;
        } catch (IOException | RuntimeException exception) {
            throw new S3FileStorageException(
                    "Unable to upload file to S3",
                    exception);
        }

    }

    /**
     * Uploads generated bytes to S3.
     *
     * @param content file bytes
     * @param fileName logical file name
     * @param contentType content type
     * @param folder destination folder
     * @param ownerId owner identifier
     * @return stored object key
     */
    @Override
    public String uploadGenerated(
            byte[] content,
            String fileName,
            String contentType,
            String folder,
            UUID ownerId) {

        if (content == null || content.length == 0) {
            throw new S3FileValidationException("File content cannot be empty");
        }
        if (content.length > MAX_FILE_SIZE) {
            throw new S3FileValidationException("File size exceeds 10 MB");
        }

        ObjectMetadata metadata = new ObjectMetadata();
        metadata.setContentLength(content.length);
        metadata.setContentType(contentType == null || contentType.isBlank()
                ? "application/octet-stream"
                : contentType);

        String safeName = fileName == null || fileName.isBlank()
                ? "generated-file"
                : fileName;
        String key = buildKey(folder, ownerId, UUID.randomUUID() + "-" + safeName);

        try {

            amazonS3.putObject(
                    new PutObjectRequest(
                            properties.bucketName(),
                            key,
                            new java.io.ByteArrayInputStream(content),
                            metadata));
            return key;
        } catch (RuntimeException exception) {
            throw new S3FileStorageException(
                    "Unable to upload generated file to S3",
                    exception);
        }
    }

    /**
     * Generates a presigned download URL for the object key.
     *
     * @param s3Key object key
     * @return presigned URL details
     */
    @Override
    public S3PresignedUrl getPresignedDownloadUrl(String s3Key) {
        if (s3Key == null || s3Key.isBlank()) {
            throw new S3FileValidationException("S3 key cannot be empty");
        }

        Duration duration = properties.presignedUrlTtl();
        Instant expiresAt = Instant.now().plus(duration);

        try {
            GeneratePresignedUrlRequest request =
                    new GeneratePresignedUrlRequest(
                            properties.bucketName(),
                            s3Key)
                            .withMethod(HttpMethod.GET)
                            .withExpiration(Date.from(expiresAt));

            URL url = amazonS3.generatePresignedUrl(request);
            return new S3PresignedUrl(url.toString(), expiresAt);
        } catch (RuntimeException exception) {
            throw new S3FileStorageException(
                    "Unable to generate S3 download URL",
                    exception);
        }
    }

    /**
     * Deletes an object from S3 when the key is present.
     *
     * @param s3Key object key
     */
    @Override
    public void delete(String s3Key) {
        if (s3Key == null || s3Key.isBlank()) {
            return;
        }

        try {
            amazonS3.deleteObject(
                    new DeleteObjectRequest(
                            properties.bucketName(),
                            s3Key));
        } catch (RuntimeException exception) {
            throw new S3FileStorageException(
                    "Unable to delete S3 object",
                    exception);
        }
    }

    /**
     * Validates file constraints for the target folder.
     *
     * @param file file content
     * @param folder destination folder
     */
    private void validate(MultipartFile file, String folder) {
        if (file == null || file.isEmpty()) {
            throw new S3FileValidationException("File cannot be empty");
        }
        if (file.getSize() > MAX_FILE_SIZE) {
            throw new S3FileValidationException("File size exceeds 10 MB");
        }
        if (file.getContentType() == null || file.getContentType().isBlank()) {
            throw new S3FileValidationException("File content type is required");
        }

        String contentType = file.getContentType().toLowerCase();
        String normalizedFolder = normalize(folder).toLowerCase();

        if (normalizedFolder.contains("profile-pictures")
                && !IMAGE_TYPES.contains(contentType)) {
            throw new S3FileValidationException(
                    "Profile picture must be JPEG, PNG, or WEBP");
        }

        if (normalizedFolder.contains("documents")
                && !DOCUMENT_TYPES.contains(contentType)) {
            throw new S3FileValidationException(
                    "Document must be PDF, JPEG, PNG, or WEBP");
        }
    }

    /**
     * Builds a normalized storage key.
     *
     * @param folder destination folder
     * @param ownerId owner identifier
     * @param fileName final file name
     * @return object key
     */
    private String buildKey(
            String folder,
            UUID ownerId,
            String fileName) {

        String prefix = normalize(properties.keyPrefix());
        String normalizedFolder = normalize(folder);
        String owner = ownerId == null ? "general" : ownerId.toString();

        StringBuilder key = new StringBuilder();
        if (!prefix.isBlank()) {
            key.append(prefix).append('/');
        }
        if (!normalizedFolder.isBlank()) {
            key.append(normalizedFolder).append('/');
        }
        key.append(owner).append('/').append(fileName);
        return key.toString();
    }

    /**
     * Removes leading and trailing slashes from a value.
     *
     * @param value input value
     * @return normalized value
     */
    private String normalize(String value) {
        if (value == null) {
            return "";
        }
        return value.trim().replaceAll("^/+|/+$", "");
    }
}
package com.insurewise.framework.s3.service;

import com.insurewise.framework.s3.exception.S3FileStorageException;
import java.util.UUID;
import org.springframework.web.multipart.MultipartFile;

public class DisabledS3FileService implements S3FileService {

    /**
     * Builds the exception raised when S3 storage is disabled.
     *
     * @return disabled-storage exception
     */
    private S3FileStorageException disabled() {
        return new S3FileStorageException(
                "S3 storage is disabled. Set S3_ENABLED=true and configure S3.");
    }

    /**
     * Upload is unavailable while S3 storage is disabled.
     *
     * @param file file content
     * @param folder destination folder
     * @param ownerId owner identifier
     * @return never returns
     */
    @Override
    public String upload(MultipartFile file, String folder, UUID ownerId) {
        throw disabled();
    }

    /**
     * Generated uploads are unavailable while S3 storage is disabled.
     *
     * @param content file bytes
     * @param fileName logical file name
     * @param contentType content type
     * @param folder destination folder
     * @param ownerId owner identifier
     * @return never returns
     */
    @Override
    public String uploadGenerated(
            byte[] content,
            String fileName,
            String contentType,
            String folder,
            UUID ownerId) {
        throw disabled();
    }

    /**
     * Presigned URLs are unavailable while S3 storage is disabled.
     *
     * @param s3Key object key
     * @return never returns
     */
    @Override
    public S3PresignedUrl getPresignedDownloadUrl(String s3Key) {
        throw disabled();
    }

    /**
     * No-op delete when S3 storage is disabled.
     *
     * @param s3Key object key
     */
    @Override
    public void delete(String s3Key) {
        // S3 is disabled; there is no remote object to delete.
    }
}
package com.insurewise.framework.s3.service;

import java.util.UUID;
import org.springframework.web.multipart.MultipartFile;

public interface S3FileService {
    /**
     * Uploads a file to the given folder.
     *
     * @param file file content
     * @param folder destination folder
     * @param ownerId owner identifier
     * @return stored object key
     */
    String upload(MultipartFile file, String folder, UUID ownerId);

    /**
     * Uploads generated content as a file.
     *
     * @param content file bytes
     * @param fileName logical file name
     * @param contentType content type
     * @param folder destination folder
     * @param ownerId owner identifier
     * @return stored object key
     */
    String uploadGenerated(
            byte[] content,
            String fileName,
            String contentType,
            String folder,
            UUID ownerId);

    /**
     * Creates a presigned download URL for the given object key.
     *
     * @param s3Key object key
     * @return presigned URL details
     */
    S3PresignedUrl getPresignedDownloadUrl(String s3Key);

    /**
     * Deletes an object when the key is present.
     *
     * @param s3Key object key
     */
    void delete(String s3Key);
}
package com.insurewise.framework.s3.service;

import java.time.Instant;

public record S3PresignedUrl(String url, Instant expiresAt) {
}
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.insurewise.framework</groupId>
        <artifactId>s3-framework-parent</artifactId>
        <version>1.0.0-SNAPSHOT</version>
    </parent>

    <artifactId>s3-file-storage</artifactId>
    <packaging>jar</packaging>

    <dependencies>
        <dependency>
            <groupId>com.amazonaws</groupId>
            <artifactId>aws-java-sdk-s3</artifactId>
            <version>${aws.sdk.version}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-aop</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>${lombok.version}</version>
            <optional>true</optional>
        </dependency>
        <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-core</artifactId>
        </dependency>
    </dependencies>
</project>
