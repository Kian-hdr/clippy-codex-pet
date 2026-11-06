"""Offline installer tests; no login, network or real Codex settings are used."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='clippy-test-')
        self.base = Path(self.temp.name)
        self.home = self.base/'codex-home'
        self.package = self.base/'package'
        self.package.mkdir()
        shutil.copy2(ROOT/'install.py', self.package/'install.py')
        shutil.copytree(ROOT/'pet', self.package/'pet')
    def tearDown(self):
        self.temp.cleanup()
    def run_install(self, *args):
        env = dict(os.environ, CODEX_HOME=str(self.home), PYTHONDONTWRITEBYTECODE='1')
        return subprocess.run([sys.executable, str(self.package/'install.py'), *args], env=env, text=True, capture_output=True)
    def test_documented_install_select_and_preservation(self):
        self.home.mkdir()
        original = {'root-sentinel':'keep', 'electron-persisted-atom-state':{'other-setting':{'keep':True}, 'selected-avatar-id':'custom:previous'}}
        state = self.home/'.codex-global-state.json'
        state.write_text(json.dumps(original))
        result = self.run_install('--select','--size','192')
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads(state.read_text())
        self.assertEqual(data['root-sentinel'],'keep')
        self.assertEqual(data['electron-persisted-atom-state']['other-setting'],{'keep':True})
        self.assertEqual(data['electron-persisted-atom-state']['selected-avatar-id'],'custom:clippy')
        self.assertEqual(data['electron-persisted-atom-state']['avatar-overlay-mascot-width-px'],192)
        backups=list(self.home.glob('.codex-global-state.json.clippy-backup-*'))
        self.assertEqual(len(backups),1)
        self.assertEqual(json.loads(backups[0].read_text()),original)
        self.assertEqual((self.home/'pets/clippy/spritesheet.png').read_bytes(),(ROOT/'pet/spritesheet.png').read_bytes())
    def test_same_package_install_is_idempotent(self):
        self.assertEqual(self.run_install().returncode,0)
        self.assertEqual(self.run_install().returncode,0)
    def test_conflicting_pet_is_preserved(self):
        self.assertEqual(self.run_install().returncode,0)
        manifest=self.home/'pets/clippy/pet.json'
        manifest.write_text('{"displayName":"Keep me"}')
        result=self.run_install()
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(manifest.read_text(),'{"displayName":"Keep me"}')
    def test_manifest_traversal_is_rejected(self):
        manifest=self.package/'pet/pet.json'
        data=json.loads(manifest.read_text());data['spritesheetPath']='../../outside.png';manifest.write_text(json.dumps(data))
        self.assertNotEqual(self.run_install().returncode,0)
        self.assertFalse((self.home/'pets/clippy').exists())
    def test_wrong_dimensions_are_rejected(self):
        image=self.package/'pet/spritesheet.png'
        data=bytearray(image.read_bytes());data[16:20]=(100).to_bytes(4,'big');image.write_bytes(data)
        self.assertNotEqual(self.run_install().returncode,0)
        self.assertFalse((self.home/'pets/clippy').exists())
    def test_size_requires_selection(self):
        self.assertNotEqual(self.run_install('--size','192').returncode,0)
        self.assertFalse(self.home.exists())
    def test_out_of_range_size_is_rejected_before_writes(self):
        self.assertNotEqual(self.run_install('--select','--size','300').returncode,0)
        self.assertFalse(self.home.exists())
    def test_symlinked_settings_are_preserved(self):
        self.home.mkdir()
        outside=self.base/'outside.json';outside.write_text('{"keep":true}')
        (self.home/'.codex-global-state.json').symlink_to(outside)
        result=self.run_install('--select')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(outside.read_text(),'{"keep":true}')

if __name__ == '__main__':
    unittest.main()
