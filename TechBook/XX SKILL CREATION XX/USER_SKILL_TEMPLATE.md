
---

# **User Skill Creation Guide**

---

## **Overview**

Write modular User skills for this framework.
No decorators, no schemas, no wrappers.
**All logic goes through an `executeAction` function.**

---

## **Skill Exposure**

* The only function exposed is `executeAction` (either as a method or a module-level function).
* All "actions" are routed through a mapping (`actionMap`, `ACTION_MAP`, etc).
* Private helpers (prefix `_`) are never exposed.
* All handler/action methods should accept `*args` for safety.
* No decorators or schemas.

---

## **Pattern 1: Singleton Class With Action Map**

```python
import threading
import logging
from HoloAI import HoloLink

logger = logging.getLogger(__name__)

class DateTimeManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DateTimeManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        self._initComponents()
        self.initialized = True

    def _initComponents(self):
        self.holoLink = HoloLink()
        self.actionMap = {
            "what is the date": self._getCurrentDate,
            "what is the time": self._getCurrentTime,
        }

    def executeAction(self, ctx: str):
        # self.holoLink.calledActions(self, locals())
        # try:
        #     ctxLower = ctx.lower()
        #     actionKey = next((key for key in self.actionMap if key in ctxLower), None)
        #     if not actionKey:
        #         return None
        #     args = ctxLower.replace(actionKey, "", 1).strip()
        #     return self.actionMap[actionKey](args)
        # except Exception as e:
        #     logger.error(f"Error executing {self.__class__.__name__.lower()}Action '{ctx}':", exc_info=True)
        #     return f"Error: {e}"
        self.holoLink.calledActions(self, locals())
        name = inspect.currentframe().f_code.co_name
        return self.holoLink.executeSkill('user', name, self.actionMap, ctx)

    def _getCurrentDate(self, *args) -> str: # FOR SAFETY REASONS ALWAYS ADD *args TO THE FUNCTION SIGNATURE EVEN IF NOT USED
        from datetime import datetime
        return datetime.now().strftime('%d-%B-%Y')

    def _getCurrentTime(self, *args) -> str: # FOR SAFETY REASONS ALWAYS ADD *args TO THE FUNCTION SIGNATURE EVEN IF NOT USED
        from datetime import datetime
        return datetime.now().strftime('%H:%M')
```

---

## **Pattern 2: Module With Action Map and executeAction**

```python
from datetime import datetime
from HoloAI import HoloLink

def _getCurrentDate(*args) -> str: # FOR SAFETY REASONS ALWAYS ADD *args TO THE FUNCTION SIGNATURE EVEN IF NOT USED
    return datetime.now().strftime('%d-%B-%Y')

def _getCurrentTime(*args) -> str: # FOR SAFETY REASONS ALWAYS ADD *args TO THE FUNCTION SIGNATURE EVEN IF NOT USED
    return datetime.now().strftime('%H:%M')

ACTION_MAP = {
    "what is the date": _getCurrentDate,
    "what is the time": _getCurrentTime,
}

holoLink = HoloLink()

def executeAction(ctx: str):
    # self.holoLink.calledActions(self, locals())
        # try:
        #     ctxLower = ctx.lower()
        #     actionKey = next((key for key in self.actionMap if key in ctxLower), None)
        #     if not actionKey:
        #         return None
        #     args = ctxLower.replace(actionKey, "", 1).strip()
        #     return self.actionMap[actionKey](args)
        # except Exception as e:
        #     logger.error(f"Error executing {self.__class__.__name__.lower()}Action '{ctx}':", exc_info=True)
        #     return f"Error: {e}"
    holoLink.calledActions(self, locals())
    name = inspect.currentframe().f_code.co_name
    return holoLink.executeSkill('user', name, self.actionMap, ctx)
```

---

## **Summary**

* **ALWAYS** use an `executeAction` entry point (either a class method or a module function).
* **ALWAYS** use an action mapping (`actionMap` or `ACTION_MAP`) to map context to actions.
* **NEVER** use plain standalone functions as skills.
* **ALWAYS** use `*args` in handler functions.
* **ONLY** import `HoloLink` from `HoloLink`.

---

*No decorators. No schemas. Only what you make public in the action map, routed through `executeAction`, is exposed.*

---
