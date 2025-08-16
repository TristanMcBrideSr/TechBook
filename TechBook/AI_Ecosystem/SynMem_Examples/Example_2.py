
# YOU WOULD NEED TO PUT THIS INSIDE YOUR SKILLS DIRECTORY SO THE SKILLGRAPH CAN FIND IT.
# E.G., TechBook_Skills/Agent/MemoryManager.py
import logging
import threading
import inspect
from AI_Ecosystem.SynMem_Examples.Example_1 import Memory
from SkillLink import SkillLink

logger = logging.getLogger(__name__)


class MemoryManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(MemoryManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, "initialized"):
            return
        self._initComponents()
        self.initialized = True

    def _initComponents(self):
        self.skillLink  = SkillLink()
        self.memory = Memory()
        self.actionMap = {
            **self.memory.actionMap, # by doing this, we can call the actionMap from within the Memory's actionMap,
            # allowing us to use the same actions defined in Memory the model can call.
        }

    def _metaData(self):
        return {
            "className": self.__class__.__name__,
            "description": "Manage memory."
        }

    def memorySkill(self, action: str, *args):
        self.skillLink.calledActions(self, locals())
        try:
            actionKey = self.actionMap.get(action.lower())
            if actionKey is None:
                return f"Invalid {self.__class__.__name__.lower()}Action provided: {action}"

            paramCount = len(inspect.signature(actionKey).parameters)
            return actionKey(*args[:paramCount]) if paramCount > 0 else actionKey()
        except Exception as e:
            logger.error(f"Error executing {self.__class__.__name__.lower()}Action '{action}':", exc_info=True)