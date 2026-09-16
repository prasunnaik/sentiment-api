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

import {
  StaffCreateRequest,
  StaffUpdateRequest
} from '../../../types/br04-05.types';

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
    fullname: FormControl<string>;
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

      fullname: [
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
     *
     * During edit, password is not sent.
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

        /*
         * Backend returns fullName.
         *
         * Angular form control is called fullname.
         */
        this.form.patchValue({

          fullname:
            user.fullName,

          email:
            user.email,

          address:
            user.address
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

      this.selectedFile = null;

      return;
    }

    const maxSize =
      5 * 1024 * 1024;

    if (file.size > maxSize) {

      this.error =
        'Profile picture must be 5 MB or smaller.';

      input.value = '';

      this.selectedFile = null;

      return;
    }

    this.error = '';

    this.selectedFile = file;

    /*
     * Create local preview.
     */
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

    /*
     * Validate form.
     */
    if (this.form.invalid) {

      this.form.markAllAsTouched();

      return;
    }

    this.saving = true;

    /*
     * =========================
     * EDIT STAFF USER
     * =========================
     */
    if (
      this.isEdit &&
      this.userId
    ) {

      const updateRequest: StaffUpdateRequest = {

        fullName:
          this.form.controls.fullname.value.trim(),

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
     * =========================
     * CREATE STAFF USER
     * =========================
     *
     * IMPORTANT:
     * Backend expects "fullName",
     * not "name" or "fullname".
     */
    const createRequest: StaffCreateRequest = {

      fullName:
        this.form.controls.fullname.value.trim(),

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

  get fullnameInvalid(): boolean {

    const control =
      this.form.controls.fullname;

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
