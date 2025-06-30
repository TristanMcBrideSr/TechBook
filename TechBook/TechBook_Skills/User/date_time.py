
from datetime import datetime
import threading
import logging
import inspect
from SkillsManager import SkillsManager

logger = logging.getLogger(__name__)


class DTManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(DTManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        self._initComponents()
        self.initialized = True

    def _initComponents(self):
        self.skillsManager = SkillsManager()
        self.actionMap = {
            "what is the date": self._getCurrentDate,
            "what is the time": self._getCurrentTime,
        }

    def _metaData(self):
        return {
            "className": f"{self.__class__.__name__}",
            "description": "Get current date and time information"
        }

    def executeAction(self, ctx: str) -> str:
        """
        We made it even easies to execute actions by using the SkillsManager to handle
        the action execution. This way, we can easily add new actions without modifying
        the code here, just by adding them to the actionMap.
        """
        # self.argParser.printArgs(self, locals())
        # try:
        #     action = ctx.lower()
        #     actionKey = next((key for key in self.actionMap if key in action), None)
        #     if not actionKey:
        #         return None
        #     args = action.replace(actionKey, "", 1).strip()
        #     return self.actionMap[actionKey](args)
        # except Exception as e:
        #     logger.error(f"Error executing {self.__class__.__name__.lower()}Action '{ctx}':", exc_info=True)
        #     return f"Error: {e}"
        self.skillsManager.argParser.printArgs(self, locals())
        name = inspect.currentframe().f_code.co_name
        return self.skillsManager.executeSkill('user', name, self.actionMap, ctx)

    def _getCurrentDate(self, *args): # FOR SAFETY REASONS ALWAYS ADD *args TO THE FUNCTION SIGNATURE EVEN IF NOT USED
        return datetime.now().strftime('%d-%B-%Y')

    def _getCurrentTime(self, *args): # FOR SAFETY REASONS ALWAYS ADD *args TO THE FUNCTION SIGNATURE EVEN IF NOT USED
        return datetime.now().strftime('%H:%M')
