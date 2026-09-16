import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

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
    private dashboardApi: DashboardApiService
  ) {}

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {
    this.loading = true;

    this.dashboardApi.getMetrics().subscribe({
      next: response => {
        this.metrics = response;
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load dashboard data.';
        this.loading = false;
      }
    });
  }
}
<div class="page">

  <div class="page-header">
    <div>
      <h2>Dashboard</h2>
      <p>Overview of insurance platform activity</p>
    </div>
  </div>

  <div *ngIf="loading" class="message">
    Loading dashboard...
  </div>

  <div *ngIf="error" class="error">
    {{ error }}
  </div>

  <div class="stats-grid" *ngIf="!loading">

    <div class="stat-card">
      <span>Staff Users</span>
      <strong>{{ metrics.staff }}</strong>
    </div>

    <div class="stat-card">
      <span>Customers</span>
      <strong>{{ metrics.customers }}</strong>
    </div>

    <div class="stat-card">
      <span>Categories</span>
      <strong>{{ metrics.categories }}</strong>
    </div>

    <div class="stat-card">
      <span>Policies</span>
      <strong>{{ metrics.policies }}</strong>
    </div>

    <div class="stat-card">
      <span>Active Policies</span>
      <strong>{{ metrics.activePolicies }}</strong>
    </div>

    <div class="stat-card">
      <span>Applications</span>
      <strong>{{ metrics.applications }}</strong>
    </div>

    <div class="stat-card">
      <span>Claims</span>
      <strong>{{ metrics.claims }}</strong>
    </div>

    <div class="stat-card">
      <span>Payments</span>
      <strong>{{ metrics.payments }}</strong>
    </div>

  </div>

</div>
import { Routes } from '@angular/router';

import { staffGuard } from '../core/rbac/staff.guard';

export const routes: Routes = [

  /*
   * Root route
   */
  {
    path: '',
    redirectTo: 'auth/staff-login',
    pathMatch: 'full'
  },

  /*
   * Staff Login
   */
  {
    path: 'auth/staff-login',
    loadComponent: () =>
      import('../pages/auth/staff-login.component')
        .then(m => m.StaffLoginComponent)
  },

  /*
   * Staff routes
   */
  {
    path: 'staff',
    canActivate: [staffGuard],
    children: [

      /*
       * Dashboard
       */
      {
        path: 'dashboard',
        loadComponent: () =>
          import('../pages/staff/dashboard/dashboard.component')
            .then(m => m.DashboardComponent)
      },

      /*
       * Manage Users
       */
      {
        path: 'manage-users',
        loadComponent: () =>
          import('../pages/staff/manage-users-list/manage-users-list.component')
            .then(m => m.ManageUsersListComponent)
      },

      /*
       * Create Staff User
       */
      {
        path: 'manage-users/new',
        loadComponent: () =>
          import('../pages/staff/manage-users-new/manage-users-new.component')
            .then(m => m.ManageUsersNewComponent)
      },

      /*
       * Edit Staff User
       */
      {
        path: 'manage-users/:id/edit',
        loadComponent: () =>
          import('../pages/staff/manage-users-new/manage-users-new.component')
            .then(m => m.ManageUsersNewComponent)
      },

      /*
       * Policies
       */
      {
        path: 'policies',
        loadComponent: () =>
          import('../pages/staff/policies-list/policies-list.component')
            .then(m => m.PoliciesListComponent)
      },

      /*
       * Create Policy
       */
      {
        path: 'policies/new',
        loadComponent: () =>
          import('../pages/staff/policies-new/policies-new.component')
            .then(m => m.PoliciesNewComponent)
      },

      /*
       * Edit Policy
       */
      {
        path: 'policies/:id/edit',
        loadComponent: () =>
          import('../pages/staff/policies-new/policies-new.component')
            .then(m => m.PoliciesNewComponent)
      },

      /*
       * Approve / Reject Policies
       */
      {
        path: 'approve-policies',
        loadComponent: () =>
          import('../pages/staff/approve-policies-list/approve-policies-list.component')
            .then(m => m.ApprovePoliciesListComponent)
      },

      /*
       * Review Policy
       */
      {
        path: 'approve-policies/:id',
        loadComponent: () =>
          import('../pages/staff/approve-policies-review/approve-policies-review.component')
            .then(m => m.ApprovePoliciesReviewComponent)
      }

    ]
  },

  /*
   * Unknown URL
   */
  {
    path: '**',
    redirectTo: 'auth/staff-login'
  }

];
