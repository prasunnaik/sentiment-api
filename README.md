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

  /*
   * Explicit form type.
   * This makes TypeScript recognise:
   * name, email and address.
   */
  form: FormGroup<{
    name: FormControl<string>;
    email: FormControl<string>;
    address: FormControl<string>;
  }>;

  constructor(
    private readonly fb: FormBuilder,
    private readonly staffUserApi: StaffUserApiService,
    private readonly route: ActivatedRoute,
    private readonly router: Router
  ) {

    /*
     * Initialize after FormBuilder has been injected.
     */
    this.form = this.fb.nonNullable.group({

      name: [
        '',
        [
          Validators.required,
          Validators.minLength(2),
          Validators.maxLength(100),

          /*
           * Allows:
           * John
           * John Doe
           * John-Doe
           * O'Connor
           *
           * Rejects:
           * John@
           * John#
           * John$
           * John123
           */
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
      ]
    });
  }

  ngOnInit(): void {

    this.userId =
      this.route.snapshot.paramMap.get('id');

    this.isEdit = !!this.userId;

    if (this.userId) {

      this.loadUser(
        this.userId
      );
    }
  }

  loadUser(id: string): void {

    this.loading = true;
    this.error = '';

    this.staffUserApi.getById(id).subscribe({

      next: (user) => {

        this.form.patchValue({

          name:
            user.name,

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

    /*
     * Allowed profile-picture formats.
     */
    const allowedTypes = [
      'image/jpeg',
      'image/png',
      'image/webp'
    ];

    if (
      !allowedTypes.includes(file.type)
    ) {

      this.error =
        'Only JPG, PNG or WEBP images are allowed.';

      input.value = '';

      return;
    }

    /*
     * Maximum file size = 5 MB.
     */
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

    /*
     * Create preview.
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

    if (this.form.invalid) {

      this.form.markAllAsTouched();

      return;
    }

    this.saving = true;

    const request = {

      name:
        this.form.controls.name.value.trim(),

      email:
        this.form.controls.email.value.trim(),

      address:
        this.form.controls.address.value.trim()
    };

    /*
     * EDIT STAFF USER
     */
    if (
      this.isEdit &&
      this.userId
    ) {

      this.staffUserApi
        .update(
          this.userId,
          request
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
    this.staffUserApi
      .create(request)
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
