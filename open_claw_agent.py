#!/usr/bin/env python3
"""
DEPRECATED ENTRYPOINT

This file was retained for compatibility but the project has consolidated its
primary CLI under `hazim_reseller_agent.py`. To remove this file from your
local clone, run:

  git rm open_claw_agent.py
  git commit -m "Refactor: eliminate core agent placeholders and consolidate unified local architecture"

The runtime behavior below ensures any accidental invocation clearly reports
the canonical entrypoint and exits with a non-zero status.
"""
import sys

if __name__ == "__main__":
    sys.stderr.write(
        "open_claw_agent.py is deprecated and removed from active development.\n"
        "Please use the primary CLI: hazim_reseller_agent.py\n"
    )
    sys.exit(2)
