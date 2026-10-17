# jules-buildscript-repro

A minimal, ordinary Python service, used to demonstrate one reported behaviour of a coding
agent's build environment. See `REPRO.md` for what to run and what to expect.

The only unusual file is `vendor/ratelib/__init__.py`. It performs one read and prints what it
saw. It writes nothing, anywhere.
