# InsureWise BRD to Package & Class Mapping

## Overview
This document maps Business Requirements (BRs) to the actual Java packages and classes in the codebase.
**Format**: Each BR shows all files/classes that a developer needs to work on if allocated that requirement.

---

## QUICK BR-TO-FILES ALLOCATION MAP

### BR01: Customer Self-Registration
**Files**:
- `auth/controller/AuthController.java`
- `auth/service/AuthService.java`
- `auth/repository/CustomerRepository.java`
- `auth/entity/Customer.java`
- `auth/dto/request/CustomerRegistrationRequest.java`
- `auth/dto/response/AuthResponse.java`
- `auth/exception/DuplicateEmailException.java`
- `common/security/JwtService.java`
- `common/security/SecurityConfig.java`
- `db/migration/V1__auth_initial_schema.sql`

---

### BR02: Customer Login & Logout
**Files**:
- `auth/controller/AuthController.java`
- `auth/service/AuthService.java`
- `auth/repository/CustomerRepository.java`
- `auth/entity/Customer.java`
- `auth/dto/request/CustomerLoginRequest.java`
- `auth/dto/response/AuthResponse.java`
- `auth/exception/InvalidCredentialsException.java`
- `common/security/JwtService.java`
- `common/security/JwtAuthenticationFilter.java`
- `common/security/SecurityConfig.java`
- `db/migration/V1__auth_initial_schema.sql`

---

### BR03: Staff Login & Worker Authentication
**Files**:
- `auth/controller/AuthController.java` (or dedicated StaffLoginController)
- `auth/service/AuthService.java`
- `auth/repository/StaffUserRepository.java`
- `auth/entity/StaffUser.java`
- `auth/dto/request/StaffLoginRequest.java`
- `auth/dto/response/AuthResponse.java`
- `auth/exception/InvalidCredentialsException.java`
- `common/security/JwtService.java`
- `common/security/JwtAuthenticationFilter.java`
- `common/security/SecurityConfig.java`
- `common/security/JwtRole.java`
- `db/migration/V1__auth_initial_schema.sql`
- `db/migration/V10__auth_seed_local_staff_user.sql`

---

### BR04: Customer Profile & Profile Pictures (S3-backed)
**Files**:
- `auth/controller/AuthController.java`
- `auth/service/AuthService.java`
- `auth/entity/Customer.java`
- `auth/repository/CustomerRepository.java`
- `auth/dto/response/CustomerProfileResponse.java`
- `common/service/S3StorageService.java`
- `common/dto/PresignedUrlResponse.java`
- `db/migration/V9__auth_add_profile_pictures.sql`
- `db/migration/V11__auth_profile_pictures_use_s3_keys.sql`

---

### BR05: Staff Profile Management
**Files**:
- `auth/controller/StaffUserManagementController.java`
- `auth/service/StaffUserService.java`
- `auth/entity/StaffUser.java`
- `auth/repository/StaffUserRepository.java`
- `auth/dto/response/StaffProfileResponse.java`
- `auth/dto/request/StaffCreateRequest.java`
- `auth/dto/request/StaffUpdateRequest.java`
- `common/service/S3StorageService.java`
- `db/migration/V1__auth_initial_schema.sql`
- `db/migration/V9__auth_add_profile_pictures.sql`
- `db/migration/V11__auth_profile_pictures_use_s3_keys.sql`

---

### BR06: Browse Active Insurance Policies
**Files**:
- `policy/controller/PolicyController.java`
- `policy/service/PolicyService.java`
- `policy/repository/PolicyRepository.java`
- `policy/entity/Policy.java`
- `policy/entity/PolicyStatus.java`
- `policy/entity/Category.java`
- `policy/entity/CategoryStatus.java`
- `policy/dto/response/PolicyResponse.java`
- `policy/dto/response/CategoryResponse.java`
- `common/dto/PageResponse.java`
- `common/dto/PaginationMetadata.java`
- `db/migration/V2__policy_initial_schema.sql`

---

### BR07: View Policy Details Before Applying
**Files**:
- `policy/controller/PolicyController.java`
- `policy/service/PolicyService.java`
- `policy/repository/PolicyRepository.java`
- `policy/entity/Policy.java`
- `policy/entity/Category.java`
- `policy/entity/CoverageType.java`
- `policy/dto/response/PolicyResponse.java`
- `db/migration/V2__policy_initial_schema.sql`

