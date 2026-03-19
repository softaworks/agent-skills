import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "session-handoff" / "scripts" / "validate_handoff.py"

spec = importlib.util.spec_from_file_location("validate_handoff", MODULE_PATH)
validate_handoff = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validate_handoff)


THIRD_LEVEL_HANDOFF = """# Task Handoff

### Current State Summary
This section explains the current state in enough detail for the next agent to
pick up the work without needing to rediscover the plan from scratch.

### Important Context
The validator should accept deeper heading levels because real handoffs often
nest sections under a top-level document title before listing the main content.

### Immediate Next Steps
Patch the regex, run the regression tests, and rebuild the plugin output so the
packaged version matches the source tree exactly.

### Architecture Overview
The script validates sections, scans for secrets, and checks file references.

### Critical Files
The main file is skills/session-handoff/scripts/validate_handoff.py.

### Files Modified
This regression touches the validator and the new tests in the repository.

### Decisions Made
Allow any standard Markdown heading level instead of hard-coding level two only.

### Assumptions Made
Markdown handoff files may use nested section headings under a document title.

### Potential Gotchas
The dist plugin copy must be rebuilt after changing the source implementation.
"""


SECOND_LEVEL_HANDOFF = """# Task Handoff

## Current State Summary
This section confirms the previous level-two format still passes after the
validator is updated to accept deeper headings as well.

## Important Context
Backward compatibility matters because existing handoffs use second-level
headings and should keep receiving high validation scores.

## Immediate Next Steps
Run the same checks against both legacy and nested heading examples to verify
the broader heading regex does not regress older files.
"""


class SessionHandoffValidatorTests(unittest.TestCase):
    def test_accepts_third_level_headings_for_required_and_recommended_sections(self):
        required_complete, missing_required = validate_handoff.check_required_sections(
            THIRD_LEVEL_HANDOFF
        )
        missing_recommended = validate_handoff.check_recommended_sections(THIRD_LEVEL_HANDOFF)

        self.assertTrue(required_complete)
        self.assertEqual(missing_required, [])
        self.assertEqual(missing_recommended, [])

    def test_keeps_support_for_second_level_required_headings(self):
        required_complete, missing_required = validate_handoff.check_required_sections(
            SECOND_LEVEL_HANDOFF
        )

        self.assertTrue(required_complete)
        self.assertEqual(missing_required, [])


if __name__ == "__main__":
    unittest.main()
