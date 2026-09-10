public StaffProfileResponse create(
        StaffCreateRequest request) {

    try {
        String email = request.email().toLowerCase();

        validateEmailNotUsed(email);

        StaffUser staffUser = new StaffUser(
                request.fullName(),
                email,
                request.address(),
                passwordEncoder.encode(request.password()));

        return toResponse(
                staffUserRepository.save(staffUser));

    } catch (Exception exception) {
        System.err.println(
                "Error in StaffUserService.create: "
                        + exception.getMessage());

        throw exception;
    }
}


@Transactional(readOnly = true)
public List<StaffProfileResponse> list() {

    try {
        return staffUserRepository.findAll()
                .stream()
                .map(this::toResponse)
                .toList();

    } catch (Exception exception) {
        System.err.println(
                "Error in StaffUserService.list: "
                        + exception.getMessage());

        throw exception;
    }
}




@Transactional(readOnly = true)
public StaffProfileResponse get(UUID id) {

    try {
        return toResponse(find(id));

    } catch (Exception exception) {
        System.err.println(
                "Error in StaffUserService.get: "
                        + exception.getMessage());

        throw exception;
    }
}



public StaffProfileResponse update(
        UUID id,
        StaffUpdateRequest request) {

    try {

        // KEEP YOUR EXISTING CODE HERE

        StaffUser staffUser = find(id);

        String email = request.email().toLowerCase();

        boolean emailUsedByAnotherStaff =
                staffUserRepository
                        .findByEmailIgnoreCase(email)
                        .filter(existing ->
                                !existing.getId().equals(id))
                        .isPresent();

        boolean emailUsedByCustomer =
                customerRepository
                        .existsByEmailIgnoreCase(email);

        if (emailUsedByAnotherStaff
                || emailUsedByCustomer) {
            throw new DuplicateEmailException(email);
        }

        String passwordHash = null;

        if (request.password() != null
                && !request.password().isBlank()) {

            passwordHash =
                    passwordEncoder.encode(request.password());
        }

        staffUser.update(
                request.fullName(),
                email,
                request.address(),
                passwordHash);

        return toResponse(staffUser);

    } catch (Exception exception) {
        System.err.println(
                "Error in StaffUserService.update: "
                        + exception.getMessage());

        throw exception;
    }
}




public void delete(UUID id) {

    try {
        StaffUser staffUser = find(id);

        staffUserRepository.delete(staffUser);

    } catch (Exception exception) {
        System.err.println(
                "Error in StaffUserService.delete: "
                        + exception.getMessage());

        throw exception;
    }
}
