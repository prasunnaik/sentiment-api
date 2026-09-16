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

    <div *ngIf="loading" class="loading">
      Loading...
    </div>

    <form
      *ngIf="!loading"
      [formGroup]="form"
      (ngSubmit)="save()">

      <!-- FULL NAME -->

      <div class="field">

        <label for="fullname">
          Full Name <span>*</span>
        </label>

        <input
          id="fullname"
          type="text"
          formControlName="fullname"
          maxlength="100"
          placeholder="Enter full name">

        <small *ngIf="fullnameInvalid">

          <span *ngIf="form.controls.fullname.errors?.['required']">
            Full name is required.
          </span>

          <span *ngIf="form.controls.fullname.errors?.['pattern']">
            Name can contain letters, spaces, apostrophes and hyphens only.
          </span>

          <span *ngIf="form.controls.fullname.errors?.['minlength']">
            Name must contain at least 2 characters.
          </span>

        </small>

      </div>


      <!-- EMAIL -->

      <div class="field">

        <label for="email">
          Email <span>*</span>
        </label>

        <input
          id="email"
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

        <label for="address">
          Address <span>*</span>
        </label>

        <textarea
          id="address"
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

        <label for="password">
          Password <span>*</span>
        </label>

        <input
          id="password"
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

        <label for="profilePicture">
          Profile Picture
        </label>

        <input
          id="profilePicture"
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








.page {
  padding: 24px;
}

.form-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 28px;
  max-width: 700px;
}

.form-card h2 {
  margin: 0;
  font-size: 26px;
}

.subtitle {
  color: #777;
  margin-top: 8px;
  margin-bottom: 24px;
}

.loading {
  color: #777;
  padding: 20px 0;
}

.field {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 7px;
}

label span {
  color: #c62828;
}

input,
textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  font-family: inherit;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #008c95;
}

textarea {
  resize: vertical;
}

small {
  display: block;
  margin-top: 5px;
  color: #777;
  font-size: 12px;
}

small span {
  display: block;
  color: #c62828;
  margin-top: 3px;
}

.preview {
  margin-top: 12px;
}

.preview img {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  display: block;
  margin-bottom: 8px;
}

.remove {
  border: 1px solid #c62828;
  color: #c62828;
  background: white;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.remove:hover {
  background: #fff5f5;
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
  background: #008c95;
  color: white;
}

.primary:hover:not(:disabled) {
  background: #00747b;
}

.secondary {
  border: 1px solid #aaa;
  background: white;
  color: #333;
}

.secondary:hover {
  background: #f5f5f5;
}

.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #c62828;
  margin: 12px 0;
  padding: 10px;
  background: #fff5f5;
  border-radius: 5px;
}

.success {
  color: #2e7d32;
  margin: 12px 0;
  padding: 10px;
  background: #f1f8f2;
  border-radius: 5px;
}
