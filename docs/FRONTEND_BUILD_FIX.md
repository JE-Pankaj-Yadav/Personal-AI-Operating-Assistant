# PA NEXUS V3.0.1 Frontend Build Fix

## Root cause
The Windows run log reached `npm run typecheck` and `npm run build`, then TypeScript failed because `frontend/src/services/api.ts` referenced `Conversation`, `Message`, `Provider`, `User`, and `Alert` without importing them. The chat page also allowed a nullable conversation variable to flow into code that requires a concrete `Conversation`, and the auth store consumed untyped/unknown API responses.

## Changes
- Added explicit type-only imports to `services/api.ts`, `ChatPage.tsx`, `auth.tsx`, and other type consumers.
- Added explicit generic return types to API methods used by authentication, conversations, messages, providers, profile, and alerts.
- Reworked chat send flow to resolve a concrete `Conversation` before using its id.
- Typed authentication credentials and auth responses.
- Kept runtime behavior unchanged for the user-facing chat workflow.
- Version bumped to frontend 3.0.1.

## Expected result on Windows
After extracting the release, run `run.bat`. The existing Python 3.14 environment and dependency installation can proceed as before. If `package-lock.json` is absent, the runner performs `npm install`; otherwise it performs `npm ci`. The frontend must then pass `npm run typecheck` and `npm run build`, producing `frontend/dist/index.html`.

## Important validation note
This sandbox cannot reliably reach the npm registry, so a clean dependency installation and Vite browser build could not be re-executed here. The reported TypeScript errors were corrected directly against the source shown in the Windows build log.
