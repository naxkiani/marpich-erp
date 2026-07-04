# Module scaffold (`_template`)

Copy this tree when creating a new bounded context. Replace `module_id` everywhere.

**Canonical spec:** `docs/architecture/MODULE_ARCHITECTURE.md`

## Copy command

```bash
cp -r backend/contexts/_template backend/contexts/{module_id}
# Then rename module_id in files, register in contexts/registry.py, wire router in main.py
```

## Checklist

- [ ] All mandatory folders present (see MODULE_ARCHITECTURE.md)
- [ ] `context.yaml` registered in `contexts/registry.py`
- [ ] REST router mounted in `core/presentation/api/main.py`
- [ ] `tests/integration/` has at least one flow test
- [ ] `docs/architecture/README.md` documents ubiquitous language
