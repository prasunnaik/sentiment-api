import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import {
  ActivatedRoute,
  Router
} from '@angular/router';

import {
  StaffUserApiService
} from '../../../services/api/staff-user-api.service';

@Component({
  selector: 'app-manage-users-new',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './manage-users-new.component.html',
  styleUrls: ['./manage-users-new.component.css']
})
export class ManageUsersNewComponent implements OnInit {

  userId: string | null = null;
  isEdit = false;

  loading = false;
  saving = false;

  error = '';
  success = '';

  selectedFile: File | null = null;
  previewUrl: string | null = null;

  form: FormGroup<{
    name: FormControl<string>;
    email: FormControl<string>;
    address: FormControl<string>;
    password: FormControl<string>;
  }>;

  constructor(
    private readonly fb: FormBuilder,
    private readonly staffUserApi: StaffUserApiService,
    private readonly route: ActivatedRoute,
    private readonly router: Router
  ) {

    this.form = this.fb.nonNullable.group({

      name: [
        '',
        [
          Validators.required,
          Validators.minLength(2),
          Validators.maxLength(100),
          Validators.pattern(
            /^[A-Za-z]+(?:[ '-][A-Za-z]+)*$/
          )
        ]
      ],

      email: [
        '',
        [
          Validators.required,
          Validators.email,
          Validators.maxLength(150)
        ]
      ],

      address: [
        '',
        [
          Validators.required,
          Validators.minLength(5),
          Validators.maxLength(250)
        ]
      ],

      password: [
        '',
        [
          Validators.required,
          Validators.minLength(6),
          Validators.maxLength(100)
        ]
      ]
    });
  }

  ngOnInit(): void {

    this.userId =
      this.route.snapshot.paramMap.get('id');

    this.isEdit = !!this.userId;

    /*
     * Password is required only when creating
     * a new staff user.
     */
    if (this.isEdit) {
      this.form.controls.password.clearValidators();
      this.form.controls.password.updateValueAndValidity();
    }

    if (this.userId) {
      this.loadUser(this.userId);
    }
  }

  loadUser(id: string): void {

    this.loading = true;
    this.error = '';

    this.staffUserApi.getById(id).subscribe({

      next: (user) => {

        this.form.patchValue({
          name: user.name,
          email: user.email,
          address: user.address
        });

        this.previewUrl =
          user.profilePictureUrl ?? null;

        this.loading = false;
      },

      error: (error: unknown) => {

        console.error(
          'Unable to load staff user.',
          error
        );

        this.error =
          'Unable to load staff user.';

        this.loading = false;
      }
    });
  }

  onFileSelected(event: Event): void {

    const input =
      event.target as HTMLInputElement;

    if (
      !input.files ||
      input.files.length === 0
    ) {
      return;
    }

    const file =
      input.files[0];

    const allowedTypes = [
      'image/jpeg',
      'image/png',
      'image/webp'
    ];

    if (!allowedTypes.includes(file.type)) {

      this.error =
        'Only JPG, PNG or WEBP images are allowed.';

      input.value = '';

      return;
    }

    const maxSize =
      5 * 1024 * 1024;

    if (file.size > maxSize) {

      this.error =
        'Profile picture must be 5 MB or smaller.';

      input.value = '';

      return;
    }

    this.error = '';
    this.selectedFile = file;

    const reader =
      new FileReader();

    reader.onload = () => {

      this.previewUrl =
        reader.result as string;
    };

    reader.readAsDataURL(file);
  }

  removeSelectedPicture(): void {

    this.selectedFile = null;
    this.previewUrl = null;
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
     * EDIT STAFF USER
     */
    if (
      this.isEdit &&
      this.userId
    ) {

      const updateRequest = {

        name:
          this.form.controls.name.value.trim(),

        email:
          this.form.controls.email.value.trim(),

        address:
          this.form.controls.address.value.trim()
      };

      this.staffUserApi
        .update(
          this.userId,
          updateRequest
        )
        .subscribe({

          next: () => {

            this.saving = false;

            this.success =
              'Staff user updated successfully.';

            setTimeout(() => {

              this.router.navigate([
                '/staff/manage-users'
              ]);

            }, 700);
          },

          error: (error: unknown) => {

            this.saving = false;

            this.error =
              this.getErrorMessage(
                error,
                'Unable to update staff user.'
              );
          }
        });

      return;
    }

    /*
     * CREATE STAFF USER
     */
    const createRequest = {

      name:
        this.form.controls.name.value.trim(),

      email:
        this.form.controls.email.value.trim(),

      address:
        this.form.controls.address.value.trim(),

      password:
        this.form.controls.password.value
    };

    this.staffUserApi
      .create(createRequest)
      .subscribe({

        next: () => {

          this.saving = false;

          this.success =
            'Staff user created successfully.';

          setTimeout(() => {

            this.router.navigate([
              '/staff/manage-users'
            ]);

          }, 700);
        },

        error: (error: unknown) => {

          this.saving = false;

          this.error =
            this.getErrorMessage(
              error,
              'Unable to create staff user.'
            );
        }
      });
  }

  cancel(): void {

    this.router.navigate([
      '/staff/manage-users'
    ]);
  }

  get nameInvalid(): boolean {

    const control =
      this.form.controls.name;

    return (
      control.invalid &&
      (
        control.dirty ||
        control.touched
      )
    );
  }

  get emailInvalid(): boolean {

    const control =
      this.form.controls.email;

    return (
      control.invalid &&
      (
        control.dirty ||
        control.touched
      )
    );
  }

  get addressInvalid(): boolean {

    const control =
      this.form.controls.address;

    return (
      control.invalid &&
      (
        control.dirty ||
        control.touched
      )
    );
  }

  get passwordInvalid(): boolean {

    const control =
      this.form.controls.password;

    return (
      control.invalid &&
      (
        control.dirty ||
        control.touched
      )
    );
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
      {{ isEdit ? 'Edit Staff User' : 'Add Staff User' }}
    </h2>

    <p class="subtitle">
      {{ isEdit
        ? 'Update staff account details'
        : 'Create a new staff account' }}
    </p>

    <div *ngIf="loading">
      Loading...
    </div>

    <form
      *ngIf="!loading"
      [formGroup]="form"
      (ngSubmit)="save()">

      <!-- NAME -->

      <div class="field">

        <label>
          Name <span>*</span>
        </label>

        <input
          type="text"
          formControlName="name"
          maxlength="100"
          placeholder="Enter name">

        <small *ngIf="nameInvalid">

          <span *ngIf="form.controls.name.errors?.['required']">
            Name is required.
          </span>

          <span *ngIf="form.controls.name.errors?.['pattern']">
            Name can contain letters, spaces, apostrophes and hyphens only.
          </span>

          <span *ngIf="form.controls.name.errors?.['minlength']">
            Name must contain at least 2 characters.
          </span>

        </small>

      </div>


      <!-- EMAIL -->

      <div class="field">

        <label>
          Email <span>*</span>
        </label>

        <input
          type="email"
          formControlName="email"
          maxlength="150"
          placeholder="Enter email">

        <small *ngIf="emailInvalid">
          Please enter a valid email address.
        </small>

      </div>


      <!-- ADDRESS -->

      <div class="field">

        <label>
          Address <span>*</span>
        </label>

        <textarea
          rows="4"
          formControlName="address"
          maxlength="250"
          placeholder="Enter address">
        </textarea>

        <small *ngIf="addressInvalid">
          Address is required and must contain valid text.
        </small>

      </div>


      <!-- PASSWORD -->

      <div
        class="field"
        *ngIf="!isEdit">

        <label>
          Password <span>*</span>
        </label>

        <input
          type="password"
          formControlName="password"
          maxlength="100"
          placeholder="Enter password">

        <small *ngIf="passwordInvalid">

          <span
            *ngIf="form.controls.password.errors?.['required']">
            Password is required.
          </span>

          <span
            *ngIf="form.controls.password.errors?.['minlength']">
            Password must contain at least 6 characters.
          </span>

        </small>

      </div>


      <!-- PROFILE PICTURE -->

      <div class="field">

        <label>
          Profile Picture
        </label>

        <input
          type="file"
          accept=".jpg,.jpeg,.png,.webp"
          (change)="onFileSelected($event)">

        <div
          class="preview"
          *ngIf="previewUrl">

          <img
            [src]="previewUrl"
            alt="Profile preview">

          <button
            type="button"
            class="remove"
            (click)="removeSelectedPicture()">
            Remove
          </button>

        </div>

        <small>
          JPG, PNG or WEBP. Maximum size: 5 MB.
        </small>

      </div>


      <!-- ERROR -->

      <div
        class="error"
        *ngIf="error">
        {{ error }}
      </div>


      <!-- SUCCESS -->

      <div
        class="success"
        *ngIf="success">
        {{ success }}
      </div>


      <!-- ACTIONS -->

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
            : (isEdit ? 'Update User' : 'Add User') }}

        </button>

      </div>

    </form>

  </div>

</div>





