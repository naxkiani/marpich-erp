# Localization — i18n/l10n bounded context

Separate from `settings` (tenant configuration).

## API

Prefix: `/api/v1/localization`

## Events

- `localization.locale.changed` — on tenant seed
- `localization.translation.updated` — on bundle upsert
- `localization.key.missing` — client-reported gaps
