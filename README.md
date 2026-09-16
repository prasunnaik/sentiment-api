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

    <!-- Loading -->
    <div
      class="loading"
      *ngIf="loading">

      Loading policy...

    </div>

    <form
      *ngIf="!loading"
      [formGroup]="form"
      (ngSubmit)="save()">

      <!-- Policy Name -->
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

          Policy name is required and can contain
          letters, numbers, spaces, hyphens and apostrophes.

        </small>

      </div>


      <!-- Category -->
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


      <!-- Premium + Coverage -->
      <div class="two-columns">

        <!-- Premium -->
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

            Premium must be greater than zero.

          </small>

        </div>


        <!-- Coverage -->
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

            Coverage must be greater than zero.

          </small>

        </div>

      </div>


      <!-- Duration -->
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


      <!-- Error -->
      <div
        class="error"
        *ngIf="error">

        {{ error }}

      </div>


      <!-- Success -->
      <div
        class="success"
        *ngIf="success">

        {{ success }}

      </div>


      <!-- Buttons -->
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
            : (isEdit ? 'Update Policy' : 'Save Policy')
          }}

        </button>

      </div>

    </form>

  </div>

</div>
