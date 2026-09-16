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
      next: response => {
        this.metrics = response;
        this.loading = false;
      },
      error: error => {
        console.error('Unable to load dashboard data.', error);
        this.error = 'Unable to load dashboard data.';
        this.loading = false;
      }
    });
  }

  addPolicy(): void {
    this.router.navigate(['/staff/policies/new']);
  }

  managePolicies(): void {
    this.router.navigate(['/staff/policies']);
  }

  addStaffUser(): void {
    this.router.navigate(['/staff/manage-users/new']);
  }

  manageStaffUsers(): void {
    this.router.navigate(['/staff/manage-users']);
  }

  reviewApplications(): void {
    this.router.navigate(['/staff/approve-policies']);
  }

  viewApplicationDocuments(): void {
    /*
     * Application review is where the staff member can inspect
     * the application and its supporting documents.
     */
    this.router.navigate(['/staff/approve-policies']);
  }

  manageCategories(): void {
    this.router.navigate(['/staff/categories']);
  }
}







<div class="page">

  <!-- ========================= -->
  <!-- DASHBOARD HEADER -->
  <!-- ========================= -->

  <div class="page-header">

    <div>
      <h2>Dashboard</h2>
      <p>Overview of insurance platform activity</p>
    </div>

  </div>


  <!-- ========================= -->
  <!-- LOADING -->
  <!-- ========================= -->

  <div
    *ngIf="loading"
    class="message">

    Loading dashboard...

  </div>


  <!-- ========================= -->
  <!-- ERROR -->
  <!-- ========================= -->

  <div
    *ngIf="error"
    class="error">

    {{ error }}

  </div>


  <!-- ========================= -->
  <!-- STATISTICS -->
  <!-- ========================= -->

  <div
    class="stats-grid"
    *ngIf="!loading">

    <div class="stat-card">

      <span>Staff Users</span>

      <strong>
        {{ metrics.staff }}
      </strong>

    </div>


    <div class="stat-card">

      <span>Customers</span>

      <strong>
        {{ metrics.customers }}
      </strong>

    </div>


    <div class="stat-card">

      <span>Categories</span>

      <strong>
        {{ metrics.categories }}
      </strong>

    </div>


    <div class="stat-card">

      <span>Policies</span>

      <strong>
        {{ metrics.policies }}
      </strong>

    </div>


    <div class="stat-card">

      <span>Active Policies</span>

      <strong>
        {{ metrics.activePolicies }}
      </strong>

    </div>


    <div class="stat-card">

      <span>Applications</span>

      <strong>
        {{ metrics.applications }}
      </strong>

    </div>


    <div class="stat-card">

      <span>Claims</span>

      <strong>
        {{ metrics.claims }}
      </strong>

    </div>


    <div class="stat-card">

      <span>Payments</span>

      <strong>
        {{ metrics.payments }}
      </strong>

    </div>

  </div>


  <!-- ========================= -->
  <!-- QUICK ACTIONS -->
  <!-- ========================= -->

  <section
    class="actions-section"
    *ngIf="!loading">

    <div class="section-header">

      <div>

        <h3>Quick Actions</h3>

        <p>
          Manage staff users, policies and applications
        </p>

      </div>

    </div>


    <div class="actions-grid">


      <!-- ADD POLICY -->

      <button
        type="button"
        class="action-card"
        (click)="addPolicy()">

        <div class="action-icon">
          +
        </div>

        <div class="action-content">

          <strong>
            Add Policy
          </strong>

          <span>
            Create a new insurance policy
          </span>

        </div>

      </button>


      <!-- MANAGE POLICIES -->

      <button
        type="button"
        class="action-card"
        (click)="managePolicies()">

        <div class="action-icon">
          ≡
        </div>

        <div class="action-content">

          <strong>
            Manage Policies
          </strong>

          <span>
            View, edit or delete policies
          </span>

        </div>

      </button>


      <!-- ADD STAFF USER -->

      <button
        type="button"
        class="action-card"
        (click)="addStaffUser()">

        <div class="action-icon">
          +
        </div>

        <div class="action-content">

          <strong>
            Add Staff User
          </strong>

          <span>
            Create a new staff account
          </span>

        </div>

      </button>


      <!-- MANAGE STAFF USERS -->

      <button
        type="button"
        class="action-card"
        (click)="manageStaffUsers()">

        <div class="action-icon">
          ≡
        </div>

        <div class="action-content">

          <strong>
            Manage Staff Users
          </strong>

          <span>
            View, edit or delete staff users
          </span>

        </div>

      </button>


      <!-- REVIEW APPLICATIONS -->

      <button
        type="button"
        class="action-card"
        (click)="reviewApplications()">

        <div class="action-icon">
          ✓
        </div>

        <div class="action-content">

          <strong>
            Review Applications
          </strong>

          <span>
            Approve or reject pending applications
          </span>

        </div>

      </button>


      <!-- APPLICATION DOCUMENTS -->

      <button
        type="button"
        class="action-card"
        (click)="viewApplicationDocuments()">

        <div class="action-icon">
          📎
        </div>

        <div class="action-content">

          <strong>
            Application Documents
          </strong>

          <span>
            Review supporting documents
          </span>

        </div>

      </button>


      <!-- CATEGORIES -->

      <button
        type="button"
        class="action-card"
        (click)="manageCategories()">

        <div class="action-icon">
          #
        </div>

        <div class="action-content">

          <strong>
            Manage Categories
          </strong>

          <span>
            View and manage policy categories
          </span>

        </div>

      </button>


    </div>

  </section>

</div>








