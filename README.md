CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE customers (
    id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name     VARCHAR(120)  NOT NULL,
    phone         VARCHAR(30)   NOT NULL,
    email         VARCHAR(160)  NOT NULL,
    password_hash VARCHAR(100)  NOT NULL,
    created_at    TIMESTAMP     NOT NULL DEFAULT now(),
    CONSTRAINT uq_customers_email UNIQUE (email)
);

CREATE TABLE staff_users (
    id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name     VARCHAR(120)  NOT NULL,
    email         VARCHAR(160)  NOT NULL,
    address       VARCHAR(240)  NOT NULL,
    password_hash VARCHAR(100)  NOT NULL,
    created_at    TIMESTAMP     NOT NULL DEFAULT now(),
    CONSTRAINT uq_staff_users_email UNIQUE (email)
);

INSERT INTO staff_users (id, full_name, email, address, password_hash)
VALUES (
    'a0000000-0000-0000-0000-000000000001',
    'System Admin',
    'admin@insurewise.com',
    'InsureWise HQ',
    '$2a$10$5HJZwqvGZgJRII/fkr8HsedsvESUF8khDwpUOBDgc7EMI578NV2qK'
);

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE categories (
    id          UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(80)   NOT NULL,
    description VARCHAR(500)  NOT NULL,
    status      VARCHAR(20)   NOT NULL,
    created_at  TIMESTAMP     NOT NULL DEFAULT now(),
    CONSTRAINT ck_categories_status CHECK (status IN ('ACTIVE', 'INACTIVE'))
);

CREATE TABLE policies (
    id              UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(120)  NOT NULL,
    category_id     UUID          NOT NULL,
    coverage_amount NUMERIC(14,2) NOT NULL,
    premium_amount  NUMERIC(10,2) NOT NULL,
    duration_label  VARCHAR(40)   NOT NULL,
    status          VARCHAR(20)   NOT NULL,
    created_at      TIMESTAMP     NOT NULL DEFAULT now(),
    CONSTRAINT ck_policies_coverage_positive CHECK (coverage_amount > 0),
    CONSTRAINT ck_policies_premium_positive  CHECK (premium_amount > 0),
    CONSTRAINT ck_policies_status CHECK (status IN ('DRAFT', 'ACTIVE', 'INACTIVE')),
    CONSTRAINT fk_policies_category FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE RESTRICT
);

CREATE INDEX idx_policies_category_id ON policies (category_id);
CREATE INDEX idx_policies_status ON policies (status);

CREATE SEQUENCE application_code_seq START WITH 1000 INCREMENT BY 1;

CREATE TABLE policy_applications (
    id                   UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    application_code     VARCHAR(20)   NOT NULL,
    customer_id          UUID          NOT NULL,
    policy_id            UUID          NOT NULL,
    coverage_type        VARCHAR(20)   NOT NULL,
    coverage_amount      NUMERIC(14,2) NOT NULL,
    premium_amount       NUMERIC(10,2) NOT NULL,
    date_of_birth        DATE          NOT NULL,
    address              VARCHAR(500)  NOT NULL,
    preferred_start_date DATE,
    nominee_name         VARCHAR(120),
    nominee_relationship VARCHAR(20),
    start_date           DATE,
    end_date             DATE,
    status               VARCHAR(20)   NOT NULL,
    decided_by           UUID,
    decided_at           TIMESTAMP,
    created_at           TIMESTAMP     NOT NULL DEFAULT now(),
    CONSTRAINT uq_application_code UNIQUE (application_code),
    CONSTRAINT ck_applications_coverage_type CHECK (coverage_type IN ('SINGLE', 'GROUP')),
    CONSTRAINT ck_applications_status CHECK (status IN ('PENDING', 'ACTIVE', 'REJECTED', 'EXPIRED')),
    CONSTRAINT ck_applications_nominee_rel CHECK (nominee_relationship IS NULL OR nominee_relationship IN ('SPOUSE', 'PARENT', 'CHILD', 'SIBLING', 'OTHER')),
    CONSTRAINT fk_applications_policy FOREIGN KEY (policy_id) REFERENCES policies (id) ON DELETE RESTRICT
);

CREATE UNIQUE INDEX uq_pending_application ON policy_applications (customer_id, policy_id) WHERE status = 'PENDING';
CREATE INDEX idx_applications_customer ON policy_applications (customer_id);
CREATE INDEX idx_applications_status ON policy_applications (status);
CREATE INDEX idx_applications_policy ON policy_applications (policy_id);

CREATE TABLE dependents (
    id                     UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_application_id  UUID         NOT NULL,
    full_name              VARCHAR(120) NOT NULL,
    relationship           VARCHAR(20)  NOT NULL,
    date_of_birth          DATE         NOT NULL,
    gender                 VARCHAR(10)  NOT NULL,
    created_at             TIMESTAMP    NOT NULL DEFAULT now(),
    CONSTRAINT ck_dependents_relationship CHECK (relationship IN ('SPOUSE', 'CHILD', 'PARENT', 'SIBLING')),
    CONSTRAINT ck_dependents_gender CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
    CONSTRAINT fk_dependents_application FOREIGN KEY (policy_application_id) REFERENCES policy_applications (id) ON DELETE CASCADE
);

