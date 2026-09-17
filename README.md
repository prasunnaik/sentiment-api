/**
 * REST controller that exposes dashboard metrics for staff users.
 */
@RestController
@RequestMapping("/api/dashboard")
@PreAuthorize("hasRole('STAFF')")
public class DashboardController {





/**
 * Retrieves aggregate metrics displayed on the staff dashboard.
 *
 * @return dashboard metrics
 */
@GetMapping("/metrics")
public DashboardMetricsResponse metrics() {





/**
 * REST controller for creating and managing policy applications.
 *
 * <p>Customers can create and view their applications, while staff
 * users can view applications and approve or reject them.</p>
 */
@RestController
@RequestMapping("/api/applications")
public class PolicyApplicationController {





/**
 * Creates a new policy application for the authenticated customer.
 *
 * @param principal authenticated customer
 * @param request policy application details
 * @return created policy application

 */





 
/**
 * Lists policy applications visible to the authenticated user.
 *
 * <p>Customers receive their own applications, while staff users
 * can retrieve applications across customers.</p>
 *
 * @param principal authenticated user
 * @param status optional application status filter
 * @return list of policy applications

 */





 /**
 * Retrieves a policy application by ID.
 *
 * @param principal authenticated user
 * @param id policy application identifier
 * @return policy application details

 */





 /**
 * Approves a pending policy application.
 *
 * @param principal authenticated staff user
 * @param id policy application identifier
 * @return result of the approval decision

 */

 



/**
 * Rejects a pending policy application.
 *
 * @param principal authenticated staff user
 * @param id policy application identifier
 * @return result of the rejection decision

 */





 /**
 * REST controller for managing insurance policies.
 *
 * <p>Customers and staff can retrieve active policies.
 * Staff users can create, update, and delete policies.</p>
 */
@RestController
@RequestMapping("/api/policies")
public class PolicyController {





/**
 * Retrieves active policies available to customers.
 *
 * @return list of active policies

 */




 /**
 * Retrieves a policy by ID.
 *
 * @param id policy identifier
 * @return policy details

 */



 

/**
 * Creates a new insurance policy.
 *
 * @param request policy creation details
 * @return created policy

 */





 /**
 * Updates an existing insurance policy.
 *
 * @param id policy identifier
 * @param request updated policy details
 * @return updated policy

 */






 /**
 * Deletes an insurance policy.
 *
 * @param id policy identifier

 */




 
