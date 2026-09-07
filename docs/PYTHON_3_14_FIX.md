# Python 3.14 Windows Runtime Fix

PA NEXUS V3.0.1 explicitly supports CPython 3.14. The previous runner rejected Python 3.14 before creating the virtual environment.

Changes:
- Windows PowerShell runner accepts Python 3.11–3.14.
- POSIX runner accepts Python 3.11–3.14.
- Pydantic upgraded to 2.12.4, which includes Python 3.14 support.
- FastAPI upgraded to 0.119.1 for the Python 3.14/Pydantic compatibility fixes.
- Cryptography upgraded to 46.0.7 with Python 3.14 wheels.
- Runner upgrades pip before installing backend dependencies.

The application still creates `.venv` inside the canonical project root and does not depend on the caller's current working directory.
