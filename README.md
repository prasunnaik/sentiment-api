export const API_CONFIG = {
  baseUrl: 'http://localhost:8080'
};



import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { API_CONFIG } from '../environment/api.config';

export interface StaffLoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  role?: string;
  expiresIn?: number;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly TOKEN_KEY = 'insurewise_token';
  private readonly ROLE_KEY = 'insurewise_role';

  private readonly loginUrl =
    `${API_CONFIG.baseUrl}/auth/staff/login`;

  constructor(private http: HttpClient) {}

  login(request: StaffLoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(this.loginUrl, request).pipe(
      tap(response => {
        if (response?.token) {
          localStorage.setItem(this.TOKEN_KEY, response.token);

          if (response.role) {
            localStorage.setItem(this.ROLE_KEY, response.role);
          } else {
            localStorage.setItem(this.ROLE_KEY, 'STAFF');
          }
        }
      })
    );
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  getRole(): string | null {
    return localStorage.getItem(this.ROLE_KEY);
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  isStaff(): boolean {
    return this.getRole() === 'STAFF';
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.ROLE_KEY);
  }
}




import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../auth/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService) {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<unknown>> {

    const token = this.authService.getToken();

    if (!token) {
      return next.handle(request);
    }

    const authenticatedRequest = request.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });

    return next.handle(authenticatedRequest);
  }
}





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






import { inject } from '@angular/core';
import {
  CanActivateFn,
  Router
} from '@angular/router';

import { AuthService } from '../auth/auth.service';

export const staffGuard: CanActivateFn = () => {

  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isLoggedIn() && authService.isStaff()) {
    return true;
  }

  authService.logout();

  return router.createUrlTree(['/auth/staff-login']);
};





export interface DashboardMetrics {
  customers: number;
  staff: number;
  categories: number;
  policies: number;
  activePolicies: number;
  applications: number;
  claims: number;
  payments: number;
}

export interface StaffUser {
  id: string;
  name: string;
  email: string;
  address: string;
  profilePictureUrl?: string | null;
}

export interface StaffCreateRequest {
  name: string;
  email: string;
  address: string;
}

export interface StaffUpdateRequest {
  name: string;
  email: string;
  address: string;
}

export interface Category {
  id: string;
  name: string;
  status: string;
}

export interface Policy {
  id: string;
  policyName: string;
  categoryId: string;
  categoryName?: string;
  premium: number;
  coverageAmount: number;
  duration: number;
  status: string;
}

export interface PolicyCreateRequest {
  policyName: string;
  categoryId: string;
  premium: number;
  coverageAmount: number;
  duration: number;
}

export interface PolicyApplication {
  id: string;
  applicationCode?: string;
  policyId?: string;
  policyName?: string;
  customerName?: string;
  status: string;
  createdAt?: string;
}

export interface ApplicationDocument {
  id: string;
  fileName: string;
  contentType: string;
  s3Key: string;
  uploadedBy?: string;
  createdAt?: string;
}





