# ADR 0002: Provision a user-managed dashboard once

- **Status:** Accepted
- **Date:** 2026-07-30
- **Scope:** Dashboard ownership, lifecycle and Home Assistant registration

## Context

The original automatic dashboard was registered as a `panel_custom` sidebar
panel. It was convenient but did not appear in Home Assistant's dashboard
settings. Users could therefore neither place it in their preferred dashboard
order nor delete it through the normal interface.

The tariff visualization should remain available without YAML while behaving
like a dashboard created by the user. Deleting it must remain an effective user
choice rather than a temporary state undone at the next restart.

## Decision

1. The integration creates a Lovelace storage dashboard on its first successful
   setup.
2. Creation uses Home Assistant's already-active `DashboardsCollection`, whose
   listeners register the dashboard and power the dashboard settings UI.
3. The stored dashboard config contains a normal panel view with the stable
   `custom:swiss-dynamic-tariffs-panel` card. Forecast entities remain
   dynamically discovered inside that card.
4. The Community strategy remains available for manually created dashboards,
   but automatic dashboard loading does not wait for strategy registration.
5. A separate integration storage marker records successful provisioning.
6. A current-layout marker without a matching dashboard means the user deleted
   it. The integration does not recreate it. A legacy marker without a
   dashboard is migrated once by creating the current static layout, because
   users may have removed the earlier dashboard after its strategy timed out.
7. An existing dashboard with the integration's URL or title is retained
   without overwriting user metadata or configuration.
8. Dashboard provisioning failure is logged but does not prevent tariff
   entities from loading.
9. A layout version in the marker migrates the exact strategy-only config from
   releases through 0.5.6. Any user-modified config is left untouched.
10. Every tariff entry exposes a config-entry options action that explicitly
    creates or restores a missing dashboard. This user-triggered action may
    override the deletion marker, but it never overwrites an existing layout.

## Why the active collection

Home Assistant does not currently publish a Python helper for creating a
storage dashboard. Creating a second `DashboardsCollection` over the same
storage file would update disk but not the live collection used by the
WebSocket API. The settings UI would then be stale, and immediate rename or
delete operations would not work reliably.

The integration therefore obtains the active collection from Home Assistant's
registered `lovelace/dashboards/list` command. This is an internal boundary and
is isolated in one documented helper so a future Home Assistant API change has
a small, testable adaptation point.

## Alternatives considered

### Keep the custom panel

Rejected because it cannot be sorted or deleted as a user dashboard.

### Recreate the dashboard whenever it is missing

Rejected because it overrides an explicit user deletion and makes ownership
misleading.

### Require every user to create the Community strategy manually

Rejected as the default because discoverability was a core reason for the
automatic visualization. Manual creation remains the recovery path after a
user deletes the initially provisioned dashboard.

### Store the Community strategy in the automatic dashboard

Rejected after field use exposed a Home Assistant startup race: Lovelace can
request the strategy before the extra JavaScript module has registered its
custom element, producing a timeout and a blank dashboard. A normal custom card
uses Lovelace's established card-loading path and removes that strategy-level
failure mode.

### Write directly to `.storage/lovelace_dashboards`

Rejected because direct file mutation bypasses Home Assistant's in-memory
collection, validation, listeners and save scheduling.

## Consequences

### Positive

- The dashboard appears in Home Assistant's normal dashboard list.
- Users control its ordering, title, icon, sidebar visibility and deletion.
- Deletion persists across integration reloads and Home Assistant restarts.
- Dashboard contents still follow configured tariff forecast entities
  automatically.
- Opening the automatic dashboard no longer depends on Community-strategy
  registration timing.
- No YAML or third-party chart card is required.

### Trade-offs

- Provisioning relies on a documented Home Assistant internal lookup until a
  public Python dashboard-creation API exists.
- The first automatic creation requires Lovelace storage mode and its active
  WebSocket collection.
- Restoring a deliberately deleted dashboard requires the explicit integration
  options action or manual creation under **Settings → Dashboards**.

## Invariants for future changes

- Never overwrite an existing matching dashboard.
- Migrate only the exact legacy strategy-only configuration created by the
  integration.
- Never recreate a dashboard deleted after the current layout was provisioned;
  recover a missing legacy dashboard once during layout migration.
- Let the explicit options action override only the deletion marker, never the
  existing-dashboard ownership guard.
- Never delete the user-owned dashboard when a tariff entry is unloaded.
- Use the active Home Assistant collection, not a parallel storage instance.
- Keep provisioning failure independent from tariff sensor availability.
