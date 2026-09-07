# PA NEXUS V3 — UI ACCEPTANCE MATRIX

This matrix converts the reference screens into executable acceptance criteria.

## Global

| ID | Requirement | PASS condition |
|---|---|---|
| UI-001 | Desktop shell fixed | Document does not scroll at target sizes |
| UI-002 | Navigation open/close | Both states work |
| UI-003 | Active navigation | Matches current route |
| UI-004 | Profile menu | Opens popover |
| UI-005 | Alert center | Opens panel |
| UI-006 | Pointer affordance | Interactive cards show pointer/hover |
| UI-007 | Dark theme | Matches visual system |
| UI-008 | Light theme | Readable dedicated palette |

## Control Center

| ID | Requirement | PASS condition |
|---|---|---|
| CC-001 | Weather | Real/configured/unavailable |
| CC-002 | Battery | Real or unavailable |
| CC-003 | Network | Measured/estimated/unavailable |
| CC-004 | CPU | Real or unavailable |
| CC-005 | RAM | Real or unavailable |
| CC-006 | AI usage | Exact/estimated label |
| CC-007 | Active model | Provider + model |
| CC-008 | Upload file | Click + drag/drop |
| CC-009 | Upload folder | Click + folder selection |
| CC-010 | System overview | Real values or explicit unavailable |
| CC-011 | No page scroll | PASS at all desktop sizes |

## Chat

| ID | Requirement | PASS condition |
|---|---|---|
| CH-001 | New conversation | Creates persisted record |
| CH-002 | Send button | Sends |
| CH-003 | Enter | Sends |
| CH-004 | Shift+Enter | Newline |
| CH-005 | Streaming | Response visibly streams |
| CH-006 | Stop | Stops generation |
| CH-007 | Rename | Persists |
| CH-008 | Delete | Persists after confirmation |
| CH-009 | Archive | Persists |
| CH-010 | Search | Finds conversations |
| CH-011 | Three dots | Opens menu |
| CH-012 | Fixed composer | Remains visible |
| CH-013 | Internal message scroll | Works |
| CH-014 | Outer page scroll | Disabled on desktop |

## Voice

| ID | Requirement | PASS condition |
|---|---|---|
| VO-001 | Start Listening | Activates state |
| VO-002 | Stop Listening | Returns idle |
| VO-003 | Permission | Handles denied/granted |
| VO-004 | VAD | Ends utterance after silence |
| VO-005 | STT | Transcript appears |
| VO-006 | AI response | Response appears |
| VO-007 | TTS | Response can be spoken |
| VO-008 | Interruption | TTS stops on new speech |
| VO-009 | Voice history | Separate dataset |
| VO-010 | History scroll | History can scroll |
| VO-011 | Main dashboard | Cannot page-scroll desktop |
| VO-012 | Rings | State-driven animation |
| VO-013 | Waveform | State-driven animation |
| VO-014 | Speak Again | Replays/repeats appropriately |

## Providers

| ID | Requirement | PASS condition |
|---|---|---|
| PR-001 | Provider select | Company can be selected |
| PR-002 | Model | Model selectable/custom |
| PR-003 | API key | Masked |
| PR-004 | Save | Persists |
| PR-005 | Test | Real/mock according to environment |
| PR-006 | Health | Accurate |
| PR-007 | Reorder | Persists |
| PR-008 | Enable/disable | Persists |
| PR-009 | Remove | Confirmed and persists |
| PR-010 | Secret | Never returned plaintext |

## Profile/security

| ID | Requirement | PASS condition |
|---|---|---|
| PF-001 | Display name | Header updates |
| PF-002 | Email | Persists |
| PF-003 | Timezone | Persists |
| PF-004 | Avatar upload | Persists |
| PF-005 | Avatar replace | Persists |
| PF-006 | Avatar remove | Persists |
| PF-007 | Current password | Works |
| PF-008 | OTP | Fake-mail E2E works |
| PF-009 | Session | Securely invalidated |
