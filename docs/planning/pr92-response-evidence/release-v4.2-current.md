Implements D8 of the parallel-sessions plan (#83). Tagged at `f34769f`; the gate run at the tag is 12/12.

**What changed**

- **`--source=github` uses the source's own manifest.** `bin/sync` and `bin/status` now install and compare against the manifest of the repository they clone, not this checkout's. Previously a source newer than your checkout was installed with the wrong file list.
- **The manifest is read as data, never run.** New `bin/_manifest_reader.py` parses the clone's `bin/_manifest.py` with `ast` and reads its constants as literals. Code in a cloned manifest no longer runs during a sync. `bin/_manifest.py` is now documented as literal data, one plain assignment per name.
- **Unsafe rows are refused before anything is written.** A row whose disposition is not `tracked` or `seed` stops the run and names the rows. This closes a defect where a source that labelled seeds differently could overwrite an adopter's own `CHANGELOG.md` with exit 0 and no `--force`. `bin/status` had the mirror-image bug (an unknown label was read as a seed, so its drift went unreported); it now refuses the same way.
- **Path checks.** A `src` or `dest` that is absolute, has a drive letter, climbs out with `..`, is `.git`, `.`, or contains a NUL byte is refused, as is a manifest that changes a name it binds.
- **Dashboard 2.11.3.** Dotfile names listed in `CONFIG_EXTS` are now categorized as config.

**Updating.** Re-run `bin/sync`. A sync from a source whose manifest cannot be read now stops with one line and a hint (`--source=local` syncs from a full checkout) and writes nothing.

**Not in this release:** no change to any phase, failure mode, quality gate, or workstream.

**Numbers:** `bin/tests.sh` goes from 243 to 261 tests; gates declared in `.quality-gates.json` stay at 12.

