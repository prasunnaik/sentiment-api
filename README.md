Error in StaffUserService.uploadProfilePicture: Unable to upload file to S3
com.insurewise.framework.s3.exception.S3FileStorageException: Unable to upload file to S3
	at com.insurewise.framework.s3.service.AwsS3FileService.upload(AwsS3FileService.java:78)
	at com.insurewise.common.service.FrameworkS3StorageService.upload(FrameworkS3StorageService.java:23)
	at com.insurewise.auth.service.StaffUserService.uploadProfilePicture(StaffUserService.java:83)
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103)
	at java.base/java.lang.reflect.Method.invoke(Method.java:580)
	at org.springframework.aop.support.AopUtils.invokeJoinpointUsingReflection(AopUtils.java:354)
	at org.springframework.aop.framework.ReflectiveMethodInvocation.invokeJoinpoint(ReflectiveMethodInvocation.java:196)
	at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:163)
	at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:768)
	at org.springframework.transaction.interceptor.TransactionInterceptor$1.proceedWithInvocation(TransactionInterceptor.java:123)
	at org.springframework.transaction.interceptor.TransactionAspectSupport.invokeWithinTransaction(TransactionAspectSupport.java:392)
	at org.springframework.transaction.interceptor.TransactionInterceptor.invoke(TransactionInterceptor.java:119)
	at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:184)
	at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:768)
	at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:720)
	at com.insurewise.auth.service.StaffUserService$$SpringCGLIB$$0.uploadProfilePicture(<generated>)
	at com.insurewise.auth.controller.StaffUserManagementController.uploadProfilePicture(StaffUserManagementController.java:86)
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103)
	at java.base/java.lang.reflect.Method.invoke(Method.java:580)
	at org.springframework.aop.support.AopUtils.invokeJoinpointUsingReflection(AopUtils.java:354)
	at org.springframework.aop.framework.ReflectiveMethodInvocation.invokeJoinpoint(ReflectiveMethodInvocation.java:196)
	at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:163)
	at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:768)
	at org.springframework.security.authorization.method.AuthorizationManagerBeforeMethodInterceptor.invoke(AuthorizationManagerBeforeMethodInterceptor.java:198)
	at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:184)
	at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:768)
	at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:720)
	at com.insurewise.auth.controller.StaffUserManagementController$$SpringCGLIB$$0.uploadProfilePicture(<generated>)
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103)
	at java.base/java.lang.reflect.Method.invoke(Method.java:580)
	at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:255)
	at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:188)
	at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:118)
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:926)
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:831)
	at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87)
	at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1089)
	at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:979)
	at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1014)
	at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:914)
	at jakarta.servlet.http.HttpServlet.service(HttpServlet.java:590)
	at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:885)
	at jakarta.servlet.http.HttpServlet.service(HttpServlet.java:658)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:206)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150)
	at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:51)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:110)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150)
	at org.springframework.web.filter.CompositeFilter$VirtualFilterChain.doFilter(CompositeFilter.java:108)
	at org.springframework.security.web.FilterChainProxy.lambda$doFilterInternal$3(FilterChainProxy.java:231)
	at org.springframework.security.web.ObservationFilterChainDecorator$FilterObservation$SimpleFilterObservation.lambda$wrap$1(ObservationFilterChainDecorator.java:479)
	at org.springframework.security.web.ObservationFilterChainDecorator$AroundFilterObservation$SimpleAroundFilterObservation.lambda$wrap$1(ObservationFilterChainDecorator.java:340)
	at org.springframework.security.web.ObservationFilterChainDecorator.lambda$wrapSecured$0(ObservationFilterChainDecorator.java:82)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:128)
	at org.springframework.security.web.access.intercept.AuthorizationFilter.doFilter(AuthorizationFilter.java:100)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:126)
	at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:120)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.session.SessionManagementFilter.doFilter(SessionManagementFilter.java:131)
	at org.springframework.security.web.session.SessionManagementFilter.doFilter(SessionManagementFilter.java:85)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.authentication.AnonymousAuthenticationFilter.doFilter(AnonymousAuthenticationFilter.java:100)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter.doFilter(SecurityContextHolderAwareRequestFilter.java:179)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.savedrequest.RequestCacheAwareFilter.doFilter(RequestCacheAwareFilter.java:63)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at com.insurewise.common.security.JwtAuthenticationFilter.doFilterInternal(JwtAuthenticationFilter.java:87)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:107)
	at org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:93)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.web.filter.CorsFilter.doFilterInternal(CorsFilter.java:91)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.header.HeaderWriterFilter.doHeadersAfter(HeaderWriterFilter.java:90)
	at org.springframework.security.web.header.HeaderWriterFilter.doFilterInternal(HeaderWriterFilter.java:75)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.context.SecurityContextHolderFilter.doFilter(SecurityContextHolderFilter.java:82)
	at org.springframework.security.web.context.SecurityContextHolderFilter.doFilter(SecurityContextHolderFilter.java:69)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter.doFilterInternal(WebAsyncManagerIntegrationFilter.java:62)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:227)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.session.DisableEncodeUrlFilter.doFilterInternal(DisableEncodeUrlFilter.java:42)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.wrapFilter(ObservationFilterChainDecorator.java:240)
	at org.springframework.security.web.ObservationFilterChainDecorator$AroundFilterObservation$SimpleAroundFilterObservation.lambda$wrap$0(ObservationFilterChainDecorator.java:323)
	at org.springframework.security.web.ObservationFilterChainDecorator$ObservationFilter.doFilter(ObservationFilterChainDecorator.java:224)
	at org.springframework.security.web.ObservationFilterChainDecorator$VirtualFilterChain.doFilter(ObservationFilterChainDecorator.java:137)
	at org.springframework.security.web.FilterChainProxy.doFilterInternal(FilterChainProxy.java:233)
	at org.springframework.security.web.FilterChainProxy.doFilter(FilterChainProxy.java:191)
	at org.springframework.web.filter.CompositeFilter$VirtualFilterChain.doFilter(CompositeFilter.java:113)
	at org.springframework.web.servlet.handler.HandlerMappingIntrospector.lambda$createCacheFilter$3(HandlerMappingIntrospector.java:195)
	at org.springframework.web.filter.CompositeFilter$VirtualFilterChain.doFilter(CompositeFilter.java:113)
	at org.springframework.web.filter.CompositeFilter.doFilter(CompositeFilter.java:74)
	at org.springframework.security.config.annotation.web.configuration.WebMvcSecurityConfiguration$CompositeFilterChainProxy.doFilter(WebMvcSecurityConfiguration.java:230)
	at org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:352)
	at org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:268)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150)
	at org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150)
	at org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150)
	at org.springframework.web.filter.ServerHttpObservationFilter.doFilterInternal(ServerHttpObservationFilter.java:109)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150)
	at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:116)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:175)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:150)
	at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:167)
	at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:90)
	at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:482)
	at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:115)
	at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:93)
	at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:74)
	at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:344)
	at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:391)
	at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:63)
	at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:896)
	at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1736)
	at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:52)
	at org.apache.tomcat.util.threads.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1191)
	at org.apache.tomcat.util.threads.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:659)
	at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:63)
	at java.base/java.lang.Thread.run(Thread.java:1583)
