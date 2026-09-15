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

    public AwsS3FileService(
            AmazonS3 amazonS3,
            S3Properties properties) {
        this.amazonS3 = amazonS3;
        this.properties = properties;
    }

    @Override
    public String upload(
            MultipartFile file,
            String folder,
            UUID ownerId) {

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
            System.err.println("========== S3 UPLOAD START ==========");
            System.err.println("Bucket: " + properties.bucketName());
            System.err.println("Key: " + key);
            System.err.println("File: " + file.getOriginalFilename());
            System.err.println("====================================");

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

    private String normalize(String value) {
        if (value == null) {
            return "";
        }
        return value.trim().replaceAll("^/+|/+$", "");
    }
}
