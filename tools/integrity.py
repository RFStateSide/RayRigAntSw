"""Exact-byte release integrity. Git attributes disable line-ending conversion.

Run python tools/integrity.py to verify without KiCad.
After reviewing intended changes, use python tools/integrity.py --write
to regenerate SHA256SUMS. No source file is normalized or rewritten.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
def inventory(root):
    files={}
    for f in root.rglob('*'):
        rel=f.relative_to(root)
        if '.git' in rel.parts:continue
        if f.is_symlink():raise ValueError('Symlink is not a release payload: '+rel.as_posix())
        if not f.is_file() or rel.as_posix()=='SHA256SUMS':continue
        if '__pycache__' in rel.parts or f.suffix in ('.kicad_prl','.pyc','.lck') or f.name=='fp-info-cache' or any(x.endswith('-backups') for x in rel.parts):
            raise ValueError('Local/generated file in release tree: '+rel.as_posix())
        files[rel.as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
    return files
def verify(root=ROOT):
    entries={}
    for line in (root/'SHA256SUMS').read_text(encoding='utf8').splitlines():
        m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
        if not m:raise ValueError('Invalid SHA256SUMS entry')
        digest,name=m.groups();p=PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name or name in entries or name=='SHA256SUMS':
            raise ValueError('Unsafe or duplicate manifest path: '+name)
        entries[name]=digest
    actual=inventory(root)
    if entries.keys()!=actual.keys():
        raise ValueError('Manifest inventory differs: missing='+str(sorted(entries.keys()-actual.keys()))+'; extra='+str(sorted(actual.keys()-entries.keys())))
    bad=[n for n in entries if entries[n]!=actual[n]]
    if bad:raise ValueError('SHA-256 mismatch: '+', '.join(bad))
    return len(entries)
def write(root=ROOT):
    entries=inventory(root)
    (root/'SHA256SUMS').write_bytes(''.join(entries[n]+'  '+n+'\n' for n in sorted(entries)).encode('utf8'))
    return verify(root)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='Regenerate the manifest after reviewing intended file changes')
    args=parser.parse_args()
    print(str(write() if args.write else verify())+' payload files verified byte-for-byte.')

