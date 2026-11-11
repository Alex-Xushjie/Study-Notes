import sys,types,unittest
from unittest.mock import patch
from storage import credentials
from storage.project import restore_device
class MacCredentialsTests(unittest.TestCase):
    def test_keychain_and_windows_project(self):
        saved={}
        backend=types.SimpleNamespace(set_password=lambda service,key,value:saved.update({key:value}),get_password=lambda service,key:saved.get(key))
        with patch.object(credentials.sys,'platform','darwin'),patch.dict(sys.modules,{'keyring':backend}):
            token=credentials.protect('test-secret')
            self.assertTrue(token.startswith('mac-keychain:'))
            self.assertNotIn('test-secret',token)
            self.assertEqual(credentials.unprotect(token),'test-secret')
            device=restore_device({'id':'r','host':'192.0.2.1','protected_credential':'old-windows-token'})
            self.assertEqual(device.password,'')
            saved.clear()
            with self.assertRaises(ValueError):credentials.unprotect(token)
