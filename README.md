private APIGatewayProxyResponseEvent response(
        int status,
        Object body) {

    try {
        return new APIGatewayProxyResponseEvent()
                .withStatusCode(status)
                .withHeaders(Map.of(
                        "Content-Type", "application/json",
                        "Access-Control-Allow-Origin", "*",
                        "Access-Control-Allow-Headers", "*",
                        "Access-Control-Allow-Methods",
                        "GET,POST,PUT,DELETE,OPTIONS"))
                .withBody(mapper.writeValueAsString(body));

    } catch (Exception e) {
        return new APIGatewayProxyResponseEvent()
                .withStatusCode(500)
                .withBody("{\"message\":\"Response creation failed\"}");
    }
}
