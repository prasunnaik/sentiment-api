/**
 * Spring Boot auto-configuration for S3 file storage.
 *
 * <p>Creates the Amazon S3 client and selects either the AWS-backed
 * or disabled S3 file service based on the configured S3 properties.</p>
 */
@Configuration
@Import(...)
@EnableConfigurationProperties(S3Properties.class)
public class S3AutoConfiguration {




/**
 * Creates and configures the Amazon S3 client.
 *
 * @param properties configured S3 properties
 * @return configured Amazon S3 client

 */





 /**
 * Creates the AWS-backed S3 file service when S3 is enabled.
 *
 * @param amazonS3 configured Amazon S3 client
 * @param properties configured S3 properties
 * @return AWS-backed S3 file service

 */






 /**
 * Creates the disabled S3 service when S3 storage is not enabled.
 *
 * @return disabled S3 file service

 */



 S3Properties
/**
 * Configuration properties for S3 file storage.
 *
 * <p>Properties are loaded using the
 * {@code ng.file-upload.s3} configuration prefix.</p>
 *
 * @param enabled whether S3 storage is enabled
 * @param bucketName S3 bucket name
 * @param region AWS region
 * @param accessKey AWS access key
 * @param secretKey AWS secret key
 * @param endpoint optional custom S3-compatible endpoint
 * @param pathStyleAccessEnabled whether path-style access is enabled
 * @param keyPrefix optional prefix applied to generated S3 keys
 * @param download download configuration
 */
@ConfigurationProperties(prefix = "ng.file-upload.s3")
public record S3Properties(



/**
 * Returns the lifetime of generated presigned download URLs.
 *
 * @return presigned URL lifetime
 */
public Duration presignedUrlTtl() {



/**
 * Configuration controlling S3 download functionality.
 *
 * @param enabled whether S3 download endpoints are enabled
 */
public record Download(boolean enabled) {
}











/**
 * REST controller for generating S3 presigned download URLs.
 *
 * <p>The controller is available only when S3 download functionality
 * is enabled.</p>
 */
@RestController
@RequestMapping("/api/storage")
...
public class S3FileController {





/**
 * Generates a temporary presigned URL for downloading an S3 object.
 *
 * @param key S3 object key
 * @return response containing the download URL and expiration timestamp
 */
@GetMapping("/download-url")
public ResponseEntity<Map<String, Object>> downloadUrl(


 
