# Marpich Infrastructure

Cloud-native deployment artifacts — separate from application code.

```
infrastructure/
├── docker/               # Images, compose, migrations
│   ├── compose/
│   ├── images/
│   ├── migrations/
│   └── scripts/
├── terraform/              # IaC
│   ├── modules/            # Reusable: networking, database, cache, …
│   └── environments/       # development | staging | production
└── kubernetes/             # K8s manifests
    ├── base/
    ├── overlays/
    └── helm/
```

## Principles

- One Terraform module per infrastructure concern (not one giant `main.tf`)
- K8s base + overlays per environment (Kustomize)
- Backend and frontend images built from `docker/images/`
