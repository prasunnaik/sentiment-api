import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';

import { AuthService } from '../../../core/auth/auth.service';

@Component({
  selector: 'app-staff-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule
  ],
  templateUrl: './staff-login.component.html',
  styleUrls: ['./staff-login.component.css']
})
export class StaffLoginComponent {

  loading = false;
  error = '';

  form!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.form = this.fb.nonNullable.group({
      email: [
        '',
        [
          Validators.required,
          Validators.email
        ]
      ],
      password: [
        '',
        [
          Validators.required
        ]
      ]
    });
  }

  login(): void {

    this.error = '';

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading = true;

    const request = {
      email: this.form.get('email')?.value?.trim(),
      password: this.form.get('password')?.value
    };

    this.authService.login(request).subscribe({

      next: () => {

        this.loading = false;

        if (this.authService.isStaff()) {
          this.router.navigate(['/staff/dashboard']);
        } else {
          this.authService.logout();
          this.error = 'You are not authorized as a staff user.';
        }
      },

      error: (error: HttpErrorResponse) => {

        this.loading = false;

        this.error =
          error?.error?.message ??
          'Invalid email or password.';
      }

    });
  }
}
