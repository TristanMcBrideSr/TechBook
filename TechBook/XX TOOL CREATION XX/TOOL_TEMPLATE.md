
---

# **Tools Creation Guide**

## **Overview**

This framework enables you to write **tools**—modular logic units for automation, integration, or utility, with:

* **No decorators required**
* **No fragile schemas**
* **No accidental exposure:**
  Only what you make public is callable—**period**.

---

## **Tool Visibility & Exposure**

* **Anything public is exposed. Anything private (starting with `_`) is hidden.**
* Applies to:

  * Methods on a class
  * Standalone functions in a module
* No need for decorators, schemas, or wrappers.

---

## **No Action Maps or Dispatchers**

* Tools **cannot** use `actionMap`, `ACTION_MAP`, or dispatcher patterns.
* Every **public function or method** is exposed directly as a tool.
* Private logic methods (like `_helper`) are never exposed.

---

## **Direct Functions & Methods**

* Any **standalone public function** (not starting with `_`) is directly callable as a **Tool**.
* Any **public method** in a class (not starting with `_`) is directly callable as a **Tool**.
* **Private helpers** (with `_`) are never exposed.

---

## **How It’s Parsed**

* **Every public method/function** is parsed as a **Tool**.
* **No action maps, no dispatchers:**
  Only real, public methods and functions are exposed as tools.
* **No decorators, no fragile JSON, no vendor lock.**
  Just real Python, as flexible as you want.

---

# **How To Create Tools**

## **1. Singleton Class With Public Methods**

All public methods are exposed as tools (no action map, no dispatcher needed).

```python
import threading
import os
import subprocess
import logging
from HoloAI import HoloLink

logger = logging.getLogger(__name__)

NAME_REPLACEMENTS = {
    "vs code":     "code",
    "vs studio":   "devenv",
    "vs insiders": "code - insiders",
    "word":        "winword",
    "powerpoint":  "powerpnt",
    "explorer":    "iexplore",
}

class Apps:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Apps, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        self._initComponents()
        self.initialized = True

    def _initComponents(self):
        self.holoLink = HoloLink()
        self.nameReplacements = NAME_REPLACEMENTS.copy()

    def _metaData(self):
        return {
            "className": f"{self.__class__.__name__}", 
            "description": "Open and close applications on my computer"
        }

    def _normalizeAppName(self, appName: str) -> str:
        app = appName.lower()
        return next(
            (replacement for key, replacement in self.nameReplacements.items() if key in app),
            appName
        )

    def openApp(self, appName: str) -> str:
        """
        Description: Open an application by its name, normalizing common names to their executable names.
        """
        app = self._normalizeAppName(appName)
        try:
            os.startfile(app)
            return f"Opened {app}"
        except Exception as e:
            logger.error(f"Error opening {app}:", exc_info=True)
            return f"An error occurred while trying to open {app}: {e}"

    def closeApp(self, appName: str) -> str:
        """
        Description: Close an application by its name, normalizing common names to their executable names.
        """
        app = self._normalizeAppName(appName)
        if not app.lower().endswith('.exe'):
            app += '.exe'
        try:
            subprocess.run(
                ["taskkill", "/f", "/im", app],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return f"Closed {app}"
        except Exception as e:
            logger.error(f"Error closing {app}:", exc_info=True)
            return f"An error occurred while trying to close {app}: {e}"

    def _privateHelper(self, ...):
        pass  # This function is private and will not be exposed as a tool
```

---

## **2. Standalone Public Functions (No Class Required)**

Whatever you put in the file is callable, as long as it’s not private (starts with `_`).
Each public function is exposed directly as a tool.
Private (underscore-prefixed) helpers are ignored.

```python
import os
import subprocess
from HoloAI import HoloLink

NAME_REPLACEMENTS = {
    "vs code":     "code",
    "vs studio":   "devenv",
    "vs insiders": "code - insiders",
    "word":        "winword",
    "powerpoint":  "powerpnt",
    "explorer":    "iexplore",
}

holoLink = HoloLink()

def openApp(appName: str) -> str:
    """
    Description: Open an application by its name, normalizing common names to their executable names.
    """
    for key, value in NAME_REPLACEMENTS.items():
        if key in appName.lower():
            appName = value
            break
    try:
        os.startfile(appName)
        return f"Opened {appName}"
    except Exception as e:
        return f"An error occurred while trying to open {appName}: {e}"

def closeApp(appName: str) -> str:
    """
    Description: Close an application by its name, normalizing common names to their executable names.
    """
    for key, value in NAME_REPLACEMENTS.items():
        if key in appName.lower():
            appName = value
            break
    if not appName.lower().endswith('.exe'):
        appName += '.exe'
    try:
        subprocess.run(
            ["taskkill", "/f", "/im", appName],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return f"Closed {appName}"
    except Exception as e:
        return f"An error occurred while trying to close {appName}: {e}"

def _privateHelper(...):
    pass  # This function is private and will not be exposed as a tool
```

---

## **What’s a “Tool”?**

* **Tool:**
  Any public function or public method in a class (not starting with `_`) in a tool file or module.
  *Example: `openApp()` in a class or module.*

* **No action maps or dispatcher methods allowed in tools.**
  Every callable tool is exposed one-to-one.

---

## **Docstrings**

* Use `"""Description: ..."""` as the first line for best results.
* Use `"""Additional Information: ..."""` as the second line for more detail.

---
