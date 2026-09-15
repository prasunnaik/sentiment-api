2026-09-15T12:01:58.335+05:30  INFO 56340 --- [insurewise-service] [           main] com.insurewise.InsurewiseApplication     : Starting InsurewiseApplication using Java 21.0.12 with PID 56340 (C:\Users\psumans\CAP-Code\insurewise-cap-angular-be\insurewise-service\target\classes started by psumans in C:\Users\psumans\CAP-Code\insurewise-cap-angular-be\insurewise-service)
2026-09-15T12:01:58.338+05:30  INFO 56340 --- [insurewise-service] [           main] com.insurewise.InsurewiseApplication     : No active profile set, falling back to 1 default profile: "default"
2026-09-15T12:02:00.097+05:30  INFO 56340 --- [insurewise-service] [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
2026-09-15T12:02:00.224+05:30  INFO 56340 --- [insurewise-service] [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 114 ms. Found 5 JPA repository interfaces.
2026-09-15T12:02:01.430+05:30  INFO 56340 --- [insurewise-service] [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port 8080 (http)
2026-09-15T12:02:01.448+05:30  INFO 56340 --- [insurewise-service] [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2026-09-15T12:02:01.449+05:30  INFO 56340 --- [insurewise-service] [           main] o.apache.catalina.core.StandardEngine    : Starting Servlet engine: [Apache Tomcat/10.1.20]
2026-09-15T12:02:01.578+05:30  INFO 56340 --- [insurewise-service] [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2026-09-15T12:02:01.579+05:30  INFO 56340 --- [insurewise-service] [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 3164 ms
Standard Commons Logging discovery in action with spring-jcl: please remove commons-logging.jar from classpath in order to avoid potential conflicts
2026-09-15T12:02:02.037+05:30  INFO 56340 --- [insurewise-service] [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
2026-09-15T12:02:02.391+05:30  INFO 56340 --- [insurewise-service] [           main] com.zaxxer.hikari.pool.HikariPool        : HikariPool-1 - Added connection org.postgresql.jdbc.PgConnection@58f7215c
2026-09-15T12:02:02.395+05:30  INFO 56340 --- [insurewise-service] [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
2026-09-15T12:02:02.535+05:30  INFO 56340 --- [insurewise-service] [           main] o.f.c.internal.license.VersionPrinter    : Flyway Community Edition 9.22.3 by Redgate
2026-09-15T12:02:02.535+05:30  INFO 56340 --- [insurewise-service] [           main] o.f.c.internal.license.VersionPrinter    : See release notes here: https://rd.gt/416ObMi
2026-09-15T12:02:02.535+05:30  INFO 56340 --- [insurewise-service] [           main] o.f.c.internal.license.VersionPrinter    : 
2026-09-15T12:02:02.560+05:30  INFO 56340 --- [insurewise-service] [           main] org.flywaydb.core.FlywayExecutor         : Database: jdbc:postgresql://localhost:5432/postgres (PostgreSQL 18.6)
2026-09-15T12:02:02.571+05:30  WARN 56340 --- [insurewise-service] [           main] o.f.c.internal.database.base.Database    : Flyway upgrade recommended: PostgreSQL 18.6 is newer than this version of Flyway and support has not been tested. The latest supported version of PostgreSQL is 15.
2026-09-15T12:02:02.685+05:30  INFO 56340 --- [insurewise-service] [           main] o.f.core.internal.command.DbValidate     : Successfully validated 12 migrations (execution time 00:00.089s)
2026-09-15T12:02:02.702+05:30  INFO 56340 --- [insurewise-service] [           main] o.f.core.internal.command.DbMigrate      : Current version of schema "public": 11
2026-09-15T12:02:02.708+05:30  INFO 56340 --- [insurewise-service] [           main] o.f.core.internal.command.DbMigrate      : Schema "public" is up to date. No migration necessary.
2026-09-15T12:02:02.871+05:30  INFO 56340 --- [insurewise-service] [           main] o.hibernate.jpa.internal.util.LogHelper  : HHH000204: Processing PersistenceUnitInfo [name: default]
2026-09-15T12:02:02.969+05:30  INFO 56340 --- [insurewise-service] [           main] org.hibernate.Version                    : HHH000412: Hibernate ORM core version 6.4.4.Final
2026-09-15T12:02:03.030+05:30  INFO 56340 --- [insurewise-service] [           main] o.h.c.internal.RegionFactoryInitiator    : HHH000026: Second-level cache disabled
2026-09-15T12:02:03.432+05:30  INFO 56340 --- [insurewise-service] [           main] o.s.o.j.p.SpringPersistenceUnitInfo      : No LoadTimeWeaver setup: ignoring JPA class transformer
2026-09-15T12:02:05.091+05:30  INFO 56340 --- [insurewise-service] [           main] o.h.e.t.j.p.i.JtaPlatformInitiator       : HHH000489: No JTA platform available (set 'hibernate.transaction.jta.platform' to enable JTA platform integration)
2026-09-15T12:02:05.257+05:30  INFO 56340 --- [insurewise-service] [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
2026-09-15T12:02:06.049+05:30  INFO 56340 --- [insurewise-service] [           main] o.s.d.j.r.query.QueryEnhancerFactory     : Hibernate is in classpath; If applicable, HQL parser will be used.
2026-09-15T12:02:06.433+05:30  WARN 56340 --- [insurewise-service] [           main] .s.s.UserDetailsServiceAutoConfiguration : 

Using generated security password: c6dad3ba-1fe5-40c7-93f9-f33173995108

This generated password is for development use only. Your security configuration must be updated before running your application in production.

2026-09-15T12:02:07.186+05:30  INFO 56340 --- [insurewise-service] [           main] o.s.b.a.e.web.EndpointLinksResolver      : Exposing 3 endpoint(s) beneath base path '/actuator'
2026-09-15T12:02:07.296+05:30  INFO 56340 --- [insurewise-service] [           main] o.s.s.web.DefaultSecurityFilterChain     : Will secure any request with [org.springframework.security.web.session.DisableEncodeUrlFilter@425a3af5, org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter@7c5eb88c, org.springframework.security.web.context.SecurityContextHolderFilter@71904ea8, org.springframework.security.web.header.HeaderWriterFilter@4addfb95, org.springframework.web.filter.CorsFilter@fc9313d, org.springframework.security.web.authentication.logout.LogoutFilter@2296ed0d, com.insurewise.common.security.JwtAuthenticationFilter@6f867b0c, org.springframework.security.web.savedrequest.RequestCacheAwareFilter@40fd9358, org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter@65c97eeb, org.springframework.security.web.authentication.AnonymousAuthenticationFilter@7f0b32c0, org.springframework.security.web.session.SessionManagementFilter@4e8e0052, org.springframework.security.web.access.ExceptionTranslationFilter@2181144e, org.springframework.security.web.access.intercept.AuthorizationFilter@19266ca3]
2026-09-15T12:02:08.224+05:30  WARN 56340 --- [insurewise-service] [           main] ConfigServletWebServerApplicationContext : Exception encountered during context initialization - cancelling refresh attempt: org.springframework.context.ApplicationContextException: Failed to start bean 'webServerStartStop'
2026-09-15T12:02:08.229+05:30  INFO 56340 --- [insurewise-service] [           main] j.LocalContainerEntityManagerFactoryBean : Closing JPA EntityManagerFactory for persistence unit 'default'
2026-09-15T12:02:08.233+05:30  INFO 56340 --- [insurewise-service] [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Shutdown initiated...
2026-09-15T12:02:08.239+05:30  INFO 56340 --- [insurewise-service] [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Shutdown completed.
2026-09-15T12:02:08.269+05:30  INFO 56340 --- [insurewise-service] [           main] .s.b.a.l.ConditionEvaluationReportLogger : 

Error starting ApplicationContext. To display the condition evaluation report re-run your application with 'debug' enabled.
2026-09-15T12:02:08.300+05:30 ERROR 56340 --- [insurewise-service] [           main] o.s.b.d.LoggingFailureAnalysisReporter   : 

***************************
APPLICATION FAILED TO START
***************************

Description:

Web server failed to start. Port 8080 was already in use.

Action:

Identify and stop the process that's listening on port 8080 or configure this application to listen on another port.

[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  15.429 s
[INFO] Finished at: 2026-09-15T12:02:08+05:30
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.springframework.boot:spring-boot-maven-plugin:3.2.5:run (default-cli) on project insurewise-service: Process terminated with exit code: 1 -> [Help 1]                                                                                                                
[ERROR] 
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR] 
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoExecutionException
