public AuthResponse registerCustomer(
        CustomerRegistrationRequest request) {

    try {
        String email = request.email().toLowerCase();

        if (customerRepository.existsByEmailIgnoreCase(email)
                || staffUserRepository.existsByEmailIgnoreCase(email)) {
            throw new DuplicateEmailException(email);
        }

        Customer customer = new Customer(
                request.fullName(),
                request.phone(),
                email,
                passwordEncoder.encode(request.password()));

        customerRepository.save(customer);

        return createResponse(customer);

    } catch (Exception exception) {
        System.err.println(
                "Error in registerCustomer: "
                        + exception.getMessage());

        throw exception;
    }
}



@Transactional(readOnly = true)
public AuthResponse loginCustomer(
        CustomerLoginRequest request) {

    try {
        Customer customer = customerRepository
                .findByEmailIgnoreCase(request.email())
                .orElseThrow(InvalidCredentialsException::new);

        if (!passwordEncoder.matches(
                request.password(),
                customer.getPasswordHash())) {
            throw new InvalidCredentialsException();
        }

        return createResponse(customer);

    } catch (Exception exception) {
        System.err.println(
                "Error in loginCustomer: "
                        + exception.getMessage());

        throw exception;
    }
}




@Transactional(readOnly = true)
public AuthResponse loginStaff(
        StaffLoginRequest request) {

    try {
        StaffUser staff = staffUserRepository
                .findByEmailIgnoreCase(request.email())
                .orElseThrow(InvalidCredentialsException::new);

        if (!passwordEncoder.matches(
                request.password(),
                staff.getPasswordHash())) {
            throw new InvalidCredentialsException();
        }

        String token = jwtService.generate(
                staff.getId(),
                staff.getEmail(),
                JwtRole.STAFF);

        return new AuthResponse(
                token,
                "Bearer",
                staff.getId(),
                staff.getEmail(),
                JwtRole.STAFF.name());

    } catch (Exception exception) {
        System.err.println(
                "Error in loginStaff: "
                        + exception.getMessage());

        throw exception;
    }
}