---

### BR08: Create Policy Application (PENDING Status)
**Files**:
- `policy/controller/PolicyApplicationController.java`
- `policy/service/PolicyApplicationService.java`
- `policy/repository/PolicyApplicationRepository.java`
- `policy/entity/PolicyApplication.java`
- `policy/entity/ApplicationStatus.java`
- `policy/entity/Dependent.java`
- `policy/entity/Gender.java`
- `policy/entity/NomineeRelationship.java`
- `policy/dto/request/PolicyApplicationCreateRequest.java`
- `policy/dto/request/DependentRequest.java`
- `policy/dto/response/PolicyApplicationResponse.java`
- `policy/dto/response/DependentResponse.java`
- `policy/exception/DuplicatePendingApplicationException.java`
- `db/migration/V2__policy_initial_schema.sql`

---

### BR09: Upload Application Supporting Documents (S3-backed)
**Files**:
- `policy/controller/ApplicationDocumentController.java`
- `policy/service/ApplicationDocumentService.java`
- `policy/repository/ApplicationDocumentRepository.java`
- `policy/entity/ApplicationDocument.java`
- `policy/dto/response/ApplicationDocumentResponse.java`
- `common/service/S3StorageService.java`
- `common/dto/PresignedUrlResponse.java`
- `db/migration/V3__policy_create_application_documents.sql`

---

### BR10: View My Policies & Actions (Make Payment, File Claim)
**Files**:
- `policy/controller/PolicyApplicationController.java`
- `policy/service/PolicyApplicationService.java`
- `policy/repository/PolicyApplicationRepository.java`
- `policy/entity/PolicyApplication.java`
- `policy/entity/ApplicationStatus.java`
- `policy/dto/response/PolicyApplicationResponse.java`
- `payments/controller/PaymentController.java`
- `claims/controller/ClaimController.java`
- `common/security/JwtPrincipal.java`

---

### BR11: File Claim with Details (Incident Type, Date, Amount, Description)
**Files**:
- `claims/controller/ClaimController.java`
- `claims/service/ClaimService.java`
- `claims/repository/ClaimRepository.java`
- `claims/entity/Claim.java`
- `claims/entity/ClaimStatus.java`
- `claims/entity/IncidentType.java`
- `claims/dto/request/ClaimCreateRequest.java`
- `claims/dto/response/ClaimResponse.java`
- `claims/client/PolicyApplicationLookupClient.java`
- `claims/client/PolicyApplicationSnapshot.java`
- `db/migration/V4__claims_initial_schema.sql`

---

### BR12: Manage Claim Dependents
**Files**:
- `claims/controller/ClaimDependentController.java`
- `claims/service/ClaimDependentService.java`
- `claims/repository/ClaimDependentRepository.java`
- `claims/entity/ClaimDependent.java`
- `claims/dto/request/ClaimDependentRequest.java`
- `claims/dto/response/ClaimDependentResponse.java`
- `db/migration/V5__claims_add_claim_dependents.sql`

---

### BR13: Upload Claim Supporting Documents (S3-backed)
**Files**:
- `claims/controller/ClaimDocumentController.java`
- `claims/service/ClaimDocumentService.java`
- `claims/repository/ClaimDocumentRepository.java`
- `claims/entity/ClaimDocument.java`
- `claims/dto/response/ClaimDocumentResponse.java`
- `common/service/S3StorageService.java`
- `common/dto/PresignedUrlResponse.java`
- `db/migration/V6__claims_create_claim_documents.sql`

---

### BR14: Make Simulated Payments (Credit Card, Debit Card, UPI, Net Banking)
**Files**:
- `payments/controller/PaymentController.java`
- `payments/service/PaymentService.java`
- `payments/repository/PaymentRepository.java`
- `payments/entity/Payment.java`
- `payments/entity/PaymentStatus.java`
- `payments/entity/PaymentMethod.java`
- `payments/dto/request/PaymentCreateRequest.java`
- `payments/dto/response/PaymentResponse.java`
- `payments/client/PaymentPolicyApplicationLookupClient.java`
- `payments/client/PaymentPolicyApplicationSnapshot.java`
- `db/migration/V7__payments_initial_schema.sql`

---

