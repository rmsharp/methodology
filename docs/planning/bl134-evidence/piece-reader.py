#!/usr/bin/env python3
"""Read stdin to EOF in the largest reads the kernel gives, and print the size of each read, comma-separated.
A reader that is already waiting sees a writer's separate write() calls as separate reads (the first bytes wake it);
one write() arrives as one read. Used by bl134-measure.sh `pieces`: how a stream reaches the final `grep -q`."""
import os
sizes = []
while True:
    b = os.read(0, 1 << 20)
    if not b:
        break
    sizes.append(len(b))
print(",".join(map(str, sizes)))
