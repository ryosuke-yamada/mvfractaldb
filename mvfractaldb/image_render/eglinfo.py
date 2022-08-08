'''eglinfo - display all available graphic deviecs
'''

import ctypes, pegl
from typing import List

EGLDeviceEXT = ctypes.c_void_p

def enumerateGraphicDevices(_maxDevices : int) -> List[EGLDeviceEXT]:
    '''enumerateGraphicDevices
    Enumerate available graphic devices. It includes software renderer if it is available.

    Args:
        _maxDevices : int - num of devices to enumerate
    
    Return:
        List[EGLDeviceEXT] - list of devices
    
    Comment:
        EGLDeviceEXT = ctypes.c_void_p
    '''
    maxDevices = ctypes.c_int32(_maxDevices)
    PEGLDevEXT = EGLDeviceEXT * _maxDevices
    _eglDevs = [None] * _maxDevices
    eglDevs = PEGLDevEXT(*_eglDevs)
    numDevices = ctypes.c_int32(_maxDevices)
    eglQueryDevicesEXT=pegl.egl._common._load_function("eglQueryDevicesEXT", None, [ctypes.c_int32, ctypes.POINTER(EGLDeviceEXT), ctypes.POINTER(ctypes.c_int32)])
    eglQueryDevicesEXT(maxDevices,eglDevs,ctypes.byref(numDevices))
    return [eglDevs[i] for i in range(numDevices.value)]


def printGraphicDevices(eglDevs : List[EGLDeviceEXT]) -> None:
    '''printGraphicDevices
    Print device name of graphic devices.

    Args:
        eglDevs : List[EGLDeviceEXT] - list of devices

    Comment:
        EGLDeviceEXT = ctypes.c_void_p
    '''
    eglQueryDeviceStringEXT=pegl.egl._common._load_function("eglQueryDeviceStringEXT", ctypes.c_char_p, [EGLDeviceEXT, ctypes.c_int32])
    for i,d in enumerate(eglDevs):
        s = eglQueryDeviceStringEXT(d, pegl.egl.EGL_EXTENSIONS)
        print(i,s)
        # EGL_NV_device_cuda
    return

if __name__=="__main__":
    printGraphicDevices(enumerateGraphicDevices(10))