### BR15: Payment Documents & Receipts (S3-backed)
**Files**:
- `payments/controller/PaymentDocumentController.java`
- `payments/service/PaymentDocumentService.java`
- `payments/repository/PaymentDocumentRepository.java`
- `payments/entity/PaymentDocument.java`
- `payments/dto/response/PaymentDocumentResponse.java`
- `common/service/S3StorageService.java`
- `common/dto/PresignedUrlResponse.java`
- `db/migration/V8__payments_create_payment_documents.sql`

---

### BR16: View Payment History
**Files**:
- `payments/controller/PaymentController.java`
- `payments/service/PaymentService.java`
- `payments/repository/PaymentRepository.java`
- `payments/entity/Payment.java`
- `payments/entity/PaymentStatus.java`
- `payments/dto/response/PaymentResponse.java`
- `common/dto/PageResponse.java`
- `common/dto/PaginationMetadata.java`
- `db/migration/V7__payments_initial_schema.sql`

---

### BR17: Staff Dashboard - Metrics & Reporting
**Files**:
- `policy/controller/DashboardController.java`
- `policy/service/DashboardService.java`
- `policy/repository/PolicyApplicationRepository.java`
- `policy/repository/PolicyRepository.java`
- `policy/repository/CategoryRepository.java`
- `claims/repository/ClaimRepository.java`
- `payments/repository/PaymentRepository.java`
- `auth/repository/CustomerRepository.java`
- `auth/repository/StaffUserRepository.java`
- `policy/dto/response/DashboardMetricsResponse.java`
- `common/security/JwtPrincipal.java`

---

### BR18: Staff - Create & Manage Categories (DRAFT, ACTIVE, INACTIVE)
**Files**:
- `policy/controller/CategoryController.java`
- `policy/service/CategoryService.java`
- `policy/repository/CategoryRepository.java`
- `policy/entity/Category.java`
- `policy/entity/CategoryStatus.java`
- `policy/dto/request/CategoryCreateRequest.java`
- `policy/dto/request/CategoryUpdateRequest.java`
- `policy/dto/response/CategoryResponse.java`
- `db/migration/V2__policy_initial_schema.sql`

---

### BR19: Staff - Create & Manage Policies with Status Control
**Files**:
- `policy/controller/PolicyController.java`
- `policy/service/PolicyService.java`
- `policy/repository/PolicyRepository.java`
- `policy/entity/Policy.java`
- `policy/entity/PolicyStatus.java`
- `policy/entity/Category.java`
- `policy/dto/request/PolicyCreateRequest.java`
- `policy/dto/request/PolicyUpdateRequest.java`
- `policy/dto/response/PolicyResponse.java`
- `db/migration/V2__policy_initial_schema.sql`

---

### BR20: Staff - Approve/Reject Policy Applications with Conflict Protection
**Files**:
- `policy/controller/PolicyApplicationController.java`
- `policy/service/PolicyApplicationService.java`
- `policy/repository/PolicyApplicationRepository.java`
- `policy/entity/PolicyApplication.java`
- `policy/entity/ApplicationStatus.java`
- `policy/dto/request/PolicyApplicationCreateRequest.java`
- `policy/dto/response/PolicyApplicationResponse.java`
- `policy/dto/response/ApplicationDecisionResponse.java`
- `policy/exception/ApplicationStateException.java`
- `policy/exception/DuplicatePendingApplicationException.java`
- `db/migration/V2__policy_initial_schema.sql`

---

### BR21: Staff - Approve/Reject Claims
**Files**:
- `claims/controller/ClaimController.java`
- `claims/service/ClaimService.java`
- `claims/repository/ClaimRepository.java`
- `claims/entity/Claim.java`
- `claims/entity/ClaimStatus.java`
- `claims/dto/response/ClaimResponse.java`
- `db/migration/V4__claims_initial_schema.sql`

---

### BR22: JWT Authentication & Token Management
**Files**:
- `common/security/JwtService.java`
- `common/security/JwtAuthenticationFilter.java`
- `common/security/JwtPrincipal.java`
- `common/security/JwtRole.java`
- `common/security/SecurityConfig.java`
- `common/security/SecurityProperties.java`
- `auth/service/AuthService.java`

---

### BR23: BCrypt Password Storage & Hashing
**Files**:
- `auth/service/AuthService.java`
- `auth/entity/Customer.java`
- `auth/entity/StaffUser.java`
- `common/security/SecurityConfig.java`

---

