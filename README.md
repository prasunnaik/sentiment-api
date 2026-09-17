/**
 * JPA entity representing a staff user.
 *
 * <p>Staff user credentials and profile information are persisted
 * in the {@code staff_users} database table.</p>
 */
@Entity
@Table(name = "staff_users")
public class StaffUser {





/**
 * Creates a staff user with the supplied profile and password hash.
 *
 * @param fullName staff user's full name
 * @param email staff user's email address
 * @param address staff user's address
 * @param passwordHash encoded password
 */
public StaffUser(
        String fullName,
        String email,
        String address,
        String passwordHash) {






/**
 * Initializes the creation timestamp before the entity is persisted.
 */
@PrePersist
void prePersist() {





/**
 * Updates the staff user's profile information.
 *
 * <p>The password is updated only when a non-blank password hash
 * is supplied.</p>
 *
 * @param fullName updated full name
 * @param email updated email address
 * @param address updated address
 * @param passwordHash optional encoded password
 */
public void update(






/**
 * Updates the S3 key associated with the staff user's profile picture.
 *
 * @param s3Key S3 object key, or {@code null} to remove the association
 */
public void updateProfilePictureS3Key(String s3Key) {






/**
 * JPA entity representing a customer.
 *
 * <p>Customer information is persisted in the {@code customers}
 * database table.</p>
 */
@Entity
@Table(name = "customers")
public class Customer {






/**
 * Creates a customer with the supplied profile information.
 *
 * @param fullName customer's full name
 * @param phone customer's phone number
 * @param email customer's email address
 * @param passwordHash encoded password
 */
public Customer(







/**
 * Initializes the creation timestamp before the customer is persisted.
 */
@PrePersist
void prePersist() {







/**
 * Updates the customer's editable profile information.
 *
 * @param fullName updated full name
 * @param phone updated phone number
 */
public void update(String fullName, String phone) {







/**
 * Repository for performing persistence operations on customers.
 */
public interface CustomerRepository
        extends JpaRepository<Customer, UUID> {






/**
 * Checks whether a customer exists with the specified email,
 * ignoring case.
 *
 * @param email email address to check
 * @return {@code true} if a customer with the email exists;
 *         otherwise {@code false}
 */
boolean existsByEmailIgnoreCase(String email);






/**
 * Finds a customer by email, ignoring case.
 *
 * @param email email address to search for
 * @return matching customer, if present
 */
Optional<Customer> findByEmailIgnoreCase(String email);






/**
 * Repository for performing persistence operations on staff users.
 */
public interface StaffUserRepository
        extends JpaRepository<StaffUser, UUID> {
