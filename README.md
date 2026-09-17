/**
 * Enables automatic S3 file upload processing around a method.
 *
 * <p>The associated aspect searches the method arguments for a
 * {@link MultipartFile} and stores the resulting S3 key in a field
 * annotated with {@link S3FileField}.</p>
 *
 * @return folder in which the uploaded file should be stored
 */
String folder() default "uploads";




import org.springframework.web.multipart.MultipartFile;



/**
 * Enables automatic deletion of an S3 object before the annotated
 * method executes.
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface EnableS3Delete {
}





/**
 * Marks a String field as containing an S3 object key.
 *
 * <p>S3 upload and delete aspects use this annotation to locate
 * the S3 key on an object.</p>
 *
 * @return folder associated with the S3 file
 */
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface S3FileField {