### BR24: Pagination Support
**Files**:
- `common/dto/PageResponse.java`
- `common/dto/PaginationMetadata.java`
- `policy/service/PolicyService.java`
- `policy/service/PolicyApplicationService.java`
- `claims/service/ClaimService.java`
- `payments/service/PaymentService.java`

---

### BR25: Standard Error Responses
**Files**:
- `common/dto/ApiErrorResponse.java`
- `common/exception/GlobalExceptionHandler.java`
- `auth/exception/DuplicateEmailException.java`
- `auth/exception/InvalidCredentialsException.java`
- `policy/exception/ApplicationNotFoundException.java`
- `policy/exception/ApplicationStateException.java`
- `policy/exception/DuplicatePendingApplicationException.java`

---

### BR26: S3 Document Storage & Retrieval
**Files**:
- `common/service/S3StorageService.java`
- `common/service/DisabledS3StorageService.java`
- `common/dto/PresignedUrlResponse.java`
- `policy/service/ApplicationDocumentService.java`
- `claims/service/ClaimDocumentService.java`
- `payments/service/PaymentDocumentService.java`

---

### BR27: Idempotency Keys (Claims & Payments)
**Files**:
- `claims/entity/Claim.java`
- `claims/service/ClaimService.java`
- `payments/entity/Payment.java`
- `payments/service/PaymentService.java`
- `db/migration/V4__claims_initial_schema.sql`
- `db/migration/V7__payments_initial_schema.sql`

---

### BR28: Role-Based Access Control (CUSTOMER vs STAFF)
**Files**:
- `common/security/JwtRole.java`
- `common/security/SecurityConfig.java`
- `common/security/JwtPrincipal.java`
- `auth/controller/AuthController.java`
- `auth/controller/StaffUserManagementController.java`
- `policy/controller/PolicyApplicationController.java`
- `policy/controller/CategoryController.java`
- `policy/controller/DashboardController.java`

---

### BR29: Unique Pending Application Constraint
**Files**:
- `policy/entity/PolicyApplication.java`
- `policy/repository/PolicyApplicationRepository.java`
- `policy/service/PolicyApplicationService.java`
- `policy/exception/DuplicatePendingApplicationException.java`
- `db/migration/V2__policy_initial_schema.sql`

---

### BR30: Database Migrations & Schema Management
**Files**:
- `db/migration/V1__auth_initial_schema.sql`
- `db/migration/V2__policy_initial_schema.sql`
- `db/migration/V3__policy_create_application_documents.sql`
- `db/migration/V4__claims_initial_schema.sql`
- `db/migration/V5__claims_add_claim_dependents.sql`
- `db/migration/V6__claims_create_claim_documents.sql`
- `db/migration/V7__payments_initial_schema.sql`
- `db/migration/V8__payments_create_payment_documents.sql`
- `db/migration/V9__auth_add_profile_pictures.sql`
- `db/migration/V10__auth_seed_local_staff_user.sql`
- `db/migration/V11__auth_profile_pictures_use_s3_keys.sql`

---

---

## BR ALLOCATION SUMMARY TABLE

| BR Code | Requirement | Package(s) | # of Files | Complexity |
|---------|-------------|-----------|-----------|-----------|
| BR01 | Customer Self-Registration | auth, common | 10 | Medium |
| BR02 | Customer Login & Logout | auth, common | 11 | Medium |
| BR03 | Staff Login | auth, common | 12 | Medium |
| BR04 | Customer Profile & Pictures (S3) | auth, common | 9 | Medium |
| BR05 | Staff Profile Management | auth, common | 9 | Medium |
| BR06 | Browse Active Policies | policy, common | 12 | Low |
| BR07 | View Policy Details | policy | 8 | Low |
| BR08 | Create Policy Application | policy | 14 | High |
| BR09 | Upload Application Documents | policy, common | 8 | Medium |
| BR10 | View My Policies & Actions | policy, payments, claims | 8 | Medium |
| BR11 | File Claim | claims, policy | 10 | High |
| BR12 | Manage Claim Dependents | claims | 6 | Low |
| BR13 | Upload Claim Documents | claims, common | 8 | Medium |
| BR14 | Make Simulated Payments | payments, policy | 10 | High |
| BR15 | Payment Documents & Receipts | payments, common | 8 | Medium |
| BR16 | View Payment History | payments, common | 7 | Low |
| BR17 | Staff Dashboard & Metrics | policy, claims, payments, auth | 10 | High |
| BR18 | Manage Categories | policy | 9 | Medium |
| BR19 | Manage Policies | policy | 9 | Medium |
| BR20 | Approve/Reject Applications | policy | 10 | High |
| BR21 | Approve/Reject Claims | claims | 6 | Medium |
| BR22 | JWT Authentication | common, auth | 6 | Medium |
| BR23 | BCrypt Password Storage | auth, common | 4 | Low |
| BR24 | Pagination Support | common, policy, claims, payments | 5 | Low |
| BR25 | Standard Error Responses | common, auth, policy | 7 | Low |
| BR26 | S3 Document Storage | common, policy, claims, payments | 6 | Medium |
| BR27 | Idempotency Keys | claims, payments | 4 | Low |
| BR28 | Role-Based Access Control | common, auth, policy | 8 | Medium |
| BR29 | Unique Pending Application | policy | 4 | Low |
| BR30 | Database Migrations | migrations | 11 | Low |

