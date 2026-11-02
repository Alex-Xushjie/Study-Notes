"""Windows user-bound DPAPI protection; credentials never saved as plaintext."""
import base64,ctypes,os
from ctypes import wintypes
class Blob(ctypes.Structure):
    _fields_=[('size',wintypes.DWORD),('data',ctypes.POINTER(ctypes.c_ubyte))]
def transform(value,decrypt=False):
    if os.name!='nt':raise RuntimeError('Saving passwords requires Windows DPAPI on this version')
    raw=base64.b64decode(value) if decrypt else value.encode('utf-8')
    buffer=ctypes.create_string_buffer(raw); source=Blob(len(raw),ctypes.cast(buffer,ctypes.POINTER(ctypes.c_ubyte)));target=Blob()
    api=ctypes.windll.crypt32
    if decrypt:ok=api.CryptUnprotectData(ctypes.byref(source),None,None,None,None,1,ctypes.byref(target))
    else:ok=api.CryptProtectData(ctypes.byref(source),None,None,None,None,1,ctypes.byref(target))
    if not ok:raise ValueError('Cannot unlock credentials for this Windows user; re-enter device passwords')
    try:
        data=ctypes.string_at(target.data,target.size)
        return data.decode('utf-8') if decrypt else base64.b64encode(data).decode('ascii')
    finally:ctypes.windll.kernel32.LocalFree(target.data)
def protect(password):return transform(password)
def unprotect(value):return transform(value,True)
