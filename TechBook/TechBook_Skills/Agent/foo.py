
##-------------------------- This is a quick example of how to use the SkillLink to execute actions using dicts and lists --------------------------##
# Please refer to get_weather.py for a more complete example of how to use the SkillLink to execute actions using dicts and lists.

import logging
import subprocess
import os
import threading
import inspect
import requests
import json

from SkillLink import SkillLink

logger = logging.getLogger(__name__)


## Singleton class for managing application actions
class Dummy:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Dummy, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        self._initComponents()
        self.initialized = True

    def _initComponents(self):
        # self.skillLink = SkillLink()
        self.skillLink = SkillLink()
        self.listSig = {
        "_fooFunc": ["userId", "section"], # List of arguments for _fooFunc
        }
        self.dictSig = {
            "_barFunc": {"username": "User's name", "email": "User's email address"}, # Dictionary of arguments for _barFunc
        }
        self.actionMap = {
            "list-func": self._fooFunc,
            "dict-func": self._barFunc,
        }

    def fooBarSkill(self, action: str, *args):
        """
        We made it even easies to execute actions by using the SkillLink to handle
        the action execution. This way, we can easily add new actions without modifying
        the code here, just by adding them to the actionMap.
        """
        # self.argParser.printArgs(self, locals())
        # try:
        #     actionKey = self.actionMap.get(action.lower())
        #     if actionKey is None:
        #         return f"Invalid {self.__class__.__name__.lower()}Action provided: {action}"

        #     func_name = actionKey.__name__
        #     sig = inspect.signature(actionKey)
        #     # If this action expects a list, bundle all args into one list argument
        #     if func_name in self.listSig:
        #         return actionKey(list(args))
        #     # If this action expects a dict, zip your args into the dict’s keys
        #     if func_name in self.dictSig:
        #         keys = list(self.dictSig[func_name].keys())
        #         info_dict = dict(zip(keys, args))
        #         return actionKey(info_dict)
        #     # Otherwise fall back to normal positional dispatch
        #     param_count = len(sig.parameters)
        #     return actionKey(*args[:param_count])
        # except Exception as e:
        #     logger.error(f"Error executing {self.__class__.__name__.lower()}Action '{action}':", exc_info=True)
        self.skillLink.calledActions(self, locals())
        name = inspect.currentframe().f_code.co_name
        return self.skillLink.executeSkill('system', name, self.actionMap, action, *args)


    def _fooFunc(self, infoList: list) -> str:
        userId, section = infoList
        return f"Got list with userId={userId}, section={section}"

    def _barFunc(self, infoDict: dict) -> str:
        username = infoDict.get("username")
        phone = infoDict.get("phone")
        return f"Got dict with username={username}, phone={phone}"

