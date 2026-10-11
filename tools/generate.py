"""Regenerate outputs with KiCad 9. Does not alter the editable design."""
from pathlib import Path
import argparse,subprocess,json,shutil
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--kicad-cli',default='kicad-cli');args=p.parse_args()
REV='P2-prep-01';out='manufacturing/'+REV
for d in [out,'docs/images','docs/validation']:(ROOT/d).mkdir(parents=True,exist_ok=True)
board='hardware/RayRigAntSw.kicad_pcb';sch='hardware/RayRigAntSw.kicad_sch'
commands=[
 ['pcb','export','gerbers','--no-protel-ext','--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts','-o',out+'/',board],
 ['pcb','export','drill','--excellon-separate-th','--excellon-units','mm','-o',out+'/',board],
 ['pcb','export','pos','--format','csv','--units','mm','-o',out+'/RayRigAntSw-positions.csv',board],
 ['sch','export','svg','-o','docs/images/',sch],
 ['pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--layers','F.Cu,F.SilkS,Edge.Cuts','-o','docs/images/pcb-front.svg',board],
 ['pcb','drc','--schematic-parity','--format','json','-o','docs/validation/drc.json',board],
 ['sch','erc','--format','json','-o','docs/validation/erc.json',sch]]
for cmd in commands:
 r=subprocess.run([args.kicad_cli]+cmd,cwd=ROOT,capture_output=True,text=True,encoding='utf8',errors='replace')
 if r.returncode:raise RuntimeError(str(cmd)+'\n'+r.stdout+r.stderr)
 print('Completed: '+' '.join(cmd[:3]))
# Reports can contain workstation paths. Retain diagnostic content with relative locations.
for n in ['drc','erc']:
 f=ROOT/'docs/validation'/ (n+'.json');data=json.loads(f.read_text(encoding='utf8'))
 def scrub(x):
  if isinstance(x,str):return x.replace(str(ROOT),'$PROJECT').replace(ROOT.as_posix(),'$PROJECT')
  if isinstance(x,list):return [scrub(v) for v in x]
  if isinstance(x,dict):return {k:scrub(v) for k,v in x.items()}
  return x
 f.write_text(json.dumps(scrub(data),indent=2),encoding='utf8')
for n in ['LICENSE','NOTICE']:shutil.copyfile(ROOT/n,ROOT/out/n)
shutil.copyfile(ROOT/'bom/RayRigAntSw.csv',ROOT/out/'RayRigAntSw-bom.csv')
(ROOT/'docs/validation/generation.json').write_text(json.dumps({'revision':REV,'tool':subprocess.check_output([args.kicad_cli,'version'],text=True).strip(),'commands':commands},indent=2),encoding='utf8')

