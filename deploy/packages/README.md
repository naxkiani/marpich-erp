# Product packages — same canonical application. No forks.
# Commercial YAML remains under infrastructure/launch/commercial/.

| Package | Canonical adapter | Commercial YAML |
|---------|-------------------|-----------------|
| MEOS DEMO | deploy/compose + deploy/scripts/meos-demo.sh | DEMO/ |
| MEOS SINGLE-TENANT | deploy/scripts/meos-local.sh or VPS | SELF_HOSTED/ + SINGLE_TENANT/ |
| MEOS VPS | deploy/vps | VPS/ |
| MEOS CLOUD | deploy/aws · azure · gcp | CLOUD_READY/ |
| MEOS KUBERNETES | deploy/kubernetes | KUBERNETES/ |

Installer: `python3 scripts/meos-install.py --platform …` (PLAN_ONLY).
