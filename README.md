/**
 * Repository for policy application persistence and query operations.
 */
public interface PolicyApplicationRepository
        extends JpaRepository<PolicyApplication, UUID> {



   /**
 * Retrieves a customer's applications ordered from newest to oldest.
 *
 * @param customerId customer identifier
 * @return customer's applications
 */
List<PolicyApplication> findByCustomerIdOrderByCreatedAtDesc(



/**
 * Retrieves applications with the specified status, ordered from newest
 * to oldest.
 *
 * @param status application status
 * @return matching applications
 */
List<PolicyApplication> findByStatusOrderByCreatedAtDesc(




/**
 * Checks whether a customer already has an application for a policy
 * with the specified status.
 *
 * @param customerId customer identifier
 * @param policyId policy identifier
 * @param status application status
 * @return {@code true} if such an application exists
 */
boolean existsByCustomerIdAndPolicyIdAndStatus(




/**
 * Retrieves the next value from the application code database sequence.
 *
 * @return next sequence value used to generate an application code
 */
@Query(...)
Long nextApplicationCodeSequence();

