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
