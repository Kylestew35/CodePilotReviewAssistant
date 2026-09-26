# CodePilot Review Assistant — Architecture

## Overview

CodePilot Review Assistant is an AI-powered code review tool built on top of IBM Bob 2.0.
It uses Bob's parallel subagent capability to analyze multiple dimensions of a repository
simultaneously, then merges findings into actionable developer outputs.

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Developer / CI                     │
│          (pastes prompt into Bob 2.0 chat)          │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│          Bob 2.0 Orchestrator  (Agent Mode)         │
│                                                     │
│  • Reads full repository context                    │
│  • Spawns 4 parallel subagents                      │
│  • Tracks progress with update_todo_list            │
│  • Merges outputs in Review Summary Agent           │
└──┬─────────────┬──────────────┬───────────────┬────┘
   │             │              │               │
   ▼             ▼              ▼               ▼
┌──────┐    ┌──────────┐  ┌──────────┐  ┌──────────┐
│Static│    │ Change   │  │  Docs    │  │  Test    │
│Anal. │    │ Impact   │  │  Agent   │  │ Coverage │
│Agent │    │  Agent   │  │          │  │  Agent   │
└──┬───┘    └────┬─────┘  └────┬─────┘  └────┬─────┘
   │             │              │               │
   └─────────────┴──────────────┴───────────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │  Review Summary     │
            │  Agent              │
            └──────────┬──────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
  review_report.md  findings.json  improvement_plan.md
```

## Agent Responsibilities

### Orchestrator (Bob 2.0 Agent Mode)
- Reads all repository files before spawning agents
- Passes file content to each subagent via description
- Waits for all 4 agents to complete in parallel
- Invokes Review Summary Agent with combined outputs

### Static Analysis Agent
**Input:** All source files (`*.py`, `*.js`, `*.ts`, etc.)
**Output:** JSON array of findings
**Finds:**
- SQL injection, XSS, insecure crypto, hardcoded secrets
- Logic bugs (None returns, unchecked values, off-by-one)
- Code smells (magic numbers, dead code, wrong logging)
- Anti-patterns (God classes, deep nesting, no error handling)

### Change Impact Agent
**Input:** All source files + all test files
**Output:** JSON object with dependency_map, risk_assessment, missing_tests, breakage_predictions
**Finds:**
- Module-level dependency graph
- Highest-risk components for changes
- Missing tests per function
- Breakage scenarios with likelihood and mitigation

### Documentation Agent
**Input:** README, all source files, all config files
**Output:** JSON object with doc_gaps, missing_docstrings, readme_issues, config_doc_mismatches
**Finds:**
- README ↔ code mismatches
- Undocumented config fields
- Missing or incorrect docstrings
- Phantom API endpoints (documented but not implemented)

### Test Coverage Agent
**Input:** All source files + all test files
**Output:** JSON object with coverage_map, coverage_score, new_test_suggestions
**Finds:**
- Function-to-test mapping
- Untested code branches
- Estimated line coverage percentage
- Full pytest templates for each gap

### Review Summary Agent
**Input:** Outputs of all 4 agents
**Output:** Three files: `review_report.md`, `review_findings.json`, `improvement_plan.md`
**Does:**
- Deduplicates and cross-references findings
- Assigns overall risk rating
- Produces prioritized fix list (P0 → P3)
- Writes all three output artifacts

## Output Schema

### review_findings.json
```json
{
  "metadata": { "tool", "version", "agents_used", "overall_risk", "summary" },
  "static_analysis": [ { "id", "file", "line", "category", "severity", "title", "description", "suggested_fix" } ],
  "change_impact": {
    "dependency_map": [ { "from", "to", "type" } ],
    "risk_assessment": [ { "component", "risk_level", "reason" } ],
    "missing_tests": [ { "id", "function", "file", "suggested_test_name", "suggested_test_description" } ],
    "breakage_predictions": [ { "scenario", "affected_components", "likelihood", "mitigation" } ]
  },
  "documentation": {
    "doc_gaps": [...],
    "readme_issues": [...],
    "config_doc_mismatches": [...]
  },
  "test_coverage": {
    "coverage_score": { "total_functions", "functions_with_any_test", "estimated_line_coverage_pct" },
    "coverage_map": [...],
    "new_test_suggestions": [ { "id", "test_name", "test_description", "test_template" } ]
  }
}
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| AI Orchestration | IBM Bob 2.0 (Agent Mode) |
| Parallel Execution | Bob 2.0 `spawn_subagent` |
| Repo Comprehension | Bob 2.0 full context window |
| Document Understanding | Bob 2.0 `read_file`, `grep`, `FindSymbol` |
| Output Rendering | Markdown + JSON + HTML artifact |
| Demo Target Language | Python 3.10+ |

## Extending CodePilot

### Add a New Agent

1. Add a new parallel `spawn_subagent` call in the orchestrator prompt
2. Define its input (which files to read) and output schema
3. Pass its output to the Review Summary Agent
4. Update `review_findings.json` schema to include the new agent's section

### Support a New Language

The current prompts are language-agnostic — Bob reads and understands any language.
For language-specific rules, add a language context block to the Static Analysis Agent prompt:

```
For JavaScript/TypeScript files also check:
- Prototype pollution
- eval() usage
- Missing await on async calls
- setTimeout with string argument
```

### CI/CD Integration

Run the Quick Risk Scan prompt automatically on every PR using Bob hooks:

```yaml
# .bob/hooks/pre-merge.yaml
on: pull_request
prompt: prompts/prompt_pack.md#quick-risk-scan
fail_on: CRITICAL
```
