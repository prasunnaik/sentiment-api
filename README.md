package com.insurewise.auth.controller;

import com.insurewise.auth.entity.Customer;
import com.insurewise.auth.repository.CustomerRepository;
import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.security.JwtRole;
import com.insurewise.common.security.JwtService;
import com.insurewise.common.service.S3StorageService;
import java.time.Instant;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@Transactional
@TestPropertySource(properties = {
        "spring.datasource.url=jdbc:h2:mem:profile-controller-test;MODE=PostgreSQL;DB_CLOSE_DELAY=-1;DATABASE_TO_UPPER=false",
        "spring.datasource.driver-class-name=org.h2.Driver",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.H2Dialect",
        "spring.flyway.enabled=false",
        "insurewise.storage.enabled=false"
})
class ProfileControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private JwtService jwtService;

    @Autowired
    private CustomerRepository customerRepository;

    @MockBean
    private S3StorageService storageService;

    private Customer customerWithPicture;
    private Customer customerWithoutPicture;
    private String customerToken;
    private String noPictureToken;
    private String invalidCustomerToken;
    private String staffToken;

    @BeforeEach
    void setUp() {
        customerRepository.deleteAll();

        customerWithPicture = customerRepository.save(new Customer(
                "Customer One",
                "9999999999",
                "customer1@example.com",
                "encoded-password"));
        customerWithPicture.setProfilePictureS3Key("profile-pictures/customer-one.png");
        customerRepository.save(customerWithPicture);

        customerWithoutPicture = customerRepository.save(new Customer(
                "Customer Two",
                "8888888888",
                "customer2@example.com",
                "encoded-password"));

        when(storageService.getPresignedDownloadUrl(anyString()))
                .thenReturn(new PresignedUrlResponse(
                        "https://example.com/profile-picture.png",
                        Instant.parse("2030-01-01T00:00:00Z")));

        customerToken = bearerToken(customerWithPicture.getId(), JwtRole.CUSTOMER);
        noPictureToken = bearerToken(customerWithoutPicture.getId(), JwtRole.CUSTOMER);
        invalidCustomerToken = bearerToken(UUID.randomUUID(), JwtRole.CUSTOMER);
        staffToken = bearerToken(UUID.randomUUID(), JwtRole.STAFF);
    }

    @Test
    void returnsExistingProfilePictureForAuthenticatedCustomer() throws Exception {
        mockMvc.perform(get("/auth/profile-picture")
                        .header("Authorization", customerToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.customer_id").value(customerWithPicture.getId().toString()))
                .andExpect(jsonPath("$.s3_key").value("profile-pictures/customer-one.png"))
                .andExpect(jsonPath("$.download.url").value("https://example.com/profile-picture.png"));
    }

    @Test
    void returnsNoContentWhenProfilePictureIsMissing() throws Exception {
        mockMvc.perform(get("/auth/profile-picture")
                        .header("Authorization", noPictureToken))
                .andExpect(status().isNoContent());
    }

    @Test
    void returnsServerErrorForInvalidCustomer() throws Exception {
        mockMvc.perform(get("/auth/profile-picture")
                        .header("Authorization", invalidCustomerToken))
                .andExpect(status().isInternalServerError());
    }

    @Test
    void rejectsUnauthorizedAccess() throws Exception {
        mockMvc.perform(get("/auth/profile-picture"))
                .andExpect(status().isForbidden());
    }

    @Test
    void rejectsStaffAccessToCustomerProfilePictureEndpoint() throws Exception {
        mockMvc.perform(get("/auth/profile-picture")
                        .header("Authorization", staffToken))
                .andExpect(status().isForbidden());
    }

    private String bearerToken(UUID userId, JwtRole role) {
        return "Bearer " + jwtService.generate(
                userId,
                role.name().toLowerCase() + "@example.com",
                role);
    }
}
package com.insurewise.auth.service;

import com.insurewise.auth.dto.response.StaffProfileResponse;
import com.insurewise.auth.entity.StaffUser;
import com.insurewise.auth.exception.StaffUserNotFoundException;
import com.insurewise.auth.repository.CustomerRepository;
import com.insurewise.auth.repository.StaffUserRepository;
import com.insurewise.common.service.S3StorageService;
import java.util.Optional;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class StaffUserServiceTest {

    @Mock
    private StaffUserRepository staffUserRepository;

    @Mock
    private CustomerRepository customerRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private S3StorageService storageService;

    private StaffUserService service;

    @BeforeEach
    void setUp() {
        service = new StaffUserService(
                staffUserRepository,
                customerRepository,
                passwordEncoder,
                storageService);
    }

    @Test
    void returnsCurrentStaffProfile() {
        UUID staffUserId = UUID.randomUUID();
        StaffUser staffUser = new StaffUser(
                "Local Staff Admin",
                "staff.local@insurewise.com",
                "InsureWise HQ",
                "encoded-password");

        setId(staffUser, staffUserId);
        when(staffUserRepository.findById(staffUserId)).thenReturn(Optional.of(staffUser));

        StaffProfileResponse response = service.getCurrentStaffProfile(staffUserId);

        assertThat(response.id()).isEqualTo(staffUserId);
        assertThat(response.fullName()).isEqualTo("Local Staff Admin");
        assertThat(response.email()).isEqualTo("staff.local@insurewise.com");
        assertThat(response.address()).isEqualTo("InsureWise HQ");
    }

    @Test
    void throwsWhenCurrentStaffProfileDoesNotExist() {
        UUID staffUserId = UUID.randomUUID();
        when(staffUserRepository.findById(staffUserId)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> service.getCurrentStaffProfile(staffUserId))
                .isInstanceOf(StaffUserNotFoundException.class);
    }

    private void setId(StaffUser staffUser, UUID id) {
        try {
            java.lang.reflect.Field field = StaffUser.class.getDeclaredField("id");
            field.setAccessible(true);
            field.set(staffUser, id);
        } catch (ReflectiveOperationException exception) {
            throw new IllegalStateException(exception);
        }
    }
}
package com.insurewise.policy.controller;

import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.security.JwtRole;
import com.insurewise.common.security.JwtService;
import com.insurewise.common.service.S3StorageService;
import com.insurewise.policy.entity.Category;
import com.insurewise.policy.entity.CategoryStatus;
import com.insurewise.policy.entity.CoverageType;
import com.insurewise.policy.entity.NomineeRelationship;
import com.insurewise.policy.entity.Policy;
import com.insurewise.policy.entity.PolicyApplication;
import com.insurewise.policy.entity.PolicyStatus;
import com.insurewise.policy.repository.ApplicationDocumentRepository;
import com.insurewise.policy.repository.CategoryRepository;
import com.insurewise.policy.repository.PolicyApplicationRepository;
import com.insurewise.policy.repository.PolicyRepository;
import java.math.BigDecimal;
import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@Transactional
@TestPropertySource(properties = {
        "spring.datasource.url=jdbc:h2:mem:application-document-controller-test;MODE=PostgreSQL;DB_CLOSE_DELAY=-1;DATABASE_TO_UPPER=false",
        "spring.datasource.driver-class-name=org.h2.Driver",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.H2Dialect",
        "spring.flyway.enabled=false",
        "insurewise.storage.enabled=false"
})
class ApplicationDocumentControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private JwtService jwtService;

    @Autowired
    private CategoryRepository categoryRepository;

    @Autowired
    private PolicyRepository policyRepository;

    @Autowired
    private PolicyApplicationRepository applicationRepository;

    @Autowired
    private ApplicationDocumentRepository documentRepository;

    @MockBean
    private S3StorageService storageService;

    private UUID customerId;
    private String customerToken;
    private String otherCustomerToken;
    private String staffToken;
    private PolicyApplication application;

    @BeforeEach
    void setUp() {
        documentRepository.deleteAll();
        applicationRepository.deleteAll();
        policyRepository.deleteAll();
        categoryRepository.deleteAll();

        when(storageService.upload(any(), eq("application-documents"), any(), any()))
                .thenReturn("insurewise/application-documents/test-application/test.pdf");
        when(storageService.getPresignedDownloadUrl(any()))
                .thenReturn(new PresignedUrlResponse(
                        "https://example.com/documents/test.pdf",
                        Instant.parse("2030-01-01T00:00:00Z")));
        when(storageService.getPresignedPreviewUrl(any()))
                .thenReturn(new PresignedUrlResponse(
                        "https://example.com/documents/test-preview.pdf",
                        Instant.parse("2030-01-01T00:00:00Z")));

        Category category = categoryRepository.save(new Category(
                "Health",
                "Health coverage",
                CategoryStatus.ACTIVE));
        Policy policy = policyRepository.save(new Policy(
                "Silver Plan",
                category,
                new BigDecimal("500000.00"),
                new BigDecimal("1200.00"),
                "1 Year",
                PolicyStatus.ACTIVE));

        customerId = UUID.randomUUID();
        application = applicationRepository.save(new PolicyApplication(
                "APP-2000",
                customerId,
                policy,
                CoverageType.SINGLE,
                LocalDate.now().minusYears(30),
                "123 Main Street",
                LocalDate.now().plusDays(10),
                "Nominee Name",
                NomineeRelationship.SPOUSE));

        customerToken = bearerToken(customerId, JwtRole.CUSTOMER);
        otherCustomerToken = bearerToken(UUID.randomUUID(), JwtRole.CUSTOMER);
        staffToken = bearerToken(UUID.randomUUID(), JwtRole.STAFF);
    }

    @Test
    void staffCanListApplicationDocuments() throws Exception {
        UUID documentId = uploadDocument();

        mockMvc.perform(get("/api/applications/{id}/documents", application.getId())
                        .header("Authorization", staffToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(documentId.toString()))
                .andExpect(jsonPath("$[0].fileName").value("policy.pdf"))
                .andExpect(jsonPath("$[0].objectKey", Matchers.containsString(application.getId().toString())))
                .andExpect(jsonPath("$[0].fileSize").value(9))
                .andExpect(jsonPath("$[0].download.url").value("https://example.com/documents/test.pdf"));
    }

    @Test
    void staffCanViewSpecificDocument() throws Exception {
        UUID documentId = uploadDocument();

        mockMvc.perform(get("/api/applications/{id}/documents/{documentId}", application.getId(), documentId)
                        .header("Authorization", staffToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(documentId.toString()))
                .andExpect(jsonPath("$.applicationId").value(application.getId().toString()))
                .andExpect(jsonPath("$.objectKey", Matchers.containsString(application.getId().toString())))
                .andExpect(jsonPath("$.contentType").value(MediaType.APPLICATION_PDF_VALUE))
                .andExpect(jsonPath("$.fileSize").value(9))
                .andExpect(jsonPath("$.download.url").value("https://example.com/documents/test.pdf"));
    }

    @Test
    void staffCanPreviewSpecificDocument() throws Exception {
        UUID documentId = uploadDocument();

        mockMvc.perform(get("/api/applications/{id}/documents/{documentId}/preview", application.getId(), documentId)
                        .header("Authorization", staffToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.url").value("https://example.com/documents/test-preview.pdf"));
    }

    @Test
    void staffCanDownloadSpecificDocument() throws Exception {
        UUID documentId = uploadDocument();

        mockMvc.perform(get("/api/applications/{id}/documents/{documentId}/download", application.getId(), documentId)
                        .header("Authorization", staffToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.url").value("https://example.com/documents/test.pdf"));
    }

    @Test
    void documentEndpointReturnsNotFoundForMissingDocument() throws Exception {
        mockMvc.perform(get("/api/applications/{id}/documents/{documentId}", application.getId(), UUID.randomUUID())
                        .header("Authorization", staffToken))
                .andExpect(status().isNotFound());
    }

    @Test
    void documentEndpointReturnsNotFoundForMissingApplication() throws Exception {
        mockMvc.perform(get("/api/applications/{id}/documents", UUID.randomUUID())
                        .header("Authorization", staffToken))
                .andExpect(status().isNotFound());
    }

    @Test
    void otherCustomerCannotAccessAnotherCustomersDocuments() throws Exception {
        UUID documentId = uploadDocument();

        mockMvc.perform(get("/api/applications/{id}/documents/{documentId}", application.getId(), documentId)
                        .header("Authorization", otherCustomerToken))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.errorCode").value("ACCESS_DENIED"));
    }

    @Test
    void uploadRejectsInvalidContentType() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "policy.pdf",
                MediaType.TEXT_PLAIN_VALUE,
                "dummy".getBytes());

        mockMvc.perform(multipart("/api/applications/{id}/documents", application.getId())
                        .file(file)
                        .header("Authorization", customerToken))
                .andExpect(status().isBadRequest());
    }

    @Test
    void invalidUploadReturnsStructuredErrorResponse() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "policy.pdf",
                MediaType.TEXT_PLAIN_VALUE,
                "dummy".getBytes());

        mockMvc.perform(multipart("/api/applications/{id}/documents", application.getId())
                        .file(file)
                        .header("Authorization", customerToken))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.timestamp").exists())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.errorCode").value("INVALID_FILE"))
                .andExpect(jsonPath("$.message").exists())
                .andExpect(jsonPath("$.path").value("/api/applications/" + application.getId() + "/documents"))
                .andExpect(jsonPath("$.correlationId").isNotEmpty());
    }

    @Test
    void uploadRejectsOversizedFile() throws Exception {
        byte[] oversized = new byte[(int) (10L * 1024 * 1024 + 1)];
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "policy.pdf",
                MediaType.APPLICATION_PDF_VALUE,
                oversized);

        mockMvc.perform(multipart("/api/applications/{id}/documents", application.getId())
                        .file(file)
                        .header("Authorization", customerToken))
                .andExpect(status().isBadRequest());
    }

    @Test
    void customerCanPreviewOwnDocument() throws Exception {
        UUID documentId = uploadDocument();

        mockMvc.perform(get("/api/applications/{id}/documents/{documentId}/preview", application.getId(), documentId)
                        .header("Authorization", customerToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.url").value("https://example.com/documents/test-preview.pdf"));
    }

    private UUID uploadDocument() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "policy.pdf",
                MediaType.APPLICATION_PDF_VALUE,
                "dummy-pdf".getBytes());

        String response = mockMvc.perform(multipart("/api/applications/{id}/documents", application.getId())
                        .file(file)
                        .header("Authorization", customerToken))
                .andExpect(status().isOk())
                .andReturn()
                .getResponse()
                .getContentAsString();

        return UUID.fromString(response.replaceAll(".*\"id\":\"([^\"]+)\".*", "$1"));
    }

    private String bearerToken(UUID userId, JwtRole role) {
        return "Bearer " + jwtService.generate(
                userId,
                role.name().toLowerCase() + "@example.com",
                role);
    }
}
package com.insurewise.policy.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.insurewise.common.security.JwtRole;
import com.insurewise.common.security.JwtService;
import com.insurewise.policy.dto.request.PolicyApplicationCreateRequest;
import com.insurewise.policy.dto.request.PolicyApplicationDecisionRequest;
import com.insurewise.policy.entity.ApplicationStatus;
import com.insurewise.policy.entity.Category;
import com.insurewise.policy.entity.CategoryStatus;
import com.insurewise.policy.entity.CoverageType;
import com.insurewise.policy.entity.NomineeRelationship;
import com.insurewise.policy.entity.Policy;
import com.insurewise.policy.entity.PolicyStatus;
import com.insurewise.policy.repository.CategoryRepository;
import com.insurewise.policy.repository.PolicyApplicationRepository;
import com.insurewise.policy.repository.PolicyRepository;
import jakarta.persistence.EntityManager;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@Transactional
@TestPropertySource(properties = {
        "spring.datasource.url=jdbc:h2:mem:policy-application-controller-test;MODE=PostgreSQL;DB_CLOSE_DELAY=-1;DATABASE_TO_UPPER=false",
        "spring.datasource.driver-class-name=org.h2.Driver",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.H2Dialect",
        "spring.flyway.enabled=false"
})
class PolicyApplicationControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private JwtService jwtService;

    @Autowired
    private CategoryRepository categoryRepository;

    @Autowired
    private PolicyRepository policyRepository;

    @Autowired
    private PolicyApplicationRepository policyApplicationRepository;

    @Autowired
    private EntityManager entityManager;

    private String staffToken;
    private String customerToken;
    private UUID customerId;
    private Policy policy;

    @BeforeEach
    void setUp() {
        entityManager.createNativeQuery("CREATE SEQUENCE IF NOT EXISTS application_code_seq START WITH 1000 INCREMENT BY 1")
                .executeUpdate();
        policyApplicationRepository.deleteAll();
        policyRepository.deleteAll();
        categoryRepository.deleteAll();

        Category category = categoryRepository.save(new Category(
                "Health",
                "Health coverage",
                CategoryStatus.ACTIVE));
        policy = policyRepository.save(new Policy(
                "Silver Plan",
                category,
                new BigDecimal("500000.00"),
                new BigDecimal("1200.00"),
                "1 Year",
                PolicyStatus.ACTIVE));
        customerId = UUID.randomUUID();
        customerToken = bearerToken(customerId, JwtRole.CUSTOMER);
        staffToken = bearerToken(UUID.randomUUID(), JwtRole.STAFF);
    }

    @Test
    void approveApplicationPersistsApprovedStatus() throws Exception {
        UUID applicationId = createApplication();

        mockMvc.perform(put("/api/policy-applications/{id}/approve", applicationId)
                        .header("Authorization", staffToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("APPROVED"))
                .andExpect(jsonPath("$.decidedBy").isNotEmpty())
                .andExpect(jsonPath("$.decidedAt").isNotEmpty());
    }

    @Test
    void rejectApplicationPersistsRejectedStatus() throws Exception {
        UUID applicationId = createApplication();

        mockMvc.perform(put("/api/policy-applications/{id}/reject", applicationId)
                        .header("Authorization", staffToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("REJECTED"))
                .andExpect(jsonPath("$.decidedBy").isNotEmpty())
                .andExpect(jsonPath("$.decidedAt").isNotEmpty());
    }

    @Test
    void statusEndpointRejectsInvalidStatus() throws Exception {
        UUID applicationId = createApplication();

        mockMvc.perform(put("/api/policy-applications/{id}/status", applicationId)
                        .header("Authorization", staffToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(
                                new PolicyApplicationDecisionRequest(ApplicationStatus.PENDING))))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("Application status must be APPROVED or REJECTED"));
    }

    @Test
    void approveRequiresStaffAuthorization() throws Exception {
        UUID applicationId = createApplication();

        mockMvc.perform(put("/api/policy-applications/{id}/approve", applicationId)
                        .header("Authorization", customerToken))
                .andExpect(status().isForbidden());
    }

    @Test
    void rejectReturnsNotFoundForMissingId() throws Exception {
        mockMvc.perform(put("/api/policy-applications/{id}/reject", UUID.randomUUID())
                        .header("Authorization", staffToken))
                .andExpect(status().isNotFound());
    }

    @Test
    void statusEndpointRejectsUnsupportedEnumValue() throws Exception {
        UUID applicationId = createApplication();

        mockMvc.perform(put("/api/policy-applications/{id}/status", applicationId)
                        .header("Authorization", staffToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"status\":\"INVALID\"}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("status: must be one of [PENDING, APPROVED, REJECTED]"));
    }

    @Test
    void createApplicationStartsInPendingStatus() throws Exception {
        mockMvc.perform(post("/api/policy-applications")
                        .header("Authorization", customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(validCreateRequest())))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("PENDING"));
    }

    @Test
    void createApplicationRejectsNomineeRelationshipWithoutName() throws Exception {
        mockMvc.perform(post("/api/policy-applications")
                        .header("Authorization", customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "policy_id":"%s",
                                  "coverage_type":"SINGLE",
                                  "date_of_birth":"%s",
                                  "address":"123 Main Street",
                                  "preferred_start_date":"%s",
                                  "nominee_relationship":"SPOUSE"
                                }
                                """.formatted(
                                policy.getId(),
                                LocalDate.now().minusYears(30),
                                LocalDate.now().plusDays(10))))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("validNomineePair: nomineeRelationship and nomineeName must either both be provided or both be omitted"));
    }

    @Test
    void createApplicationRejectsNomineeNameWithoutRelationship() throws Exception {
        mockMvc.perform(post("/api/policy-applications")
                        .header("Authorization", customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "policy_id":"%s",
                                  "coverage_type":"SINGLE",
                                  "date_of_birth":"%s",
                                  "address":"123 Main Street",
                                  "preferred_start_date":"%s",
                                  "nominee_name":"Nominee Name"
                                }
                                """.formatted(
                                policy.getId(),
                                LocalDate.now().minusYears(30),
                                LocalDate.now().plusDays(10))))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value("validNomineePair: nomineeRelationship and nomineeName must either both be provided or both be omitted"));
    }

    private UUID createApplication() throws Exception {
        String response = mockMvc.perform(post("/api/policy-applications")
                        .header("Authorization", customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(validCreateRequest())))
                .andExpect(status().isOk())
                .andReturn()
                .getResponse()
                .getContentAsString();

        return UUID.fromString(objectMapper.readTree(response).path("id").asText());
    }

    private String bearerToken(UUID userId, JwtRole role) {
        return "Bearer " + jwtService.generate(
                userId,
                role.name().toLowerCase() + "@example.com",
                role);
    }

    private PolicyApplicationCreateRequest validCreateRequest() {
        return new PolicyApplicationCreateRequest(
                policy.getId(),
                CoverageType.SINGLE,
                LocalDate.now().minusYears(30),
                "123 Main Street",
                LocalDate.now().plusDays(10),
                "Nominee Name",
                NomineeRelationship.SPOUSE);
    }
}
package com.insurewise.policy.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.insurewise.common.security.JwtRole;
import com.insurewise.common.security.JwtService;
import com.insurewise.policy.dto.request.PolicyCreateRequest;
import com.insurewise.policy.dto.request.PolicyUpdateRequest;
import com.insurewise.policy.entity.CategoryStatus;
import com.insurewise.policy.entity.PolicyStatus;
import com.insurewise.policy.repository.CategoryRepository;
import com.insurewise.policy.repository.PolicyRepository;
import java.math.BigDecimal;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@TestPropertySource(properties = {
        "spring.datasource.url=jdbc:h2:mem:policy-controller-test;MODE=PostgreSQL;DB_CLOSE_DELAY=-1;DATABASE_TO_UPPER=false",
        "spring.datasource.driver-class-name=org.h2.Driver",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "spring.flyway.enabled=false"
})
class PolicyControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private JwtService jwtService;

    @Autowired
    private CategoryRepository categoryRepository;

    @Autowired
    private PolicyRepository policyRepository;

    private String staffToken;
    private String customerToken;
    private UUID categoryId;

    @BeforeEach
    void setUp() {
        policyRepository.deleteAll();
        categoryRepository.deleteAll();

        var category = categoryRepository.save(
                new com.insurewise.policy.entity.Category(
                        "Health",
                        "Health coverage",
                        CategoryStatus.ACTIVE));
        categoryId = category.getId();
        staffToken = bearerToken(JwtRole.STAFF);
        customerToken = bearerToken(JwtRole.CUSTOMER);
    }

    @Test
    void createPolicyReturnsCreated() throws Exception {
        PolicyCreateRequest request = new PolicyCreateRequest(
                "Silver Plan",
                categoryId,
                new BigDecimal("500000.00"),
                new BigDecimal("1200.00"),
                "1 Year",
                PolicyStatus.ACTIVE);

        mockMvc.perform(post("/api/policies")
                        .header("Authorization", staffToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("Silver Plan"))
                .andExpect(jsonPath("$.categoryId").value(categoryId.toString()))
                .andExpect(jsonPath("$.status").value("ACTIVE"));

        assertThat(policyRepository.findAll()).hasSize(1);
    }

    @Test
    void updatePolicyReturnsUpdatedPolicy() throws Exception {
        var category = categoryRepository.findById(categoryId).orElseThrow();
        var policy = policyRepository.save(new com.insurewise.policy.entity.Policy(
                "Silver Plan",
                category,
                new BigDecimal("500000.00"),
                new BigDecimal("1200.00"),
                "1 Year",
                PolicyStatus.ACTIVE));

        PolicyUpdateRequest request = new PolicyUpdateRequest(
                "Gold Plan",
                categoryId,
                new BigDecimal("750000.00"),
                new BigDecimal("1600.00"),
                "2 Years",
                PolicyStatus.INACTIVE);

        mockMvc.perform(put("/api/policies/{id}", policy.getId())
                        .header("Authorization", staffToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Gold Plan"))
                .andExpect(jsonPath("$.status").value("INACTIVE"));
    }

    @Test
    void deletePolicyReturnsNoContent() throws Exception {
        var category = categoryRepository.findById(categoryId).orElseThrow();
        var policy = policyRepository.save(new com.insurewise.policy.entity.Policy(
                "Silver Plan",
                category,
                new BigDecimal("500000.00"),
                new BigDecimal("1200.00"),
                "1 Year",
                PolicyStatus.ACTIVE));

        mockMvc.perform(delete("/api/policies/{id}", policy.getId())
                        .header("Authorization", staffToken))
                .andExpect(status().isNoContent());

        assertThat(policyRepository.findById(policy.getId())).isEmpty();
    }

    @Test
    void createPolicyRejectsInvalidRequest() throws Exception {
        PolicyCreateRequest request = new PolicyCreateRequest(
                "",
                null,
                new BigDecimal("0.00"),
                new BigDecimal("0.00"),
                "",
                null);

        mockMvc.perform(post("/api/policies")
                        .header("Authorization", staffToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest());
    }

    @Test
    void staffEndpointsRequireAuthorization() throws Exception {
        PolicyCreateRequest request = new PolicyCreateRequest(
                "Silver Plan",
                categoryId,
                new BigDecimal("500000.00"),
                new BigDecimal("1200.00"),
                "1 Year",
                PolicyStatus.ACTIVE);

        mockMvc.perform(post("/api/policies")
                        .header("Authorization", customerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isForbidden());
    }

    @Test
    void updatePolicyReturnsNotFoundForMissingId() throws Exception {
        PolicyUpdateRequest request = new PolicyUpdateRequest(
                "Gold Plan",
                categoryId,
                new BigDecimal("750000.00"),
                new BigDecimal("1600.00"),
                "2 Years",
                PolicyStatus.ACTIVE);

        mockMvc.perform(put("/api/policies/{id}", UUID.randomUUID())
                        .header("Authorization", staffToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isNotFound());
    }

    private String bearerToken(JwtRole role) {
        return "Bearer " + jwtService.generate(
                UUID.randomUUID(),
                role.name().toLowerCase() + "@example.com",
                role);
    }
}
package com.insurewise.policy.service;

import com.insurewise.common.dto.PresignedUrlResponse;
import com.insurewise.common.exception.FileStorageException;
import com.insurewise.common.exception.InvalidFileException;
import com.insurewise.common.security.JwtPrincipal;
import com.insurewise.common.security.JwtRole;
import com.insurewise.common.service.S3StorageService;
import com.insurewise.policy.entity.CoverageType;
import com.insurewise.policy.entity.NomineeRelationship;
import com.insurewise.policy.entity.Policy;
import com.insurewise.policy.entity.PolicyApplication;
import com.insurewise.policy.entity.Category;
import com.insurewise.policy.entity.CategoryStatus;
import com.insurewise.policy.entity.PolicyStatus;
import com.insurewise.policy.exception.ApplicationNotFoundException;
import com.insurewise.policy.repository.ApplicationDocumentRepository;
import java.math.BigDecimal;
import java.lang.reflect.Field;
import java.time.LocalDate;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ApplicationDocumentServiceTest {

    @Mock
    private ApplicationDocumentRepository documentRepository;

    @Mock
    private PolicyApplicationService applicationService;

    @Mock
    private S3StorageService storageService;

    @InjectMocks
    private ApplicationDocumentService service;

    private JwtPrincipal customerPrincipal;
    private PolicyApplication application;

    @BeforeEach
    void setUp() {
        UUID customerId = UUID.randomUUID();
        customerPrincipal = new JwtPrincipal(customerId, JwtRole.CUSTOMER, "customer@example.com");
        UUID applicationId = UUID.randomUUID();

        Category category = new Category("Health", "Health coverage", CategoryStatus.ACTIVE);
        Policy policy = new Policy(
                "Silver Plan",
                category,
                new BigDecimal("500000.00"),
                new BigDecimal("1200.00"),
                "1 Year",
                PolicyStatus.ACTIVE);

        application = new PolicyApplication(
                "APP-2000",
                customerId,
                policy,
                CoverageType.SINGLE,
                LocalDate.now().minusYears(30),
                "123 Main Street",
                LocalDate.now().plusDays(10),
                "Nominee Name",
                NomineeRelationship.SPOUSE);
        setField(application, "id", applicationId);
    }

    @Test
    void uploadPersistsMetadataAfterS3UploadSucceeds() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "policy.pdf",
                MediaType.APPLICATION_PDF_VALUE,
                "dummy-pdf".getBytes());

        when(applicationService.getApplicationEntityForInternalUse(application.getId())).thenReturn(application);
        when(documentRepository.saveAndFlush(any()))
                .thenAnswer(invocation -> invocation.getArgument(0));

        var saved = service.uploadApplicationDocument(customerPrincipal, application.getId(), file);

        ArgumentCaptor<String> keyCaptor = ArgumentCaptor.forClass(String.class);
        verify(storageService).upload(eq(file), eq("application-documents"), eq(customerPrincipal.userId()), keyCaptor.capture());
        String key = keyCaptor.getValue();
        assertThat(key).contains(application.getId().toString());
        assertThat(key).endsWith(".pdf");
        assertThat(saved.objectKey()).isEqualTo(key);
        assertThat(saved.fileName()).isEqualTo("policy.pdf");
        assertThat(saved.fileSize()).isEqualTo(9);
    }

    @Test
    void uploadDeletesS3ObjectWhenDatabasePersistenceFails() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "policy.pdf",
                MediaType.APPLICATION_PDF_VALUE,
                "dummy-pdf".getBytes());

        when(applicationService.getApplicationEntityForInternalUse(application.getId())).thenReturn(application);
        when(documentRepository.saveAndFlush(any()))
                .thenThrow(new IllegalStateException("db failure"));

        assertThatThrownBy(() -> service.uploadApplicationDocument(customerPrincipal, application.getId(), file))
                .isInstanceOf(IllegalStateException.class)
                .hasMessage("db failure");

        ArgumentCaptor<String> keyCaptor = ArgumentCaptor.forClass(String.class);
        verify(storageService).upload(eq(file), eq("application-documents"), eq(customerPrincipal.userId()), keyCaptor.capture());
        verify(storageService).delete(keyCaptor.getValue());
    }

    @Test
    void uploadRejectsMissingBucketFailureFromStorage() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "policy.pdf",
                MediaType.APPLICATION_PDF_VALUE,
                "dummy-pdf".getBytes());

        when(applicationService.getApplicationEntityForInternalUse(application.getId())).thenReturn(application);
        doThrow(new FileStorageException("Unable to store the file."))
                .when(storageService)
                .upload(eq(file), eq("application-documents"), eq(customerPrincipal.userId()), any());

        assertThatThrownBy(() -> service.uploadApplicationDocument(customerPrincipal, application.getId(), file))
                .isInstanceOf(FileStorageException.class);

        verify(documentRepository, never()).saveAndFlush(any());
    }

    @Test
    void uploadRejectsInvalidFile() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "policy.txt",
                MediaType.TEXT_PLAIN_VALUE,
                "dummy".getBytes());

        when(applicationService.getApplicationEntityForInternalUse(application.getId())).thenReturn(application);

        assertThatThrownBy(() -> service.uploadApplicationDocument(customerPrincipal, application.getId(), file))
                .isInstanceOf(InvalidFileException.class)
                .hasMessage("Document must be a .pdf file");
    }

    @Test
    void uploadRejectsOversizedFile() {
        byte[] oversized = new byte[(int) (10L * 1024 * 1024 + 1)];
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "policy.pdf",
                MediaType.APPLICATION_PDF_VALUE,
                oversized);

        when(applicationService.getApplicationEntityForInternalUse(application.getId())).thenReturn(application);

        assertThatThrownBy(() -> service.uploadApplicationDocument(customerPrincipal, application.getId(), file))
                .isInstanceOf(InvalidFileException.class)
                .hasMessage("Document size cannot exceed 10MB");
    }

    @Test
    void uploadRejectsMissingApplication() {
        MockMultipartFile file = new MockMultipartFile(
                "file",
                "policy.pdf",
                MediaType.APPLICATION_PDF_VALUE,
                "dummy-pdf".getBytes());

        when(applicationService.getApplicationEntityForInternalUse(application.getId()))
                .thenThrow(new ApplicationNotFoundException(application.getId()));

        assertThatThrownBy(() -> service.uploadApplicationDocument(customerPrincipal, application.getId(), file))
                .isInstanceOf(ApplicationNotFoundException.class);
    }

    private void setField(Object target, String fieldName, Object value) {
        try {
            Field field = target.getClass().getDeclaredField(fieldName);
            field.setAccessible(true);
            field.set(target, value);
        } catch (ReflectiveOperationException exception) {
            throw new IllegalStateException(exception);
        }
    }
}
package com.insurewise.policy.service;

