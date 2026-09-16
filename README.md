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

  getById(id: string): Observable<StaffUser> {

    return this.http
      .get<unknown>(
        `${this.url}/${id}`
      )
      .pipe(
        map(user =>
          this.normalizeUser(user)
        )
      );
  }

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

  delete(id: string): Observable<void> {

    return this.http.delete<void>(
      `${this.url}/${id}`
    );
  }

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

      /*
       * Backend currently returns:
       * full_name
       */
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
