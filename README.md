public ClaimDependentResponse addDependent(
        UUID customerId,
        UUID claimId,
        ClaimDependentRequest request) {

    try {

        // existing code

    } catch (Exception exception) {
        System.err.println(
                "Error in ClaimDependentService.addDependent: "
                        + exception.getMessage());

        throw exception;
    }
}



@Transactional(readOnly = true)
public List<ClaimDependentResponse> listDependents(
        UUID customerId,
        UUID claimId) {

    try {

        // existing code

    } catch (Exception exception) {
        System.err.println(
                "Error in ClaimDependentService.listDependents: "
                        + exception.getMessage());

        throw exception;
    }
}
