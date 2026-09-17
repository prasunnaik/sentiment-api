/**
 * Service responsible for policy application creation,
 * retrieval, and approval or rejection decisions.
 */
@Service
@Transactional
public class PolicyApplicationService {




/**
 * Creates a new pending policy application for a customer.
 *
 * <p>The selected policy must be active and the customer cannot have
 * another pending application for the same policy.</p>
 *
 * @param customerId authenticated customer's identifier
 * @param request policy application details
 * @return created policy application
 * @throws ApplicationStateException if the policy is not active
 * @throws DuplicatePendingApplicationException if a pending application
 *         already exists for the customer and policy
 */







 /**
 * Retrieves policy applications visible to the authenticated user.
 *
 * <p>Staff users can retrieve applications across customers, while
 * customers can retrieve only their own applications.</p>
 *
 * @param principal authenticated user
 * @param status optional status filter
 * @return list of policy applications

 */






 /**
 * Retrieves a policy application after checking customer ownership.
 *
 * @param principal authenticated user
 * @param applicationId policy application identifier
 * @return policy application details
 * @throws ApplicationNotFoundException if the application does not exist
 *         or is not accessible by the customer
 */







 /**
 * Approves a pending policy application and calculates its end date
 * using the policy duration.
 *
 * @param staffUserId staff user making the approval decision
 * @param applicationId policy application identifier
 * @return approval decision details
 * @throws ApplicationStateException if the application cannot be approved

 */






 /**
 * Rejects a pending policy application.
 *
 * @param staffUserId staff user making the rejection decision
 * @param applicationId policy application identifier
 * @return rejection decision details
 * @throws ApplicationStateException if the application cannot be rejected

 */






/**
 * Retrieves a policy application entity for use by collaborating services.
 *
 * @param applicationId policy application identifier
 * @return policy application entity
 * @throws ApplicationNotFoundException if the application does not exist
 */
public PolicyApplication getApplicationEntityForInternalUse(






/**
 * Calculates an application end date from the policy duration label.
 *
 * <p>The numeric portion of the duration label is interpreted as years.
 * When no numeric value is available, one year is used as the default.</p>
 *
 * @param startDate application start date
 * @param durationLabel policy duration label
 * @return calculated policy end date

 */




 
 
