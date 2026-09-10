package com.insurewise.auth.exception;

import java.util.UUID;

public class StaffUserNotFoundException extends RuntimeException {

    public StaffUserNotFoundException(UUID id) {
        super("Staff user not found: " + id);
    }
}


package com.insurewise.claims.exception;

import java.util.UUID;

public class ClaimNotFoundException extends RuntimeException {

    public ClaimNotFoundException(UUID id) {
        super("Claim not found: " + id);
    }

    public ClaimNotFoundException() {
        super("Claim not found");
    }
}




package com.insurewise.claims.exception;

import java.util.UUID;

public class ClaimDocumentNotFoundException extends RuntimeException {

    public ClaimDocumentNotFoundException(UUID id) {
        super("Claim document not found: " + id);
    }
}




package com.insurewise.payments.exception;

import java.util.UUID;

public class PaymentNotFoundException extends RuntimeException {

    public PaymentNotFoundException(UUID id) {
        super("Payment not found: " + id);
    }

    public PaymentNotFoundException() {
        super("Payment not found");
    }
}



package com.insurewise.payments.exception;

import java.util.UUID;

public class PaymentDocumentNotFoundException
        extends RuntimeException {

    public PaymentDocumentNotFoundException(UUID id) {
        super("Payment document not found: " + id);
    }
}


package com.insurewise.payments.exception;

public class PaymentStateException extends RuntimeException {

    public PaymentStateException(String message) {
        super(message);
    }
}


package com.insurewise.payments.exception;

public class PaymentDocumentStateException
        extends RuntimeException {

    public PaymentDocumentStateException(String message) {
        super(message);
    }
}


package com.insurewise.policy.exception;

import java.util.UUID;

public class PolicyNotFoundException extends RuntimeException {

    public PolicyNotFoundException(UUID id) {
        super("Policy not found: " + id);
    }
}


package com.insurewise.policy.exception;

import java.util.UUID;

public class CategoryNotFoundException extends RuntimeException {

    public CategoryNotFoundException(UUID id) {
        super("Category not found: " + id);
    }
}


package com.insurewise.policy.exception;

import java.util.UUID;

public class DependentNotFoundException extends RuntimeException {

    public DependentNotFoundException(UUID id) {
        super("Dependent not found: " + id);
    }
}


package com.insurewise.policy.exception;

import java.util.UUID;

public class ApplicationDocumentNotFoundException
        extends RuntimeException {

    public ApplicationDocumentNotFoundException(UUID id) {
        super("Application document not found: " + id);
    }
}


package com.insurewise.common.exception;

public class InvalidFileException extends RuntimeException {

    public InvalidFileException(String message) {
        super(message);
    }
}


package com.insurewise.common.exception;

public class IdempotencyKeyConflictException
        extends RuntimeException {

    public IdempotencyKeyConflictException(String message) {
        super(message);
    }
}


package com.insurewise.common.exception;

import com.insurewise.auth.exception.DuplicateEmailException;
import com.insurewise.auth.exception.InvalidCredentialsException;
import com.insurewise.auth.exception.StaffUserNotFoundException;
import com.insurewise.claims.exception.ClaimDocumentNotFoundException;
import com.insurewise.claims.exception.ClaimNotFoundException;
import com.insurewise.common.dto.ApiErrorResponse;
import com.insurewise.payments.exception.PaymentDocumentNotFoundException;
import com.insurewise.payments.exception.PaymentDocumentStateException;
import com.insurewise.payments.exception.PaymentNotFoundException;
import com.insurewise.payments.exception.PaymentStateException;
import com.insurewise.policy.exception.ApplicationDocumentNotFoundException;
import com.insurewise.policy.exception.ApplicationNotFoundException;
import com.insurewise.policy.exception.ApplicationStateException;
import com.insurewise.policy.exception.CategoryNotFoundException;
import com.insurewise.policy.exception.DependentNotFoundException;
import com.insurewise.policy.exception.DuplicatePendingApplicationException;
import com.insurewise.policy.exception.PolicyNotFoundException;
import jakarta.servlet.http.HttpServletRequest;
import java.time.LocalDateTime;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(DuplicateEmailException.class)
    ResponseEntity<ApiErrorResponse> handleDuplicate(
            DuplicateEmailException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.CONFLICT,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(InvalidCredentialsException.class)
    ResponseEntity<ApiErrorResponse> handleInvalidCredentials(
            InvalidCredentialsException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.UNAUTHORIZED,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ResponseEntity<ApiErrorResponse> handleValidation(
            MethodArgumentNotValidException exception,
            HttpServletRequest request) {

        String message = exception.getBindingResult()
                .getFieldErrors()
                .stream()
                .findFirst()
                .map(error -> error.getField()
                        + ": "
                        + error.getDefaultMessage())
                .orElse("Request validation failed");

        return build(
                HttpStatus.BAD_REQUEST,
                message,
                request.getRequestURI());
    }

    @ExceptionHandler(DuplicatePendingApplicationException.class)
    ResponseEntity<ApiErrorResponse> handleDuplicateApplication(
            DuplicatePendingApplicationException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.CONFLICT,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(ApplicationStateException.class)
    ResponseEntity<ApiErrorResponse> handleApplicationState(
            ApplicationStateException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.BAD_REQUEST,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(ApplicationNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handleApplicationNotFound(
            ApplicationNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(StaffUserNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handleStaffUserNotFound(
            StaffUserNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(ClaimNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handleClaimNotFound(
            ClaimNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(ClaimDocumentNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handleClaimDocumentNotFound(
            ClaimDocumentNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(PaymentNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handlePaymentNotFound(
            PaymentNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(PaymentDocumentNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handlePaymentDocumentNotFound(
            PaymentDocumentNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(PolicyNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handlePolicyNotFound(
            PolicyNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(CategoryNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handleCategoryNotFound(
            CategoryNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(DependentNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handleDependentNotFound(
            DependentNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(ApplicationDocumentNotFoundException.class)
    ResponseEntity<ApiErrorResponse> handleApplicationDocumentNotFound(
            ApplicationDocumentNotFoundException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.NOT_FOUND,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(InvalidFileException.class)
    ResponseEntity<ApiErrorResponse> handleInvalidFile(
            InvalidFileException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.BAD_REQUEST,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(IdempotencyKeyConflictException.class)
    ResponseEntity<ApiErrorResponse> handleIdempotencyConflict(
            IdempotencyKeyConflictException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.CONFLICT,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(PaymentStateException.class)
    ResponseEntity<ApiErrorResponse> handlePaymentState(
            PaymentStateException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.CONFLICT,
                exception.getMessage(),
                request.getRequestURI());
    }

    @ExceptionHandler(PaymentDocumentStateException.class)
    ResponseEntity<ApiErrorResponse> handlePaymentDocumentState(
            PaymentDocumentStateException exception,
            HttpServletRequest request) {

        return build(
                HttpStatus.CONFLICT,
                exception.getMessage(),
                request.getRequestURI());
    }

    private ResponseEntity<ApiErrorResponse> build(
            HttpStatus status,
            String message,
            String path) {

        return ResponseEntity.status(status).body(
                new ApiErrorResponse(
                        LocalDateTime.now(),
                        status.value(),
                        status.getReasonPhrase(),
                        message,
                        path));
    }
}



@ExceptionHandler(ApplicationStateException.class)
ResponseEntity<ApiErrorResponse> handleApplicationState(
        ApplicationStateException exception,
        HttpServletRequest request) {



        

