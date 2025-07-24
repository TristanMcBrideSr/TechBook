# Very easy example of how to use the BitSig make sure you have the BitSig package installed. 'pip install BitSig'
#In your main file, you can use the BitSig as follows:
# Option 1:
from BitSig import BitSig
path = "Your/Path/" # choose a directory where you want to save the Log files
level= "DEBUG" # or "INFO", "WARNING", "ERROR", "CRITICAL" that you want to set for printing to the console
BitSig(path, level)

# Option 2:
from BitSig import configureBitSig
path = "Your/Path/" # choose a directory where you want to save the Log files
level= "DEBUG" # or "INFO", "WARNING", "ERROR", "CRITICAL" that you want to set for printing to the console
configureBitSig(path, level)

# All your other imports and code can remain the same after this line.
