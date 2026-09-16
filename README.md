import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

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

  constructor(
    private readonly http: HttpClient
  ) {}

  /*
   * GET ALL STAFF USERS
   */
  getAll(): Observable<StaffUser[]> {

    return this.http
      .get<unknown[]>(this.url)
      .pipe(
        map(users =>
          users.map(user =>
            this.normalizeUser(user)
          )
        )
      );
  }

  /*
   * GET STAFF USER BY ID
   */
  getById(id: string): Observable<StaffUser> {

    return this.http
      .get<unknown>(`${this.url}/${id}`)
      .pipe(
        map(user =>
          this.normalizeUser(user)
        )
      );
  }

  /*
   * CREATE STAFF USER
   */
  create(
    request: StaffCreateRequest
  ): Observable<StaffUser> {

    return this.http
      .post<unknown>(
        this.url,
        request
      )
      .pipe(
        map(user =>
          this.normalizeUser(user)
        )
      );
  }

  /*
   * UPDATE STAFF USER
   */
  update(
    id: string,
    request: StaffUpdateRequest
  ): Observable<StaffUser> {

    return this.http
      .put<unknown>(
        `${this.url}/${id}`,
        request
      )
      .pipe(
        map(user =>
          this.normalizeUser(user)
        )
      );
  }

  /*
   * UPLOAD PROFILE PICTURE
   *
   * Backend:
   * POST /api/staff/users/{id}/profile-picture
   *
   * Multipart field name must be:
   * file
   */
  uploadProfilePicture(
    id: string,
    file: File
  ): Observable<StaffUser> {

    const formData =
      new FormData();

    formData.append(
      'file',
      file
    );

    return this.http
      .post<unknown>(
        `${this.url}/${id}/profile-picture`,
        formData
      )
      .pipe(
        map(user =>
          this.normalizeUser(user)
        )
      );
  }

  /*
   * DELETE PROFILE PICTURE
   */
  deleteProfilePicture(
    id: string
  ): Observable<void> {

    return this.http.delete<void>(
      `${this.url}/${id}/profile-picture`
    );
  }

  /*
   * DELETE STAFF USER
   */
  delete(
    id: string
  ): Observable<void> {

    return this.http.delete<void>(
      `${this.url}/${id}`
    );
  }

  /*
   * NORMALIZE BACKEND RESPONSE
   *
   * Backend returns:
   *
   * "full_name": "Paarth Chandan"
   *
   * Angular uses:
   *
   * fullName
   */
  private normalizeUser(
    response: unknown
  ): StaffUser {

    const user =
      response as {
        id?: string;

        fullName?: string;
        full_name?: string;
        fullname?: string;
        name?: string;

        email?: string;
        address?: string;

        profilePictureUrl?: string | null;
      };

    return {

      id:
        user.id ?? '',

      fullName:
        user.fullName ??
        user.full_name ??
        user.fullname ??
        user.name ??
        '',

      email:
        user.email ?? '',

      address:
        user.address ?? '',

      profilePictureUrl:
        user.profilePictureUrl ?? null
    };
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

  /*
   * Used when editing an existing user.
   *
   * If the user clicks Remove and saves,
   * the existing S3 profile picture will be deleted.
   */
  removeExistingPicture = false;

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

    this.form =
      this.fb.nonNullable.group({

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

        /*
         * Backend requires minimum 8 characters.
         */
        password: [
          '',
          [
            Validators.required,
            Validators.minLength(8),
            Validators.maxLength(100)
          ]
        ]
      });
  }

  ngOnInit(): void {

    this.userId =
      this.route.snapshot.paramMap.get('id');

    this.isEdit =
      !!this.userId;

    /*
     * Password is required only
     * when creating a staff user.
     */
    if (this.isEdit) {

      this.form.controls.password.clearValidators();

      this.form.controls.password.updateValueAndValidity();
    }

    if (this.userId) {

      this.loadUser(
        this.userId
      );
    }
  }

  /*
   * =========================
   * LOAD USER
   * =========================
   */
  loadUser(id: string): void {

    this.loading = true;

    this.error = '';

    this.staffUserApi
      .getById(id)
      .subscribe({

        next: (user) => {

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

          this.removeExistingPicture =
            false;

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

  /*
   * =========================
   * SELECT PROFILE PICTURE
   * =========================
   */
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
     * Allowed image formats.
     */
    const allowedTypes = [
      'image/jpeg',
      'image/png',
      'image/webp'
    ];

    if (
      !allowedTypes.includes(
        file.type
      )
    ) {

      this.error =
        'Only JPG, PNG or WEBP images are allowed.';

      input.value = '';

      this.selectedFile = null;

      return;
    }

    /*
     * Maximum 5 MB.
     */
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

    this.selectedFile =
      file;

    this.removeExistingPicture =
      false;

    /*
     * Browser preview.
     */
    const reader =
      new FileReader();

    reader.onload = () => {

      this.previewUrl =
        reader.result as string;
    };

    reader.readAsDataURL(file);
  }

  /*
   * =========================
   * REMOVE PROFILE PICTURE
   * =========================
   */
  removeSelectedPicture(): void {

    this.selectedFile = null;

    this.previewUrl = null;

    /*
     * For an existing user, remember
     * that the S3 picture must be deleted.
     */
    if (this.isEdit) {

      this.removeExistingPicture =
        true;
    }
  }

  /*
   * =========================
   * SAVE
   * =========================
   */
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
     * EDIT USER
     * =========================
     */
    if (
      this.isEdit &&
      this.userId
    ) {

      this.updateUser(
        this.userId
      );

      return;
    }

    /*
     * =========================
     * CREATE USER
     * =========================
     */
    this.createUser();
  }

  /*
   * =========================
   * CREATE USER
   * =========================
   */
  private createUser(): void {

    const request: StaffCreateRequest = {

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
      .create(request)
      .subscribe({

        next: (createdUser) => {

          /*
           * User has now been created.
           *
           * If a profile picture was selected,
           * upload it using the newly-created
           * user's ID.
           */
          if (
            this.selectedFile &&
            createdUser.id
          ) {

            this.uploadProfilePicture(
              createdUser.id
            );

            return;
          }

          /*
           * No picture selected.
           */
          this.finishSave(
            'Staff user created successfully.'
          );
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

  /*
   * =========================
   * UPDATE USER
   * =========================
   */
  private updateUser(
    id: string
  ): void {

    const request: StaffUpdateRequest = {

      fullName:
        this.form.controls.fullname.value.trim(),

      email:
        this.form.controls.email.value.trim(),

      address:
        this.form.controls.address.value.trim(),

      /*
       * Keep existing password unchanged
       * unless you later add a password field
       * for edit.
       */
      password: undefined
    };

    this.staffUserApi
      .update(
        id,
        request
      )
      .subscribe({

        next: () => {

          /*
           * New picture selected.
           */
          if (this.selectedFile) {

            this.uploadProfilePicture(id);

            return;
          }

          /*
           * User removed existing picture.
           */
          if (this.removeExistingPicture) {

            this.deleteProfilePicture(id);

            return;
          }

          this.finishSave(
            'Staff user updated successfully.'
          );
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
  }

  /*
   * =========================
   * UPLOAD PROFILE PICTURE
   * =========================
   */
  private uploadProfilePicture(
    id: string
  ): void {

    if (!this.selectedFile) {

      this.finishSave(
        this.isEdit
          ? 'Staff user updated successfully.'
          : 'Staff user created successfully.'
      );

      return;
    }

    this.staffUserApi
      .uploadProfilePicture(
        id,
        this.selectedFile
      )
      .subscribe({

        next: () => {

          this.finishSave(
            this.isEdit
              ? 'Staff user and profile picture updated successfully.'
              : 'Staff user and profile picture created successfully.'
          );
        },

        error: (error: unknown) => {

          /*
           * The staff user itself was already created,
           * but the profile picture upload failed.
           */
          this.saving = false;

          this.error =
            this.getErrorMessage(
              error,
              'Staff user was created, but the profile picture could not be uploaded.'
            );
        }
      });
  }

  /*
   * =========================
   * DELETE PROFILE PICTURE
   * =========================
   */
  private deleteProfilePicture(
    id: string
  ): void {

    this.staffUserApi
      .deleteProfilePicture(id)
      .subscribe({

        next: () => {

          this.finishSave(
            'Staff user updated successfully.'
          );
        },

        error: (error: unknown) => {

          this.saving = false;

          this.error =
            this.getErrorMessage(
              error,
              'Staff user was updated, but the profile picture could not be deleted.'
            );
        }
      });
  }

  /*
   * =========================
   * FINISH
   * =========================
   */
  private finishSave(
    message: string
  ): void {

    this.saving = false;

    this.success = message;

    setTimeout(() => {

      this.router.navigate([
        '/staff/manage-users'
      ]);

    }, 700);
  }

  /*
   * =========================
   * CANCEL
   * =========================
   */
  cancel(): void {

    this.router.navigate([
      '/staff/manage-users'
    ]);
  }

  /*
   * =========================
   * VALIDATION HELPERS
   * =========================
   */

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

  /*
   * =========================
   * ERROR MESSAGE
   * =========================
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





