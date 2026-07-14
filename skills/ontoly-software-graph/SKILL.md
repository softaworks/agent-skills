---
name: ontoly-software-graph
description: Use Ontoly's deterministic Software Graph and MCP capabilities for architecture review, request tracing, dependency analysis, and impact analysis.
---

# Ontoly Software Graph

Use Ontoly when an agent needs graph-backed software understanding before searching repository files directly.

## When to Use

- Explain repository architecture, modules, packages, services, routes, controllers, or ownership.
- Trace a request, route, controller, service, provider, dependency, or call chain.
- Estimate impact for removing, renaming, or refactoring a symbol, module, package, route, or service.
- Review unresolved imports, circular dependencies, dead code, configuration usage, environment variables, or graph diagnostics.

## Workflow

1. Check for Ontoly artifacts such as `.ontoly/`, `SoftwareGraph.json`, diagnostics, validation output, or MCP configuration.
2. If the graph is missing and local graph output is acceptable, run `ontoly build .`.
3. Review diagnostics, trust, semantic coverage, framework detection, graph hash, and validation status before making claims.
4. Prefer Ontoly CLI or MCP capabilities for architecture summaries, request tracing, dependency analysis, configuration lookup, framework reports, and impact analysis.
5. Inspect source files only when Ontoly cannot answer, the graph is incomplete, or the user asks for source-level verification.

## Output

- Cite graph nodes, edges, packages, routes, diagnostics, or query outputs when available.
- Separate measured graph facts from inference.
- Include confidence based on graph evidence and diagnostics.
- Explain any fallback source inspection and why it was needed.

## Guardrails

- Do not invent relationships that are not present in the graph.
- Treat unresolved imports, low trust, missing framework detection, and validation failures as limitations.
- Rebuild the graph after meaningful repository changes before answering current-state questions.
