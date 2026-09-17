/**
 * Service responsible for uploading, retrieving, and deleting
 * documents associated with policy applications.
 *
 * <p>Document files are stored in S3 while their metadata is stored
 * in the application database.</p>
 */
@Service
@Transactional
public class ApplicationDocumentService {





/**
 * Uploads a document for a policy application and stores its metadata.
 *
 * @param principal authenticated user
 * @param applicationId policy application identifier
 * @param file document to upload
 * @return uploaded document metadata and presigned download URL
 * @throws InvalidFileException if the file is missing or empty
 * @throws ApplicationNotFoundException if the application cannot be accessed

 */






 /**
 * Lists documents associated with a policy application.
 *
 * @param principal authenticated user
 * @param applicationId policy application identifier
 * @return application documents ordered by creation time

 */






/**
 * Deletes an application document from both S3 and the database.
 *
 * @param principal authenticated user
 * @param applicationId policy application identifier
 * @param documentId document identifier

 */



 /**
 * Retrieves an application and verifies that the authenticated customer
 * owns it when the caller has the CUSTOMER role.
 *
 * <p>Staff users are allowed to access applications without an ownership
 * restriction.</p>
 *
 * @param principal authenticated user
 * @param applicationId policy application identifier
 * @return accessible policy application
 * @throws ApplicationNotFoundException if the application does not exist
 *         or a customer attempts to access another customer's application
 */




/**
 * Converts an application document entity into its API response.
 *
 * @param document application document entity
 * @return document response containing a presigned download URL

 */




 


 
 
