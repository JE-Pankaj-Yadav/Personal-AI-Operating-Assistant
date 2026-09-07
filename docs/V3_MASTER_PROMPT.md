# PA NEXUS V3 — SINGLE MASTER PROMPT
## COPY THIS PROMPT TO THE CODING AI

---

# 0. STOP. READ BEFORE WRITING ANY CODE.

You are not being asked to repair an old application.

You are being asked to create a **brand-new PA NEXUS application from an empty directory**.

The old PA NEXUS/JARVIS projects, old ZIPs, old source code, old build artifacts, old virtual environments and old runtime assumptions are **evidence and lessons only**.

Do not import old code.

Do not copy old source files.

Do not patch old architecture.

Do not reuse an old `frontend/src/app.js`.

Do not reuse an old database.

Do not reuse an old `.venv`.

Do not use an old `node_modules`.

Do not assume an old port.

Do not assume an old working directory.

Create the new project from scratch.

The only things you may reuse conceptually are:
1. functional requirements;
2. lessons from failures;
3. visual design language from the supplied screenshots;
4. validated architectural ideas.

---

# 1. YOUR ROLES

You must execute the project as a controlled engineering organization.

## Role A — Principal Architect

Before coding:
- define architecture;
- define boundaries;
- define data model;
- define API contracts;
- define runtime contract;
- define provider interface;
- define routing contract;
- define UI shell contract;
- define test architecture.

## Role B — Senior Software Developer

Implement the application.

Do not stop at mock screens.

Every visible control must have a real implementation or must be clearly marked as unavailable/configuration-dependent.

## Role C — Senior AI Engineer

Implement:
- multi-provider adapters;
- model selection;
- capability matching;
- quota/usage abstraction;
- auto-switch;
- Context Capsule continuity;
- source-aware routing.

## Role D — Senior DevOps Engineer

Implement:
- deterministic runner;
- clean environment bootstrap;
- migrations;
- build;
- health checks;
- packaging;
- Docker.

## Role E — Senior Security Engineer

Implement:
- authentication;
- authorization;
- password hashing;
- OTP;
- secure sessions;
- encrypted provider secrets;
- upload security;
- safe logging.

## Role F — Senior UI/UX Engineer

Reproduce the supplied visual language at high fidelity.

Do not replace the reference with a generic dashboard.

## Role G — Senior QA Engineer

Build automated tests before declaring feature completion.

## Role H — Independent Senior Tester

Do not trust the Developer's claims.

Run the application.

Click the actual UI.

Inspect browser console/network failures.

Test persistence.

Test failure paths.

Test clean installation.

## Role I — AI Engineering Manager

Review only after evidence exists.

Do not award 10/10 unless the objective acceptance gate passes.

---

# 2. THE MOST IMPORTANT LESSON FROM THE PREVIOUS FAILURE

The previous project could produce:
- a passing JavaScript syntax check;
- a passing build;
- passing backend tests;
- passing API QA cycles;

while still not meeting the intended product quality.

The previous manager report explicitly identified the dependency-light frontend as an architectural deviation and stated that browser acceptance was blocked/unverified.

Therefore:

# A BUILD IS NOT A PRODUCT.

A passing unit test is not proof that a UI works.

An API test is not proof that a button works.

A generated screenshot is not proof that the page behaves correctly.

A server health endpoint is not proof that the application works.

A “10-cycle” API test is not proof of ten complete Developer/Tester UI cycles.

A manager must never infer missing evidence.

---

# 3. ARCHITECTURE CONFORMANCE IS A HARD GATE

The previous generated application used:
- a dependency-light frontend;
- a single `frontend/src/app.js`;
- a single compressed/minified CSS file;
- no real React component architecture.

That implementation is rejected for V3.

## Mandatory frontend

Use:
- React;
- TypeScript;
- Vite;
- componentized architecture.

The final source must visibly contain:
- `package.json` with React dependencies;
- `.tsx` components;
- typed interfaces/types;
- route/page components;
- shared layout components;
- hooks/services/stores as appropriate;
- a real TypeScript build.

Do not create a fake React-looking folder while implementing everything in one JavaScript file.

## Mandatory architecture test

