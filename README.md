/**
 * Creates a new pending policy application using the current policy's
 * coverage and premium amounts.
 *
 * @param applicationCode unique application code
 * @param customerId customer submitting the application
 * @param policy policy being applied for
 * @param coverageType selected coverage type
 * @param dateOfBirth customer's date of birth
 * @param address customer's address
 * @param preferredStartDate requested policy start date
 * @param nomineeName nominee's name
 * @param nomineeRelationship nominee's relationship to the customer

 */




 /**
 * Approves a pending policy application.
 *
 * @param staffUserId staff user making the decision
 * @param startDate policy start date
 * @param endDate policy end date
 * @throws IllegalStateException if the application is not pending
 */
public void approve(





/**
 * Rejects a pending policy application.
 *
 * @param staffUserId staff user making the rejection decision
 * @throws IllegalStateException if the application is not pending
 */
public void reject(UUID staffUserId) {





/**
 * Checks whether the application belongs to the specified customer.
 *
 * @param customerId customer identifier
 * @return {@code true} if the application belongs to the customer
 */
public boolean isOwnedBy(UUID customerId) {





/**
 * Checks whether the application has an ACTIVE status.
 *
 * @return {@code true} when the application is active
 */
public boolean isActive() {

