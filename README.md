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
  Policy
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
    coverageAmount: FormControl<number>;
    premiumAmount: FormControl<number>;
    durationLabel: FormControl<string>;
    status: FormControl<string>;
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

      coverageAmount: [
        0,
        [
          Validators.required,
          Validators.min(0.01)
        ]
      ],

      premiumAmount: [
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
      ],

      status: [
        'ACTIVE',
        Validators.required
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

        const policy = policies.find(
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

          name: policy.name,

          categoryId:
            policy.categoryId,

          coverageAmount:
            policy.coverageAmount,

          premiumAmount:
            policy.premiumAmount,

          durationLabel:
            policy.durationLabel,

          status:
            policy.status

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

    /*
     * IMPORTANT:
     * These names exactly match PolicyCreateRequest
     * and PolicyUpdateRequest in Spring Boot.
     */
    const request = {

      name:
        this.form.controls.name.value.trim(),

      categoryId:
        this.form.controls.categoryId.value,

      coverageAmount:
        Number(
          this.form.controls.coverageAmount.value
        ),

      premiumAmount:
        Number(
          this.form.controls.premiumAmount.value
        ),

      durationLabel:
        this.form.controls.durationLabel.value.trim(),

      status:
        this.form.controls.status.value

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

        console.error(
          'Unable to save policy.',
          error
        );

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





<div class="page">

  <div class="form-card">

    <h2>
      {{ isEdit ? 'Edit Policy' : 'Add Policy' }}
    </h2>

    <p>
      {{ isEdit
        ? 'Update the insurance policy details.'
        : 'Create a new insurance policy.'
      }}
    </p>

    <div
      class="error"
      *ngIf="error">

      {{ error }}

    </div>

    <div
      class="success"
      *ngIf="success">

      {{ success }}

    </div>

    <div
      class="loading"
      *ngIf="loading">

      Loading policy...

    </div>

    <form
      *ngIf="!loading"
      [formGroup]="form"
      (ngSubmit)="save()">

      <!-- POLICY NAME -->

      <div class="field">

        <label for="name">
          Policy Name *
        </label>

        <input
          id="name"
          type="text"
          formControlName="name"
          maxlength="120"
          placeholder="Enter policy name">

        <small
          *ngIf="
            form.controls.name.invalid &&
            form.controls.name.touched
          ">

          Policy name is required.

        </small>

      </div>


      <!-- CATEGORY -->

      <div class="field">

        <label for="categoryId">
          Category *
        </label>

        <select
          id="categoryId"
          formControlName="categoryId">

          <option value="">
            Select category
          </option>

          <option
            *ngFor="let category of categories"
            [value]="category.id">

            {{ category.name }}

          </option>

        </select>

        <small
          *ngIf="
            form.controls.categoryId.invalid &&
            form.controls.categoryId.touched
          ">

          Category is required.

        </small>

      </div>


      <!-- COVERAGE + PREMIUM -->

      <div class="two-columns">

        <div class="field">

          <label for="coverageAmount">
            Coverage Amount *
          </label>

          <input
            id="coverageAmount"
            type="number"
            min="0.01"
            step="0.01"
            formControlName="coverageAmount"
            placeholder="Enter coverage amount">

          <small
            *ngIf="
              form.controls.coverageAmount.invalid &&
              form.controls.coverageAmount.touched
            ">

            Coverage amount must be greater than zero.

          </small>

        </div>


        <div class="field">

          <label for="premiumAmount">
            Premium Amount *
          </label>

          <input
            id="premiumAmount"
            type="number"
            min="0.01"
            step="0.01"
            formControlName="premiumAmount"
            placeholder="Enter premium amount">

          <small
            *ngIf="
              form.controls.premiumAmount.invalid &&
              form.controls.premiumAmount.touched
            ">

            Premium amount must be greater than zero.

          </small>

        </div>

      </div>


      <!-- DURATION -->

      <div class="field">

        <label for="durationLabel">
          Duration *
        </label>

        <input
          id="durationLabel"
          type="text"
          maxlength="40"
          formControlName="durationLabel"
          placeholder="Example: 1 Year">

        <small
          *ngIf="
            form.controls.durationLabel.invalid &&
            form.controls.durationLabel.touched
          ">

          Duration is required.

        </small>

      </div>


      <!-- STATUS -->

      <div class="field">

        <label for="status">
          Status *
        </label>

        <select
          id="status"
          formControlName="status">

          <option value="ACTIVE">
            ACTIVE
          </option>

          <option value="DRAFT">
            DRAFT
          </option>

          <option value="INACTIVE">
            INACTIVE
          </option>

        </select>

      </div>


      <!-- BUTTONS -->

      <div class="actions">

        <button
          type="button"
          class="secondary"
          (click)="cancel()">

          Cancel

        </button>

        <button
          type="submit"
          class="primary"
          [disabled]="saving">

          {{ saving
            ? 'Saving...'
            : (isEdit ? 'Update Policy' : 'Add Policy')
          }}

        </button>

      </div>

    </form>

  </div>

</div>






.page {
  padding: 24px;
}

.form-card {
  max-width: 750px;
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 28px;
  box-sizing: border-box;
}

.form-card h2 {
  margin: 0;
}

.form-card > p {
  color: #777;
  margin-bottom: 25px;
}

.field {
  margin-bottom: 18px;
}

label {
  display: block;
  margin-bottom: 7px;
  font-weight: 600;
}

input,
select {
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}

input:focus,
select:focus {
  outline: none;
  border-color: #777;
}

.two-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

small {
  display: block;
  margin-top: 5px;
  color: #c62828;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 25px;
}

.primary,
.secondary {
  padding: 10px 18px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.primary {
  border: 0;
  background: #263238;
  color: white;
}

.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.secondary {
  background: white;
  border: 1px solid #aaa;
}

.error {
  margin-bottom: 15px;
  padding: 10px;
  background: #ffebee;
  color: #c62828;
  border-radius: 5px;
}

.success {
  margin-bottom: 15px;
  padding: 10px;
  background: #e8f5e9;
  color: #2e7d32;
  border-radius: 5px;
}

.loading {
  padding: 20px 0;
  color: #777;
}

@media (max-width: 700px) {

  .two-columns {
    grid-template-columns: 1fr;
  }

  .form-card {
    padding: 20px;
  }
}





create(request: {
  name: string;
  categoryId: string;
  coverageAmount: number;
  premiumAmount: number;
  durationLabel: string;
  status: string;
}) {
  return this.http.post<Policy>(
    `${API_URL}/api/policies`,
    request
  );
}







update(
  id: string,
  request: {
    name: string;
    categoryId: string;
    coverageAmount: number;
    premiumAmount: number;
    durationLabel: string;
    status: string;
  }
) {
  return this.http.put<Policy>(
    `${API_URL}/api/policies/${id}`,
    request
  );
}
