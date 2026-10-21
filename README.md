# field-reports-lab

The practice repository for **Spec-Driven Software Development with Claude Code** from We Can Code IT.

It holds a small, working Python program with real problems in it. Over seven modules you write a
spec for each problem, prove the problem with a failing test, have Claude Code fix it in a small pull
request, and review the fix with a second AI model.

## The program

`fieldreports` reads a fictional construction-management service called Crewbook and counts, per
project and per week, the evidence that crews did their required paperwork: daily reports and
safety checklists (forms), and two-week look-aheads and toolbox talks (files in folders). It writes
the counts to a CSV for a dashboard. Every name, project and address in it is made up.

The tests never touch a network. `tests/mock_api.py` answers every Crewbook call inside Python, from
the JSON files in `fixtures/`.

## Get started

1. Click **Use this template**, then **Create a new repository**, at the top of this page. Do not
   fork it: a fork shares this repository's settings, and a template gives you your own clean copy.
2. Make your copy **public** if you are on GitHub's free plan. Branch protection and required checks
   on private repositories need a paid plan.
3. Open the **Actions** tab of your new repository and confirm the `lab` workflow is enabled. If
   GitHub shows a button to enable workflows, click it.
4. Clone your copy, then from its folder:

```
python -m venv .venv
.venv/bin/pip install -e ".[dev]"          # Windows: .venv\Scripts\pip install -e ".[dev]"
python labcheck.py m0                      # checks Python 3.11+, Git, GitHub CLI and Claude Code
python labcheck.py m1                      # fails until you finish module 1
```

**Never put employer code, data or keys in this repository.** It is public, and it is for practice.

## Checking your work

| Command | What it does |
|---|---|
| `python labcheck.py m0` | checks your setup |
| `python labcheck.py m3` | runs the checks for modules 1 to 3, and nothing later |
| `python labcheck.py current` | runs the checks up to the module set in `lab.toml` (CI runs this) |
| `python labcheck.py restore m4` | stuck? resets the code and tests to the start of module 4 |

`docs/acceptance-criteria.md` says, in plain words, what each module's checks expect.

The API key in `fieldreports/config.py` is fake. It is there on purpose, for module 2.
