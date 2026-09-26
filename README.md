# 🚀 CodePilot Review Assistant

> **IBM Bob 2.0 Hackathon Submission**
> Automate and accelerate the code review process using Bob 2.0's parallel subagents, repository context, and document understanding.

---

## 📺 Demo Video

> 🎬 **[Watch the Demo on YouTube →](#)**
> *(Replace `#` with your video link before submission)*

---

## 🎯 What It Does

CodePilot Review Assistant is a working prototype that drops into any repository and produces a complete, actionable code review in seconds — not hours.

It spins up **5 parallel Bob 2.0 subagents** that each analyze a different dimension of the codebase simultaneously:

| Agent | Job |
|-------|-----|
| 🔍 Static Analysis Agent | Code smells, anti-patterns, security vulnerabilities, complexity |
| 🔄 Change Impact Agent | Dependency graph, breakage risk, missing tests |
| 📄 Documentation Agent | README vs code mismatches, missing docstrings, config gaps |
| 🧪 Test Coverage Agent | Function-to-test map, coverage score, test templates |
| 📋 Review Summary Agent | Merges all findings into a single prioritized report |

---

## 📊 Sample Output (Demo Repository)

The included demo repo (`src/sample_repo/`) is a realistic Python e-commerce Order Processing Service. Running CodePilot on it found:

| Dimension | Score | Status |
|-----------|-------|--------|
| Security | 1/10 | 🔴 Critical |
| Code Quality | 4/10 | 🟠 High Risk |
| Test Coverage | 9% | 🔴 Critical |
| Documentation | 3/10 | 🟠 High Risk |
| Change Safety | 2/10 | 🔴 Critical |

**24 static findings** including 2 SQL injection vulnerabilities, plaintext password storage, and a logic bug that makes `generate_report()` always return empty results.

---

## 📂 Repository Structure

```
CodePilot Review Assistant/
│
├── README.md                    ← You are here
├── review_report.md             ← 📋 Full human-readable review (OUTPUT)
├── review_findings.json         ← 🔧 Structured machine-readable findings (OUTPUT)
├── improvement_plan.md          ← 🗺️ Step-by-step remediation plan (OUTPUT)
│
├── prompts/
│   └── prompt_pack.md           ← 📦 Prompt pack — reusable Bob 2.0 prompts
│
├── docs/
│   └── ARCHITECTURE.md          ← System architecture overview
│
└── src/
    └── sample_repo/             ← 🎯 Demo target repository
        ├── app.py               ← Main application (intentionally flawed)
        ├── utils.py             ← Utility functions
        ├── config.json          ← Configuration file
        ├── requirements.txt     ← Python dependencies
        ├── README.md            ← Demo repo README
        └── tests/
            └── test_orders.py   ← Existing test suite (9% coverage)
```

---

## ⚡ Quick Start

### Prerequisites

- [IBM Bob 2.0](https://www.ibm.com/products/watsonx-code-assistant) (Agent Mode)
- Python 3.10+ (for running the demo repo locally)

### Run Against the Demo Repo

1. **Clone this repository:**
   ```bash
   git clone https://github.com/Kylestew35/CodePilotReviewAssistant.git
   cd CodePilotReviewAssistant
   ```

2. **Open in Bob 2.0** and switch to **Agent Mode**.

3. **Paste the main prompt** from `prompts/prompt_pack.md` → *"Master Analysis Prompt"* into the Bob chat.

4. Bob will spin up 4 parallel subagents and return:
   - `review_report.md` — human-readable review
   - `review_findings.json` — structured findings
   - `improvement_plan.md` — step-by-step fix plan

### Run Against Your Own Repository

1. Replace the contents of `src/sample_repo/` with your own code.
2. Use the **"Custom Repo Prompt"** from `prompts/prompt_pack.md`.
3. Bob reads your repo, runs all agents in parallel, and produces the same three output files tailored to your code.

---

## 📸 Screenshots

### Dashboard Overview
![Dashboard](docs/screenshots/dashboard.png)

### Agent Pipeline (Bob 2.0 Chat)
![Agent Pipeline](docs/screenshots/agent_pipeline.png)

### review_report.md Output
![Report](docs/screenshots/review_report.png)

> 📝 *Screenshots are in `docs/screenshots/`. Add your own after running the demo.*

---

## 📦 Prompt Pack

All reusable prompts are in [`prompts/prompt_pack.md`](prompts/prompt_pack.md). Includes:

- **Master Analysis Prompt** — full parallel-agent review
- **Static Analysis Only** — deep security/smell scan
- **Test Coverage Audit** — coverage map + test generation
- **Docs vs Code Audit** — README and docstring alignment
- **Quick Risk Scan** — 2-minute breakage risk summary

---

## 🧠 How It Uses Bob 2.0 Features

| Bob 2.0 Feature | How CodePilot Uses It |
|----------------|----------------------|
| **Agent Mode** | Orchestrates the full 5-agent pipeline |
| **Parallel Subagents** | All 4 analysis agents run simultaneously |
| **Full Repo Context** | Reads every file before analysis starts |
| **Document Understanding** | Parses README, config.json, and docstrings |
| **Structured Output** | Produces JSON + Markdown artifacts |
| **Task Tracking** | Uses `update_todo_list` to track agent progress |

---

## 📈 Measurable Improvements

Running CodePilot on the demo repo produced these measurable outcomes:

| Metric | Before | After Plan |
|--------|--------|-----------|
| Security vulnerabilities | 5 critical | 0 |
| Test coverage | 9% | 80%+ |
| Undocumented config fields | 4/5 | 0/5 |
| SQL injection vectors | 2 | 0 |
| Functions with no test | 18/21 (86%) | < 4/21 (19%) |
| Estimated review time (manual) | 4–8 hours | < 5 minutes |

---

## 🗺️ Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full system design.

```
User Prompt
    │
    ▼
Bob 2.0 Orchestrator (Agent Mode)
    │
    ├──▶ StaticAnalysisAgent ──────────────┐
    ├──▶ ChangeImpactAgent ────────────────┤
    ├──▶ DocumentationAgent ───────────────┼──▶ ReviewSummaryAgent
    └──▶ TestCoverageAgent ────────────────┘         │
                                                      ▼
                                           review_report.md
                                           review_findings.json
                                           improvement_plan.md
```

---

## 📄 Output Files

### `review_report.md`
Full code review document including:
- Executive summary with risk scores
- Prioritized issue list (Critical → Low)
- Security analysis with fix code
- Impact analysis and dependency map
- Test coverage map
- Documentation gap analysis
- Remediation priority list

### `review_findings.json`
Machine-readable structured output:
- All 24 issues with locations, severity, reasoning
- 25 new test suggestions with full pytest templates
- Dependency graph edges
- Breakage predictions with mitigation strategies
- Documentation mismatch catalog

### `improvement_plan.md`
Step-by-step 5-phase improvement plan:
- Phase 1: Critical security fixes (P0)
- Phase 2: Logic bug fixes (P1)
- Phase 3: Test suite (80% target)
- Phase 4: Code quality refactors
- Phase 5: Documentation and CI/CD

---

## 🤝 Contributing

This is a hackathon prototype. To extend it:

1. Add new agent prompts to `prompts/prompt_pack.md`
2. Add support for other languages (JS, Java, Go) by adjusting the static analysis prompt
3. Add a GitHub Actions workflow that runs CodePilot on every PR

---

## 📜 License

MIT — see [LICENSE](LICENSE)

---

## 🏆 Hackathon Compliance Checklist

- [x] Uses Bob 2.0 Agent Mode
- [x] Uses parallel subagents (4 simultaneous)
- [x] Uses full repository context
- [x] Uses document understanding (README, config, docstrings)
- [x] Produces measurable improvements (tracked metrics)
- [x] Generates submission-ready artifacts (3 output files + HTML dashboard)
- [x] Runnable as prototype inside any repository
- [x] Improves real developer workflow (code review)

---

*Built with ❤️ using IBM Bob 2.0 · CodePilot Review Assistant*
