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
export class AppComponent {
}




import { bootstrapApplication } from '@angular/platform-browser';
import {
  provideHttpClient,
  withInterceptorsFromDi
} from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { provideRouter } from '@angular/router';

import { AppComponent } from './app/app.component';
import { routes } from './app/routing/app.routes';
import { AuthInterceptor } from './app/core/http/auth.interceptor';

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

import { staffGuard } from '../core/rbac/staff.guard';

export const routes: Routes = [

  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'staff/dashboard'
  },

  {
    path: 'staff',
    canActivate: [staffGuard],
    children: [

      {
        path: '',
        pathMatch: 'full',
        redirectTo: 'dashboard'
      },

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



<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>InsureWise Angular</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body>
  <app-root></app-root>
</body>
</html>