A test must fail the build if:
- React dependency is missing;
- TypeScript is missing;
- Vite is missing;
- source contains a single-file monolith above the defined threshold;
- required page/component directories are missing.

---

# 4. TECHNOLOGY DECISION

Preferred stack:

Frontend:
- React
- TypeScript
- Vite
- Tailwind CSS or a carefully designed CSS system
- Lucide React or equivalent SVG icon library
- React Router
- TanStack Query or equivalent where useful
- lightweight state management

Backend:
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- HTTPX

Testing:
- Vitest
- React Testing Library
- Playwright
- pytest

Database:
- SQLite for local development;
- PostgreSQL-ready.

Container:
- Docker.

Do not select versions by using unpinned `latest`.

Create a compatibility matrix.

---

# 5. REQUIRED PROJECT TREE

Use a structure similar to:

PA_NEXUS/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── users/
│   │   ├── conversations/
│   │   ├── messages/
│   │   ├── providers/
│   │   ├── models/
│   │   ├── routing/
│   │   ├── usage/
│   │   ├── capsule/
│   │   ├── voice/
│   │   ├── files/
│   │   ├── projects/
│   │   ├── weather/
│   │   ├── wikipedia/
│   │   ├── notifications/
│   │   ├── monitoring/
│   │   ├── security/
│   │   └── database/
│   ├── migrations/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── features/
│   │   │   ├── chat/
│   │   │   ├── voice/
│   │   │   ├── providers/
│   │   │   ├── profile/
│   │   │   ├── projects/
│   │   │   └── dashboard/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── types/
│   │   ├── lib/
│   │   └── styles/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.ts
├── tests/
│   ├── e2e/
│   ├── frontend/
│   ├── backend/
│   ├── security/
│   ├── architecture/
│   └── fixtures/
├── scripts/
│   ├── run.bat
│   ├── run.ps1
│   ├── run.sh
│   ├── healthcheck.bat
│   ├── healthcheck.sh
│   └── verify_release.*
├── docker/
├── docs/
├── data/
├── uploads/
├── logs/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md

Do not create an artificial structure and then ignore it.

---

# 6. VISUAL REFERENCE CONTRACT

Three reference screens are supplied:
- Chat Assistant Dashboard;
- Control Center Dashboard;
- Voice Assistant Dashboard.

Treat them as visual acceptance references.

The product should feel like the same product family:
- dark navy/black;
- cyan primary accent;
- blue/violet secondary accents;
- thin luminous borders;
- compact cards;
- dense professional information layout;
- subtle depth;
- restrained glow;
- fixed desktop shell;
- large circular voice visualization;
- waveform;
- compact status badges.

Do not make it:
- a generic SaaS dashboard;
- a gaming HUD;
- a purple-heavy AI template;
- a card grid with unrelated spacing;
- a simplistic chatbot.

Use real SVG icons.

Do not use arbitrary Unicode characters such as `◉`, `♩`, `⌂`, `▣`, `⚿` as the primary icon system.

---

# 7. DESKTOP SHELL — ABSOLUTE SCROLL CONTRACT

This requirement is especially important because the previous implementation still did not provide the intended visual acceptance proof.

At desktop target sizes:
- 1366×768
- 1440×900
- 1536×1024
- 1920×1080

The global page must not vertically scroll.

Use:

html,
body,
#root {
  width: 100%;
  height: 100%;
}

The desktop shell must use:
- fixed viewport;
- explicit header height;
- explicit navigation region;
- content region constrained to remaining viewport;
- internal overflow containers.

## Control Center

No browser page scrollbar.

## Chat

Only:
- conversation list;
- message list;
- code block;
may scroll.

Header and composer remain fixed.

## Voice

This is non-negotiable:

The **main Voice Assistant dashboard must not scroll**.

The outer browser page must not scroll.

The main voice interaction area must remain fixed in the viewport.

Only:
- Voice Conversation History;
- transcript panel when necessary

may scroll.

If the content does not fit:
do not add page scrolling.

Redesign the internal grid.

## Navigation

Left navigation may collapse.

Expanded and collapsed states must not alter the global page scroll contract.

## Mobile

Mobile may scroll.

The desktop and mobile layout systems must be intentionally different.

---

# 8. GLOBAL NAVIGATION

