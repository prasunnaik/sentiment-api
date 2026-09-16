import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_CONFIG } from '../../core/environment/api.config';

import {
  StaffUser,
  StaffCreateRequest,
  StaffUpdateRequest
} from '../../types/br04-05.types';

@Injectable({
  providedIn: 'root'
})
export class StaffUserApiService {

  private readonly url =
    `${API_CONFIG.baseUrl}/api/staff/users`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<StaffUser[]> {
    return this.http.get<StaffUser[]>(this.url);
  }

  getById(id: string): Observable<StaffUser> {
    return this.http.get<StaffUser>(
      `${this.url}/${id}`
    );
  }

  create(request: StaffCreateRequest): Observable<StaffUser> {
    return this.http.post<StaffUser>(
      this.url,
      request
    );
  }

  update(
    id: string,
    request: StaffUpdateRequest
  ): Observable<StaffUser> {
    return this.http.put<StaffUser>(
      `${this.url}/${id}`,
      request
    );
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(
      `${this.url}/${id}`
    );
  }
}
