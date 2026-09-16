import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import {
  StaffUser
} from '../../../types/br04-05.types';

import {
  StaffUserApiService
} from '../../../services/api/staff-user-api.service';

@Component({
  selector: 'app-manage-users-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './manage-users-list.component.html',
  styleUrls: ['./manage-users-list.component.css']
})
export class ManageUsersListComponent implements OnInit {

  users: StaffUser[] = [];
  loading = true;
  error = '';

  constructor(
    private staffUserApi: StaffUserApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.loading = true;

    this.staffUserApi.getAll().subscribe({
      next: users => {
        this.users = users;
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load staff users.';
        this.loading = false;
      }
    });
  }

  addUser(): void {
    this.router.navigate(['/staff/manage-users/new']);
  }

  editUser(id: string): void {
    this.router.navigate([
      '/staff/manage-users',
      id,
      'edit'
    ]);
  }

  deleteUser(user: StaffUser): void {

    const confirmed = window.confirm(
      `Delete staff user "${user.name}"?`
    );

    if (!confirmed) {
      return;
    }

    this.staffUserApi.delete(user.id).subscribe({
      next: () => {
        this.loadUsers();
      },
      error: () => {
        this.error = 'Unable to delete staff user.';
      }
    });
  }
}
<div class="page">

  <div class="header">
    <div>
      <h2>Manage Users</h2>
      <p>View and manage staff users</p>
    </div>

    <button
      class="primary-button"
      type="button"
      (click)="addUser()">
      + Add User
    </button>
  </div>

  <div *ngIf="loading">
    Loading users...
  </div>

  <div *ngIf="error" class="error">
    {{ error }}
  </div>

  <div class="table-container" *ngIf="!loading">

    <table>
      <thead>
        <tr>
          <th>NAME</th>
          <th>EMAIL</th>
          <th>ADDRESS</th>
          <th>ACTIONS</th>
        </tr>
      </thead>

      <tbody>

        <tr *ngFor="let user of users">

          <td>
            <div class="user-cell">

              <img
                *ngIf="user.profilePictureUrl"
                [src]="user.profilePictureUrl"
                alt="Profile">

              <div
                *ngIf="!user.profilePictureUrl"
                class="avatar">
                {{ user.name.charAt(0).toUpperCase() }}
              </div>

              <span>{{ user.name }}</span>

            </div>
          </td>

          <td>{{ user.email }}</td>

          <td>{{ user.address }}</td>

          <td class="actions">

            <button
              type="button"
              class="edit"
              (click)="editUser(user.id)">
              Edit
            </button>

            <button
              type="button"
              class="delete"
              (click)="deleteUser(user)">
              Delete
            </button>

          </td>

        </tr>

        <tr *ngIf="users.length === 0">
          <td colspan="4">
            No staff users found.
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

.primary-button {
  border: 0;
  border-radius: 5px;
  padding: 10px 18px;
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
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  font-size: 12px;
  color: #666;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-cell img,
.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
}

.user-cell img {
  object-fit: cover;
}

.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eee;
}

.actions {
  display: flex;
  gap: 8px;
}

.edit,
.delete {
  background: transparent;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.edit {
  border: 1px solid #888;
}

.delete {
  border: 1px solid #d66;
  color: #c00;
}

.error {
  color: #c62828;
}



