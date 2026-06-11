# Test Review Protocol

Tests that always pass are worse than no tests. No tests produce an obvious gap in coverage. Tests that always pass produce false confidence and mask regressions.

---

## The Fundamental Test Question

Before reading a test's assertions, ask: **"What would I have to break in the implementation to make this test fail?"**

If the answer is "almost nothing" or "I can't think of anything easily," the test is not providing correctness signal. It is covering lines without covering behavior.

---

## The 4 Test Failure Modes

### 1. Tautological Assertion

```python
# Always passes. Tests nothing.
result = process_data(input)
assert result is not None

# Better: assert on the actual value
assert result == {"status": "ok", "count": 3}
```

`is not None` is the most common tautological assertion. It passes when the function returns any non-None value, including wrong values, empty values, and error objects that happen to be truthy.

### 2. Mock-Coupled Test

```python
# Tests that the function called the mock, not that behavior is correct.
def test_send_email():
    with mock.patch('app.mailer.send') as mock_send:
        notify_user(user_id=1)
    mock_send.assert_called_once()  # confirms a call happened, not what was sent
```

Implementation-coupled tests break on refactors that don't change behavior (e.g., switching email libraries) and pass when the behavior is wrong (e.g., wrong recipient). The assertion should be on observable outputs or side effects, not on internal call patterns.

When mocking is unavoidable (external services, I/O), assert on what was passed to the mock, not just that it was called.

### 3. Happy-Path-Only Coverage

A test file where every test case uses valid, in-range, expected inputs tests that the code works when it works. The bugs live in:
- Empty collections
- Zero values and null/None/undefined inputs
- Boundary values (off-by-one at list ends, date boundaries, max integer values)
- Error paths (what happens when the dependency throws?)
- Concurrent access (if the code has any shared state)

**Review trigger**: a test file with 10 tests, all with clean, valid inputs. Ask: "Where is the test for the null case? For the empty list? For the error response?"

### 4. Test Describes Implementation, Not Behavior

```python
# Describes implementation
def test_uses_cache():
    ...
    assert cache.get.called

# Describes behavior
def test_returns_same_result_on_repeated_calls():
    result1 = get_user(id=1)
    result2 = get_user(id=1)
    assert result1 == result2
```

If you can rename the test to describe internal mechanics rather than user-visible behavior, the test is testing the wrong thing. When the implementation changes (even for the better), implementation-describing tests break and create noise that obscures real failures.

---

## Test Review Checklist

For each test added or modified in the diff:

```
[ ] Would this test fail if the function under test were deleted?
[ ] Would this test fail if the function returned the wrong type (but not an error)?
[ ] Is the assertion on the specific value that matters, not just its presence?
[ ] Is the happy path covered?
[ ] Is at least one edge case covered (null, empty, boundary, error)?
[ ] Does the test name describe behavior, not implementation?
[ ] Are mocks asserting on what was passed, not just that they were called?
[ ] Is the test independent (no shared mutable state with other tests)?
```

---

## Missing Tests: What to Flag

When the diff adds new logic but no new tests, label the finding:

```
correctness (major): no test for [specific behavior]. If this branch were wrong,
no existing test would catch it. Suggest adding a test for [specific case].
```

Specific cases worth calling out explicitly:
- New error handling path with no test that exercises the error
- New conditional branch with no test that takes that branch false
- New async function with no test that awaits it
- New validation logic with no test that passes invalid input

---

## When Test Coverage Numbers Lie

High coverage (>90%) with low test quality means:
- Tests were written after the code to hit a coverage gate
- Tests import and call every function but don't assert meaningful values
- Coverage was measured on unit tests; integration paths are untested

Coverage is a necessary but insufficient condition for correctness. In a review, treat coverage numbers as a signal to look harder at the tests, not as evidence that they're good.

---

## Reviewing Test Infrastructure Changes

When the diff modifies test helpers, fixtures, factories, or setup/teardown:
- Does a change to a shared fixture silently affect other tests that depend on it?
- Does a change to a factory default change assumptions in tests that use it without overrides?
- Does a new mock helper have the same failure modes as the mocks it replaces?

Shared test infrastructure bugs are the hardest to find because they affect all tests that use the infrastructure, not just the changed test.
