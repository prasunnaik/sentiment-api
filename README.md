package com.insurewise.auth.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record StaffCreateRequest(

        @NotBlank
        @Size(max = 120)
        String fullName,

        @NotBlank
        @Email
        @Size(max = 160)
        String email,

        @NotBlank
        @Size(max = 240)
        String address,

        @NotBlank
        @Size(min = 8, max = 100)
        String password
) {
}


package com.insurewise.auth.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record StaffUpdateRequest(

        @NotBlank
        @Size(max = 120)
        String fullName,

        @NotBlank
        @Email
        @Size(max = 160)
        String email,

        @NotBlank
        @Size(max = 240)
        String address,

        @Size(min = 8, max = 100)
        String password
) {
}



public void update(
        String fullName,
        String email,
        String address,
        String passwordHash) {

    this.fullName = fullName;
    this.email = email.toLowerCase();
    this.address = address;

    if (passwordHash != null && !passwordHash.isBlank()) {
        this.passwordHash = passwordHash;
    }
}
