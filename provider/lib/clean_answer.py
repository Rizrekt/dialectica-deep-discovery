#!/usr/bin/env python3
"""stdin -> citation-cleaned answer on stdout (pipeline stage)."""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from citation_patch import clean

text = sys.stdin.read()
out, hits = clean(text)
if hits:
    print(f"clean_answer: stripped {len(hits)} fake citation(s)", file=sys.stderr)
sys.stdout.write(out)
