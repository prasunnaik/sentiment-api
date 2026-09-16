import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import {
  Policy
} from '../../../types/br04-br05.types';

import {
  PolicyApiService
} from '../../../services/api/policy-api.service';

@Component({
  selector: 'app-policies-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './policies-list.component.html',
  styleUrls: ['./policies-list.component.css']
})
export class PoliciesListComponent implements OnInit {

  policies: Policy[] = [];
  loading = true;
  error = '';

  constructor(
    private policyApi: PolicyApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadPolicies();
  }

  loadPolicies(): void {

    this.loading = true;

    this.policyApi.getAll().subscribe({
      next: policies => {
        this.policies = policies;
        this.loading = false;
      },

      error: () => {
        this.error = 'Unable to load policies.';
        this.loading = false;
      }
    });
  }

  addPolicy(): void {
    this.router.navigate([
      '/staff/policies/new'
    ]);
  }

  editPolicy(id: string): void {
    this.router.navigate([
      '/staff/policies',
      id,
      'edit'
    ]);
  }

  deletePolicy(policy: Policy): void {

    if (!window.confirm(
      `Delete policy "${policy.policyName}"?`
    )) {
      return;
    }

    this.policyApi.delete(policy.id).subscribe({
      next: () => this.loadPolicies(),
      error: () => {
        this.error = 'Unable to delete policy.';
      }
    });
  }
}






<div class="page">

  <div class="header">

    <div>
      <h2>Manage Policies</h2>
      <p>View and manage insurance policies</p>
    </div>

    <button
      class="primary"
      (click)="addPolicy()">
      + Add Policy
    </button>

  </div>

  <div *ngIf="loading">
    Loading policies...
  </div>

  <div *ngIf="error" class="error">
    {{ error }}
  </div>

  <div
    class="table-container"
    *ngIf="!loading">

    <table>

      <thead>
        <tr>
          <th>POLICY NAME</th>
          <th>CATEGORY</th>
          <th>PREMIUM</th>
          <th>COVERAGE</th>
          <th>DURATION</th>
          <th>STATUS</th>
          <th>ACTIONS</th>
        </tr>
      </thead>

      <tbody>

        <tr *ngFor="let policy of policies">

          <td>{{ policy.policyName }}</td>

          <td>
            {{ policy.categoryName || policy.categoryId }}
          </td>

          <td>
            {{ policy.premium | currency:'INR' }}
          </td>

          <td>
            {{ policy.coverageAmount | currency:'INR' }}
          </td>

          <td>
            {{ policy.duration }}
          </td>

          <td>
            <span class="status">
              {{ policy.status }}
            </span>
          </td>

          <td>

            <button
              class="edit"
              (click)="editPolicy(policy.id)">
              Edit
            </button>

            <button
              class="delete"
              (click)="deletePolicy(policy)">
              Delete
            </button>

          </td>

        </tr>

        <tr *ngIf="policies.length === 0">
          <td colspan="7">
            No policies found.
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

.primary {
  border: 0;
  padding: 10px 18px;
  border-radius: 5px;
  cursor: pointer;
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

.status {
  font-size: 13px;
}

.edit,
.delete {
  padding: 6px 10px;
  margin-right: 5px;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.edit {
  border: 1px solid #888;
}

.delete {
  border: 1px solid #c62828;
  color: #c62828;
}

.error {
  color: #c62828;
}






