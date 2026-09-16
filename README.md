import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { DashboardApiService } from '../../../services/api/dashboard-api.service';
import { DashboardMetrics } from '../../../types/br04-05.types';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  metrics: DashboardMetrics = {
    customers: 0,
    staff: 0,
    categories: 0,
    policies: 0,
    activePolicies: 0,
    applications: 0,
    claims: 0,
    payments: 0
  };

  loading = true;
  error = '';

  constructor(
    private readonly dashboardApi: DashboardApiService,
    private readonly router: Router
  ) {}

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {
    this.loading = true;
    this.error = '';

    this.dashboardApi.getMetrics().subscribe({
      next: (response) => {
        this.metrics = response;
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load dashboard data.';
        this.loading = false;
      }
    });
  }

  // Staff User Management
  addStaffUser(): void {
    this.router.navigate(['/staff/manage-users/new']);
  }

  manageStaffUsers(): void {
    this.router.navigate(['/staff/manage-users']);
  }

  // Policy Management
  addPolicy(): void {
    this.router.navigate(['/staff/policies/new']);
  }

  managePolicies(): void {
    this.router.navigate(['/staff/policies']);
  }

  // Policy Application Approval/Rejection
  approvePolicies(): void {
    this.router.navigate(['/staff/approve-policies']);
  }
}








<div class="page">

  <div class="page-header">
    <div>
      <h2>Staff Dashboard</h2>
      <p>Manage staff users, policies and policy applications.</p>
    </div>
  </div>

  <!-- Loading -->
  <div class="loading" *ngIf="loading">
    Loading dashboard...
  </div>

  <!-- Error -->
  <div class="error" *ngIf="error && !loading">
    {{ error }}
  </div>

  <ng-container *ngIf="!loading">

    <!-- Dashboard Statistics -->
    <section class="stats-section">

      <div class="stat-card">
        <span class="stat-label">Customers</span>
        <strong>{{ metrics.customers }}</strong>
      </div>

      <div class="stat-card">
        <span class="stat-label">Staff Users</span>
        <strong>{{ metrics.staff }}</strong>
      </div>

      <div class="stat-card">
        <span class="stat-label">Policies</span>
        <strong>{{ metrics.policies }}</strong>
      </div>

      <div class="stat-card">
        <span class="stat-label">Active Policies</span>
        <strong>{{ metrics.activePolicies }}</strong>
      </div>

      <div class="stat-card">
        <span class="stat-label">Applications</span>
        <strong>{{ metrics.applications }}</strong>
      </div>

      <div class="stat-card">
        <span class="stat-label">Claims</span>
        <strong>{{ metrics.claims }}</strong>
      </div>

      <div class="stat-card">
        <span class="stat-label">Payments</span>
        <strong>{{ metrics.payments }}</strong>
      </div>

    </section>


    <!-- Quick Actions -->
    <section class="actions-section">

      <div class="section-header">
        <h3>Quick Actions</h3>
        <p>Staff and policy management</p>
      </div>

      <div class="actions-grid">

        <!-- Add Staff -->
        <button
          type="button"
          class="action-card"
          (click)="addStaffUser()">

          <div class="action-icon">+</div>

          <div class="action-content">
            <strong>Add Staff User</strong>
            <span>Create a new staff account</span>
          </div>

        </button>


        <!-- Manage Staff -->
        <button
          type="button"
          class="action-card"
          (click)="manageStaffUsers()">

          <div class="action-icon">👥</div>

          <div class="action-content">
            <strong>Manage Staff Users</strong>
            <span>View, edit or delete staff users</span>
          </div>

        </button>


        <!-- Add Policy -->
        <button
          type="button"
          class="action-card"
          (click)="addPolicy()">

          <div class="action-icon">+</div>

          <div class="action-content">
            <strong>Add Policy</strong>
            <span>Create a new insurance policy</span>
          </div>

        </button>


        <!-- Manage Policies -->
        <button
          type="button"
          class="action-card"
          (click)="managePolicies()">

          <div class="action-icon">📋</div>

          <div class="action-content">
            <strong>Manage Policies</strong>
            <span>View, edit or delete policies</span>
          </div>

        </button>


        <!-- Approve / Reject Applications -->
        <button
          type="button"
          class="action-card"
          (click)="approvePolicies()">

          <div class="action-icon">✓</div>

          <div class="action-content">
            <strong>Approve Policies</strong>
            <span>Review applications and approve or reject by ID</span>
          </div>

        </button>

      </div>

    </section>

  </ng-container>

