
from pathlib import Path
import sys
import os
from dotenv import load_dotenv
from HoloOps import HoloOps
import threading

# ---- 1. Detect Project Root and Name ----
PROJECT_ROOT, PROJECT_NAME = HoloOps.detectProject()
load_dotenv(override=True)
MARKER_FILE = f".{PROJECT_NAME}"

# Create marker file so the project can always be detected
HoloOps.createMarkerFile(PROJECT_ROOT, MARKER_FILE)


ROOT_DIR = Path(__file__).parent.resolve()


class ClassName:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ClassName, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.setInternalDirs()
        self.setExternalDirs()
        self.setExcludedDirs()
        self.setCloudProviders()

        self.baseDirs = {
            "root":        PROJECT_ROOT / PROJECT_NAME,
            "sourceDir":   PROJECT_ROOT / PROJECT_NAME,
            "internalDirs": PROJECT_ROOT / PROJECT_NAME,
            "externalDirs": PROJECT_ROOT,
        }
        
        self.mappingConfig = {
            "internalDirs": self.internalDirs,
            "externalDirs": self.externalDirs,
        }
        
        self.storageOptionFn = lambda: os.getenv("STORAGE_OPTION", "local").lower()

        self.holoOps = HoloOps(
            projectName     = PROJECT_NAME,
            baseDirs        = self.baseDirs,
            mappingConfig   = self.mappingConfig,
            markerFile      = MARKER_FILE,
            storageOptionFn = self.storageOptionFn,
            cloudProviders  = self.cloudProviders,
            excludedDirs    = self.excludedDirs,
            useDotenv       = True
        )

        self._initialized = True

    def getDir(self, name: str):
        return self.holoOps.getDir(name)

    def dirNames(self):
        return self.holoOps.dirNames()

    def dirMap(self) -> dict[str, Path]:
        return self.holoOps.dirMap()

    def setExcludedDirs(self):
        self.excludedDirs = [
            ".vs", "bin", "obj", "__pycache__", ".git", ".idea", ".vscode", ".pytest_cache",
            "node_modules", "dist", "build", "coverage", "logs", "temp", "tmp"
        ]

    def setCloudProviders(self):
        self.cloudProviders = [
            "OneDrive", "Google Drive", "Google Drive File Stream", "Dropbox", "iCloudDrive", "Box", "pCloudDrive"
        ]

    def setInternalDirs(self):
        # Internal directories are typically within the project root
        self.internalDirs = {
        "example_1": ["start_dir", "some_name", "and", "so_on"],
        "example_2": ["dir2", "some_name", "and", "so_on"],
        "example_3": ["dir3", "some_name", "and", "so_on"],

    }

    def setExternalDirs(self):
        # External directories are typically 1 level up from the project root
        self.externalDirs = {
            "example_4": ["some_dir", "some_name", "and", "so_on"],
            "example_5": ["some_other_dir", "some_name", "and", "so_on"],
        }


# Example usage
cn = ClassName()
cn.getDir("example_1")