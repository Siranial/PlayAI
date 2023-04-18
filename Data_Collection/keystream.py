import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
while (True):
    """
    time.sleep(4)
    PressKey(0x1E) #a
    time.sleep(0.1)
    ReleaseKey(0x1E) #a
    time.sleep(0.1)
    PressKey(0x1E) #a
    PressKey(0x2D) #x
    time.sleep(0.1)
    ReleaseKey(0x1E) #a
    ReleaseKey(0x2D) #x
    time.sleep(0.1)
    """
    time.sleep(4)
    PressKey(0x1E) #a
    time.sleep(0.05)
    ReleaseKey(0x1E) #a
    time.sleep(0.05)
    PressKey(0x20) #d
    time.sleep(0.05)
    ReleaseKey(0x20) #d
    time.sleep(0.05)
    PressKey(0x4B) #numpad 4
    time.sleep(0.05)
    ReleaseKey(0x4B) #numpad 4
    time.sleep(0.05)
    PressKey(0x2C) #z
    time.sleep(0.05)
    ReleaseKey(0x2C) #z
    time.sleep(0.05)
    PressKey(0x2E) #c
    time.sleep(0.05)
    ReleaseKey(0x2E) #c
    """
    time.sleep(2)
    PressKey(0x21) #f
    time.sleep(0.05)
    ReleaseKey(0x21) #f
    time.sleep(0.05)
    """
    exit()