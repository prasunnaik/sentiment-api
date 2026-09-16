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

  /*
   * Explicitly define the form controls.
   * This allows TypeScript to recognise:
   * policyName, categoryId, premium,
   * coverageAmount and duration.
   */
  form: FormGroup<{
    policyName: FormControl<string>;
    categoryId: FormControl<string>;
    premium: FormControl<number>;
    coverageAmount: FormControl<number>;
    duration: FormControl<number>;
  }>;

  constructor(
    private readonly fb: FormBuilder,
    private readonly policyApi: PolicyApiService,
    private readonly route: ActivatedRoute,
    private readonly router: Router
  ) {
    /*
     * FormBuilder is available here because it has already
     * been injected by Angular.
     */
    this.form = this.fb.nonNullable.group({

      policyName: [
        '',
        [
          Validators.required,
          Validators.minLength(2),
          Validators.maxLength(100),

          /*
           * Allows letters/numbers with optional spaces,
           * apostrophes or hyphens between words.
           *
           * Examples allowed:
           * Health Insurance
           * Life-Insurance
           * Motor Insurance 2
           * Children's Insurance
           *
           * Examples rejected:
           * Health@Insurance
           * Life#Insurance
           * Policy$
           * Test%
           */
          Validators.pattern(
            /^[A-Za-z0-9]+(?:[ '-][A-Za-z0-9]+)*$/
          )
        ]
      ],

      categoryId: [
        '',
        Validators.required
      ],

      premium: [
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

      duration: [
        1,
        [
          Validators.required,
          Validators.min(1),
          Validators.max(100)
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

          policyName:
            policy.policyName,

          categoryId:
            policy.categoryId,

          premium:
            policy.premium,

          coverageAmount:
            policy.coverageAmount,

          duration:
            policy.duration
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

    const request = {

      policyName:
        this.form.controls.policyName.value.trim(),

      categoryId:
        this.form.controls.categoryId.value,

      premium:
        Number(
          this.form.controls.premium.value
        ),

      coverageAmount:
        Number(
          this.form.controls.coverageAmount.value
        ),

      duration:
        Number(
          this.form.controls.duration.value
        )
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
<div class="page">

  <div class="form-card">

    <h2>
      {{ isEdit ? 'Edit Policy' : 'Add Policy' }}
    </h2>

    <p>
      Create or update an insurance policy.
    </p>

    <form
      [formGroup]="form"
      (ngSubmit)="save()">

      <div class="field">

        <label>Policy Name *</label>

        <input
          type="text"
          formControlName="policyName"
          maxlength="100"
          placeholder="Enter policy name">

        <small
          *ngIf="form.controls.policyName.invalid &&
                 form.controls.policyName.touched">

          Policy name is required and can contain
          letters, numbers, spaces, hyphens and apostrophes.
        </small>

      </div>

      <div class="field">

        <label>Category *</label>

        <select formControlName="categoryId">

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
          *ngIf="form.controls.categoryId.invalid &&
                 form.controls.categoryId.touched">

          Category is required.
        </small>

      </div>

      <div class="two-columns">

        <div class="field">

          <label>Premium Amount *</label>

          <input
            type="number"
            min="0.01"
            step="0.01"
            formControlName="premium">

          <small
            *ngIf="form.controls.premium.invalid &&
                   form.controls.premium.touched">

            Premium must be greater than zero.
          </small>

        </div>

        <div class="field">

          <label>Coverage Amount *</label>

          <input
            type="number"
            min="0.01"
            step="0.01"
            formControlName="coverageAmount">

          <small
            *ngIf="form.controls.coverageAmount.invalid &&
                   form.controls.coverageAmount.touched">

            Coverage must be greater than zero.
          </small>

        </div>

      </div>

      <div class="field">

        <label>Duration *</label>

        <input
          type="number"
          min="1"
          formControlName="duration">

        <small
          *ngIf="form.controls.duration.invalid &&
                 form.controls.duration.touched">

          Duration must be at least 1.
        </small>

      </div>

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

          {{ saving ? 'Saving...' : 'Save Policy' }}

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
}

.primary {
  border: 0;
}

.secondary {
  background: white;
  border: 1px solid #aaa;
}

.error {
  color: #c62828;
}

.success {
  color: #2e7d32;
}

@media (max-width: 700px) {
  .two-columns {
    grid-template-columns: 1fr;
  }
}
