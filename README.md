private updateUser(
  id: string
): void {

  const request: StaffUpdateRequest = {

    fullName:
      this.form.controls.fullname.value.trim(),

    email:
      this.form.controls.email.value.trim(),

    address:
      this.form.controls.address.value.trim()
  };

  this.staffUserApi
    .update(
      id,
      request
    )
    .subscribe({

      next: () => {

        /*
         * If a new profile picture was selected,
         * upload it after the staff user is updated.
         */
        if (this.selectedFile) {

          this.uploadProfilePicture(id);

          return;
        }

        /*
         * If the existing picture was removed,
         * delete it from S3.
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