CREATE INDEX idx_dependents_application ON dependents (policy_application_id);
CREATE TABLE application_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    policy_application_id UUID NOT NULL REFERENCES policy_applications(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    content_type VARCHAR(100),
    s3_key VARCHAR(600) NOT NULL,
    uploaded_by UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_application_documents_application_id ON application_documents(policy_application_id);
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE SEQUENCE claim_code_seq START WITH 1000 INCREMENT BY 1;

CREATE TABLE claims (
    id                     UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_code             VARCHAR(20)    NOT NULL,
    idempotency_key        VARCHAR(80)    NOT NULL,
    customer_id            UUID           NOT NULL,
    policy_application_id  UUID           NOT NULL,
    policy_name_snapshot   VARCHAR(120)   NOT NULL,
    incident_type          VARCHAR(40)    NOT NULL,
    incident_date          DATE           NOT NULL,
    amount                 NUMERIC(14,2)  NOT NULL,
    description            VARCHAR(1000)  NOT NULL,
    document_ref           VARCHAR(300),
    status                 VARCHAR(20)    NOT NULL,
    processed_by           UUID,
    processed_at           TIMESTAMP,
    created_at             TIMESTAMP      NOT NULL DEFAULT now(),
    CONSTRAINT uq_claims_claim_code      UNIQUE (claim_code),
    CONSTRAINT uq_claims_idempotency_key UNIQUE (idempotency_key),
    CONSTRAINT ck_claims_amount_positive CHECK (amount > 0),
    CONSTRAINT ck_claims_incident_type CHECK (incident_type IN ('ACCIDENT','HOSPITALIZATION','THEFT','NATURAL_DISASTER','FIRE','DEATH','DISABILITY','PROPERTY_DAMAGE','OTHER')),
    CONSTRAINT ck_claims_status CHECK (status IN ('PENDING','UNDER_REVIEW','APPROVED','REJECTED'))
);

CREATE INDEX idx_claims_customer ON claims (customer_id);
CREATE INDEX idx_claims_status ON claims (status);
CREATE INDEX idx_claims_policy_app ON claims (policy_application_id);
CREATE TABLE claim_dependents (
    id              UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id        UUID           NOT NULL,
    full_name       VARCHAR(120)   NOT NULL,
    relationship    VARCHAR(20)    NOT NULL,
    date_of_birth   DATE           NOT NULL,
    gender          VARCHAR(10)    NOT NULL,
    CONSTRAINT ck_claim_dependents_relationship CHECK (relationship IN ('SPOUSE', 'CHILD', 'PARENT', 'SIBLING')),
    CONSTRAINT ck_claim_dependents_gender CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
    CONSTRAINT fk_claim_dependents_claim FOREIGN KEY (claim_id) REFERENCES claims (id) ON DELETE CASCADE
);

CREATE INDEX idx_claim_dependents_claim ON claim_dependents (claim_id);
CREATE TABLE claim_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    content_type VARCHAR(100),
    s3_key VARCHAR(600) NOT NULL,
    uploaded_by UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_claim_documents_claim_id ON claim_documents(claim_id);
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE payments (
    id                     UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    idempotency_key        VARCHAR(80)   NOT NULL,
    customer_id            UUID          NOT NULL,
    policy_application_id  UUID          NOT NULL,
    policy_name_snapshot   VARCHAR(120)  NOT NULL,
    amount                 NUMERIC(10,2) NOT NULL,
    method                 VARCHAR(20)   NOT NULL,
    status                 VARCHAR(20)   NOT NULL,
    transaction_ref        VARCHAR(40)   NOT NULL,
    paid_at                TIMESTAMP     NOT NULL,
    created_at             TIMESTAMP     NOT NULL DEFAULT now(),
    CONSTRAINT uq_payments_idempotency_key UNIQUE (idempotency_key),
    CONSTRAINT uq_payments_transaction_ref UNIQUE (transaction_ref),
    CONSTRAINT ck_payments_amount_positive CHECK (amount > 0),
    CONSTRAINT ck_payments_method CHECK (method IN ('CREDIT_CARD','DEBIT_CARD','UPI','NET_BANKING')),
    CONSTRAINT ck_payments_status CHECK (status IN ('SUCCESS','FAILED','PENDING'))
);

CREATE INDEX idx_payments_customer ON payments (customer_id);
CREATE INDEX idx_payments_status ON payments (status);
CREATE INDEX idx_payments_policy_app ON payments (policy_application_id);
CREATE TABLE payment_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_id UUID NOT NULL REFERENCES payments(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    content_type VARCHAR(100),
    s3_key VARCHAR(600) NOT NULL,
    uploaded_by UUID NOT NULL,
    system_generated BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_payment_documents_payment_id ON payment_documents(payment_id);
ALTER TABLE customers
    ADD COLUMN profile_picture TEXT;

ALTER TABLE staff_users
    ADD COLUMN profile_picture TEXT;
INSERT INTO staff_users (id, full_name, email, address, password_hash)
VALUES (
    '2a3ef9df-1c18-429e-ab38-2f1e6f8fa6c7',
    'Local Staff Admin',
    'staff.local@insurewise.com',
    'InsureWise HQ',
    '$2a$10$hUGRG47rHX4zg8Ccj1lT.eQn3Tkni9zu2HU9.Og5TMjOBNR6i3GfG'
)
ON CONFLICT (email) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    address = EXCLUDED.address,
    password_hash = EXCLUDED.password_hash;
UPDATE customers
SET profile_picture = NULL
WHERE profile_picture IS NOT NULL
  AND profile_picture LIKE 'data:%';

UPDATE staff_users
SET profile_picture = NULL
WHERE profile_picture IS NOT NULL
  AND profile_picture LIKE 'data:%';

ALTER TABLE customers
    RENAME COLUMN profile_picture TO profile_picture_s3_key;

ALTER TABLE staff_users
    RENAME COLUMN profile_picture TO profile_picture_s3_key;

ALTER TABLE customers
    ALTER COLUMN profile_picture_s3_key TYPE VARCHAR(600);

ALTER TABLE staff_users
    ALTER COLUMN profile_picture_s3_key TYPE VARCHAR(600);