import com.insurewise.policy.dto.request.PolicyApplicationCreateRequest;
import com.insurewise.policy.entity.ApplicationStatus;
import com.insurewise.policy.entity.Category;
import com.insurewise.policy.entity.CategoryStatus;
import com.insurewise.policy.entity.CoverageType;
import com.insurewise.policy.entity.NomineeRelationship;
import com.insurewise.policy.entity.Policy;
import com.insurewise.policy.entity.PolicyStatus;
import com.insurewise.policy.exception.ApplicationStateException;
import com.insurewise.policy.repository.CategoryRepository;
import com.insurewise.policy.repository.PolicyApplicationRepository;
import com.insurewise.policy.repository.PolicyRepository;
import jakarta.persistence.EntityManager;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.transaction.annotation.Transactional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

@SpringBootTest
@Transactional
@TestPropertySource(properties = {
        "spring.datasource.url=jdbc:h2:mem:policy-application-service-test;MODE=PostgreSQL;DB_CLOSE_DELAY=-1;DATABASE_TO_UPPER=false",
        "spring.datasource.driver-class-name=org.h2.Driver",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.H2Dialect",
        "spring.flyway.enabled=false"
})
class PolicyApplicationServiceTest {

    @Autowired
    private PolicyApplicationService service;

    @Autowired
    private PolicyApplicationRepository applicationRepository;

