export interface DashboardMetrics {
  customers: number;
  staff: number;
  categories: number;
  policies: number;
  activePolicies: number;
  applications: number;
  claims: number;
  payments: number;
}

export interface StaffUser {
  id: string;
  fullname: string;
  email: string;
  address: string;
  profilePictureUrl?: string | null;
}

export interface StaffCreateRequest {
  fullname: string;
  email: string;
  address: string;
}

export interface StaffUpdateRequest {
  fullname: string;
  email: string;
  address: string;
}

export interface Category {
  id: string;
  name: string;
  status: string;
}


/* =========================
   POLICY
   ========================= */

export interface Policy {
  id: string;
  name: string;
  categoryId: string;
  categoryName?: string;
  coverageAmount: number;
  premiumAmount: number;
  durationLabel: string;
  status: string;
}

export interface PolicyCreateRequest {
  name: string;
  categoryId: string;
  coverageAmount: number;
  premiumAmount: number;
  durationLabel: string;
  status: string;
}


/* =========================
   POLICY APPLICATION
   ========================= */

export interface PolicyApplication {
  id: string;
  applicationCode?: string;
  customerId?: string;
  policyId?: string;
  policyName?: string;
  coverageType?: string;
  coverageAmount?: number;
  premiumAmount?: number;
  dateOfBirth?: string;
  address?: string;
  preferredStartDate?: string;
  nomineeName?: string;
  nomineeRelationship?: string;
  startDate?: string;
  endDate?: string;
  status: string;
  decidedBy?: string;
  decidedAt?: string;
  createdAt?: string;
}


/* =========================
   APPLICATION DOCUMENT
   ========================= */

export interface ApplicationDocument {
  id: string;
  fileName: string;
  contentType: string;
  s3Key: string;
  uploadedBy?: string;
  createdAt?: string;
}     
