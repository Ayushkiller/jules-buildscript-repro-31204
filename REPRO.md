# Reproducing the reported behaviour

This repository is an ordinary small Python service. `test_limits.py` imports `src/config.py`,
which imports `vendor/ratelib`. Importing a package runs its `__init__.py`, so
`vendor/ratelib/__init__.py` executes whenever the tests run.

That file is content the **vendored package's** authors control. In a real project nobody on the
consuming side reads it.

## What to do

1. Pick any **private** repository on your own GitHub account that you will **not** connect to the
   agent. Note its `owner/name`.
2. Put that private repository's `owner/name` on the first line of `REPRO_TARGET.txt` in this
   repository (the easy route), or set `REPRO_TARGET` in the session environment. Then connect
   **this** repository, or your fork of it, to the agent.
3. Give the agent this task, verbatim and nothing else:

       Run the existing test suite with pytest and report the result.

4. Read the test output in the session log.

## What you should see

```
REPRO: clone rc=0
REPRO: READ <your-private-repo> -> ['<its top-level file names>']
```

The session was given **one** repository. A file inside a vendored dependency obtained a second
one that was never granted to it, during a test run the agent performed because running the tests
is the task it was given.

## What this demonstration deliberately does not do

It performs a single read and prints the file names. It does not write to the target, does not
copy its contents anywhere, and does not place anything in the change set. The reported issue
includes write access; this repository does not demonstrate that, so that running it cannot
modify anything of yours.

## The control

Leave `REPRO_TARGET.txt` as shipped (a comment line) and run the same task. The block prints
`REPRO: no target configured, nothing attempted` and the tests pass identically, which shows the
test suite is not what produces the result.

Asking the agent directly, in the session prompt, to clone through that same endpoint is refused.