Required entries:
- Control Center
- Chat Assistant
- Voice Assistant
- Projects
- Files
- AI Providers
- Usage
- Settings
- Logs
- Help
- Logout

Navigation:
- open;
- collapsed;
- active;
- hover;
- focus;
- tooltip when collapsed.

Active state must derive from the router.

Do not maintain an independent `state.page` that can disagree with the URL.

## Mandatory regression

For every route:
- URL;
- rendered page;
- highlighted navigation item

must agree.

---

# 9. PROFILE BUTTON

The profile/avatar control in the header is an account control.

Clicking it must open:
- account menu;
- profile;
- settings;
- logout;
- optional status.

It must NOT unexpectedly navigate directly to Settings.

This exact failure occurred previously.

Add a browser regression test:
1. open dashboard;
2. click profile;
3. assert popover appears;
4. assert URL did not unexpectedly change to Settings;
5. click Settings within popover;
6. assert navigation.

---

# 10. ALERT CENTER

Notification bell must open a real panel.

The panel contains:
- unread count;
- severity;
- title;
- message;
- source;
- timestamp;
- action;
- mark read;
- mark all read;
- optional filtering.

Clicking the bell must be testable in Playwright.

Do not make the panel a static hidden HTML block that is never actually wired.

---

# 11. CONTROL CENTER

Build the dashboard composition shown in the reference.

Top:
- Weather;
- Battery;
- Network;
- AI Usage;
- AI Assistant.

Middle:
- CPU;
- RAM;
- Active Model.

Lower:
- Camera/device;
- Upload File;
- Upload Folder.

Bottom:
- System Overview.

Right-side:
- Chat mini panel;
- Voice mini panel.

Each card must have a meaningful state.

Allowed terminal states:
- value;
- not configured;
- unavailable;
- permission required;
- error.

Never allow:
- infinite `Loading...`;
- spinner forever;
- fake values.

---

# 12. BATTERY

If the browser/device exposes battery information:
show:
- percentage;
- charging;
- charging time where available;
- discharging time where available.

If not:
show:
`Battery information unavailable on this device/browser.`

Do not show:
`87%`
unless the value actually came from a supported source.

Test both:
- API available fixture;
- API unavailable fixture.

---

# 13. NETWORK SPEED

Do not fabricate network speed.

Distinguish:
- browser connection hints;
- measured download;
- measured upload;
- ping;
- unavailable.

Do not run heavy speed tests every second.

Provide configurable polling or manual measurement.

Show:
`Measured`
or
`Estimated`
or
`Unavailable`.

Never label an estimate as an official speed test.

---

# 14. WEATHER

Settings must allow:
- provider;
- API key where required;
- location;
- units;
- refresh interval;
- test connection;
- save;
- remove/reset.

Control Center reads the saved configuration.

If missing:
`Weather API not configured`.

If network/API fails:
show a useful error and preserve dashboard operation.

---

# 15. CHAT ASSISTANT

Visual composition must closely follow the reference.

Required:
- conversation sidebar;
- New Conversation;
- search;
- files area;
- main conversation;
- fixed composer;
- assistant response cards;
- user bubbles;
- code blocks;
- message actions.

## Keyboard behavior

Enter:
send.

Shift+Enter:
newline.

Send button:
must call the same `submitMessage()` implementation.

No duplicate implementation.

## Browser test

Type:
`Hello`

press Enter.

Assert:
- user message appears;
- network request is sent;
- assistant response appears or deterministic mock response;
- conversation persists after refresh.

Then:
type two-line text using Shift+Enter;
assert no submission occurred until Enter.

---

# 16. CHAT PERSISTENCE

A conversation must survive:
- route change;
- browser refresh;
- logout/login;
- provider switch.

Conversation identity belongs to PA NEXUS, not to an external provider.

---

# 17. CONVERSATION HISTORY

Chat and Voice histories are separate.

Database field:
`conversation_type`.

Allowed:
- `chat`
- `voice`

Never merge them accidentally.

## Three-dot menu

Every history item must have:
- Rename;
- Delete;
- Archive;
- Export;
- Clone/branch where supported;
- Context Capsule.

Destructive operations require confirmation.

Rename must persist to database.

Delete must persist.

Refresh must show the renamed title.

---

# 18. VOICE ASSISTANT

Voice is not a decorative microphone animation.