Caused by: com.amazonaws.services.s3.model.AmazonS3Exception: The specified bucket is not valid. (Service: Amazon S3; Status Code: 400; Error Code: InvalidBucketName; Request ID: HVJFHYEDC19CNEWQ; S3 Extended Request ID: RgjfsrrHWolVNm9brc3iHLQLG57ParTTpeSI9vJ+DGGdbpzJGaIBcnVOsof8urvIcg0aIG3klPc=; Proxy: null), S3 Extended Request ID: RgjfsrrHWolVNm9brc3iHLQLG57ParTTpeSI9vJ+DGGdbpzJGaIBcnVOsof8urvIcg0aIG3klPc=
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.handleErrorResponse(AmazonHttpClient.java:1879)
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.handleServiceErrorResponse(AmazonHttpClient.java:1418)
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.executeOneRequest(AmazonHttpClient.java:1387)
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.executeHelper(AmazonHttpClient.java:1157)
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.doExecute(AmazonHttpClient.java:814)
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.executeWithTimer(AmazonHttpClient.java:781)
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.execute(AmazonHttpClient.java:755)
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.access$500(AmazonHttpClient.java:715)
	at com.amazonaws.http.AmazonHttpClient$RequestExecutionBuilderImpl.execute(AmazonHttpClient.java:697)
	at com.amazonaws.http.AmazonHttpClient.execute(AmazonHttpClient.java:561)
	at com.amazonaws.http.AmazonHttpClient.execute(AmazonHttpClient.java:541)
	at com.amazonaws.services.s3.AmazonS3Client.invoke(AmazonS3Client.java:5456)
	at com.amazonaws.services.s3.AmazonS3Client.invoke(AmazonS3Client.java:5403)
	at com.amazonaws.services.s3.AmazonS3Client.access$300(AmazonS3Client.java:421)
	at com.amazonaws.services.s3.AmazonS3Client$PutObjectStrategy.invokeServiceCall(AmazonS3Client.java:6532)
	at com.amazonaws.services.s3.AmazonS3Client.uploadObject(AmazonS3Client.java:1861)
	at com.amazonaws.services.s3.AmazonS3Client.putObject(AmazonS3Client.java:1821)
	at com.insurewise.framework.s3.service.AwsS3FileService.upload(AwsS3FileService.java:70)
	... 162 more
