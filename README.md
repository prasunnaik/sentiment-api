package com.insurewise.common.service;

import com.insurewise.common.dto.PresignedUrlResponse;
import java.util.UUID;
import org.springframework.web.multipart.MultipartFile;

public interface S3StorageService {

    String upload(
            MultipartFile file,
            String folder,
            UUID ownerId);

    String uploadGenerated(
            byte[] content,
            String fileName,
            String contentType,
            String folder,
            UUID ownerId);

    PresignedUrlResponse getPresignedDownloadUrl(
            String s3Key);

    void delete(String s3Key);
}






package com.insurewise.common.service;

import com.insurewise.common.dto.PresignedUrlResponse;
import java.util.UUID;
import org.springframework.web.multipart.MultipartFile;

public class DisabledS3StorageService implements S3StorageService {

    @Override
    public String upload(
            MultipartFile file,
            String folder,
            UUID ownerId) {
        throw disabledException();
    }

    @Override
    public String uploadGenerated(
            byte[] content,
            String fileName,
            String contentType,
            String folder,
            UUID ownerId) {
        throw disabledException();
    }

    @Override
    public PresignedUrlResponse getPresignedDownloadUrl(
            String s3Key) {
        throw disabledException();
    }

    @Override
    public void delete(String s3Key) {
        // No action because S3 is disabled.
    }

    private IllegalStateException disabledException() {
        return new IllegalStateException(
                "S3 storage is disabled. Set S3_ENABLED=true "
                        + "and configure an S3 implementation."
        );
    }
}






package com.insurewise.framework.s3.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "s3")
public class S3Properties {

    private boolean enabled;
    private String bucket;
    private String region;
    private long presignedUrlMinutes = 15;

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public String getBucket() {
        return bucket;
    }

    public void setBucket(String bucket) {
        this.bucket = bucket;
    }

    public String getRegion() {
        return region;
    }

    public void setRegion(String region) {
        this.region = region;
    }

    public long getPresignedUrlMinutes() {
        return presignedUrlMinutes;
    }

    public void setPresignedUrlMinutes(long presignedUrlMinutes) {
        this.presignedUrlMinutes = presignedUrlMinutes;
    }
}






package com.insurewise.framework.s3.config;

import java.net.URI;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.presigner.S3Presigner;

@Configuration
@EnableConfigurationProperties(S3Properties.class)
public class S3Config {

    @Bean
    public S3Client s3Client(S3Properties properties) {
        S3Client.Builder builder = S3Client.builder()
                .region(Region.of(properties.getRegion()))
                .credentialsProvider(
                        DefaultCredentialsProvider.create());

        return builder.build();
    }

    @Bean
    public S3Presigner s3Presigner(S3Properties properties) {
        return S3Presigner.builder()
                .region(Region.of(properties.getRegion()))
                .credentialsProvider(
                        DefaultCredentialsProvider.create())
                .build();
    }
}






package com.insurewise.framework.s3.exception;

public class S3StorageException extends RuntimeException {

    public S3StorageException(String message) {
        super(message);
    }

    public S3StorageException(
            String message,
            Throwable cause) {
        super(message, cause);
    }
}






package com.insurewise.framework.s3.service;

import com.insurewise.framework.s3.config.S3Properties;
import com.insurewise.framework.s3.exception.S3StorageException;
import java.time.Duration;
import java.time.Instant;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.DeleteObjectRequest;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.presigner.S3Presigner;
import software.amazon.awssdk.services.s3.presigner.model.GetObjectPresignRequest;
import software.amazon.awssdk.services.s3.presigner.model.PresignedGetObjectRequest;

@Service
public class S3FileStorageService {

    private final S3Client s3Client;
    private final S3Presigner s3Presigner;
    private final S3Properties properties;

    public S3FileStorageService(
            S3Client s3Client,
            S3Presigner s3Presigner,
            S3Properties properties) {
        this.s3Client = s3Client;
        this.s3Presigner = s3Presigner;
        this.properties = properties;
    }

    public String upload(
            MultipartFile file,
            String folder,
            UUID ownerId) {

        if (file == null || file.isEmpty()) {
            throw new S3StorageException(
                    "File cannot be empty.");
        }

        String fileName = file.getOriginalFilename();

        if (fileName == null || fileName.isBlank()) {
            throw new S3StorageException(
                    "File name cannot be empty.");
        }

        String key = buildKey(
                folder,
                ownerId,
                fileName);

        try {
            PutObjectRequest request =
                    PutObjectRequest.builder()
                            .bucket(properties.getBucket())
                            .key(key)
                            .contentType(file.getContentType())
                            .build();

            s3Client.putObject(
                    request,
                    RequestBody.fromBytes(file.getBytes()));

            return key;

        } catch (Exception exception) {
            throw new S3StorageException(
                    "Failed to upload file to S3.",
                    exception);
        }
    }

    public String uploadGenerated(
            byte[] content,
            String fileName,
            String contentType,
            String folder,
            UUID ownerId) {

        if (content == null || content.length == 0) {
            throw new S3StorageException(
                    "Generated content cannot be empty.");
        }

        if (fileName == null || fileName.isBlank()) {
            throw new S3StorageException(
                    "File name cannot be empty.");
        }

        String key = buildKey(
                folder,
                ownerId,
                fileName);

        try {
            PutObjectRequest request =
                    PutObjectRequest.builder()
                            .bucket(properties.getBucket())
                            .key(key)
                            .contentType(contentType)
                            .build();

            s3Client.putObject(
                    request,
                    RequestBody.fromBytes(content));

            return key;

        } catch (Exception exception) {
            throw new S3StorageException(
                    "Failed to upload generated file to S3.",
                    exception);
        }
    }

    public S3PresignedDownload createPresignedDownload(
            String s3Key) {

        if (s3Key == null || s3Key.isBlank()) {
            throw new S3StorageException(
                    "S3 key cannot be empty.");
        }

        try {
            GetObjectRequest getObjectRequest =
                    GetObjectRequest.builder()
                            .bucket(properties.getBucket())
                            .key(s3Key)
                            .build();

            GetObjectPresignRequest presignRequest =
                    GetObjectPresignRequest.builder()
                            .signatureDuration(
                                    Duration.ofMinutes(
                                            properties
                                                    .getPresignedUrlMinutes()))
                            .getObjectRequest(
                                    getObjectRequest)
                            .build();

            PresignedGetObjectRequest presigned =
                    s3Presigner.presignGetObject(
                            presignRequest);

            Instant expiresAt =
                    Instant.now().plus(
                            Duration.ofMinutes(
                                    properties
                                            .getPresignedUrlMinutes()));

            return new S3PresignedDownload(
                    presigned.url().toString(),
                    expiresAt);

        } catch (Exception exception) {
            throw new S3StorageException(
                    "Failed to generate S3 download URL.",
                    exception);
        }
    }

    public void delete(String s3Key) {

        if (s3Key == null || s3Key.isBlank()) {
            throw new S3StorageException(
                    "S3 key cannot be empty.");
        }

        try {
            DeleteObjectRequest request =
                    DeleteObjectRequest.builder()
                            .bucket(properties.getBucket())
                            .key(s3Key)
                            .build();

            s3Client.deleteObject(request);

        } catch (Exception exception) {
            throw new S3StorageException(
                    "Failed to delete file from S3.",
                    exception);
        }
    }

    private String buildKey(
            String folder,
            UUID ownerId,
            String fileName) {

        String safeFolder =
                folder == null ? "files" : folder.trim();

        String owner =
                ownerId == null
                        ? "system"
                        : ownerId.toString();

        return safeFolder
                + "/"
                + owner
                + "/"
                + UUID.randomUUID()
                + "-"
                + fileName;
    }

    public record S3PresignedDownload(
            String url,
            Instant expiresAt) {
    }
}






package com.insurewise.common.service;

import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.framework.s3.service.S3FileStorageService;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class AwsS3StorageService implements S3StorageService {

    private final S3FileStorageService s3FileStorageService;

    public AwsS3StorageService(
            S3FileStorageService s3FileStorageService) {
        this.s3FileStorageService =
                s3FileStorageService;
    }

    @Override
    public String upload(
            MultipartFile file,
            String folder,
            UUID ownerId) {

        return s3FileStorageService.upload(
                file,
                folder,
                ownerId);
    }

    @Override
    public String uploadGenerated(
            byte[] content,
            String fileName,
            String contentType,
            String folder,
            UUID ownerId) {

        return s3FileStorageService.uploadGenerated(
                content,
                fileName,
                contentType,
                folder,
                ownerId);
    }

    @Override
    public PresignedUrlResponse getPresignedDownloadUrl(
            String s3Key) {

        S3FileStorageService.S3PresignedDownload result =
                s3FileStorageService.createPresignedDownload(
                        s3Key);

        return new PresignedUrlResponse(
                result.url(),
                result.expiresAt());
    }

    @Override
    public void delete(String s3Key) {

        s3FileStorageService.delete(s3Key);
    }
}







package com.insurewise.framework.s3.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface S3Operation {
}






package com.insurewise.framework.s3.aspect;

import com.insurewise.framework.s3.annotation.S3Operation;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class S3OperationAspect {

    @Around("@annotation(s3Operation)")
    public Object handleS3Operation(
            ProceedingJoinPoint joinPoint,
            S3Operation s3Operation)
            throws Throwable {

        try {
            return joinPoint.proceed();

        } catch (Exception exception) {
            System.err.println(
                    "S3 operation failed: "
                            + exception.getMessage());

            throw exception;
        }
    }
}







<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
</dependency>

<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3-presigner</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>






