# PA NEXUS V3 — BROWSER TEST PROTOCOL

## Browser is the final UI authority

API tests cannot prove:
- CSS loaded;
- buttons clickable;
- popovers open;
- scroll is correct;
- layout fits;
- avatar appears;
- three-dot menus work.

Therefore Playwright is mandatory.

## Target viewports

1366×768
1440×900
1536×1024
1920×1080

## Console

Fail on:
- uncaught exception;
- failed module load;
- failed stylesheet;
- critical console error.

## Network

Fail on:
- JS 404;
- CSS 404;
- API 500;
- unexpected authentication loop.

## Chat test

- login;
- open Chat;
- create conversation;
- send via button;
- send via Enter;
- newline via Shift+Enter;
- refresh;
- rename;
- delete;
- reopen.

## Voice test

- login;
- open Voice;
- verify outer document fixed;
- scroll history;
- verify outer document remains fixed;
- start;
- stop;
- permission state;
- transcript fixture;
- response fixture;
- interruption fixture.

## Navigation test

For every route:
- click;
- verify URL;
- verify page heading;
- verify active nav.

## Profile test

- click avatar;
- verify account menu;
- verify no unexpected navigation;
- open profile;
- update display name;
- verify header.

## Alert test

- generate test alert;
- click bell;
- verify panel;
- mark read.

## Provider test

- open settings;
- select provider;
- select model;
- enter mock key;
- save;
- verify card;
- test;
- reorder;
- refresh;
- verify order.

## Scroll test

At every desktop viewport:
- outer document height == client height;
- designated scroll container scrollTop changes when content is long.

Voice:
- main workspace must remain fixed.

## Screenshot test

Capture:
- dashboard;
- chat;
- voice;
- provider settings.

Store artifacts with cycle number.

## Environment gate

If browser cannot launch:
mark:
`BLOCKED — BROWSER ENVIRONMENT`

Never:
`PASS`.