---

## DEVELOPER ALLOCATION TEMPLATE

```
Developer 1:
  - BR01: Customer Self-Registration
  - BR02: Customer Login & Logout
  - BR22: JWT Authentication

Developer 2:
  - BR03: Staff Login
  - BR04: Customer Profile (S3)
  - BR23: BCrypt Password Storage

Developer 3:
  - BR06: Browse Policies
  - BR07: View Policy Details
  - BR18: Manage Categories

Developer 4:
  - BR08: Create Policy Application
  - BR09: Upload Application Documents
  - BR29: Unique Pending Application

Developer 5:
  - BR11: File Claim
  - BR12: Manage Claim Dependents
  - BR13: Upload Claim Documents

Developer 6:
  - BR14: Make Payments
  - BR15: Payment Documents & Receipts
  - BR16: View Payment History

Developer 7:
  - BR20: Approve/Reject Applications
  - BR21: Approve/Reject Claims
  - BR17: Staff Dashboard

Developer 8:
  - BR24: Pagination Support
  - BR25: Standard Error Responses
  - BR26: S3 Document Storage
  - BR27: Idempotency Keys
  - BR28: Role-Based Access
  - BR30: Database Migrations
```

---

## DETAILED REQUIREMENT BREAKDOWN

## 1. AUTH & USER DOMAIN
**BRD Area**: V1__auth_initial_schema.sql, V9__auth_add_profile_pictures.sql, V10__auth_seed_local_staff_user.sql, V11__auth_profile_pictures_use_s3_keys.sql

**BRD Requirements**:
- Customer self-registration, login, sign-out, and role-aware navigation
- Staff login through a separate worker login flow
- Profile pictures for customer and staff users using S3 keys
- Initial System Admin seeded through Auth migration

**Package**: `com.insurewise.auth`

### Entities
- **Customer.java** - Represents customer user accounts with profile pictures
- **StaffUser.java** - Represents staff/worker user accounts with profile pictures

### Controllers
- **AuthController.java** - Handles customer registration and login
- **StaffUserManagementController.java** - Handles staff login and management

### Services
- **AuthService.java** - Core authentication logic for customers (registration, login)
- **StaffUserService.java** - Staff user management and authentication

### Repositories
- **CustomerRepository.java** - Data access for customer accounts
- **StaffUserRepository.java** - Data access for staff accounts

### DTOs (Request/Response)
- **CustomerRegistrationRequest.java** - Input model for customer signup
- **CustomerLoginRequest.java** - Input model for customer login
- **StaffLoginRequest.java** - Input model for staff login
- **StaffCreateRequest.java** - Input model for creating staff accounts
- **StaffUpdateRequest.java** - Input model for updating staff accounts
- **AuthResponse.java** - Response with JWT token after successful auth
- **CustomerProfileResponse.java** - Customer profile information response
- **StaffProfileResponse.java** - Staff profile information response

### Security/Configuration
- **AuthBeansConfig.java** - Spring configuration for auth beans
- **SecurityConfig.java** - JWT security configuration (in common package)
- **JwtService.java** - JWT token generation and validation (in common package)

### Exceptions
- **DuplicateEmailException.java** - Thrown when email already exists
- **InvalidCredentialsException.java** - Thrown when login credentials are invalid

---

