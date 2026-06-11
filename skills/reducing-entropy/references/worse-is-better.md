---
description: A simpler, less-correct design that ships beats a complete, elegant design that doesn't. Interface simplicity over implementation simplicity — systems that do slightly less but are easier to build will out-survive those that try to do everything right.
---

# Worse Is Better

## The Core Insight

> "The right thing is rarely the right thing to build."

Richard Gabriel's 1991 essay describes two design philosophies: the MIT/Stanford "Right Thing" approach (correctness and completeness above all) vs the New Jersey "Worse is Better" approach (simplicity first, even at cost of correctness). Worse-is-Better systems win in practice.

## Why This Matters

A system with 50% of the right features but half the code:
- Ships sooner
- Has fewer bugs
- Is easier to port and maintain
- Accumulates improvements over time

The "Right Thing" system is often never finished. Even if finished, it's too complex to maintain. Perfection is the enemy of shipped.

## Interface vs Implementation Simplicity

The key inversion: **interface simplicity takes priority over implementation simplicity**.

- It's acceptable to have a complicated implementation to keep the interface simple
- It is NOT acceptable to complicate the interface to simplify the implementation
- Users interact with interfaces; developers maintain implementations

## Practical Application

When tempted to add completeness:
- Would removing this feature make the interface simpler?
- Is this feature needed for first ship, or is it "right thing" thinking?
- Could we solve this with a simpler, slightly wrong approach that we can fix later?

When evaluating design options:
- Which option produces a simpler interface, even if the implementation is messier?
- Which option can we ship and iterate on?
- Which option survives contact with reality?

**Bias toward the thing that works now. Completeness is a direction, not a gate.**

## External References

- [Worse Is Better](https://www.dreamsongs.com/WorseIsBetter.html) - Richard Gabriel's original essay
- [Is Worse Really Better?](https://www.dreamsongs.com/Files/IsWorseReallyBetter.pdf) - Gabriel's follow-up
- [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) - Rich Hickey on related themes
