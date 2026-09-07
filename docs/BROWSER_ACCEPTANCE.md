# Browser Acceptance

1. Install dependencies and build frontend.
2. Start the application on `127.0.0.1:8011`.
3. Launch Chromium/Playwright.
4. Test 1366x768, 1440x900, 1536x1024, 1920x1080.
5. Verify no outer scroll on Control Center, Chat and Voice desktop pages.
6. Verify route-driven active navigation, profile popover, alert center, chat Enter/Shift+Enter/send, voice start/stop, provider save/test/reorder, profile save, uploads and refresh persistence.
7. Fail on console exceptions, stylesheet/module 404, API 500 or auth loops.
8. Store screenshots per cycle.
9. If browser navigation is blocked by the environment, record `BLOCKED — BROWSER ENVIRONMENT`.
