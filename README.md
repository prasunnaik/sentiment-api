/**
 * REST controller for managing staff users.
 *
 * <p>All endpoints in this controller are restricted to authenticated
 * users with the STAFF role.</p>
 */
@RestController
@RequestMapping("/api/staff/users")
@PreAuthorize("hasRole('STAFF')")
public class StaffUserManagementController {





/**
 * Creates the staff user management controller.
 *
 * @param staffUserService service responsible for staff user operations
 */
public StaffUserManagementController(
        StaffUserService staffUserService) {
    this.staffUserService = staffUserService;
}





/**
 * Creates a new staff user.
 *
 * @param request staff user details to create
 * @return the created staff user's profile
 */
@PostMapping
public ResponseEntity<StaffProfileResponse> create(
        @Valid @RequestBody StaffCreateRequest request) {







/**
 * Retrieves all staff users.
 *
 * @return list of staff user profiles
 */
@GetMapping
public List<StaffProfileResponse> list() {







/**
 * Retrieves a staff user by ID.
 *
 * @param id unique identifier of the staff user
 * @return the requested staff user's profile
 */
@GetMapping("/{id}")
public StaffProfileResponse get(
        @PathVariable UUID id) {






/**
 * Updates an existing staff user's details.
 *
 * @param id unique identifier of the staff user
 * @param request updated staff user details
 * @return the updated staff user's profile
 */
@PutMapping("/{id}")
public StaffProfileResponse update(
        @PathVariable UUID id,
        @Valid @RequestBody StaffUpdateRequest request) {






/**
 * Deletes a staff user and any associated profile picture.
 *
 * @param id unique identifier of the staff user
 */
@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(
        @PathVariable UUID id) {







/**
 * Uploads or replaces the profile picture for a staff user.
 *
 * @param id unique identifier of the staff user
 * @param file profile picture to upload
 * @return updated staff user profile containing the profile picture URL
 */
@PostMapping(
        value = "/{id}/profile-picture",
        consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
public StaffProfileResponse uploadProfilePicture(
        @PathVariable UUID id,
        @RequestPart("file") MultipartFile file) {







/**
 * Deletes the profile picture associated with a staff user.
 *
 * @param id unique identifier of the staff user
 */
@DeleteMapping("/{id}/profile-picture")
public ResponseEntity<Void> deleteProfilePicture(
        @PathVariable UUID id) {




   
