/**
 * S3 file service implementation used when S3 storage is disabled.
 *
 * <p>Upload and download operations fail explicitly, while delete
 * operations are treated as no-ops because no remote object is expected.</p>
 */
public class DisabledS3FileService implements S3FileService {





/**
 * Abstraction for file storage operations backed by S3.
 */
public interface S3FileService {





/**
 * Uploads a multipart file to storage.
 *
 * @param file file to upload
 * @param folder logical folder in storage
 * @param ownerId identifier of the file owner
 * @return stored object's S3 key
 */
String upload(





/**
 * Uploads generated content to storage.
 *
 * @param content file content
 * @param fileName file name
 * @param contentType MIME type
 * @param folder logical folder in storage
 * @param ownerId identifier of the file owner
 * @return stored object's S3 key
 */
String uploadGenerated(






/**
 * Generates a temporary URL for downloading a stored object.
 *
 * @param s3Key S3 object key
 * @return presigned download URL information
 */
S3PresignedUrl getPresignedDownloadUrl(






/**
 * Deletes a stored object.
 *
 * @param s3Key S3 object key
 */
void delete(String s3Key);

