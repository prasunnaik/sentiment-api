/**
 * Request data used to create a staff user.
 *
 * @param fullName staff user's full name
 * @param email staff user's email address
 * @param address staff user's address
 * @param password plain-text password supplied during creation
 */
public record StaffCreateRequest(




/**
 * Request data used to update an existing staff user.
 *
 * <p>The password is optional. When omitted or blank, the existing
 * password is retained.</p>
 *
 * @param fullName updated staff user's full name
 * @param email updated staff user's email address
 * @param address updated staff user's address
 * @param password optional new password
 */
public record StaffUpdateRequest(





/**
 * Request data used to authenticate a customer.
 *
 * @param email customer's email address
 * @param password customer's password
 */
public record CustomerLoginRequest(






/**
 * Request data used to register a new customer.
 *
 * @param fullName customer's full name
 * @param phone customer's phone number
 * @param email customer's email address
 * @param password customer's password
 */
public record CustomerRegistrationRequest(






/**
 * Request data used to authenticate a staff user.
 *
 * @param email staff user's email address
 * @param password staff user's password
 */
public record StaffLoginRequest(







/**
 * Response containing staff user profile information.
 *
 * @param id unique identifier of the staff user
 * @param fullName staff user's full name
 * @param email staff user's email address
 * @param address staff user's address
 * @param profilePictureUrl temporary URL used to access the profile picture
 */
public record StaffProfileResponse(






/**
 * Response containing customer profile information.
 *
 * @param id unique identifier of the customer
 * @param fullName customer's full name
 * @param phone customer's phone number
 * @param email customer's email address
 */
public record CustomerProfileResponse(





