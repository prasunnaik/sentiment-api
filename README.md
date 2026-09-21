SecurityConfig

@Configuration: Registers this class as Spring configuration.
@EnableMethodSecurity: Enables annotations such as @PreAuthorize on controller/service methods.
SecurityFilterChain: Defines how incoming requests are secured.

Request rules

CSRF disabled: Common for APIs using JWTs instead of browser sessions.
CORS enabled: Allows requests from http://localhost:4200, likely an Angular frontend.
Stateless sessions: The server does not store login sessions; each request must include its JWT.
Public endpoints:

/auth/**, /api/auth/** — login and registration
/actuator/health — health check
Swagger/OpenAPI paths — API documentation
/error — error handling
OPTIONS /** — browser CORS pre-flight requests


All other endpoints: Require authentication.

Filters

CorrelationIdFilter: Adds or tracks an X-Correlation-Id so requests can be traced through logs.
JwtAuthenticationFilter: Reads and validates the JWT, then identifies the logged-in user.
Both filters run before Spring’s username/password authentication filter.

CORS settings

Allows methods such as GET, POST, PUT, PATCH, and DELETE.
Allows headers including Authorization and X-Correlation-Id.
Exposes X-Correlation-Id to the frontend.
allowCredentials(true) allows credentials, but the allowed origin must not be *.

SecurityProperties
This record reads security settings from configuration properties beginning with:
insurewise.security
For example, it may hold:

issuer: Identifies who issued the JWT.
jwtSecret: Secret used to sign or validate tokens.
tokenTtl: How long tokens remain valid.

This class only stores the values; the JWT service or filter must use them. Ensure jwtSecret is supplied securely through environment variables or a secrets manager, not committed to source control.
One implementation detail: SecurityProperties must be registered using @ConfigurationPropertiesScan or @EnableConfigurationProperties(SecurityProperties.class) for Spring Boot to create it automatically.





1. Application and database

Runs on port 8080 by default; SERVER_PORT can override it.
Application name is insurewise-service.
Connects to PostgreSQL using DB_URL, DB_USERNAME, and DB_PASSWORD.
ddl-auto: none means Hibernate will not create or update tables automatically.
Flyway is disabled by default, so database migrations will not run unless FLYWAY_ENABLED=true.

2. JWT security
These properties correspond to your SecurityProperties record:

issuer: Identifies the token issuer; default is insurewise.
jwt-secret: Secret used to sign or validate JWTs.
token-ttl: Token lifetime; 24h means tokens expire after 24 hours.

The JwtAuthenticationFilter or JWT service must read these values to validate tokens. The jwt: section is a legacy compatibility section for code that still expects properties such as jwt.secret and jwt.expiration-hours.
Important: The default JWT secret is only for local development. Replace it in any shared, test, staging, or production environment.
3. How this connects to SecurityConfig
Your security rules:

Require JWT authentication for most endpoints.
Allow login, registration, health, Swagger, and CORS pre-flight requests without authentication.
Use stateless sessions, so every protected request must send a JWT.
Allow the Angular frontend at http://localhost:4200 to call the API.

The Swagger paths configured here match the public paths permitted in SecurityConfig:

API documentation: /api-docs
Swagger UI: /swagger-ui.html

4. File uploads and storage

Requests and individual files are limited to 10 MB by default.
insurewise.storage defines the application’s S3 bucket, region, and presigned URL lifetime.
The custom S3 upload framework is disabled by default with S3_ENABLED=false.
S3 downloads are also disabled by default.
AWS credentials come from environment variables rather than being hardcoded.

5. Monitoring and logging

Exposes health, info, and metrics endpoints.
/actuator/health is publicly permitted by your security configuration.
Health details are intended to appear only for authorized users.
Application and Spring Security logs are set to INFO.

Overall behavior
By default, this is a local-development configuration: PostgreSQL is expected locally, Flyway and S3 are disabled, JWTs last 24 hours, Swagger is enabled, and the Angular frontend can call the API. For production, override database credentials, JWT secrets, CORS origins, migration settings, and storage credentials through environment variables.







Reads the token from the request’s Authorization header:
Bearer <JWT>


Uses jwt-secret to verify the token’s signature. This confirms the token was created by a trusted application and was not altered.


Checks the token issuer against insurewise.security.issuer (insurewise). This is used only if issuer validation is configured.


Checks expiration. The filter validates the token’s exp claim. The token-ttl: 24h is usually used when creating tokens; it does not extend an already expired token.


Extracts user information, such as username, user ID, or roles, from the token claims.


Creates an authenticated security context, allowing the request to pass .authenticated() checks in SecurityConfig.


Rejects or ignores invalid tokens. The request will ultimately receive 401 Unauthorized if it reaches a protected endpoint without valid authentication.


The filter may use either:

insurewise.security.jwt-secret through SecurityProperties, or
the legacy jwt.secret property through an older JwtService.

Your configuration defines both for compatibility, but they should contain the same secret. The JWT filter must also have access to SecurityProperties through @ConfigurationPropertiesScan or @EnableConfigurationProperties.
token-ttl is primarily relevant to the JWT creation service, while the filter mainly validates the token’s signature, issuer, and expiration.
