# PA NEXUS V3 — REGRESSION DEFECT CATALOG

These are seed defects from previous generations. The new project must contain tests that would catch them if they reappeared.

## DEF-001 — One-file frontend
Expected: React/TypeScript component architecture.
Failure: plain JavaScript monolith.
Detection: architecture test.

## DEF-002 — Profile redirects to Settings
Expected: account popover.
Detection: Playwright click assertion.

## DEF-003 — Active sidebar wrong
Expected: route-driven active state.
Detection: route matrix E2E.

## DEF-004 — Voice outer scroll
Expected: fixed desktop shell.
Detection: document scroll-height test.

## DEF-005 — Chat send button dead
Expected: same submit path as Enter.
Detection: button click E2E.

## DEF-006 — Enter does not submit
Expected: Enter sends.
Detection: keyboard E2E.

## DEF-007 — Shift+Enter sends unexpectedly
Expected: newline.
Detection: keyboard E2E.

## DEF-008 — Chat/Voice history mixed
Expected: independent datasets.
Detection: database/API/E2E.

## DEF-009 — Three-dot menu decorative
Expected: real menu.
Detection: click/rename/delete.

## DEF-010 — Alert bell decorative
Expected: open panel.
Detection: click.

## DEF-011 — Battery fake
Expected: real/unavailable.
Detection: source-tagged telemetry test.

## DEF-012 — Network fake
Expected: measured/estimated/unavailable.
Detection: telemetry contract.

## DEF-013 — Weather stuck loading
Expected: success/error/unavailable terminal state.
Detection: timeout fixture.

## DEF-014 — Provider save without persistence
Expected: refresh-safe persistence.
Detection: save → reload.

## DEF-015 — Provider key exposed
Expected: never plaintext.
Detection: API response scan.

## DEF-016 — Drag reorder not persistent
Expected: priority persisted.
Detection: reorder → refresh.

## DEF-017 — Password change missing confirmation
Expected: Current/New/Confirm.
Detection: form test.

## DEF-018 — OTP not fully implemented
Expected: request/verify/reset.
Detection: fake mail E2E.

## DEF-019 — Avatar only cosmetic
Expected: upload/replace/remove persistence.
Detection: E2E.

## DEF-020 — SQLite path depends on cwd
Expected: canonical root path.
Detection: run migration from different cwd.

## DEF-021 — npm executes in scripts
Expected: frontend cwd.
Detection: runner test.

## DEF-022 — Unsupported Node accepted
Expected: deterministic runtime.
Detection: runtime matrix.

## DEF-023 — Python import failure
Expected: import smoke test.
Detection: runner preflight.

## DEF-024 — Assets 404
Expected: build/HTTP asset test.
Detection: asset crawler.

## DEF-025 — Browser test falsely PASS
Expected: blocked test remains blocked.
Detection: test result integrity.

## DEF-026 — Fake manager 10/10
Expected: score tied to evidence.
Detection: manager checklist.

## DEF-027 — Project page superficial
Expected: tasks/memory/bugs/notes etc.
Detection: feature matrix.

## DEF-028 — Voice animation decorative
Expected: state-driven animation.
Detection: state assertions.

## DEF-029 — Provider health inferred from saved key
Expected: actual test.
Detection: invalid-key test.

## DEF-030 — Auto-switch loses context
Expected: same conversation + capsule.
Detection: deterministic two-provider test.

## DEF-031 — Auto-switch infinite retry
Expected: bounded candidates.
Detection: simulated failures.

## DEF-032 — Estimated quota shown as exact
Expected: certainty label.
Detection: UI assertion.

## DEF-033 — Secret written to logs
Expected: redaction.
Detection: log scan.

## DEF-034 — Private data visible before login
Expected: auth gate.
Detection: unauthenticated browser test.

## DEF-035 — Upload executes
Expected: never execute.
Detection: security test.

## DEF-036 — Light mode unreadable
Expected: dedicated accessible theme.
Detection: screenshot/contrast test.

## DEF-037 — Infinite loading
Expected: timeout/error.
Detection: delayed-service fixture.

## DEF-038 — Wrong route after refresh
Expected: router preserves route.
Detection: refresh E2E.

## DEF-039 — Conversation rename only frontend
Expected: DB persistence.
Detection: reload.

## DEF-040 — Delete not confirmed
Expected: confirmation.
Detection: destructive action E2E.
