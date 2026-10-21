"""Lab checks for Spec-Driven Software Development with Claude Code.

    python labcheck.py m0           check your setup: Python 3.11+, Git, GitHub CLI login, Claude Code
    python labcheck.py m3           run the checks for modules 1 to 3 (later modules are left alone)
    python labcheck.py current      run the checks up to the module in lab.toml
    python labcheck.py restore m4   stuck? reset the code and tests to the start of module 4

Exit code 0 means every check passed; 1 means at least one failed.
"""

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LAST_MODULE = 7
MIN_PYTHON = (3, 11)
UPSTREAM = "https://github.com/WeCanCodeIT/field-reports-lab.git"
RESTORED_PATHS = ["fieldreports", "tests", "fixtures"]


def _ok(label, passed, hint=""):
    print(f"[{'ok' if passed else 'MISSING'}] {label}" + ("" if passed else f": {hint}"))
    return passed


def _runs(command):
    if shutil.which(command[0]) is None:
        return False
    return subprocess.run(command, capture_output=True).returncode == 0


def setup_check():
    results = [
        _ok("Python 3.11 or later", sys.version_info >= MIN_PYTHON, f"you have {sys.version.split()[0]}"),
        _ok("Git", _runs(["git", "--version"]), "install Git from git-scm.com"),
        _ok("GitHub CLI, signed in", _runs(["gh", "auth", "status"]), "install from cli.github.com, then run: gh auth login"),
        _ok("Claude Code", _runs(["claude", "--version"]), "install Claude Code, then run: claude"),
    ]
    return 0 if all(results) else 1


def module_check(module):
    files = [str(ROOT / "tests" / "test_contract.py")]
    for number in range(1, module + 1):
        files += sorted(str(path) for path in (ROOT / "tests").glob(f"test_m{number}_*.py"))
    result = subprocess.run([sys.executable, "-m", "pytest", *files], cwd=ROOT)
    print(f"labcheck m{module}: " + ("PASS" if result.returncode == 0 else "not yet"))
    return 0 if result.returncode == 0 else 1


def current_module():
    return tomllib.loads((ROOT / "lab.toml").read_text(encoding="utf-8"))["module"]


def restore(module):
    tag = f"m{module}-start"
    fetch = ["git", "fetch", "--no-tags", UPSTREAM, f"refs/tags/{tag}:refs/tags/{tag}"]
    if subprocess.run(fetch, cwd=ROOT).returncode != 0:
        return 1
    subprocess.run(["git", "checkout", tag, "--", *RESTORED_PATHS], cwd=ROOT, check=True)
    print(f"Restored {', '.join(RESTORED_PATHS)} to the start of module {module}. Review with: git status")
    return 0


def parse_module(text):
    if not (text.startswith("m") and text[1:].isdigit() and 0 <= int(text[1:]) <= LAST_MODULE):
        sys.exit(f"expected m0 to m{LAST_MODULE}, got {text!r}")
    return int(text[1:])


def main(args):
    if not args:
        print(__doc__)
        return 1
    if args[0] == "current":
        return module_check(current_module())
    if args[0] == "restore" and len(args) == 2:
        return restore(parse_module(args[1]))
    module = parse_module(args[0])
    return setup_check() if module == 0 else module_check(module)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
