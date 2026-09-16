import { Routes } from '@angular/router';

import { staffGuard } from '../core/rbac/staff.guard';

export const routes: Routes = [

  /*
   * Keep your existing auth/customer/shared routes here.
   */

  {
    path: 'staff',
    canActivate: [staffGuard],
    children: [

      {
        path: 'dashboard',
        loadComponent: () =>
          import('../pages/staff/dashboard/dashboard.component')
            .then(m => m.DashboardComponent)
      },

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
  }

];
import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppComponent } from './app/app.component';
import { AuthInterceptor } from './app/core/http/auth.interceptor';

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(withInterceptorsFromDi()),

    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ]
}).catch(err => console.error(err));






