/**
 * REST controller for uploading, listing, and deleting documents
 * associated with policy applications.
 *
 * <p>Both customers and staff users can access these endpoints,
 * subject to application ownership checks performed by the service.</p>
 */
@RestController
@RequestMapping("/api/applications/{id}/documents")
@PreAuthorize("hasAnyRole('CUSTOMER', 'STAFF')")
public class ApplicationDocumentController {




/**
 * Uploads a document for a policy application.
 *
 * @param principal authenticated user information
 * @param id policy application identifier
 * @param file document to upload
 * @return metadata and download information for the uploaded document
 */
@PostMapping(...)
public ApplicationDocumentResponse upload(







/**
 * Lists documents associated with a policy application.
 *
 * @param principal authenticated user information
 * @param id policy application identifier
 * @return documents associated with the application
 */
@GetMapping
public List<ApplicationDocumentResponse> list(







/**
 * Deletes a document associated with a policy application.
 *
 * @param principal authenticated user information
 * @param id policy application identifier
 * @param documentId document identifier
 */
@DeleteMapping("/{documentId}")
public void delete(





/**
 * REST controller for managing insurance policy categories.
 *
 * <p>Staff users can create, update, and delete categories.
 * Both customers and staff users can retrieve categories.</p>
 */
@RestController
@RequestMapping("/api/categories")
public class CategoryController {





/**
 * Creates a new policy category.
 *
 * @param request category creation details
 * @return created category

 */




 /**
 * Retrieves all policy categories.
 *
 * @return list of categories

 */



 /**
 * Updates an existing policy category.
 *
 * @param id category identifier
 * @param request updated category details
 * @return updated category

 */




 /**
 * Deletes a policy category.
 *
 * @param id category identifier
 */