It is a real state machine.

States:

IDLE
LISTENING
PROCESSING
SPEAKING
INTERRUPTED
ERROR
PERMISSION_REQUIRED

Main control:

IDLE:
`Start Listening`

LISTENING:
`Stop Listening`

No ambiguous duplicate microphone buttons.

---

# 19. VOICE LOOP

Start:
→ microphone permission
→ listening
→ VAD/silence detection
→ transcription
→ AI routing
→ response
→ TTS
→ listening again

Stop:
→ cancel active listening
→ cancel active TTS where appropriate
→ return to IDLE.

If the user speaks while TTS is playing:
- interrupt TTS;
- begin a new utterance.

---

# 20. VOICE HISTORY

Voice history has its own:
- search;
- New Conversation;
- rename;
- delete;
- archive;
- export;
- three-dot menu.

The history panel may scroll.

The main voice dashboard may not page-scroll on desktop.

---

# 21. VOICE REFERENCE QUALITY

Main workspace must visually contain:
- Voice Interaction heading;
- listening state;
- large central microphone;
- concentric rings;
- left/right waveform;
- timer;
- Start/Stop;
- response card;
- response waveform;
- Speak Again;
- PA identity/avatar.

The rings and waveform should animate according to state.

They must not be a permanently looping decoration while the system is idle.

---

# 22. PROVIDER SETTINGS

This must be a first-class settings area.

The user must be able to configure multiple providers.

Entry flow:

1. Provider company
2. Model
3. API key
4. Optional endpoint/configuration
5. Save
6. Test
7. Provider card appears

Providers may include:
- Google/Gemini;
- OpenAI;
- Anthropic;
- NVIDIA;
- custom OpenAI-compatible;
- Mock provider.

Do not hardcode one provider.

---

# 23. PROVIDER CARD

Each card displays:
- company/provider;
- model;
- masked API key;
- health;
- enabled/disabled;
- priority;
- preferred;
- last tested;
- latency;
- usage;
- exact/estimated indicator.

Actions:
- Test Connection;
- Edit;
- Enable;
- Disable;
- Remove;
- Set Preferred;
- Reorder.

---

# 24. DRAG-AND-DROP

Provider/model cards are reorderable.

Dragging changes:
- priority;
- fallback order.

The order persists.

Drag-and-drop must have:
- drag handle;
- drag-over state;
- drop indicator;
- keyboard alternative.

Do not make drag-and-drop the only reordering mechanism.

---

# 25. TEST CONNECTION

Test Connection must perform a real request in real-provider mode.

Result states:
- testing;
- healthy;
- authentication failed;
- rate limited;
- model unavailable;
- timeout;
- network error;
- provider unavailable;
- invalid request.

Display:
- provider;
- model;
- latency;
- safe HTTP status;
- timestamp;
- request ID.

Never display the API key.

Never claim healthy without an actual successful test.

---

# 26. API CREDENTIAL STORAGE

This requirement needs a security correction compared with simplistic earlier implementations.

The authoritative user credential store must be:
- server-side;
- encrypted at rest;
- accessible only through authorized server services.

The `.env` file is for application/bootstrap secrets.

Do not automatically write every user's API key into a plaintext `.env`.

If this is a single-user local mode and the user explicitly requests `.env` synchronization:
- make it explicit;
- warn that it is sensitive;
- protect the file;
- never expose it to the frontend;
- never commit it;
- never log it.

The database/encrypted store remains the authoritative credential record.

---

# 27. PROVIDER MODEL DISCOVERY

Where the provider supports model discovery:
- fetch model list;
- filter by capabilities;
- show supported models.

Where it does not:
- show known configured models;
- allow custom model ID.

Do not pretend that every provider supports model discovery.

---

# 28. PROVIDER ADAPTER CONTRACT

Conversation layer must never contain provider-specific HTTP code.

Interface:

- health_check;
- list_models;
- chat;
- stream;
- count_tokens if available;
- usage;
- capabilities;
- normalize_error.

Provider-specific SDK/API behavior stays in adapters.

---

# 29. AUTO SWITCHING

Default:
- 80% informational;
- 90% critical warning;
- 95% switch.

The user can configure thresholds.

Usage can be:
- exact;
- estimated;
- configured local quota.

