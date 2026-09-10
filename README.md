@ExceptionHandler(Exception.class)
ResponseEntity<ApiErrorResponse> handleGenericException(
        Exception exception,
        HttpServletRequest request) {

    return build(
            HttpStatus.INTERNAL_SERVER_ERROR,
            exception.getMessage(),
            request.getRequestURI());
}
