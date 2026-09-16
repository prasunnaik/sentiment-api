import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

import { API_CONFIG } from '../../config/api.config';

export interface StaffLoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  email: string;
  role: string;
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

    return this.http
      .post<LoginResponse>(this.loginUrl, request)
      .pipe(
        tap(response => {

          // Backend returns "access_token", NOT "token"
          if (response?.access_token) {

            localStorage.setItem(
              this.TOKEN_KEY,
              response.access_token
            );

            localStorage.setItem(
              this.ROLE_KEY,
              response.role ?? ''
            );
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
  HttpInterceptor,
  HttpRequest,
  HttpHandler
} from '@angular/common/http';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  intercept(req: HttpRequest<any>, next: HttpHandler) {

    const token =
      localStorage.getItem('insurewise_token');

    if (token) {

      req = req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    return next.handle(req);
  }
}