The UI must explicitly state which one it is.

---

# 30. CONTEXT CAPSULE

Do not wait until 95% to create the first capsule.

Maintain incrementally:
- objective;
- current task;
- requirements;
- constraints;
- decisions;
- stack;
- files;
- important code;
- known bugs;
- pending work;
- recent messages;
- user project preferences;
- model/provider history.

Version every capsule.

---

# 31. SWITCHING ALGORITHM

Before each request:

1. load conversation;
2. load project;
3. load capsule;
4. load usage;
5. calculate projected usage where possible;
6. evaluate threshold;
7. determine required capabilities;
8. select active provider if safe;
9. otherwise select compatible healthy fallback;
10. prepare capsule;
11. switch;
12. persist switch event;
13. notify user;
14. continue the same conversation.

Do not silently create a new conversation.

---

# 32. CAPABILITY MATCHING

If the current request needs:
- text;
- image;
- audio;
- code;
- structured output;

the replacement model must support the required capability.

Never route blindly by provider priority alone.

---

# 33. SWITCH FAILURE

If candidate 1 fails:
try candidate 2.

Maximum fallback count configurable.

Do not retry forever.

Authentication failures should not be endlessly retried.

If all candidates fail:
- preserve the conversation;
- show actionable error;
- create alert;
- do not lose the user's message.

---

# 34. PROFILE

Settings:
- display name;
- username;
- email;
- timezone;
- language;
- avatar;
- theme;
- notifications.

Header reflects saved profile immediately.

Avatar:
- upload;
- replace;
- remove;
- validate;
- persist;
- refresh-safe.

---

# 35. PASSWORD CHANGE

Normal flow:

Current Password
New Password
Confirm New Password

Use Argon2id.

Verify current password before changing.

Invalidate appropriate sessions after successful change.

---

# 36. OTP PASSWORD RESET

Flow:

Forgot Password
→ email
→ OTP
→ verify
→ new password
→ confirm
→ reset.

OTP:
- six digits;
- hashed at rest;
- short TTL;
- one-time use;
- attempt limit;
- resend cooldown;
- rate limit.

SMTP is environment-dependent.

Automated tests must use a fake mail provider.

A real SMTP test may be environment-gated but must not be falsely reported as PASS.

---

# 37. AUTHENTICATION GATE

Before authentication state is known:
show a controlled loading/auth-check state.

If unauthenticated:
show login.

Never render private dashboard data before authentication.

First visit must not accidentally open an authenticated dashboard.

---

# 38. FILES

Support:
PDF
DOCX
TXT
CSV
XLSX
JSON
PNG
JPG
JPEG
WEBP

Validate:
- extension;
- MIME;
- size;
- filename.

Store safely.

Never execute uploads.

Show progress/status/error.

Upload cards:
- pointer cursor;
- hover;
- drag-over state;
- keyboard focus.

---

# 39. PROJECTS

Projects must contain:
- overview;
- requirements;
- tasks;
- conversations;
- files;
- architecture;
- decisions;
- bugs;
- notes;
- memory;
- Context Capsule.

Do not implement only a “Create Project” button and call Projects complete.

---

# 40. ERROR UX

Never use only:
`Something went wrong.`

Every failure must identify:
- module;
- category;
- user-safe explanation;
- action;
- request ID.

Examples:
- API authentication failed;
- weather not configured;
- microphone permission denied;
- database unavailable;
- upload rejected.

---

# 41. LOADING STATES

Every asynchronous UI has:
- initial loading;
- success;
- empty;
- error;
- retry.

No infinite spinner.

Set timeouts.

---

# 42. REAL DATA POLICY

Never fabricate:
- CPU;
- RAM;
- battery;
- network;
- weather;
- AI health;
- token quota.

Use:
- actual value;
- estimated value with label;
- unavailable;
- not configured.

---

# 43. LIGHT THEME

Light mode must be deliberately designed.

Do not simply invert the dark theme.

Test:
- text;
- borders;
- icons;
- cards;
- inputs;
- status colors;
- charts;
- dialogs.

---

# 44. SECURITY

Mandatory:
- Argon2id;
- secure sessions;
- authorization;
- encrypted provider secrets;
- rate limiting;
- safe uploads;
- XSS-safe markdown;
- SQL parameterization/ORM;
- secure headers;
- restricted CORS;
- no secret logs.

