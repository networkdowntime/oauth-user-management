# TODO:

- let's add a hydra sync API endpoint to auth-backend and a “Sync Hydra” button to the UI.  it should fetch from Hydra, compare to what's in the auth-backend's database, and create/remove/update Hydra to make it match the database for clients (service accounts) & scopes.
- admin_service.py:get_system_stats() needs to be updated to fetch the correct Service Accounts counts
- Remove references to user_type from backend unit tests
- Add a Scopes View page
- Role list shows User counts, need to add Service Account counts
- Change Scopes Edit from a modal to a page, should let you add/remove the scope from service accounts like we do for Role Edit
- Chips on View Users, View Service Accounts for Roles & Scopes should be clickable links.

- Seem to be missing these on Service Accounts:
  "post_logout_redirect_uris": [
    "http://localhost:3000/",
    "http://localhost:3000/login"
  ],

  "allowed_cors_origins": [
    "http://localhost:3000"
  ],