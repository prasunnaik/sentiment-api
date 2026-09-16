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
    private readonly staffUserApi: StaffUserApiService,
    private readonly router: Router
  ) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {

    this.loading = true;
    this.error = '';

    this.staffUserApi.getAll().subscribe({

      next: (users) => {

        this.users = users;
        this.loading = false;
      },

      error: (error: unknown) => {

        console.error(
          'Unable to load staff users.',
          error
        );

        this.error =
          'Unable to load staff users.';

        this.loading = false;
      }
    });
  }

  addUser(): void {

    this.router.navigate([
      '/staff/manage-users/new'
    ]);
  }

  editUser(id: string): void {

    this.router.navigate([
      '/staff/manage-users',
      id,
      'edit'
    ]);
  }

  deleteUser(user: StaffUser): void {

    const confirmed =
      window.confirm(
        `Delete staff user "${user.fullName}"?`
      );

    if (!confirmed) {
      return;
    }

    this.error = '';

    this.staffUserApi
      .delete(user.id)
      .subscribe({

        next: () => {

          this.loadUsers();
        },

        error: (error: unknown) => {

          console.error(
            'Unable to delete staff user.',
            error
          );

          this.error =
            'Unable to delete staff user.';
        }
      });
  }
}




<div class="page">

  <!-- HEADER -->

  <div class="header">

    <div>
      <h2>Manage Users</h2>

      <p>
        View and manage staff users
      </p>
    </div>

    <button
      class="primary-button"
      type="button"
      (click)="addUser()">

      + Add User

    </button>

  </div>


  <!-- LOADING -->

  <div
    *ngIf="loading"
    class="loading">

    Loading users...

  </div>


  <!-- ERROR -->

  <div
    *ngIf="error"
    class="error">

    {{ error }}

  </div>


  <!-- TABLE -->

  <div
    class="table-container"
    *ngIf="!loading">

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

        <!-- STAFF USERS -->

        <tr
          *ngFor="let user of users">

          <td>

            <div class="user-cell">

              <!-- Profile Picture -->

              <img
                *ngIf="user.profilePictureUrl"
                [src]="user.profilePictureUrl"
                alt="Profile picture">


              <!-- Default Avatar -->

              <div
                *ngIf="!user.profilePictureUrl"
                class="avatar">

                {{ user.fullName.charAt(0).toUpperCase() }}

              </div>


              <!-- Full Name -->

              <span>
                {{ user.fullName }}
              </span>

            </div>

          </td>


          <!-- EMAIL -->

          <td>
            {{ user.email }}
          </td>


          <!-- ADDRESS -->

          <td>
            {{ user.address }}
          </td>


          <!-- ACTIONS -->

          <td>

            <div class="actions">

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

            </div>

          </td>

        </tr>


        <!-- NO USERS -->

        <tr
          *ngIf="users.length === 0">

          <td
            colspan="4"
            class="empty">

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


/* =========================
   HEADER
   ========================= */

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  font-size: 26px;
}

.header p {
  margin: 6px 0 0;
  color: #777;
}


/* =========================
   ADD USER BUTTON
   ========================= */

.primary-button {
  border: 0;
  border-radius: 5px;
  padding: 10px 18px;
  cursor: pointer;
  background: #008c95;
  color: white;
  font-size: 14px;
}

.primary-button:hover {
  background: #00747b;
}


/* =========================
   LOADING
   ========================= */

.loading {
  padding: 20px 0;
  color: #777;
}


/* =========================
   TABLE
   ========================= */

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
  font-weight: 600;
  background: #fafafa;
}

tbody tr:last-child td {
  border-bottom: none;
}


/* =========================
   USER CELL
   ========================= */

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
  flex-shrink: 0;
}

.user-cell img {
  object-fit: cover;
}

.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eee;
  color: #555;
  font-weight: 600;
}

.user-cell span {
  font-weight: 500;
}


/* =========================
   ACTIONS
   ========================= */

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
  font-size: 13px;
}

.edit {
  border: 1px solid #888;
  color: #444;
}

.edit:hover {
  background: #f5f5f5;
}

.delete {
  border: 1px solid #d66;
  color: #c00;
}

.delete:hover {
  background: #fff5f5;
}


/* =========================
   ERROR
   ========================= */

.error {
  color: #c62828;
  margin: 12px 0;
  padding: 10px;
  background: #fff5f5;
  border-radius: 5px;
}


/* =========================
   EMPTY STATE
   ========================= */

.empty {
  text-align: center;
  color: #777;
  padding: 30px;
}


/* =========================
   RESPONSIVE
   ========================= */

@media (max-width: 700px) {

  .page {
    padding: 16px;
  }

  .header {
    align-items: flex-start;
    gap: 15px;
    flex-direction: column;
  }

  .primary-button {
    width: 100%;
  }

  th,
  td {
    padding: 10px;
  }

}