/* ========================= */
/* QUICK ACTIONS */
/* ========================= */

.actions-section {
  margin-top: 32px;
}

.section-header {
  margin-bottom: 18px;
}

.section-header h3 {
  margin: 0;
  font-size: 20px;
}

.section-header p {
  margin: 6px 0 0;
  color: #777;
}


/* ========================= */
/* ACTION GRID */
/* ========================= */

.actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}


/* ========================= */
/* ACTION CARD */
/* ========================= */

.action-card {
  display: flex;
  align-items: center;
  gap: 15px;

  width: 100%;
  min-height: 95px;

  padding: 18px;

  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;

  cursor: pointer;

  text-align: left;

  transition:
    transform 0.15s ease,
    box-shadow 0.15s ease,
    border-color 0.15s ease;
}

.action-card:hover {
  transform: translateY(-2px);
  border-color: #aaa;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}


/* ========================= */
/* ICON */
/* ========================= */

.action-icon {
  width: 44px;
  height: 44px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 8px;

  background: #f1f4f6;

  font-size: 24px;
  font-weight: 600;
}


/* ========================= */
/* CONTENT */
/* ========================= */

.action-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.action-content strong {
  font-size: 16px;
}

.action-content span {
  color: #777;
  font-size: 13px;
}


/* ========================= */
/* RESPONSIVE */
/* ========================= */

@media (max-width: 1000px) {

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }

}

@media (max-width: 650px) {

  .actions-grid {
    grid-template-columns: 1fr;
  }

}








<div class="page">

  <!-- Dashboard Header -->
  <div class="page-header">
    <div>
      <h2>Dashboard</h2>
      <p>Overview of insurance platform activity</p>
    </div>
  </div>


  <!-- Loading -->
  <div
    *ngIf="loading"
    class="message">

    Loading dashboard...

  </div>


  <!-- Error -->
  <div
    *ngIf="error"
    class="error">

    {{ error }}

  </div>


  <!-- Dashboard Statistics -->
  <div
    class="stats-grid"
    *ngIf="!loading">

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


  <!-- Quick Actions -->
  <section
    class="actions-section"
    *ngIf="!loading">

    <div class="section-header">

      <h3>Quick Actions</h3>

      <p>
        Staff and policy management
      </p>

    </div>


    <div class="actions-grid">


      <!-- Add Staff User -->
      <button
        type="button"
        class="action-card"
        (click)="addStaffUser()">

        <div class="action-icon">
          +
        </div>

        <div class="action-content">

          <strong>
            Add Staff User
          </strong>

          <span>
            Create a new staff account
          </span>

        </div>

      </button>


      <!-- Manage Staff Users -->
      <button
        type="button"
        class="action-card"
        (click)="manageStaffUsers()">

        <div class="action-icon">
          👥
        </div>

        <div class="action-content">

          <strong>
            Manage Staff Users
          </strong>

          <span>
            View, edit or delete staff users
          </span>

        </div>

      </button>


      <!-- Add Policy -->
      <button
        type="button"
        class="action-card"
        (click)="addPolicy()">

        <div class="action-icon">
          +
        </div>

        <div class="action-content">

          <strong>
            Add Policy
          </strong>

          <span>
            Create a new insurance policy
          </span>

        </div>

      </button>


      <!-- Manage Policies -->
      <button
        type="button"
        class="action-card"
        (click)="managePolicies()">

        <div class="action-icon">
          📋
        </div>

        <div class="action-content">

          <strong>
            Manage Policies
          </strong>

          <span>
            View, edit or delete policies
          </span>

        </div>

      </button>


      <!-- Review Applications -->
      <button
        type="button"
        class="action-card"
        (click)="reviewApplications()">

        <div class="action-icon">
          ✓
        </div>

        <div class="action-content">

          <strong>
            Review Applications
          </strong>

          <span>
            Approve or reject policy applications
          </span>

        </div>

      </button>


      <!-- Application Documents -->
      <button
        type="button"
        class="action-card"
        (click)="viewApplicationDocuments()">

        <div class="action-icon">
          📎
        </div>

        <div class="action-content">

          <strong>
            Application Documents
          </strong>

          <span>
            View supporting documents
          </span>

        </div>

      </button>


    </div>

  </section>

</div>









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

      next: response => {

        this.metrics = response;
        this.loading = false;

      },

      error: error => {

        console.error(
          'Unable to load dashboard data.',
          error
        );

        this.error =
          'Unable to load dashboard data.';

        this.loading = false;
      }
    });
  }


  // =========================
  // BR04 - STAFF MANAGEMENT
  // =========================

  addStaffUser(): void {

    this.router.navigate([
      '/staff/manage-users/new'
    ]);
  }


  manageStaffUsers(): void {

    this.router.navigate([
      '/staff/manage-users'
    ]);
  }


  // =========================
  // BR05 - POLICY MANAGEMENT
  // =========================

  addPolicy(): void {

    this.router.navigate([
      '/staff/policies/new'
    ]);
  }


  managePolicies(): void {

    this.router.navigate([
      '/staff/policies'
    ]);
  }


  // =========================
  // BR05 - APPLICATION REVIEW
  // =========================

  reviewApplications(): void {

    this.router.navigate([
      '/staff/approve-policies'
    ]);
  }


  // =========================
  // BR05 - DOCUMENTS
  // =========================

  viewApplicationDocuments(): void {

    /*
     * Documents belong to a policy application.
     * Therefore staff first goes to the application
     * review/list page and selects an application
     * to view its supporting documents.
     */
    this.router.navigate([
      '/staff/approve-policies'
    ]);
  }
}
