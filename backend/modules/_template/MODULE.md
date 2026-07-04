# Module namespace scaffold (deprecated path)

**Canonical implementation:** `backend/contexts/{module_id}/`  
**Canonical scaffold:** `backend/contexts/_template/`  
**Canonical spec:** `docs/architecture/MODULE_ARCHITECTURE.md`

This `backend/modules/` tree holds namespace placeholders only. New modules are created under `backend/contexts/`, not here.

Copy:

```bash
cp -r backend/contexts/_template backend/contexts/{module_id}
```

See `backend/contexts/_template/MODULE.md` for the checklist.
