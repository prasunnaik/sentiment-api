<div class="page">

  <div class="header">

    <div>
      <h2>Approve Policies</h2>
      <p>Review pending policy applications</p>
    </div>

  </div>

  <div *ngIf="loading">
    Loading applications...
  </div>

  <div
    class="error"
    *ngIf="error">

    {{ error }}

  </div>

  <div
    class="table-container"
    *ngIf="!loading">

    <table>

      <thead>

        <tr>
          <th>APPLICATION</th>
          <th>POLICY</th>
          <th>CUSTOMER</th>
          <th>STATUS</th>
          <th>ACTION</th>
        </tr>

      </thead>

      <tbody>

        <tr
          *ngFor="let application of applications">

          <td>
            {{ application.applicationCode || application.id }}
          </td>

          <td>
            {{ application.policyName }}
          </td>

          <td>
            {{ application.customerName }}
          </td>

          <td>
            {{ application.status }}
          </td>

          <td>

            <button
              class="review"
              (click)="review(application.id)">

              Review

            </button>

          </td>

        </tr>

        <tr *ngIf="applications.length === 0">

          <td colspan="5">
            No pending applications.
          </td>

        </tr>

      </tbody>

    </table>

  </div>

</div>







.page {
  padding: 24px;
}

.header {
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
}

.header p {
  color: #777;
}

.table-container {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 14px;
  border-bottom: 1px solid #eee;
  text-align: left;
}

th {
  font-size: 12px;
  color: #666;
}

.review {
  padding: 7px 12px;
  border: 1px solid #777;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.error {
  color: #c62828;
}





import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

import {
  PolicyApplication,
  ApplicationDocument
} from '../../../types/br04-br05.types';

import {
  PolicyApplicationApiService
} from '../../../services/api/policy-application-api.service';

import {
  ApplicationDocumentApiService
} from '../../../services/api/application-document-api.service';

@Component({
  selector: 'app-approve-policies-review',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './approve-policies-review.component.html',
  styleUrls: ['./approve-policies-review.component.css']
})
export class ApprovePoliciesReviewComponent implements OnInit {

  application: PolicyApplication | null = null;

  documents: ApplicationDocument[] = [];

  loading = true;
  processing = false;

  error = '';
  success = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private applicationApi: PolicyApplicationApiService,
    private documentApi: ApplicationDocumentApiService
  ) {}

  ngOnInit(): void {

    const id =
      this.route.snapshot.paramMap.get('id');

    if (!id) {
      this.error = 'Application ID is missing.';
      this.loading = false;
      return;
    }

    this.loadApplication(id);
    this.loadDocuments(id);
  }

  loadApplication(id: string): void {

    this.applicationApi
      .getById(id)
      .subscribe({

        next: application => {
          this.application = application;
          this.loading = false;
        },

        error: () => {
          this.error =
            'Unable to load application.';
          this.loading = false;
        }

      });
  }

  loadDocuments(id: string): void {

    this.documentApi
      .getByApplicationId(id)
      .subscribe({

        next: documents => {
          this.documents = documents;
        },

        error: () => {
          this.error =
            'Unable to load supporting documents.';
        }

      });
  }

  approve(): void {

    if (!this.application) {
      return;
    }

    if (!window.confirm(
      'Approve this policy application?'
    )) {
      return;
    }

    this.processing = true;

    this.applicationApi
      .approve(this.application.id)
      .subscribe({

        next: application => {

          this.application = application;
          this.processing = false;

          this.success =
            'Policy application approved successfully.';
        },

        error: error => {

          this.processing = false;

          this.error =
            error?.error?.message ??
            'Unable to approve application.';
        }

      });
  }

  reject(): void {

    if (!this.application) {
      return;
    }

    if (!window.confirm(
      'Reject this policy application?'
    )) {
      return;
    }

    this.processing = true;

    this.applicationApi
      .reject(this.application.id)
      .subscribe({

        next: application => {

          this.application = application;
          this.processing = false;

          this.success =
            'Policy application rejected.';
        },

        error: error => {

          this.processing = false;

          this.error =
            error?.error?.message ??
            'Unable to reject application.';
        }

      });
  }

  openDocument(document: ApplicationDocument): void {

    this.documentApi
      .getDownloadUrl(document.id)
      .subscribe({

        next: response => {

          if (response?.url) {
            window.open(
              response.url,
              '_blank'
            );
          }
        },

        error: () => {
          this.error =
            'Unable to retrieve document.';
        }

      });
  }

  back(): void {
    this.router.navigate([
      '/staff/approve-policies'
    ]);
  }
}






<div class="page">

  <div class="header">

    <div>
      <h2>Application Review</h2>
      <p>Review and process policy application</p>
    </div>

    <button
      class="back"
      (click)="back()">

      Back

    </button>

  </div>

  <div *ngIf="loading">
    Loading application...
  </div>

  <div
    class="error"
    *ngIf="error">

    {{ error }}

  </div>

  <div
    class="success"
    *ngIf="success">

    {{ success }}

  </div>

  <div
    class="review-card"
    *ngIf="application">

    <h3>Application Information</h3>

    <div class="details">

      <div>
        <span>Application</span>
        <strong>
          {{ application.applicationCode || application.id }}
        </strong>
      </div>

      <div>
        <span>Policy</span>
        <strong>
          {{ application.policyName }}
        </strong>
      </div>

      <div>
        <span>Customer</span>
        <strong>
          {{ application.customerName }}
        </strong>
      </div>

      <div>
        <span>Status</span>
        <strong>
          {{ application.status }}
        </strong>
      </div>

    </div>

  </div>

  <div
    class="review-card"
    *ngIf="application">

    <h3>Supporting Documents</h3>

    <div
      *ngIf="documents.length === 0"
      class="empty">

      No supporting documents found.

    </div>

    <div
      class="document"
      *ngFor="let document of documents">

      <div>

        <strong>
          {{ document.fileName }}
        </strong>

        <small>
          {{ document.contentType }}
        </small>

      </div>

      <button
        class="view"
        (click)="openDocument(document)">

        View / Download

      </button>

    </div>

  </div>

  <div
    class="actions"
    *ngIf="application &&
           application.status === 'PENDING'">

    <button
      class="reject"
      [disabled]="processing"
      (click)="reject()">

      Reject Application

    </button>

    <button
      class="approve"
      [disabled]="processing"
      (click)="approve()">

      Approve Application

    </button>

  </div>

</div>





.page {
  padding: 24px;
  max-width: 1000px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
}

.header p {
  color: #777;
}

.back {
  padding: 8px 14px;
  background: white;
  border: 1px solid #aaa;
  border-radius: 5px;
}

.review-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 22px;
  margin-bottom: 18px;
}

.review-card h3 {
  margin-top: 0;
}

.details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.details span,
.document small {
  display: block;
  color: #777;
  margin-bottom: 5px;
}

.document {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid #eee;
}

.view {
  padding: 7px 12px;
  background: white;
  border: 1px solid #777;
  border-radius: 4px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.approve,
.reject {
  padding: 10px 18px;
  border-radius: 5px;
  cursor: pointer;
}

.approve {
  border: 0;
}

.reject {
  border: 1px solid #c62828;
  background: white;
  color: #c62828;
}

.approve:disabled,
.reject:disabled {
  opacity: 0.5;
}

.error {
  color: #c62828;
  margin-bottom: 15px;
}

.success {
  color: #2e7d32;
  margin-bottom: 15px;
}

.empty {
  color: #777;
}

@media (max-width: 700px) {
  .details {
    grid-template-columns: 1fr;
  }
}