</div>







.page {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
}

.page-header p {
  margin: 6px 0 0;
  color: #666;
}

.loading {
  padding: 30px;
  text-align: center;
  color: #666;
}

.error {
  padding: 12px 16px;
  margin-bottom: 20px;
  border: 1px solid #f0b7b7;
  border-radius: 6px;
  background: #fff4f4;
  color: #b42318;
}


/* Statistics */

.stats-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  padding: 20px;
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
}

.stat-label {
  display: block;
  margin-bottom: 8px;
  color: #666;
  font-size: 14px;
}

.stat-card strong {
  font-size: 28px;
  font-weight: 600;
}


/* Quick Actions */

.actions-section {
  margin-top: 10px;
}

.section-header {
  margin-bottom: 16px;
}

.section-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.section-header p {
  margin: 5px 0 0;
  color: #666;
  font-size: 14px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
  padding: 18px;
  text-align: left;
  background: #ffffff;
  border: 1px solid #e2e2e2;
  border-radius: 8px;
  cursor: pointer;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.action-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
}

.action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  flex-shrink: 0;
  border-radius: 6px;
  background: #f3f4f6;
  font-size: 20px;
}

.action-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.action-content strong {
  font-size: 15px;
  font-weight: 600;
}

.action-content span {
  color: #666;
  font-size: 13px;
}


/* Responsive */

@media (max-width: 900px) {
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .page {
    padding: 16px;
  }

  .stats-section,
  .actions-grid {
    grid-template-columns: 1fr;
  }
}







import { Routes } from '@angular/router';
import { staffGuard } from '../core/rbac/staff.guard';

export const routes: Routes = [

  // Default route
  {
    path: '',
    redirectTo: 'auth/staff-login',
    pathMatch: 'full'
  },

  // Staff Login
  {
    path: 'auth/staff-login',
    loadComponent: () =>
      import('../pages/auth/staff-login.component')
        .then(m => m.StaffLoginComponent)
  },

  // Staff Area
  {
    path: 'staff',
    canActivate: [staffGuard],
    children: [

      // Dashboard
      {
        path: 'dashboard',
        loadComponent: () =>
          import('../pages/staff/dashboard/dashboard.component')
            .then(m => m.DashboardComponent)
      },

      // -------------------------
      // Staff User Management
      // -------------------------

      {
        path: 'manage-users',
        loadComponent: () =>
          import('../pages/staff/manage-users-list/manage-users-list.component')
            .then(m => m.ManageUsersListComponent)
      },

      {
        path: 'manage-users/new',
        loadComponent: () =>
          import('../pages/staff/manage-users-new/manage-users-new.component')
            .then(m => m.ManageUsersNewComponent)
      },

      {
        path: 'manage-users/:id/edit',
        loadComponent: () =>
          import('../pages/staff/manage-users-new/manage-users-new.component')
            .then(m => m.ManageUsersNewComponent)
      },

      // -------------------------
      // Policy Management
      // -------------------------

      {
        path: 'policies',
        loadComponent: () =>
          import('../pages/staff/policies-list/policies-list.component')
            .then(m => m.PoliciesListComponent)
      },

      {
        path: 'policies/new',
        loadComponent: () =>
          import('../pages/staff/policies-new/policies-new.component')
            .then(m => m.PoliciesNewComponent)
      },

      {
        path: 'policies/:id/edit',
        loadComponent: () =>
          import('../pages/staff/policies-new/policies-new.component')
            .then(m => m.PoliciesNewComponent)
      },

      // -------------------------
      // Policy Application Approval
      // -------------------------

      {
        path: 'approve-policies',
        loadComponent: () =>
          import('../pages/staff/approve-policies-list/approve-policies-list.component')
            .then(m => m.ApprovePoliciesListComponent)
      },

      {
        path: 'approve-policies/:id',
        loadComponent: () =>
          import('../pages/staff/approve-policies-review/approve-policies-review.component')
            .then(m => m.ApprovePoliciesReviewComponent)
      }
    ]
  },

  // Unknown route
  {
    path: '**',
    redirectTo: 'auth/staff-login'
  }
];