AI-generated code must never execute directly on the host.

---

# 45. RUNNER — FIX THE PREVIOUS RUNTIME PROBLEMS

The previous project had real failures including:
- Node 24 while the runner expected Node 20–22;
- `npm`/`npm.cmd` environment differences;
- npm executing in `scripts` and looking for `scripts/package.json`;
- SQLite unable to open because path resolution depended on execution context;
- `ModuleNotFoundError: No module named 'app'`;
- Windows path/URL confusion;
- asset mismatch/404 risk;
- browser acceptance blocked/unverified;
- a frontend architecture much lighter than specified.

V3 must prevent these classes permanently.

---

# 46. PROJECT ROOT

Every script must derive the project root from its own location.

Never depend on:
`%CD%`
or the caller's working directory.

Use:
- Windows batch-safe root resolution;
- PowerShell root resolution;
- POSIX shell root resolution.

---

# 47. WINDOWS RUNNER

Required:
`run.bat`
`run.ps1`

The runner must:
1. resolve root;
2. print root;
3. verify runtime;
4. choose project-managed runtime if available;
5. create Python venv;
6. install backend dependencies;
7. install frontend dependencies from `frontend`;
8. run type check;
9. build frontend;
10. run migrations;
11. run backend import smoke test;
12. start server;
13. health-check;
14. print URL.

Use:
`pushd "%ROOT%\frontend"`
and `popd`.

When invoking batch-based npm commands, use `call` where required.

But do not hard-code `npm.cmd`.

Resolve the actual executable safely.

---

# 48. NODE RUNTIME

The previous runner failed because it encountered Node 24.20.0 while requiring Node 20–22.

V3 must not merely say:
“Node 20–22 required.”

It must either:
- use a project-managed pinned Node runtime;
- use Docker;
- or provide a deterministic supported-runtime bootstrap.

If global Node is used as an explicitly supported fallback:
- detect version;
- reject unsupported versions;
- explain exactly what to install/use.

Never silently use Node 24 when package compatibility requires another version.

---

# 49. PYTHON RUNTIME

Use a documented supported Python version.

Create `.venv`.

Run:
`python -m pip`

not a random global `pip`.

Before server startup:
run:
- import smoke test;
- settings load;
- DB connection;
- migration status.

---

# 50. PYTHON IMPORT CONTRACT

Choose exactly one package strategy.

Preferred:
install backend package or use explicit `--app-dir`.

Internal imports must consistently use:
`from app...`

or another single strategy.

Do not mix:
`backend.app...`
with:
`app...`

Test:
`python -c "import app.main"`

from the exact execution context used by the runner.

---

# 51. DATABASE PATH CONTRACT

SQLite path must be canonical.

Do not depend on current directory.

Compute:
`PROJECT_ROOT/data/pa_nexus.db`

Create the parent directory before opening SQLite.

Alembic and runtime must use the same resolved path.

Test from:
- project root;
- `scripts`;
- another working directory.

All must point to the same database.

---

# 52. WINDOWS PATH CONTRACT

Never create filesystem paths by string-concatenating URLs.

Do not produce:
`E:\E:\...`

Do not treat:
`%20`
as a literal filesystem path.

Use platform-aware path libraries.

---

# 53. FRONTEND ASSET CONTRACT

Frontend build output and backend static serving must agree exactly.

After build:
- parse generated HTML;
- find JS/CSS asset references;
- verify files exist;
- start server;
- request every referenced asset;
- assert HTTP 200.

This is a mandatory automated test.

Do not call the application ready while `/assets/*` returns 404.

---

# 54. DATABASE MIGRATIONS

Use Alembic.

Never rely on:
`Base.metadata.create_all()`

as the production schema migration mechanism.

Fresh database:
migration upgrade
→ startup
→ health
→ smoke test.

---

# 55. DEPENDENCY MANAGEMENT

Pin:
- backend dependencies;
- frontend dependencies;
- browser test dependencies.

Use lock files.

Do not use:
`npm install` when deterministic `npm ci` is appropriate.

Do not use:
`pip install package`
without a pinned requirements/lock strategy.

---

# 56. DOCKER

