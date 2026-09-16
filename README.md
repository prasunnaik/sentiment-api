<div class="login-page">

  <div class="login-card">

    <div class="login-header">
      <h1>InsureWise</h1>
      <p>Staff Login</p>
    </div>

    <form [formGroup]="form" (ngSubmit)="login()">

      <div class="form-group">

        <label for="email">
          Email
        </label>

        <input
          id="email"
          type="email"
          formControlName="email"
          placeholder="Enter your email"
        />

        <div
          class="validation-error"
          *ngIf="
            form.get('email')?.invalid &&
            (form.get('email')?.touched ||
             form.get('email')?.dirty)
          "
        >

          <span *ngIf="form.get('email')?.hasError('required')">
            Email is required.
          </span>

          <span *ngIf="form.get('email')?.hasError('email')">
            Enter a valid email address.
          </span>

        </div>

      </div>


      <div class="form-group">

        <label for="password">
          Password
        </label>

        <input
          id="password"
          type="password"
          formControlName="password"
          placeholder="Enter your password"
        />

        <div
          class="validation-error"
          *ngIf="
            form.get('password')?.invalid &&
            (form.get('password')?.touched ||
             form.get('password')?.dirty)
          "
        >
          Password is required.
        </div>

      </div>


      <div
        class="error-message"
        *ngIf="error"
      >
        {{ error }}
      </div>


      <button
        type="submit"
        [disabled]="loading"
      >
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>

    </form>

  </div>

</div>






.login-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f4f6f8;
  padding: 20px;
  box-sizing: border-box;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
}

.login-header p {
  margin-top: 8px;
  color: #666666;
  font-size: 18px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

.form-group input {
  width: 100%;
  box-sizing: border-box;
  padding: 12px 14px;
  border: 1px solid #cccccc;
  border-radius: 6px;
  font-size: 15px;
}

.form-group input:focus {
  outline: none;
  border-color: #333333;
}

.validation-error {
  margin-top: 6px;
  color: #d32f2f;
  font-size: 13px;
}

.error-message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 6px;
  background: #fdecea;
  color: #d32f2f;
  font-size: 14px;
}

button {
  width: 100%;
  padding: 13px;
  border: none;
  border-radius: 6px;
  background: #222222;
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

button:hover:not(:disabled) {
  opacity: 0.9;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}





import { inject } from '@angular/core';
import {
  CanActivateFn,
  Router
} from '@angular/router';

import { AuthService } from '../auth/auth.service';

export const staffGuard: CanActivateFn = () => {

  const authService = inject(AuthService);
  const router = inject(Router);

  if (
    authService.isLoggedIn() &&
    authService.isStaff()
  ) {
    return true;
  }

  authService.logout();

  return router.createUrlTree(['/auth/staff-login']);
};






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
      import('../pages/auth/staff-login/staff-login.component')
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




import { bootstrapApplication } from '@angular/platform-browser';

import {
  provideHttpClient,
  withInterceptorsFromDi
} from '@angular/common/http';

import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { provideRouter } from '@angular/router';

import { AppComponent } from './app/app.component';

import { AuthInterceptor } from './app/core/http/auth.interceptor';

import { routes } from './app/routing/app.routes';


bootstrapApplication(AppComponent, {

  providers: [

    provideRouter(routes),

    provideHttpClient(
      withInterceptorsFromDi()
    ),

    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }

  ]

}).catch(error => console.error(error));





