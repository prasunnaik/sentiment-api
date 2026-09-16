import { bootstrapApplication } from '@angular/platform-browser';
import {
  provideHttpClient,
  withInterceptorsFromDi
} from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { provideRouter } from '@angular/router';

import { AppComponent } from './app/app.component';
import { AuthInterceptor } from './app/core/http/auth.interceptor';
import { routes } from './app/app.routes';

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
}).catch(err => console.error(err));





import { Routes } from '@angular/router';

import { staffGuard } from './core/rbac/staff.guard';

export const routes: Routes = [

  {
    path: '',
    redirectTo: 'auth/staff-login',
    pathMatch: 'full'
  },

  {
    path: 'staff',
    canActivate: [staffGuard],
    children: [

      {
        path: 'dashboard',
        loadComponent: () =>
          import('./pages/staff/dashboard/dashboard.component')
            .then(m => m.DashboardComponent)
      },

      {
        path: 'manage-users',
        loadComponent: () =>
          import('./pages/staff/manage-users-list/manage-users-list.component')
            .then(m => m.ManageUsersListComponent)
      },

      {
        path: 'manage-users/new',
        loadComponent: () =>
          import('./pages/staff/manage-users-new/manage-users-new.component')
            .then(m => m.ManageUsersNewComponent)
      },

      {
        path: 'manage-users/:id/edit',
        loadComponent: () =>
          import('./pages/staff/manage-users-new/manage-users-new.component')
            .then(m => m.ManageUsersNewComponent)
      },

      {
        path: 'policies',
        loadComponent: () =>
          import('./pages/staff/policies-list/policies-list.component')
            .then(m => m.PoliciesListComponent)
      },

      {
        path: 'policies/new',
        loadComponent: () =>
          import('./pages/staff/policies-new/policies-new.component')
            .then(m => m.PoliciesNewComponent)
      },

      {
        path: 'policies/:id/edit',
        loadComponent: () =>
          import('./pages/staff/policies-new/policies-new.component')
            .then(m => m.PoliciesNewComponent)
      },

      {
        path: 'approve-policies',
        loadComponent: () =>
          import('./pages/staff/approve-policies-list/approve-policies-list.component')
            .then(m => m.ApprovePoliciesListComponent)
      },

      {
        path: 'approve-policies/:id',
        loadComponent: () =>
          import('./pages/staff/approve-policies-review/approve-policies-review.component')
            .then(m => m.ApprovePoliciesReviewComponent)
      }

    ]
  }

];





import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-staff-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './staff-login.component.html',
  styleUrls: ['./staff-login.component.css']
})
export class StaffLoginComponent {

  loading = false;
  error = '';

  form = this.fb.nonNullable.group({
    email: [
      '',
      [
        Validators.required,
        Validators.email
      ]
    ],

    password: [
      '',
      [
        Validators.required
      ]
    ]
  });

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  login(): void {

    this.error = '';

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading = true;

    const request = {
      email: this.form.controls.email.value.trim(),
      password: this.form.controls.password.value
    };

    this.authService.login(request).subscribe({

      next: () => {

        this.loading = false;

        if (this.authService.isStaff()) {
          this.router.navigate(['/staff/dashboard']);
        } else {
          this.authService.logout();
          this.error = 'You are not authorized as a staff user.';
        }
      },

      error: error => {

        this.loading = false;

        this.error =
          error?.error?.message ??
          'Invalid email or password.';
      }

    });
  }
}





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
            form.controls.email.invalid &&
            (form.controls.email.touched ||
             form.controls.email.dirty)
          "
        >
          <span *ngIf="form.controls.email.hasError('required')">
            Email is required.
          </span>

          <span *ngIf="form.controls.email.hasError('email')">
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
            form.controls.password.invalid &&
            (form.controls.password.touched ||
             form.controls.password.dirty)
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
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
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
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}




import { Routes } from '@angular/router';

import { staffGuard } from './core/rbac/staff.guard';

export const routes: Routes = [

  {
    path: '',
    redirectTo: 'auth/staff-login',
    pathMatch: 'full'
  },

  {
    path: 'auth/staff-login',
    loadComponent: () =>
      import('./pages/auth/staff-login/staff-login.component')
        .then(m => m.StaffLoginComponent)
  },

  {
    path: 'staff',
    canActivate: [staffGuard],
    children: [

      {
        path: 'dashboard',
        loadComponent: () =>
          import('./pages/staff/dashboard/dashboard.component')
            .then(m => m.DashboardComponent)
      },

      {
        path: 'manage-users',
        loadComponent: () =>
          import('./pages/staff/manage-users-list/manage-users-list.component')
            .then(m => m.ManageUsersListComponent)
      },

      {
        path: 'manage-users/new',
        loadComponent: () =>
          import('./pages/staff/manage-users-new/manage-users-new.component')
            .then(m => m.ManageUsersNewComponent)
      },

      {
        path: 'manage-users/:id/edit',
        loadComponent: () =>
          import('./pages/staff/manage-users-new/manage-users-new.component')
            .then(m => m.ManageUsersNewComponent)
      },

      {
        path: 'policies',
        loadComponent: () =>
          import('./pages/staff/policies-list/policies-list.component')
            .then(m => m.PoliciesListComponent)
      },

      {
        path: 'policies/new',
        loadComponent: () =>
          import('./pages/staff/policies-new/policies-new.component')
            .then(m => m.PoliciesNewComponent)
      },

      {
        path: 'policies/:id/edit',
        loadComponent: () =>
          import('./pages/staff/policies-new/policies-new.component')
            .then(m => m.PoliciesNewComponent)
      },

      {
        path: 'approve-policies',
        loadComponent: () =>
          import('./pages/staff/approve-policies-list/approve-policies-list.component')
            .then(m => m.ApprovePoliciesListComponent)
      },

      {
        path: 'approve-policies/:id',
        loadComponent: () =>
          import('./pages/staff/approve-policies-review/approve-policies-review.component')
            .then(m => m.ApprovePoliciesReviewComponent)
      }

    ]
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
import { routes } from './app/app.routes';

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
}).catch(err => console.error(err));





import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `
    <router-outlet></router-outlet>
  `
})
export class 