Provide a first-class Docker build.

The container must not depend on host Python/Node.

Use:
- pinned base images;
- multi-stage build;
- non-root runtime where practical;
- healthcheck;
- environment variables;
- no baked secrets.

---

# 57. CLEAN-ROOM TEST

Before release:

1. Create a brand-new directory with spaces in its path.
2. Extract ZIP.
3. Confirm no `.venv`.
4. Confirm no `node_modules`.
5. Run `run.bat`.
6. Confirm runtime.
7. Confirm dependencies.
8. Confirm migrations.
9. Confirm frontend build.
10. Confirm asset HTTP 200.
11. Confirm backend health.
12. Open browser.
13. Login.
14. Test Chat.
15. Test Voice.
16. Test Provider.
17. Test Profile.
18. Test Password/OTP mock.
19. Test Weather.
20. Test history.
21. Test alerts.
22. Test fixed-shell behavior.
23. Restart.
24. Repeat smoke test.

---

# 58. TEST ARCHITECTURE

You must create:
- unit tests;
- integration tests;
- API tests;
- database tests;
- frontend component tests;
- browser E2E tests;
- security tests;
- architecture conformance tests;
- runner tests;
- asset tests.

---

# 59. BROWSER TESTS ARE MANDATORY

The previous release had Playwright tests that could not execute because the environment blocked localhost navigation.

Therefore:
- if the current environment can run browser tests, run them;
- if not, do not call them PASS;
- provide a clearly marked environment-gated result;
- the final release must include instructions for a real browser acceptance run;
- do not allow manager 10/10 until actual browser acceptance is completed in an environment capable of it.

---

# 60. SCREENSHOT ACCEPTANCE

For each target size:
- capture screenshot;
- inspect layout;
- compare against reference;
- record differences.

Targets:
1366×768
1440×900
1536×1024
1920×1080

Test:
- Control Center;
- Chat;
- Voice;
- Settings;
- Provider settings.

---

# 61. SCROLL ACCEPTANCE TEST

Use Playwright:

At each desktop size:
assert:
`document.documentElement.scrollHeight === document.documentElement.clientHeight`

for:
- Control Center;
- Chat;
- Voice.

Then assert designated internal containers have scrollable overflow where expected.

For Voice specifically:
- main shell remains fixed;
- history panel scrolls;
- outer document does not.

---

# 62. INTERACTION ACCEPTANCE

Every major button must have a test.

Minimum:
- New Conversation;
- Send;
- Enter;
- Stop generation;
- Start Listening;
- Stop Listening;
- Rename;
- Delete;
- Archive;
- three-dot;
- notification;
- profile;
- navigation;
- collapse;
- provider save;
- provider test;
- provider reorder;
- provider remove;
- profile save;
- avatar upload;
- password change;
- OTP reset;
- weather save;
- upload file;
- upload folder.

---

# 63. TEN QA CYCLES

Run ten **complete** cycles.

Each cycle must include:
Developer build/fix
→ independent Tester
→ defect report
→ Developer root-cause fix
→ Tester retest
→ regression
→ evidence
→ sign-off.

The cycles must not be ten API-only test functions.

---

# 64. CYCLE 1 — FOUNDATION

Test:
- install;
- auth;
- navigation;
- dashboard;
- routing;
- assets;
- database.

---

# 65. CYCLE 2 — UI SHELL

Test:
- header;
- sidebar;
- open/close;
- profile menu;
- alert center;
- dark/light;
- desktop scroll.

---

# 66. CYCLE 3 — CHAT

Test:
- create;
- send;
- Enter;
- Shift+Enter;
- streaming;
- cancel;
- persistence;
- rename;
- delete;
- search;
- three-dot.

---

# 67. CYCLE 4 — VOICE

Test:
- permission;
- start;
- stop;
- VAD;
- transcript;
- response;
- TTS;
- interruption;
- separate history;
- no page scroll.

---

# 68. CYCLE 5 — PROVIDERS

Test:
- provider selection;
- model;
- key;
- save;
- encryption;
- test connection;
- reorder;
- enable;
- disable;
- remove;
- model discovery.

---

# 69. CYCLE 6 — ROUTING/SWITCH

