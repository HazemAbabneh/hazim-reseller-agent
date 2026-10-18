#!/usr/bin/env python3
"""
Compatibility shim renamed to hazim_agent.py. This file is intentionally minimal
and informs users about the canonical entrypoint.
"""
import sys

if __name__ == "__main__":
    sys.stderr.write(
        "This file has been superseded. Use the canonical CLI: hazim_reseller_agent.py\n"
    )
    sys.exit(2)
