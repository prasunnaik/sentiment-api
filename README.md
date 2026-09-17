/**
 * Aspect responsible for automatically uploading multipart files to S3
 * for methods annotated with {@link EnableS3Upload}.
 */
@Aspect
@Component
public class S3UploadAspect {





/**
 * Intercepts methods annotated with {@link EnableS3Upload}, uploads the
 * supplied multipart file to S3, and stores the resulting S3 key on the
 * target object's {@link S3FileField}-annotated field.
 *
 * @param joinPoint intercepted method invocation
 * @param enableS3Upload S3 upload configuration from the annotation
 * @return result of the intercepted method
 * @throws Throwable if the intercepted method or S3 processing fails
 */
@Around("@annotation(enableS3Upload)")
public Object upload(





/**
 * Sets the supplied S3 key on the first String field annotated
 * with {@link S3FileField}.
 *
 * @param target object containing the S3 key field
 * @param key S3 object key
 * @throws IllegalAccessException if the field cannot be accessed
 */
private void setS3FileField(





/**
 * Aspect responsible for deleting S3 objects for methods annotated
 * with {@link EnableS3Delete}.
 */
@Aspect
@Component
public class S3DeleteAspect {





/**
 * Intercepts methods annotated with {@link EnableS3Delete}, locates an
 * S3 key on method arguments, deletes the corresponding S3 object,
 * and then proceeds with the original method.
 *
 * @param joinPoint intercepted method invocation
 * @param enableS3Delete S3 deletion annotation
 * @return result of the intercepted method
 * @throws Throwable if S3 deletion or the intercepted method fails

 */





 /**
 * Finds the S3 object key from an object containing a
 * {@link S3FileField}-annotated String field.
 *
 * @param target object to inspect
 * @return S3 object key, or {@code null} when no key is found
 * @throws IllegalAccessException if the field cannot be accessed
 */
