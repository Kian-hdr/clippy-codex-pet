#!/usr/bin/env python3
"""Install a local Clippy pet package without changing other Codex settings."""
import argparse, hashlib, json, os, shutil, struct, tempfile
from pathlib import Path
from datetime import datetime, timezone

def select(home, size=None):
    if size is not None and not 80 <= size <= 224:
        raise ValueError('Pet size must be between 80 and 224 pixels.')
    state=home/'.codex-global-state.json'
    if state.is_symlink():
        raise ValueError('Refusing to replace a symlinked settings file.')
    data=json.loads(state.read_text()) if state.exists() else {}
    if not isinstance(data,dict):raise ValueError('Expected an object in settings.')
    atoms=data.setdefault('electron-persisted-atom-state',{})
    if not isinstance(atoms,dict):raise ValueError('Expected a settings atom object.')
    atoms['selected-avatar-id']='custom:clippy'
    if size is not None:atoms['avatar-overlay-mascot-width-px']=size
    if state.exists():
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copy2(state,state.with_name(state.name+'.clippy-backup-'+stamp))
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=home,prefix='.clippy-state-',delete=False) as f:
        json.dump(data,f,indent=2);f.write('\n');temp=Path(f.name)
    try:
        temp.chmod(state.stat().st_mode & 0o777 if state.exists() else 0o600)
        os.replace(temp,state)
    finally:
        if temp.exists():temp.unlink()
    return state

def install(source, home):
    manifest=json.loads((source/'pet.json').read_text())
    if manifest.get('spriteVersionNumber')!=2 or manifest.get('spritesheetPath')!='spritesheet.png':
        raise ValueError('Unsupported pet manifest.')
    image=source/manifest['spritesheetPath']
    data=image.read_bytes()
    if len(data)<24 or data[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',data[16:24])!=(1536,2288):
        raise ValueError('Expected a transparent v2 PNG atlas, 1536x2288.')
    target=home/'pets'/'clippy'
    if target.exists():
        existing=target/manifest['spritesheetPath']
        if existing.is_file() and existing.read_bytes()==data and (target/'pet.json').read_text()==(source/'pet.json').read_text():
            return target
        raise FileExistsError('An existing clippy pet differs; back it up or choose a separate Codex configuration.')
    target.parent.mkdir(parents=True,exist_ok=True)
    staging=Path(tempfile.mkdtemp(prefix='.clippy-',dir=target.parent))
    try:
        for name in ['pet.json',manifest['spritesheetPath']]:shutil.copy2(source/name,staging/name)
        staging.rename(target)
    finally:
        if staging.exists():shutil.rmtree(staging)
    return target

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--codex-home',type=Path,default=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex'))))
    p.add_argument('--select',action='store_true',help='Select Clippy in persisted desktop settings. Close Codex first.')
    p.add_argument('--size',type=int,help='Optional desktop width in pixels (80–224); requires --select.')
    args=p.parse_args()
    if args.size is not None and not args.select:p.error('--size requires --select')
    if args.size is not None and not 80 <= args.size <= 224:p.error('--size must be between 80 and 224')
    target=install(Path(__file__).resolve().parent/'pet',args.codex_home.expanduser().resolve())
    if args.select:
        select(args.codex_home.expanduser().resolve(),args.size)
    print(f'Installed: {target}\n'+('Clippy selected in persisted settings. Reopen Codex to load it.' if args.select else 'Reload Codex and select Clippy in the pet picker.'))
