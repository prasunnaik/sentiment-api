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


/* =========================
   POLICY
   ========================= */

export interface Policy {
  id: string;
  name: string;
  categoryId: string;
  categoryName?: string;
  coverageAmount: number;
  premiumAmount: number;
  durationLabel: string;
  status: string;
}

export interface PolicyCreateRequest {
  name: string;
  categoryId: string;
  coverageAmount: number;
  premiumAmount: number;
  durationLabel: string;
  status: string;
}


/* =========================
   POLICY APPLICATION
   ========================= */

export interface PolicyApplication {
  id: string;
  applicationCode?: string;
  customerId?: string;
  policyId?: string;
  policyName?: string;
  coverageType?: string;
  coverageAmount?: number;
  premiumAmount?: number;
  dateOfBirth?: string;
  address?: string;
  preferredStartDate?: string;
  nomineeName?: string;
  nomineeRelationship?: string;
  startDate?: string;
  endDate?: string;
  status: string;
  decidedBy?: string;
  decidedAt?: string;
  createdAt?: string;
}


/* =========================
   APPLICATION DOCUMENT
   ========================= */

export interface ApplicationDocument {
  id: string;
  fileName: string;
  contentType: string;
  s3Key: string;
  uploadedBy?: string;
  createdAt?: string;
}






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

  constructor(
    private readonly http: HttpClient
  ) {}

  /**
   * GET /api/policies
   */
  getAll(): Observable<Policy[]> {
    return this.http.get<Policy[]>(
      this.policyUrl
    );
  }

  /**
   * POST /api/policies
   */
  create(
    request: PolicyCreateRequest
  ): Observable<Policy> {
    return this.http.post<Policy>(
      this.policyUrl,
      request
    );
  }

  /**
   * PUT /api/policies/{id}
   */
  update(
    id: string,
    request: PolicyCreateRequest
  ): Observable<Policy> {
    return this.http.put<Policy>(
      `${this.policyUrl}/${id}`,
      request
    );
  }

  /**
   * DELETE /api/policies/{id}
   */
  delete(id: string): Observable<void> {
    return this.http.delete<void>(
      `${this.policyUrl}/${id}`
    );
  }

  /**
   * GET /api/categories
   */
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(
      this.categoryUrl
    );
  }
}






import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { PolicyApiService } from '../../../services/api/policy-api.service';

import {
  Category,
  Policy,
  PolicyCreateRequest
} from '../../../types/br04-05.types';

@Component({
  selector: 'app-policies-new',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './policies-new.component.html',
  styleUrls: ['./policies-new.component.css']
})
export class PoliciesNewComponent implements OnInit {

  policyId: string | null = null;
  isEdit = false;

  categories: Category[] = [];

  loading = false;
  saving = false;

  error = '';
  success = '';

  form: FormGroup<{
    name: FormControl<string>;
    categoryId: FormControl<string>;
    premiumAmount: FormControl<number>;
    coverageAmount: FormControl<number>;
    durationLabel: FormControl<string>;
  }>;

  constructor(
    private readonly fb: FormBuilder,
    private readonly policyApi: PolicyApiService,
    private readonly route: ActivatedRoute,
    private readonly router: Router
  ) {
    this.form = this.fb.nonNullable.group({

      name: [
        '',
        [
          Validators.required,
          Validators.minLength(2),
          Validators.maxLength(120),
          Validators.pattern(
            /^[A-Za-z0-9]+(?:[ '-][A-Za-z0-9]+)*$/
          )
        ]
      ],

      categoryId: [
        '',
        Validators.required
      ],

      premiumAmount: [
        0,
        [
          Validators.required,
          Validators.min(0.01)
        ]
      ],

      coverageAmount: [
        0,
        [
          Validators.required,
          Validators.min(0.01)
        ]
      ],

      durationLabel: [
        '',
        [
          Validators.required,
          Validators.maxLength(40)
        ]
      ]
    });
  }

  ngOnInit(): void {

    this.policyId =
      this.route.snapshot.paramMap.get('id');

    this.isEdit = !!this.policyId;

    this.loadCategories();

    if (this.policyId) {
      this.loadPolicy(this.policyId);
    }
  }

  loadCategories(): void {

    this.policyApi.getCategories().subscribe({

      next: (categories: Category[]) => {

        this.categories = categories.filter(
          (category: Category) =>
            category.status === 'ACTIVE'
        );
      },

      error: (error: unknown) => {

        console.error(
          'Unable to load categories.',
          error
        );

        this.error =
          'Unable to load active categories.';
      }
    });
  }

  loadPolicy(id: string): void {

    this.loading = true;
    this.error = '';

    this.policyApi.getAll().subscribe({

      next: (policies: Policy[]) => {

        const policy =
          policies.find(
            (item: Policy) =>
              item.id === id
          );

        if (!policy) {

          this.error =
            'Policy not found.';

          this.loading = false;
          return;
        }

        this.form.patchValue({

          name:
            policy.name,

          categoryId:
            policy.categoryId,

          premiumAmount:
            policy.premiumAmount,

          coverageAmount:
            policy.coverageAmount,

          durationLabel:
            policy.durationLabel
        });

        this.loading = false;
      },

      error: (error: unknown) => {

        console.error(
          'Unable to load policy.',
          error
        );

        this.error =
          'Unable to load policy.';

        this.loading = false;
      }
    });
  }

  save(): void {

    this.error = '';
    this.success = '';

    if (this.form.invalid) {

      this.form.markAllAsTouched();

      return;
    }

    this.saving = true;

    const request: PolicyCreateRequest = {

      name:
        this.form.controls.name.value.trim(),

      categoryId:
        this.form.controls.categoryId.value,

      premiumAmount:
        Number(
          this.form.controls.premiumAmount.value
        ),

      coverageAmount:
        Number(
          this.form.controls.coverageAmount.value
        ),

      durationLabel:
        this.form.controls.durationLabel.value.trim(),

      status: 'ACTIVE'
    };

    const operation =
      this.isEdit && this.policyId
        ? this.policyApi.update(
            this.policyId,
            request
          )
        : this.policyApi.create(
            request
          );

    operation.subscribe({

      next: () => {

        this.saving = false;

        this.success =
          this.isEdit
            ? 'Policy updated successfully.'
            : 'Policy created successfully.';

        setTimeout(() => {

          this.router.navigate([
            '/staff/policies'
          ]);

        }, 700);
      },

      error: (error: unknown) => {

        this.saving = false;

        this.error =
          this.getErrorMessage(
            error,
            'Unable to save policy.'
          );
      }
    });
  }

  cancel(): void {

    this.router.navigate([
      '/staff/policies'
    ]);
  }

  private getErrorMessage(
    error: unknown,
    defaultMessage: string
  ): string {

    if (
      error !== null &&
      typeof error === 'object' &&
      'error' in error
    ) {

      const response =
        error as {
          error?: {
            message?: string;
          };
        };

      return (
        response.error?.message ??
        defaultMessage
      );
    }

    return defaultMessage;
  }
}




