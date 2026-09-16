import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_CONFIG } from '../../core/environment/api.config';
import { DashboardMetrics } from '../../types/br04-br05.types';

@Injectable({
  providedIn: 'root'
})
export class DashboardApiService {

  private readonly url =
    `${API_CONFIG.baseUrl}/api/dashboard/metrics`;

  constructor(private http: HttpClient) {}

  getMetrics(): Observable<DashboardMetrics> {
    return this.http.get<DashboardMetrics>(this.url);
  }
}





import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_CONFIG } from '../../core/environment/api.config';

import {
  StaffUser,
  StaffCreateRequest,
  StaffUpdateRequest
} from '../../types/br04-br05.types';

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





import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_CONFIG } from '../../core/environment/api.config';

import {
  Policy,
  PolicyCreateRequest,
  Category
} from '../../types/br04-br05.types';

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






import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_CONFIG } from '../../core/environment/api.config';

import {
  PolicyApplication
} from '../../types/br04-br05.types';

@Injectable({
  providedIn: 'root'
})
export class PolicyApplicationApiService {

  private readonly url =
    `${API_CONFIG.baseUrl}/api/policy-applications`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<PolicyApplication[]> {
    return this.http.get<PolicyApplication[]>(
      this.url
    );
  }

  getPending(): Observable<PolicyApplication[]> {
    return this.http.get<PolicyApplication[]>(
      `${this.url}/pending`
    );
  }

  getById(id: string): Observable<PolicyApplication> {
    return this.http.get<PolicyApplication>(
      `${this.url}/${id}`
    );
  }

  approve(id: string): Observable<PolicyApplication> {
    return this.http.put<PolicyApplication>(
      `${this.url}/${id}/approve`,
      {}
    );
  }

  reject(id: string): Observable<PolicyApplication> {
    return this.http.put<PolicyApplication>(
      `${this.url}/${id}/reject`,
      {}
    );
  }
}





import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_CONFIG } from '../../core/environment/api.config';

import {
  ApplicationDocument
} from '../../types/br04-br05.types';

@Injectable({
  providedIn: 'root'
})
export class ApplicationDocumentApiService {

  private readonly url =
    `${API_CONFIG.baseUrl}/api/application-documents`;

  constructor(private http: HttpClient) {}

  getByApplicationId(
    applicationId: string
  ): Observable<ApplicationDocument[]> {
    return this.http.get<ApplicationDocument[]>(
      `${this.url}/application/${applicationId}`
    );
  }

  getDownloadUrl(
    documentId: string
  ): Observable<{ url: string }> {
    return this.http.get<{ url: string }>(
      `${this.url}/${documentId}/download`
    );
  }
}






import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DashboardApiService } from '../../../services/api/dashboard-api.service';
import { DashboardMetrics } from '../../../types/br04-br05.types';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  metrics: DashboardMetrics = {
    customers: 0,
    staff: 0,
    categories: 0,
    policies: 0,
    activePolicies: 0,
    applications: 0,
    claims: 0,
    payments: 0
  };

  loading = true;
  error = '';

  constructor(
    private dashboardApi: DashboardApiService
  ) {}

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {
    this.loading = true;

    this.dashboardApi.getMetrics().subscribe({
      next: response => {
        this.metrics = response;
        this.loading = false;
      },
      error: () => {
        this.error = 'Unable to load dashboard data.';
        this.loading = false;
      }
    });
  }
}






