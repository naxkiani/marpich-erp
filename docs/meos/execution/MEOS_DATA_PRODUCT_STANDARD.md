# MEOS Data Product Standard

**Date:** 2026-08-19T06:20:00Z  
**Overlay on** P212 `data_governance` catalogs and P229/P263 **design** (ACL). **Not** a second catalog or mesh.

## Law

A data product is **PUBLISHED/ACTIVE** only with a contract, owner, source, and consumer evidence. In-memory `/catalog` flags are **DESIGNED**, not publication.

## Current state

`published_data_product_count: 0` · `active_data_product_count: 0` · `data_product_platform` **ABSENT** · `data_products` table **ABSENT**.

Allowed evidenced states now: none operational. Catalog rows must not be shown as ACTIVE in UX.

## Required fields (when a product is later published)

DATA_PRODUCT · OWNER · DOMAIN · PURPOSE · CONSUMERS · SOURCE · CONTRACT · QUALITY · SECURITY · STATUS  

Owner today: **NOT_AVAILABLE**. SLA/SLO: **NOT_SET**.
