# InsureWise Angular UI Scaffold

This repository is an Angular scaffold for the InsureWise UI. It intentionally renders only `InsureWise` from the root component so developers can implement the screens from a clean starting point.

## Runtime

```bash
npm install
npm run dev
npm run build
```

The app is configured for deployment under `/insurance/`.

## Environment

```env
NG_APP_BASE_HREF=/insurance/
NG_APP_API_BASE_URL=/insurance/api
```

For local backend testing, set `NG_APP_API_BASE_URL` to the local API endpoint, for example:

```env
NG_APP_API_BASE_URL=http://localhost:1234/api
```

The current scaffold keeps env values documented in `.env` and `.env.example`. When implementation begins, add either Angular file replacements or a runtime config loader to consume those values.

## Existing Minimal App Files

```text
src/app/app.component.ts    Blank root component that renders only InsureWise
src/main.ts                 Angular bootstrap
src/index.html              Host HTML with /insurance/ base href
src/styles.css              Minimal blank-screen styling
```

Do not add screen behavior directly into the bootstrap files unless it belongs to global app setup.

## Folder Structure To Implement

```text
src/
  assets/
  app/
    components/
      common/
        badge/
        button/
        card/
        document-viewer-modal/
        input/
        modal/
        select/
        spinner/
        table/
        toast/
      composites/
      data-display/
        empty-state/
        policy-card/
        stat-tile/
      domain/
        category-filter/
        documents-panel/
        document-uploader/
        payment-method-selector/
      forms/
        form-actions/
        form-field/
        form-row/
      layout/
    config/
    core/
      auth/
      environment/
      http/
      rbac/
    pages/
      auth/
      customer/
        browse-policies/
        claim-documents/
        file-claim/
        make-new-payment/
        make-policy-payment/
        my-claims-file-new/
        my-claims/
        my-payments/
        my-policies/
        policy-details/
        policy-documents/
      shared/
        payment-documents/
      staff/
        approve-policies-list/
        approve-policies-review/
        categories-list/
        categories-new/
        dashboard/
        manage-users-list/
        manage-users-new/
        policies-list/
        policies-new/
        process-claims-list/
        process-claims-review/
        view-payments/
    routing/
    services/
      api/
    types/
    utils/
```

## Implementation Guidance

Implement standalone reusable UI components first under `components/common`, then composed form/display components, then domain components. Keep API services under `services/api` or `core/http`, auth state and guards under `core/auth`, RBAC helpers under `core/rbac`, and route definitions under `routing`.

Each screen should be implemented in its matching folder under `pages`. Keep customer, staff, and shared screens separate so teams can work in parallel without stepping on each other.

Recommended first implementation order:

1. Auth shell: login, signup, token persistence, route guards.
2. Layout shell: customer top navigation and staff navigation.
3. Catalog flow: browse policies, policy details, application form.
4. Documents flow: reusable uploader, viewer, policy/claim/payment document screens.
5. Payments and claims flows.
6. Staff administration screens.

Keep the deployment contract intact: production builds should continue to use `/insurance/` as both `base-href` and `deploy-url`.
