# 🔐 ORY Hydra Login & Consent UI + Auth Endpoint Integration Spec

This document outlines the requirements to implement the authentication and consent endpoints for ORY Hydra, using a unified **Login & Consent UI**. It supports both **email/password** and **federated logins** (Google, Apple, GitHub) and integrates with an external Python-based authentication service.

---

## ✅ Overview

### Goals
- Provide a unified Login + Consent UI
- Handle Hydra’s `/login` and `/consent` challenge flow
- Support:
  - Email + password login
  - Federated login via Google, Apple, GitHub (OIDC)
  - Client-side session management (JWT expiration)
  - Logout endpoint
  - Skipped consent for first-party clients

### Deployment
- Monorepo project
- Docker Compose orchestration
- Hydra already deployed with Postgres

---

## 1. 🖥️ Login & Consent UI: Elements & Behavior

### Login Page (at `/login`)
- Fields:
  - Email
  - Password
  - "Remember Me" checkbox (stores token in localStorage/sessionStorage)
  - Federated login buttons:
    - “Continue with Google”
    - “Continue with Apple”
    - “Continue with GitHub”
- UX:
  - Submitting credentials sends request to auth-backend
  - On success:
    - Gets redirected to `/consent?consent_challenge=...` (if required by Hydra)
    - Or final redirect URI if `skip_consent=true`

### Consent Page (at `/consent`)
- Only shown for third-party clients
- Elements:
  - Requested scopes
  - Client name and logo
  - “Allow” and “Deny” buttons
- Logic:
  - Automatically skip if `skip=true` (first-party clients)

### Logout Page (at `/logout`)
- Clears JWT from local/session storage
- Redirects to login

---

## 2. 🔁 Auth & Consent Endpoint Flow

### Hydra Challenge Flow

#### Login Endpoint: `POST /login`
- Called by UI with `login_challenge`
- Authenticates user (email/password or federated via auth-backend)
- Sends decision to Hydra’s `accept_login_request`
- Redirects user to next step (consent or redirect URI)

#### Consent Endpoint: `POST /consent`
- Called by UI with `consent_challenge`
- Accepts scopes
- Calls `accept_consent_request` from Hydra Admin API
- Redirects to client app

### Federated Login Flow
- User clicks provider button → redirects to OIDC flow
- Upon completion:
  - Validates user in auth-backend
  - Issues JWT and continues with `accept_login_request`

---

## 3. ⚙️ Required Hydra Config Changes

```yaml
serve:
  public:
    port: 4444
  admin:
    port: 4445

urls:
  self:
    issuer: http://hydra:4444
  consent: http://login-ui:3000/consent
  login: http://login-ui:3000/login
  logout: http://login-ui:3000/logout
  post_logout_redirect: http://login-ui:3000/login

oauth2:
  skip_consent_for_first_party_clients: true
  expose_internal_errors: true

secrets:
  system: [YOUR_SECRET]
```

- Add first-party clients as `trusted`
- Ensure public/private URLs resolve inside Docker network

---

## 4. ⏱️ Session & Token Expiration

- JWT expiration: 15 minutes
- No refresh token for browser login
- “Remember Me” stores token locally — not secure but fine for MVP
- On expiration:
  - Redirect user to `/login`
- Logout:
  - Clears token and client data

---

## 5. 🔖 Role Claims and ID Token Enrichment

If you want to embed custom claims like roles or GUIDs:

1. Auth-backend adds roles/guid to session during `accept_login_request`
2. Hydra ID token claim example:

```json
{
  "sub": "user-guid",
  "email": "user@example.com",
  "roles": ["user_admin", "editor"]
}
```

3. Include in `id_token_hint` if needed for UI or services

---

## 🔚 Summary

| Feature | Support |
|--------|---------|
| Unified Login & Consent UI | ✅ |
| Email + Password login | ✅ |
| Federated Login (Google, Apple, GitHub) | ✅ |
| JWTs stored in client | ✅ |
| Consent skipped for first-party clients | ✅ |
| Admin API used to accept/deny login & consent | ✅ |
| Logout endpoint | ✅ |
| Claims passed into JWTs | ✅ |