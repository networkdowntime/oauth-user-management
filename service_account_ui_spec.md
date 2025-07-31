# 🧾 Service Account Management UI Specification

This document outlines the requirements for managing OAuth2 clients (service accounts) in a secure, admin-facing management UI. It supports both **service-to-service** accounts and **browser-based** (SPA) applications using ORY Hydra as the OAuth2 Authorization Server.

---

## 📘 Overview

Service accounts allow integration with internal or external systems via OAuth2 flows. The UI must support:

- Creation, editing, and deletion of service accounts
- Differentiation between **Service** and **Browser App** clients
- Scope assignment and management
- Secret handling, regeneration, and auditability
- Enforcement of secure OAuth2 grant flows

---

## 🧩 Service Account Types

### 1. **Service-to-Service**
- Uses the `client_credentials` grant
- Authenticates with a `client_secret`
- Headless services (e.g. data sync, workers)

### 2. **Browser App**
- Uses `authorization_code` + **PKCE**
- No secret (public clients)
- SPAs (React, Angular, etc.)

> ⚠️ The `client_type` is immutable after creation

---

## 🧱 Service Account: Create & Edit Form Fields

### 🟦 Common Fields (All Clients)

| Field | Type | Required | Editable After Creation | Notes |
|-------|------|----------|--------------------------|-------|
| Client ID | Text | ✅ | ❌ | Unique slug or UUID |
| Client Name | Text | ✅ | ✅ | Human-readable label |
| Description | TextArea | ❌ | ✅ | Optional purpose |
| Client Type | Radio: `Service` or `Browser App` | ✅ | ❌ | Immutable |
| Scopes | Multi-select | ✅ | ✅ | At least one |
| Audience | List of URIs | ❌ | ✅ | Optional for access control |
| Owner | Email or user ID | ❌ | ✅ | For traceability |
| Metadata | Key-value pairs | ❌ | ✅ | Custom tags |
| Is Active | Toggle | ✅ | ✅ | Disables access without deletion |

### 🟦 Conditional Fields

#### Service-to-Service Clients

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Grant Types | Multi-select (only `client_credentials`) | ✅ | All others disabled |
| Client Secret | Auto-generated password | ✅ | Shown with eye icon |
| Token Auth Method | Dropdown: `client_secret_basic`, `client_secret_post` | ✅ | Default: `client_secret_basic` |

#### Browser Apps

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Grant Types | Multi-select (`authorization_code` only) | ✅ | PKCE implied |
| Redirect URIs | Multi-line input | ✅ | Must be HTTPS |
| Token Auth Method | Fixed to `none` | ✅ | Public client |

---

## 🔐 Client Secret Behavior

- Auto-generated on creation
- Shown with "show/hide" password icon
- Regenerable via action button
- Browser apps **must not have** secrets

---

## 📄 Client Details View

- View all fields
- Copy `client_id`
- Masked client secret (toggleable)
- Assigned scopes
- Grant types and token method
- Last activity (optional)
- Actions: Regenerate secret, deactivate/reactivate, delete

---

## 🗂️ Scope Management UI

### Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Scope Name | Text | ✅ | Alphanumeric (e.g. `data:read`) |
| Description | TextArea | ✅ | Tooltip in UI |
| Applies To | Multi-select: Service, Browser | ✅ | Limits visibility |
| Is Active | Toggle | ✅ | Prevents assignment when off |

---

## ✅ OAuth2 Grant Types (Predefined)

| Grant Type | Description | Allowed For |
|------------|-------------|--------------|
| `authorization_code` | Web/browser login with PKCE | Browser App |
| `client_credentials` | Service-to-service | Service |
| `refresh_token` | Long session refresh | ❌ Not supported |
| `implicit` | Deprecated browser flow | ❌ |
| `password` | Deprecated user/pass flow | ❌ |

---

## ✨ UX & Validation Rules

- Client type is immutable after creation
- Secret is required only for service accounts
- Scope selection filtered by client type
- Grant type UI filtered by client type
- Auto-generate secrets and show once
- Allow regeneration with confirmation
- Validate `client_id` uniqueness

---

## 📦 Optional Enhancements

- Copy-to-clipboard icons for ID/secret
- Regenerate secret action
- Filterable audit log per client
- “Test Token” button for service clients
- Read-only JWT viewer panel for issued tokens

---

## 🔐 Security Notes

- PKCE required for browser clients
- No secrets for public clients
- All clients must be tied to known scopes
- Secrets should not be logged
- Optional: bind `client_id` to IP/CIDR for service clients