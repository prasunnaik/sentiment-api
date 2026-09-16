import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
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
   * The form is declared here but NOT initialized here.
   *
   * It is initialized inside ngOnInit() after FormBuilder
   * has been injected by the constructor.
   */
  form!: ReturnType<FormBuilder['nonNullable']['group']>;

  constructor(
    private readonly fb: FormBuilder,
    private readonly policyApi: PolicyApiService,
    private readonly route: ActivatedRoute,
    private readonly router: Router
  ) {}

  ngOnInit(): void {

    /*
     * Initialize the form after FormBuilder is available.
     */
    this.form = this.fb.nonNullable.group({

      policyName: [
        '',
        [
          Validators.required,
          Validators.minLength(2),
          Validators.maxLength(100),

          /*
           * Allows:
           * Life Insurance
           * Motor Insurance
           * Health-Insurance
           * Health's Insurance
           *
           * Rejects arbitrary special characters such as:
           * @ # $ % & * etc.
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

    /*
     * Check whether this is Add or Edit.
     */
    this.policyId =
      this.route.snapshot.paramMap.get('id');

    this.isEdit = !!this.policyId;

    /*
     * Load only active categories.
     */
    this.loadCategories();

    /*
     * If an ID exists, load the existing policy.
     */
    if (this.policyId) {
      this.loadPolicy(this.policyId);
    }
  }

  loadCategories(): void {

    this.policyApi.getCategories().subscribe({

      next: (categories: Category[]) => {

        this.categories =
          categories.filter(
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

    /*
     * Validate the complete form.
     */
    if (this.form.invalid) {

      this.form.markAllAsTouched();

      return;
    }

    this.saving = true;

    /*
     * Prepare request for Spring Boot.
     */
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

    /*
     * Add or Edit.
     */
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

        /*
         * Return to Manage Policies.
         */
        setTimeout(() => {

          this.router.navigate([
            '/staff/policies'
          ]);

        }, 700);
      },

      error: (error: unknown) => {

        this.saving = false;

        /*
         * Don't use "error: error =>" because
         * strict TypeScript reports implicit any.
         */
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

          this.error =
            response.error?.message ??
            'Unable to save policy.';

        } else {

          this.error =
            'Unable to save policy.';
        }
      }
    });
  }

  cancel(): void {

    this.router.navigate([
      '/staff/policies'
    ]);
  }
}







import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
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
   * Declare the form only.
   *
   * It is initialized inside ngOnInit() because
   * FormBuilder is injected through the constructor.
   */
  form!: ReturnType<FormBuilder['nonNullable']['group']>;

  constructor(
    private readonly fb: FormBuilder,
    private readonly staffUserApi: StaffUserApiService,
    private readonly route: ActivatedRoute,
    private readonly router: Router
  ) {}

  ngOnInit(): void {

    /*
     * Initialize form after FormBuilder is available.
     */
    this.form = this.fb.nonNullable.group({

      name: [
        '',
        [
          Validators.required,
          Validators.minLength(2),
          Validators.maxLength(100),

          /*
           * Allows normal names such as:
           * John
           * John Doe
           * Mary-Jane
           * O'Connor
           *
           * Prevents arbitrary special characters.
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

    /*
     * Check whether this is Add or Edit.
     */
    this.userId =
      this.route.snapshot.paramMap.get('id');

    this.isEdit = !!this.userId;

    /*
     * If editing an existing staff user,
     * load the user details.
     */
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

          name:
            user.name,

          email:
            user.email,

          address:
            user.address
        });

        /*
         * Display existing profile picture
         * when available.
         */
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
     * BR04 profile picture types.
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
     * Maximum profile picture size: 5 MB.
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
     * Display image preview.
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
     * Stop submission if validation fails.
     */
    if (this.form.invalid) {

      this.form.markAllAsTouched();

      return;
    }

    this.saving = true;

    /*
     * Prepare staff user request.
     */
    const request = {

      name:
        this.form.controls.name.value.trim(),

      email:
        this.form.controls.email.value.trim(),

      address:
        this.form.controls.address.value.trim()
    };

    /*
     * EDIT existing staff user.
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
     * CREATE new staff user.
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

  /*
   * Used by the HTML to show validation state.
   */
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

  /*
   * Safely extract a backend error message
   * without using "any".
   */
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
