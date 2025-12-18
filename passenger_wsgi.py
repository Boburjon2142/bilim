import os
import sys

# Absolute path to project root (update <username> if kerak bo'lsa)
PROJECT_HOME = os.environ.get("PROJECT_HOME") or os.path.dirname(os.path.abspath(__file__))
VENV_ACTIVATE = os.path.join(PROJECT_HOME, "venv", "bin", "activate_this.py")

if PROJECT_HOME not in sys.path:
    sys.path.insert(0, PROJECT_HOME)

if os.path.exists(VENV_ACTIVATE):
    with open(VENV_ACTIVATE) as f:
        exec(f.read(), {"__file__": VENV_ACTIVATE})

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402
