/**
 * JPA entity representing an insurance policy category.
 */
@Entity
@Table(name = "categories")
public class Category {





/**
 * Creates a policy category.
 *
 * @param name category name
 * @param description category description
 * @param status


/**
 * Creates a policy category.
 *
 * @param name category name
 * @param description category description
 * @param status category status

 */




 /**
 * Initializes the creation timestamp before persistence.
/**
 * Initializes the creation timestamp before persistence.
 */




/**
 * Updates the category's editable fields.
 *
 * @param name updated category name
 * @param description updated category description
 * @param status updated category status

 */




 /**
 * JPA entity representing an insurance policy.
 */
@Entity
@Table(name = "policies")
public class Policy {




/**
 * Creates an insurance policy.
 *
 * @param name policy name
 * @param category policy category
 * @param coverageAmount amount covered by the policy
 * @param premiumAmount premium amount
 * @param durationLabel policy duration
 * @param status policy status

 */





 /**
 * Determines whether the policy can currently be shown to customers.
 *
 * <p>A policy is customer-active only when both the policy and its
 * category have an ACTIVE status.</p>
 *
 * @return {@code true} when the policy and category are active;
 *         otherwise {@code false}
 */
public boolean isActiveForCustomer() {





