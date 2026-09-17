/**
 * Repository for insurance policy persistence and query operations.
 */
public interface PolicyRepository
        extends JpaRepository<Policy, UUID> {



   /**
 * Retrieves policies with the specified status ordered from newest
 * to oldest.
 *
 * @param status policy status
 * @return matching policies
 */
List<Policy> findAllByStatusOrderByCreatedAtDesc(
