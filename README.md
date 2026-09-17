/**
 * Creates an application document record.
 *
 * @param policyApplication policy application associated with the document
 * @param fileName original file name
 * @param contentType MIME type of the file
 * @param s3Key S3 object key
 * @param uploadedBy identifier of the user who uploaded the file

 */




 /**
 * Represents the lifecycle status of a policy application.
 */
public enum ApplicationStatus {




/**
 * Represents the status of an insurance policy category.
 */
public enum CategoryStatus {






/**
 * Represents the type of coverage selected for a policy application.
 */
public enum CoverageType {





/**
 * Represents the relationship between a customer and their nominee.
 */
public enum NomineeRelationship {





/**
 * Represents the lifecycle status of an insurance policy.
 */
public enum PolicyStatus {







/**
 * Repository for policy application document persistence operations.
 */
public interface ApplicationDocumentRepository
        extends JpaRepository<ApplicationDocument, UUID> {






   /**
 * Retrieves documents for a policy application in reverse chronological order.
 *
 * @param policyApplicationId policy application identifier
 * @return list of documents ordered from newest to oldest
 */
List<ApplicationDocument> findByPolicyApplicationIdOrderByCreatedAtDesc(
        UUID policyApplicationId);