## 2. POLICY DOMAIN
**BRD Area**: V2__policy_initial_schema.sql, V3__policy_create_application_documents.sql

**BRD Requirements**:
- Customer browsing of active insurance policies and policy detail review
- Policy application creation with PENDING status, coverage type, date of birth, address, preferred start date, nominee details, optional dependents
- Application supporting document persistence (S3-backed)
- Staff category and policy catalog management (validation, status control, deletion guards)
- Staff application approval/rejection workflows with conflict protection
- Pending-application uniqueness constraint
- Staff dashboard metrics for users, categories, policy counts, claim counts, payment count, and revenue

**Package**: `com.insurewise.policy`

### Core Entities
- **Policy.java** - Insurance policies (products)
- **PolicyStatus.java** - Enum: DRAFT, ACTIVE, INACTIVE
- **Category.java** - Policy categories/types
- **CategoryStatus.java** - Enum: DRAFT, ACTIVE, INACTIVE
- **PolicyApplication.java** - Customer applications for policies
- **ApplicationStatus.java** - Enum: PENDING, APPROVED, REJECTED
- **CoverageType.java** - Enum: Coverage types available
- **ApplicationDocument.java** - Supporting documents for applications (S3-backed)
- **Dependent.java** - Dependent/nominee information in applications
- **Gender.java** - Enum: M, F, OTHER
- **NomineeRelationship.java** - Enum: Relationship of nominee to applicant
- **Relationship.java** - Enum: Relationship types

### Controllers
- **PolicyController.java** - Handles policy browsing and retrieval
- **CategoryController.java** - Handles category management (staff)
- **PolicyApplicationController.java** - Handles policy applications (create, approve, reject)
- **ApplicationDocumentController.java** - Handles application document upload/retrieval
- **DependentController.java** - Handles dependent information management
- **DashboardController.java** - Handles staff dashboard metrics

### Services
- **PolicyService.java** - Policy management (list, detail, create, update, delete)
- **CategoryService.java** - Category management with governance rules
- **PolicyApplicationService.java** - Application workflow (create, approve, reject)
- **ApplicationDocumentService.java** - Document upload and retrieval (S3-backed)
- **DependentService.java** - Dependent/nominee management
- **DashboardService.java** - Dashboard metrics calculation

### Repositories
- **PolicyRepository.java** - Data access for policies
- **CategoryRepository.java** - Data access for categories
- **PolicyApplicationRepository.java** - Data access for applications
- **ApplicationDocumentRepository.java** - Data access for application documents
- **DependentRepository.java** - Data access for dependents

### DTOs (Request/Response)
- **PolicyCreateRequest.java** - Input for creating policies
- **PolicyUpdateRequest.java** - Input for updating policies
- **PolicyResponse.java** - Policy data response
- **CategoryCreateRequest.java** - Input for creating categories
- **CategoryUpdateRequest.java** - Input for updating categories
- **CategoryResponse.java** - Category data response
- **PolicyApplicationCreateRequest.java** - Input for applying for policy
- **PolicyApplicationResponse.java** - Application status/details response
- **ApplicationDecisionResponse.java** - Staff approval/rejection decision response
- **ApplicationDocumentResponse.java** - Application document metadata response
- **DependentRequest.java** - Input for dependent information
- **DependentResponse.java** - Dependent information response
- **DashboardMetricsResponse.java** - Dashboard metrics response

### Exceptions
- **ApplicationNotFoundException.java** - When application doesn't exist
- **ApplicationStateException.java** - When operation not allowed in current state
- **DuplicatePendingApplicationException.java** - When duplicate PENDING application exists

---

## 3. CLAIMS DOMAIN
**BRD Area**: V4__claims_initial_schema.sql, V5__claims_add_claim_dependents.sql, V6__claims_create_claim_documents.sql

**BRD Requirements**:
- Customer claim filing with incident type, incident date, amount, description, optional document references, dependent support, and claim history tracking
- Claim supporting documents (S3-backed)
- Claim dependent details tracking
- Staff claim approval/rejection workflows
- Reduce duplicate claims through unique idempotency keys

**Package**: `com.insurewise.claims`

### Core Entities
- **Claim.java** - Customer insurance claims
- **ClaimStatus.java** - Enum: FILED, APPROVED, REJECTED, PAID
- **IncidentType.java** - Enum: Types of incidents (theft, accident, etc.)
- **ClaimDependent.java** - Dependents/claimants associated with claim
- **ClaimDocument.java** - Supporting documents for claim (S3-backed)

