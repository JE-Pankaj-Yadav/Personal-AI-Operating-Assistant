# PA NEXUS V3 — ARCHITECTURE GATES

The Developer may not proceed to Manager review unless all gates pass.

## Gate A — Frontend architecture

Required:
- React;
- TypeScript;
- Vite;
- router;
- component hierarchy;
- typed API client;
- tests.

Reject:
- one-file frontend;
- plain JS pretending to be TypeScript;
- manual DOM rendering as the primary UI architecture;
- missing React dependencies.

## Gate B — Backend architecture

Required:
- FastAPI;
- service layer;
- repositories or equivalent boundary;
- provider adapters;
- migrations;
- settings/config;
- security module.

Reject:
- giant `main.py`;
- provider HTTP code inside routes;
- direct database access from UI concerns.

## Gate C — Provider abstraction

Required:
- provider interface;
- adapters;
- health;
- model;
- streaming;
- usage;
- normalized errors.

## Gate D — Database

Required:
- migrations;
- canonical paths;
- ownership constraints;
- indexes;
- test database;
- fresh migration test.

## Gate E — Runtime

Required:
- pinned supported versions;
- project root resolution;
- isolated Python;
- deterministic Node strategy;
- lock files;
- runner.

## Gate F — Browser

Required:
- Playwright;
- target viewport tests;
- interaction tests;
- console/network checks;
- screenshot evidence.

## Gate G — Security

Required:
- password hashing;
- secret encryption;
- authorization;
- OTP protection;
- upload protection;
- safe logs.

## Gate H — Release

Required:
- clean ZIP;
- no credentials;
- no caches;
- validation report;
- clean-room evidence.
