/**
 * Represents a temporary S3 download URL and its expiration time.
 *
 * @param url presigned URL
 * @param expiresAt timestamp at which the URL expires
 */
public record S3PresignedUrl(
        String url,
        Instant expiresAt) {
}
