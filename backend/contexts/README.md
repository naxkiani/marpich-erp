# Bounded Contexts

**44 independent domains** — each folder is a deployable bounded context.

**Master catalog:** `docs/architecture/BOUNDED_CONTEXTS_REGISTRY.md`  
**Code registry:** `contexts/registry.py`

```
contexts/{name}/
├── context.yaml          # Manifest: aggregates, events, schema
├── domain/               # Pure domain — NO cross-context imports
├── application/
├── infrastructure/
│   └── acl/              # Anti-corruption layers for subscribed events
├── presentation/
├── tests/
└── docs/                 # Ubiquitous language glossary
```

Detail per context: `docs/architecture/BOUNDED_CONTEXTS.md`

## Rules

1. **Never merge unrelated domains** — hospital ≠ clinic, government ≠ municipality
2. Communicate only via **integration events**, **public APIs**, **application contracts**
3. Reference other contexts by **ID**, never by object or shared table
4. Every subscriber has an **ACL** in `infrastructure/acl/`
5. Every table: `tenant_id` column; schema `{context}_*`
6. Independent: terminology, models, rules, permissions, workflows, events, docs
