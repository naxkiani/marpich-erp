# Account security self-service — architecture notes

**Owning platforms:**  
- Identity (`identity`) — MFA, sessions, password change  
- Authentication (`authentication`) — WebAuthn / passkeys, federation  

**UI surfaces:** `/login` (P34), `/account/security` (P28), `/account/mfa` (P29), `/account/passkeys` (P30), `/account/change-password` (P31)

## Sign-in desk (P34)

`AccountLoginPage` + shared `LoginGate` — central Identity login for admin portal.

- Draft: `marpich.account.login.draft` (tenant + email only — never password)
- Workflow: Identity → credentials → authenticate → enter (`StepProgress`)
- Live auth via auth-provider → Identity token issuance; passkey button delegates to Authentication WebAuthn
- i18n: `login.*` (en / fa / ar)

## Admin UI depth (P28)

`AccountSecurityPage` — UI-only hub with deep links to MFA, passkeys, recovery.

## MFA enrollment desk (P29)

`AccountMfaEnrollmentPage` → Identity `/users/me/mfa/*`

## Passkey desk (P30)

`AccountPasskeysPage` → Authentication `/authentication/webauthn/*`

## Recovery / change-password desk (P31)

`AccountRecoveryPage` → Identity password API (wiring restored for desk):

| Step | API |
|------|-----|
| Status | `GET /api/v1/users/me` → `password_must_change`, `password_changed_at` |
| Change | `POST /api/v1/users/me/password` `{ current_password, new_password, revoke_other_sessions }` |

Draft: `marpich.account.recovery.draft` (revoke preference only — never plaintext passwords)  
Permission: `identity.password.change`  
Audit: `identity.password.updated`

Application method `change_password` verifies current password, hashes via `IPasswordHasher`, updates aggregate, optionally `revoke_all_for_user`.