### Controllers
- **ClaimController.java** - Handles claim filing, retrieval, and status updates
- **ClaimDependentController.java** - Handles dependent information in claims
- **ClaimDocumentController.java** - Handles claim document upload/retrieval

### Services
- **ClaimService.java** - Core claim workflow (file, approve, reject, track)
- **ClaimDependentService.java** - Manage dependents associated with claims
- **ClaimDocumentService.java** - Handle document upload and S3 storage

### Repositories
- **ClaimRepository.java** - Data access for claims
- **ClaimDependentRepository.java** - Data access for claim dependents
- **ClaimDocumentRepository.java** - Data access for claim documents

### DTOs (Request/Response)
- **ClaimCreateRequest.java** - Input for filing a claim
- **ClaimResponse.java** - Claim data and status response
- **ClaimDependentRequest.java** - Input for dependent information
- **ClaimDependentResponse.java** - Dependent information response
- **ClaimDocumentResponse.java** - Claim document metadata response

### Client Integration
- **PolicyApplicationLookupClient.java** - Calls Policy Service to verify active policies
- **PolicyApplicationSnapshot.java** - Cached policy application data for claim validation

---

## 4. PAYMENTS DOMAIN
**BRD Area**: V7__payments_initial_schema.sql, V8__payments_create_payment_documents.sql

**BRD Requirements**:
- Customer payment history and simulated payment submission
- Support for credit card, debit card, UPI, net banking
- Payment documents (S3-backed)
- System-generated artifacts such as receipts
- Reduce duplicate payments through unique idempotency keys
- Payment visibility for customers and staff

**Package**: `com.insurewise.payments`

### Core Entities
- **Payment.java** - Payment transactions
- **PaymentStatus.java** - Enum: PENDING, COMPLETED, FAILED, REFUNDED
- **PaymentMethod.java** - Enum: CREDIT_CARD, DEBIT_CARD, UPI, NET_BANKING
- **PaymentDocument.java** - Payment receipts and artifacts (S3-backed)

### Controllers
- **PaymentController.java** - Handles payment submission and history
- **PaymentDocumentController.java** - Handles payment document retrieval

### Services
- **PaymentService.java** - Payment processing and tracking
- **PaymentDocumentService.java** - Payment artifact generation and storage (S3)

### Repositories
- **PaymentRepository.java** - Data access for payments
- **PaymentDocumentRepository.java** - Data access for payment documents

### DTOs (Request/Response)
- **PaymentCreateRequest.java** - Input for submitting payment
- **PaymentResponse.java** - Payment status and history response
- **PaymentDocumentResponse.java** - Payment document/receipt response

### Client Integration
- **PaymentPolicyApplicationLookupClient.java** - Calls Policy Service to verify active policies
- **PaymentPolicyApplicationSnapshot.java** - Cached policy application data for payment validation

---

## 5. COMMON DOMAIN
**BRD Area**: JWT authentication, BCrypt password storage, pagination, standard error responses, S3 document storage, observability hooks

**BRD Requirements**:
- JWT authentication for both customer and staff
- BCrypt password storage and verification
- Pagination support
- Standard error responses
- S3-key-backed document storage for all documents
- Standard error handling and logging

**Package**: `com.insurewise.common`

### Security Components
- **JwtService.java** - JWT token generation, validation, and claims extraction
- **JwtAuthenticationFilter.java** - Spring Security filter for JWT validation
- **SecurityConfig.java** - Spring Security configuration
- **SecurityProperties.java** - Security configuration properties
- **JwtPrincipal.java** - JWT principal/user context
- **JwtRole.java** - Enum: CUSTOMER, STAFF roles

### Storage Services
- **S3StorageService.java** - S3 integration for document storage
- **DisabledS3StorageService.java** - Mock S3 service for local development

### DTOs (Request/Response)
- **ApiErrorResponse.java** - Standard error response format
- **PageResponse.java** - Paginated response wrapper
- **PaginationMetadata.java** - Pagination information (page, size, total)
- **PresignedUrlResponse.java** - Pre-signed S3 URL for document access

### Exception Handling
- **GlobalExceptionHandler.java** - Central exception handler for all services

---

## 6. DATABASE MIGRATIONS ALIGNMENT

