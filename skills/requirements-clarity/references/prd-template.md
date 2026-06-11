# PRD Template

Once clarity score ≥ 90, generate the file at `./docs/prds/{feature-name}-v{version}-prd.md`.

```markdown
# {Feature Name} — Product Requirements Document

## Background
- **Business Problem**: [what pain/need this addresses]
- **Target Users**: [who, not "users"]
- **Value Proposition**: [why now, why this approach]

## Feature Scope
- **Included**: [explicit list]
- **Excluded**: [what's out — prevents scope creep]
- **User Scenarios**: [2-3 concrete flows]

## Detailed Requirements
- **Inputs / Outputs**: [specific, typed]
- **User Interaction**: [step-by-step flow]
- **Data Requirements**: [schema, validation rules]
- **Edge Cases**: [enumerated, not "handle errors"]

## Technical Approach
- **Architecture**: [decision + rationale]
- **Key Components**: [list]
- **Data Storage**: [model + storage choice]
- **Interfaces**: [API contract or UI spec]

## Constraints
- **Performance**: [e.g., p99 < 200ms, 1k rps]
- **Compatibility**: [browsers, OS, API versions]
- **Security**: [auth, data sensitivity, compliance]
- **Scalability**: [growth assumptions]

## Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [technical risk] | H/M/L | H/M/L | [action] |
| [dependency risk] | H/M/L | H/M/L | [action] |

## Acceptance Criteria

### Functional
- [ ] [specific, testable condition]
- [ ] [specific, testable condition]

### Quality
- [ ] Test coverage ≥ X%
- [ ] Performance: [specific metric passes]
- [ ] Security: [specific check passes]

### User Acceptance
- [ ] [UX condition]
- [ ] Documentation delivered

## Execution Phases

### Phase 1: Preparation
- [ ] [task]
- **Deliverable**: [artifact]
- **Estimate**: [time]

### Phase 2: Core Development
- [ ] [task]
- **Deliverable**: [artifact]
- **Estimate**: [time]

### Phase 3: Integration & Testing
- [ ] [task]
- **Deliverable**: [artifact]
- **Estimate**: [time]

### Phase 4: Deployment
- [ ] [task]
- **Deliverable**: [artifact]
- **Estimate**: [time]

---
**Version**: {version}  **Created**: {date}  **Rounds**: {n}  **Score**: {score}/100
```
