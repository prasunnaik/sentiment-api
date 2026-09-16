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
      .get<unknown>(
        `${this.url}/${id}`
      )
      .pipe(
        map(user =>
          this.normalizeUser(user)
        )
      );
  }

  /*
   * CREATE STAFF USER
   *
   * Sends:
   * fullName
   * email
   * address
   * password
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
   * DELETE STAFF USER
   */
  delete(id: string): Observable<void> {

    return this.http.delete<void>(
      `${this.url}/${id}`
    );
  }

  /*
   * NORMALIZE BACKEND RESPONSE
   *
   * Handles possible backend property names:
   *
   * fullName
   * fullname
   * name
   */
  private normalizeUser(
    response: unknown
  ): StaffUser {

    const user =
      response as {
        id?: string;
        fullName?: string;
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