| Migration | Domain | Purpose | Related Package |
|-----------|--------|---------|-----------------|
| V1__auth_initial_schema.sql | Auth | Create Customer and Staff user tables | `auth` |
| V2__policy_initial_schema.sql | Policy | Create categories, policies, applications, dependents | `policy` |
| V3__policy_create_application_documents.sql | Policy | Create application_documents for S3-backed files | `policy` |
| V4__claims_initial_schema.sql | Claims | Create claims with incident type and idempotency | `claims` |
| V5__claims_add_claim_dependents.sql | Claims | Create claim_dependents for claimants/dependents | `claims` |
| V6__claims_create_claim_documents.sql | Claims | Create claim_documents for S3-backed files | `claims` |
| V7__payments_initial_schema.sql | Payments | Create payments with idempotency and transaction refs | `payments` |
| V8__payments_create_payment_documents.sql | Payments | Create payment_documents for receipts/artifacts | `payments` |
| V9__auth_add_profile_pictures.sql | Auth | Add profile picture columns to users | `auth` |
| V10__auth_seed_local_staff_user.sql | Auth | Seed initial staff user for local testing | `auth` |
| V11__auth_profile_pictures_use_s3_keys.sql | Auth | Convert profile pictures to S3-key storage | `auth` + `common` |

---

## 7. SUMMARY TABLE

| BRD Domain | Java Package | Purpose | Key Controllers | Key Services | Key Entities |
|---|---|---|---|---|---|
| **Auth & User** | `com.insurewise.auth` | User registration, login, profile management | AuthController, StaffUserManagementController | AuthService, StaffUserService | Customer, StaffUser |
| **Policy** | `com.insurewise.policy` | Policy browsing, applications, approvals, documents | PolicyController, CategoryController, PolicyApplicationController, DashboardController, ApplicationDocumentController | PolicyService, CategoryService, PolicyApplicationService, ApplicationDocumentService, DashboardService | Policy, Category, PolicyApplication, ApplicationDocument, Dependent |
| **Claims** | `com.insurewise.claims` | Claim filing, tracking, dependent management, documents | ClaimController, ClaimDependentController, ClaimDocumentController | ClaimService, ClaimDependentService, ClaimDocumentService | Claim, ClaimDependent, ClaimDocument |
| **Payments** | `com.insurewise.payments` | Payment processing, history, receipts | PaymentController, PaymentDocumentController | PaymentService, PaymentDocumentService | Payment, PaymentDocument |
| **Common** | `com.insurewise.common` | Cross-cutting security, storage, error handling | N/A | JwtService, S3StorageService | N/A |

---

## 8. KEY ARCHITECTURAL PATTERNS

### Layered Architecture
```
Controller Layer → Service Layer → Repository Layer → Database
      ↓                ↓                ↓
  Request/Response   Business Logic   Data Access
```

### Cross-Domain Integration
- **Claims ↔ Policy**: ClaimService validates claims against active PolicyApplications
- **Payments ↔ Policy**: PaymentService validates payments against active PolicyApplications
- **All ↔ Common**: All domains use JwtService for security and S3StorageService for documents

### Document Handling
- ApplicationDocument, ClaimDocument, and PaymentDocument all use S3-backed storage
- S3StorageService handles all document upload/retrieval operations
- PresignedUrlResponse provides temporary access to S3 objects

---

## 9. IMPLEMENTATION NOTES

### Status Management
- **Application Status**: PENDING → APPROVED/REJECTED
- **Claim Status**: FILED → APPROVED/REJECTED → PAID
- **Payment Status**: PENDING → COMPLETED/FAILED
- **Policy/Category Status**: DRAFT → ACTIVE → INACTIVE (with deletion guards)

### Uniqueness Constraints
- **Idempotency Keys**: Claims and Payments use idempotency keys to prevent duplicate submissions
- **Unique Pending Application**: Only one PENDING application allowed per (customer, policy) pair

### Role-Based Access
- **CUSTOMER Role**: Can browse active policies, submit applications/claims/payments, upload documents
- **STAFF Role**: Can manage catalog, approve/reject applications and claims, view dashboard metrics

### Service-to-Service Communication
- Claims and Payments use Feign clients to call Policy Service
- PolicyApplicationLookupClient and PaymentPolicyApplicationLookupClient enable inter-service validation
