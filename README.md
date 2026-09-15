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
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Configuration
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
