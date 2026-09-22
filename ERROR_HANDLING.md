# Error Handling & User-Friendly Messages

## Overview
All errors displayed to users on the frontend are now guaranteed to be in human-readable format, never exposing technical details, stack traces, or exception language.

## Error Flow

```
Backend Error
    ↓
Error Interceptor (normalizes & sanitizes)
    ↓
User-Friendly Message
    ↓
Toast Notification or Inline Form Errors
```

## Key Components

### 1. Error Interceptor (`error.interceptor.ts`)
**Purpose**: Intercepts all HTTP errors and converts them to standardized format

**Features**:
- Normalizes errors to `ApiError` format
- Sanitizes messages to remove technical content
- Prevents stack traces from reaching UI
- Logs technical details to browser console (developer-only)
- Shows user-friendly toast for unexpected errors (network, 5xx)
- Preserves field-level errors for form validation

**Message Sanitization**:
- Removes stack traces and line numbers (`.java:123)`)
- Strips exception keywords (`Exception`, `Error:`, `[ERROR]`)
- Removes `null`/`undefined` references
- Replaces technical jargon with simple language
- Falls back to generic message if content is too technical

### 2. Error Utilities (`api-error.util.ts`)
**Helper Functions**:

```typescript
// Extract error from HttpErrorResponse
getApiError(error: unknown): ApiError | null

// Format error for UI display (removes tech details)
formatErrorMessage(error: ApiError): string

// Check if error contains field validation errors
hasFieldErrors(error: ApiError): boolean

// Get field-level errors as a map
formatFieldErrors(error: ApiError): Map<string, string>

// Get friendly category name for error
getErrorCategory(errorCode: string): string
```

### 3. Error Model (`api-error.model.ts`)
**Structure**:
```typescript
interface ApiError {
  timestamp: string;          // ISO-8601 timestamp
  status: number;             // HTTP status code
  errorCode: string;          // Backend error code (e.g., 'VALIDATION_ERROR')
  message: string;            // User-friendly message
  path?: string;              // API endpoint (developer-only)
  correlationId?: string;     // For error tracking
  fieldErrors?: ApiFieldError[]; // Form field errors
}
```

## User-Facing Messages

### Examples

#### Good (User-Friendly)
- ✅ "Invalid email address"
- ✅ "Password must be at least 8 characters"
- ✅ "Email already registered"
- ✅ "Unable to reach the server. Check your connection and try again."

#### Bad (Technical - Will Be Sanitized)
- ❌ `NullPointerException at UserService.java:45`
- ❌ `[ERROR] SQLException: constraint violation`
- ❌ `Exception in thread "main" java.lang.RuntimeException`
- ❌ `undefined is not a function`

## How Errors Are Displayed

### Toast Notifications (Unexpected Errors)
Shown for network errors and 5xx server errors:

```typescript
// Before: Raw message potentially with stack trace
this.toast.error(apiError.message, correlationId);

// After: Sanitized, user-friendly message
const userMessage = this.getUserFriendlyMessage(apiError);
this.toast.error(userMessage, correlationId);
```

### Form Field Errors (Validation Errors)
Handled separately by components and displayed inline:

```typescript
const apiError = getApiError(error);
if (hasFieldErrors(apiError)) {
  const fieldErrors = formatFieldErrors(apiError);
  // fieldErrors.get('email') → "Invalid email address"
}
```

### Error Category Names
Maps technical codes to friendly names:

```typescript
getErrorCategory('VALIDATION_ERROR')  // → "Validation Error"
getErrorCategory('NETWORK_ERROR')     // → "Connection Error"
getErrorCategory('AUTHENTICATION_ERROR') // → "Login Failed"
```

## Backend Requirements

For proper error handling, the backend should return error responses in this format:

```json
{
  "timestamp": "2025-09-22T10:30:00Z",
  "status": 400,
  "errorCode": "VALIDATION_ERROR",
  "message": "Email is already registered",
  "path": "/auth/customers",
  "correlationId": "req-abc123",
  "fieldErrors": [
    {
      "field": "email",
      "message": "This email is already in use"
    }
  ]
}
```

### Error Code Guidelines
Use clear, descriptive error codes:
- `VALIDATION_ERROR` - Input validation failed
- `AUTHENTICATION_ERROR` - Login failed
- `AUTHORIZATION_ERROR` - User lacks permission
- `NOT_FOUND_ERROR` - Resource not found
- `CONFLICT_ERROR` - Resource conflict (e.g., duplicate)
- `NETWORK_ERROR` - Frontend network failure

### Message Guidelines
Always provide user-friendly messages:
- ✅ Explain what went wrong in simple language
- ✅ Suggest corrective action when possible
- ❌ Never include stack traces
- ❌ Never include technical exception names
- ❌ Never include file paths or line numbers

## Testing Error Messages

### In Unit Tests
```typescript
it('should show user-friendly error message', () => {
  const error = {
    status: 400,
    errorCode: 'VALIDATION_ERROR',
    message: 'Email is invalid'  // Already user-friendly
  };
  
  const userMessage = getUserFriendlyMessage(error);
  expect(userMessage).toBe('Email is invalid');
});
```

### In E2E Tests
```typescript
// Verify toast shows user-friendly text, not tech details
page.locator('[role="alert"]').contains('Email is invalid');
page.locator('[role="alert"]').not.contains('Exception');
page.locator('[role="alert"]').not.contains('at java');
```

## Logging for Developers

Technical details are ONLY logged to browser console:

```
[HTTP 400] POST /auth/customers errorCode=VALIDATION_ERROR correlationId=req-abc123
```

Users never see this. Developer can use correlationId to find server logs.

## Common Scenarios

### Network Error (No Server Connection)
```
User sees: "Unable to reach the server. Check your connection and try again."
Dev sees in console: "[HTTP 0] ... errorCode=NETWORK_ERROR"
```

### Server Error (5xx)
```
Backend returns stack trace → Stripped → Generic message shown
User sees: "Something went wrong. Please try again."
Dev sees in console: "[HTTP 500] ... correlationId=req-xyz789"
→ Dev uses correlationId to check server logs
```

### Validation Error (4xx)
```
Backend returns: { message: "Email already registered", ... }
User sees: "Email already registered" (in form or toast)
User NOT shown: Error codes, stack traces, or technical details
```

## Utilities

### For Component Developers

When handling errors in components:

```typescript
import { getApiError, hasFieldErrors, formatFieldErrors } from '@core/errors';

// In error handler
catch((error) => {
  const apiError = getApiError(error);
  
  if (apiError && hasFieldErrors(apiError)) {
    const fieldErrors = formatFieldErrors(apiError);
    this.form.setErrors(fieldErrors);
  } else if (apiError) {
    // Show as toast (already handled by interceptor for unexpected errors)
    // OR show custom inline message for expected validation errors
  }
});
```

## Compliance & Security

✅ **User Safety**: No technical details exposed to users  
✅ **Developer Debugging**: Full details logged to console with correlation IDs  
✅ **Security**: Stack traces never sent to client  
✅ **Consistency**: All errors follow same format and flow  
✅ **Accessibility**: Messages are clear and actionable  

