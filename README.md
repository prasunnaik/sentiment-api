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
