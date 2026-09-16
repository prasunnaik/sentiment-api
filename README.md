import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_CONFIG } from '../../core/environment/api.config';

import {
  Policy,
  PolicyCreateRequest,
  Category
} from '../../types/br04-05.types';

@Injectable({
  providedIn: 'root'
})
export class PolicyApiService {

  private readonly policyUrl =
    `${API_CONFIG.baseUrl}/api/policies`;

  private readonly categoryUrl =
    `${API_CONFIG.baseUrl}/api/categories`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<Policy[]> {
    return this.http.get<Policy[]>(
      this.policyUrl
    );
  }

  getActive(): Observable<Policy[]> {
    return this.http.get<Policy[]>(
      `${this.policyUrl}/active`
    );
  }

  create(
    request: PolicyCreateRequest
  ): Observable<Policy> {
    return this.http.post<Policy>(
      this.policyUrl,
      request
    );
  }

  update(
    id: string,
    request: PolicyCreateRequest
  ): Observable<Policy> {
    return this.http.put<Policy>(
      `${this.policyUrl}/${id}`,
      request
    );
  }

  approve(id: string): Observable<Policy> {
    return this.http.put<Policy>(
      `${this.policyUrl}/${id}/approve`,
      {}
    );
  }

  reject(id: string): Observable<Policy> {
    return this.http.put<Policy>(
      `${this.policyUrl}/${id}/reject`,
      {}
    );
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(
      `${this.policyUrl}/${id}`
    );
  }

  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(
      this.categoryUrl
    );
  }
}
