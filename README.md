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

  constructor(
    private readonly http: HttpClient
  ) {}

  login(
    request: StaffLoginRequest
  ): Observable<LoginResponse> {

    return this.http
      .post<LoginResponse>(
        this.loginUrl,
        request
      )
      .pipe(
        tap((response: LoginResponse) => {

          /*
           * Backend returns:
           *
           * {
           *   "access_token": "...",
           *   "token_type": "Bearer",
           *   "user_id": "...",
           *   "email": "...",
           *   "role": "STAFF"
           * }
           */

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
    return localStorage.getItem(
      this.TOKEN_KEY
    );
  }

  getRole(): string | null {
    return localStorage.getItem(
      this.ROLE_KEY
    );
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  isStaff(): boolean {
    return this.getRole() === 'STAFF';
  }

  logout(): void {
    localStorage.removeItem(
      this.TOKEN_KEY
    );

    localStorage.removeItem(
      this.ROLE_KEY
    );
  }
}
