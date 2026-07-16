# Messenger P5.3 — E2EE + LiveKit

**Domain type:** Supporting  
**Capability:** Internal secure chat + realtime A/V rooms

## Laws

- Server never invents E2EE ciphertext — clients encrypt; API accepts `ciphertext` only when `e2ee_enabled`
- LiveKit only via Integration connector (`IRealtimeMediaPort` → `livekit` adapter)
- No LiveKit / WebRTC SDK in messenger domain or application

## Lifecycle

1. Open conversation (`e2ee_enabled`, optional `issue_livekit_token`)
2. Send message: plaintext **or** client ciphertext (mutually exclusive by E2EE flag)
3. `POST .../livekit-token` for member AccessToken refresh

## LiveKit

| Mode | Condition | Token |
|------|-----------|-------|
| Simulated | Missing `LIVEKIT_API_KEY`+`SECRET` | `lk_` HMAC |
| Real | Secrets present | LiveKit AccessToken JWT (HS256 + video grants) |

Env: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `LIVEKIT_TOKEN_TTL_SECONDS`

### Secrets smoke (real A/V only)

Simulated tokens are enough for messaging. When you need real LiveKit A/V:

```bash
cd backend
# exit 0 = simulated OK (no secrets) OR real JWT mint+verify passed
.venv/bin/python scripts/smoke_livekit_secrets.py

# optional pytest (skips without env secrets)
LIVEKIT_API_KEY=… LIVEKIT_API_SECRET=… LIVEKIT_URL=wss://… \
  .venv/bin/pytest contexts/messenger/tests/test_livekit_secrets_smoke.py -q
```

Does not join a room (no LiveKit client SDK). Verifies Integration connector mint + HS256.

## Persistence

Schema `messenger.*` — conversations (member_ids, e2ee, room) + messages (body/ciphertext). Memory default; Postgres when `PERSISTENCE_BACKEND=postgres`.

## Events

`messenger.conversation.opened` · `messenger.message.sent` · `messenger.livekit.token_issued`  
(Events never carry message plaintext or tokens.)