package com.insurewise.auth.service;

import com.insurewise.auth.dto.request.StaffCreateRequest;
import com.insurewise.auth.dto.request.StaffUpdateRequest;
import com.insurewise.auth.dto.response.StaffProfileResponse;
import com.insurewise.auth.entity.StaffUser;
import com.insurewise.auth.exception.DuplicateEmailException;
import com.insurewise.auth.exception.StaffUserNotFoundException;
import com.insurewise.auth.repository.CustomerRepository;
import com.insurewise.auth.repository.StaffUserRepository;
import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.service.S3StorageService;
import java.util.List;
import java.util.UUID;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

@Service
@Transactional
public class StaffUserService {

    private final StaffUserRepository staffUserRepository;
    private final CustomerRepository customerRepository;
    private final PasswordEncoder passwordEncoder;
    private final S3StorageService storageService;

    public StaffUserService(
            StaffUserRepository staffUserRepository,
            CustomerRepository customerRepository,
            PasswordEncoder passwordEncoder,
            S3StorageService storageService) {

        this.staffUserRepository = staffUserRepository;
        this.customerRepository = customerRepository;
        this.passwordEncoder = passwordEncoder;
        this.storageService = storageService;
    }

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

    public StaffProfileResponse uploadProfilePicture(
            UUID id,
            MultipartFile file) {

        try {
            StaffUser staffUser = find(id);

            if (file == null || file.isEmpty()) {
                throw new IllegalArgumentException(
                        "Profile picture file cannot be empty");
            }

            String oldS3Key =
                    staffUser.getProfilePictureS3Key();

            String newS3Key =
                    storageService.upload(
                            file,
                            "profile-pictures",
                            staffUser.getId());

            staffUser.updateProfilePictureS3Key(
                    newS3Key);

            if (oldS3Key != null
                    && !oldS3Key.isBlank()) {

                storageService.delete(oldS3Key);
            }

            return toResponse(staffUser);

        } catch (Exception exception) {

            System.err.println(
                    "Error in StaffUserService.uploadProfilePicture: "
                            + exception.getMessage());

            exception.printStackTrace();

            throw exception;
        }
    }

    public void deleteProfilePicture(UUID id) {

        try {
            StaffUser staffUser = find(id);

            String s3Key =
                    staffUser.getProfilePictureS3Key();

            if (s3Key != null && !s3Key.isBlank()) {
                storageService.delete(s3Key);
            }

            staffUser.updateProfilePictureS3Key(null);

        } catch (Exception exception) {

            System.err.println(
                    "Error in StaffUserService.deleteProfilePicture: "
                            + exception.getMessage());

            exception.printStackTrace();

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

            StaffUser staffUser = find(id);

            String email =
                    request.email().toLowerCase();

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
                        passwordEncoder.encode(
                                request.password());
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

            String s3Key =
                    staffUser.getProfilePictureS3Key();

            if (s3Key != null
                    && !s3Key.isBlank()) {

                storageService.delete(s3Key);
            }

            staffUserRepository.delete(staffUser);

        } catch (Exception exception) {

            System.err.println(
                    "Error in StaffUserService.delete: "
                            + exception.getMessage());

            throw exception;
        }
    }

    private StaffUser find(UUID id) {

        return staffUserRepository.findById(id)
                .orElseThrow(() ->
                        new StaffUserNotFoundException(id));
    }

    private void validateEmailNotUsed(
            String email) {

        if (staffUserRepository
                .existsByEmailIgnoreCase(email)
                || customerRepository
                .existsByEmailIgnoreCase(email)) {

            throw new DuplicateEmailException(email);
        }
    }

    private StaffProfileResponse toResponse(
            StaffUser staffUser) {

        String profilePictureUrl = null;

        String s3Key =
                staffUser.getProfilePictureS3Key();

        if (s3Key != null
                && !s3Key.isBlank()) {

            PresignedUrlResponse download =
                    storageService
                            .getPresignedDownloadUrl(
                                    s3Key);

            profilePictureUrl =
                    download.url();
        }

        return new StaffProfileResponse(
                staffUser.getId(),
                staffUser.getFullName(),
                staffUser.getEmail(),
                staffUser.getAddress(),
                profilePictureUrl);
    }
}