Test:
- 80%;
- 90%;
- 95%;
- capability matching;
- capsule;
- switch event;
- alert;
- fallback;
- switch failure;
- conversation continuity.

---

# 70. CYCLE 7 — PROFILE/SECURITY

Test:
- profile;
- avatar;
- email;
- timezone;
- current-password change;
- OTP;
- session invalidation;
- rate limiting;
- authorization;
- secret leakage.

---

# 71. CYCLE 8 — FILES/PROJECTS/WEATHER

Test:
- uploads;
- drag/drop;
- file security;
- projects;
- tasks;
- memory;
- weather;
- failure states.

---

# 72. CYCLE 9 — PERFORMANCE/FAILURE

Test:
- long chat;
- many history items;
- provider timeout;
- 401;
- 429;
- 5xx;
- network loss;
- DB unavailable;
- restart;
- recovery.

---

# 73. CYCLE 10 — FULL RELEASE REGRESSION

Repeat:
- all critical workflows;
- all security;
- all UI;
- all browser;
- all runtime;
- all asset;
- all provider;
- all switching;
- all profile;
- all file tests.

No shortcut.

---

# 74. DEFECT REPORT

Every defect:

ID
Severity
Environment
Module
Preconditions
Steps
Expected
Actual
Screenshot/video/log
Request ID
Root cause
Fix
Regression test
Retest result

Severity:
P0 blocker
P1 critical
P2 high
P3 medium
P4 cosmetic

No P0/P1 release.

---

# 75. TEST INTEGRITY

The Tester must never:
- edit production code to make a test pass;
- weaken assertions;
- skip a failing test;
- mark a blocked test PASS;
- accept screenshots as proof of functionality.

---

# 76. MANAGER REVIEW

After ten cycles, Manager reviews:
- architecture;
- UI;
- functionality;
- AI routing;
- provider system;
- switching;
- continuity;
- security;
- performance;
- installation;
- testing;
- documentation.

Score 0–10 for each.

The final score is evidence-based.

---

# 77. 10/10 GATE

10/10 requires:
- no known P0/P1;
- architecture conformance;
- real browser acceptance;
- all mandatory interaction tests;
- all critical security tests;
- clean-room installation;
- asset checks;
- fixed-scroll checks;
- provider workflow;
- profile workflow;
- OTP mock workflow;
- switching continuity;
- ten complete QA cycles;
- documentation;
- release ZIP verification.

If score is 9.9, it is NOT 10/10.

Send back to Developer.

---

# 78. NO FAKE COMPLETION

Never write:
- “completed” because files exist;
- “tested” because tests were written;
- “10/10” because tests were green;
- “API healthy” without real health result;
- “zero bugs” when browser testing was not performed.

Use:
PASS
FAIL
BLOCKED
NOT EXECUTED
ENVIRONMENT-GATED

---

# 79. RELEASE ARTIFACT

Final ZIP must not contain:
- `.venv`;
- `node_modules`;
- real `.env`;
- real API keys;
- passwords;
- OTPs;
- temporary logs;
- cache.

It must contain:
- source;
- lock files;
- migrations;
- tests;
- runner;
- Docker;
- docs;
- `.env.example`;
- validation report.

---

# 80. FINAL RELEASE REPORT

Include:
- architecture;
- runtime versions;
- build result;
- test counts;
- ten-cycle results;
- browser results;
- security results;
- known limitations;
- manager score;
- release decision.

---

# 81. FINAL COMMAND

Now execute the project as a senior engineering organization.

Do not merely generate a UI.

Do not create a fake demo.

Do not build a single-file JavaScript substitute for the requested React/TypeScript architecture.

Do not copy the previous implementation.

Do not rely on the current working directory.

Do not rely on unsupported Node/Python versions.

Do not use relative SQLite paths.

Do not mix Python import roots.

Do not leave `/assets` unverified.

Do not leave profile click behavior ambiguous.

Do not leave telemetry stuck in loading.

Do not leave provider configuration superficial.

Do not leave password recovery incomplete.

Do not leave avatar handling disconnected.

Do not mix Chat and Voice histories.

Do not allow Voice desktop page scrolling.

Do not allow fake metrics.

Do not allow decorative dead controls.

Do not allow a fake 10/10.

Build from scratch.

Test from scratch.

Package from scratch.

Release only after evidence.
