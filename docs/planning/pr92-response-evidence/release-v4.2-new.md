Implements D8 of the parallel-sessions plan (#83). Tagged at `f34769f`; the gate run at the tag is 12/12.

**What changed**

- **`--source=github` uses the source's own manifest.** `bin/sync` and `bin/status` now install and compare against the manifest of the repository they clone, not this checkout's. Previously a source newer than your checkout was installed with the wrong file list.
- **The manifest is read as data, never run.** Because the source's manifest now decides what is written and where, new `bin/_manifest_reader.py` parses it with `ast` and reads its constants as literals. `bin/_manifest.py` is now documented as literal data, one plain assignment per name.
- **Unsafe rows are refused before anything is written.** A row whose disposition is not `tracked` or `seed` stops the run and names the rows. Without this, a source that labelled seeds differently would have its seeds written over an adopter's own copies. `bin/status` refuses the same way.
- **Path checks.** A `src` or `dest` that is absolute, has a drive letter, climbs out with `..`, is or lies inside `.git`, names no file (`.`), or contains a NUL byte is refused, as is a manifest that changes a name it binds.
- **Dashboard 2.11.3.** Dotfile names listed in `CONFIG_EXTS` are now categorized as config.

**Updating.** Update your methodology checkout, then re-run `bin/sync`; sync itself delivers only the 2.11.3 dashboard. With the updated checkout, a sync from a source whose manifest cannot be read stops with one line and a hint (`--source=local` syncs from a full checkout) and writes nothing.

**Not in this release:** no change to any phase, failure mode, quality gate, or workstream.

**Numbers:** `bin/tests.sh` goes from 243 to 261 tests; gates declared in `.quality-gates.json` stay at 12.