    @Autowired
    private PolicyRepository policyRepository;

    @Autowired
    private CategoryRepository categoryRepository;

    @Autowired
    private EntityManager entityManager;

    private Policy policy;

    @BeforeEach
    void setUp() {
        entityManager.createNativeQuery("CREATE SEQUENCE IF NOT EXISTS application_code_seq START WITH 1000 INCREMENT BY 1")
                .executeUpdate();
        applicationRepository.deleteAll();
        policyRepository.deleteAll();
        categoryRepository.deleteAll();

        Category category = categoryRepository.save(new Category(
                "Health",
                "Health coverage",
                CategoryStatus.ACTIVE));
        policy = policyRepository.save(new Policy(
                "Silver Plan",
                category,
                new BigDecimal("500000.00"),
                new BigDecimal("1200.00"),
                "1 Year",
                PolicyStatus.ACTIVE));
    }

    @Test
    void createApplicationGeneratesSequentialApplicationCodes() {
        UUID firstCustomer = UUID.randomUUID();
        UUID secondCustomer = UUID.randomUUID();

        String firstCode = service.createApplication(firstCustomer, validRequest()).applicationCode();
        String secondCode = service.createApplication(secondCustomer, validRequest()).applicationCode();

        assertEquals("APP-1000", firstCode);
        assertEquals("APP-1001", secondCode);
    }

    @Test
    void createApplicationRejectsBlankNomineeNameWhenRelationshipProvided() {
        PolicyApplicationCreateRequest request = new PolicyApplicationCreateRequest(
                policy.getId(),
                CoverageType.SINGLE,
                LocalDate.now().minusYears(30),
                "123 Main Street",
                LocalDate.now().plusDays(10),
                "   ",
                NomineeRelationship.SPOUSE);

        ApplicationStateException exception = assertThrows(
                ApplicationStateException.class,
                () -> service.createApplication(UUID.randomUUID(), request));

        assertEquals("nomineeName is required when nomineeRelationship is provided", exception.getMessage());
    }

    @Test
    void createApplicationStoresPendingStatus() {
        ApplicationStatus status = service.createApplication(UUID.randomUUID(), validRequest()).status();
        assertEquals(ApplicationStatus.PENDING, status);
    }

    private PolicyApplicationCreateRequest validRequest() {
        return new PolicyApplicationCreateRequest(
                policy.getId(),
                CoverageType.SINGLE,
                LocalDate.now().minusYears(30),
                "123 Main Street",
                LocalDate.now().plusDays(10),
                "Nominee Name",
                NomineeRelationship.SPOUSE);
    }
}
