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
  name: string;
  email: string;
  address: string;
  profilePictureUrl?: string | null;
}

export interface StaffCreateRequest {
  name: string;
  email: string;
  address: string;
}

export interface StaffUpdateRequest {
  name: string;
  email: string;
  address: string;
}

export interface Category {
  id: string;
  name: string;
  status: string;
}

export interface Policy {
  id: string;
  policyName: string;
  categoryId: string;
  categoryName?: string;
  premium: number;
  coverageAmount: number;
  duration: number;
  status: string;
}

export interface PolicyCreateRequest {
  policyName: string;
  categoryId: string;
  premium: number;
  coverageAmount: number;
  duration: number;
}

export interface PolicyApplication {
  id: string;
  applicationCode?: string;
  policyId?: string;
  policyName?: string;
  customerName?: string;
  status: string;
  createdAt?: string;
}

export interface ApplicationDocument {
  id: string;
  fileName: string;
  contentType: string;
  s3Key: string;
  uploadedBy?: string;
  createdAt?: string;
}
