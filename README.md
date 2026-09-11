package com.insurewise.policy.exception;

public class CategoryNotFoundException extends RuntimeException {

    public CategoryNotFoundException(String message) {
        super(message);
    }
}


package com.insurewise.policy.exception;

public class PolicyNotFoundException extends RuntimeException {

    public PolicyNotFoundException(String message) {
        super(message);
    }
}



import com.insurewise.policy.exception.CategoryNotFoundException;
import com.insurewise.policy.exception.PolicyNotFoundException;


@ExceptionHandler(CategoryNotFoundException.class)
public ResponseEntity<ApiErrorResponse> handleCategoryNotFound(
        CategoryNotFoundException exception,
        HttpServletRequest request) {

    return build(
            HttpStatus.NOT_FOUND,
            exception.getMessage(),
            request.getRequestURI()
    );
}




@ExceptionHandler(PolicyNotFoundException.class)
public ResponseEntity<ApiErrorResponse> handlePolicyNotFound(
        PolicyNotFoundException exception,
        HttpServletRequest request) {

    return build(
            HttpStatus.NOT_FOUND,
            exception.getMessage(),
            request.getRequestURI()
    );
}
