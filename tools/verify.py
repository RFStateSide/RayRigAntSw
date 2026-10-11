from pathlib import Path
import argparse,subprocess,tempfile,xml.etree.ElementTree as ET,json,re,csv,hashlib,collections,math
ROOT=Path(__file__).resolve().parents[1]
def parse(s):
 stack=[];root=[];cur=root
 for t in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s):
  if t=='(':n=[];cur.append(n);stack.append(cur);cur=n
  elif t==')':cur=stack.pop()
  else:cur.append(t[1:-1] if t.startswith('"') else t)
 return root[0]
def it(n,k):return [x for x in n if isinstance(x,list) and x and x[0]==k]
def one(n,k):return next(iter(it(n,k)),[])
def prop(n,k):return next((x[2] for x in it(n,'property') if x[1]==k),'')
def check(cli):
 pcb=parse((ROOT/'hardware/RayRigAntSw.kicad_pcb').read_text(encoding='utf8'))
 sch=parse((ROOT/'hardware/RayRigAntSw.kicad_sch').read_text(encoding='utf8'))
 fps={prop(f,'Reference'):f for f in it(pcb,'footprint')}
 syms={prop(f,'Reference'):f for f in it(sch,'symbol') if not prop(f,'Reference').startswith('#')}
 assert set(fps)==set(syms)
 lib=parse((ROOT/'hardware/libraries/RayRigAntSw.kicad_sym').read_text(encoding='utf8'))
 libnames={x[1] for x in it(lib,'symbol')}
 for f in it(sch,'symbol'):assert one(f,'lib_id')[1].split(':',1)[1] in libnames
 for ref,f in fps.items():
  assert not it(f,'model')
  assert (ROOT/'hardware/libraries/RayRigAntSw.pretty'/(f[1].split(':',1)[1]+'.kicad_mod')).exists()
  assert prop(syms[ref],'Footprint')==f[1]
  assert prop(syms[ref],'Value')==prop(f,'Value')
 with tempfile.TemporaryDirectory() as t:
  out=Path(t)/'net.xml'
  subprocess.run([cli,'sch','export','netlist','--format','kicadxml','-o',str(out),str(ROOT/'hardware/RayRigAntSw.kicad_sch')],check=True,capture_output=True)
  xml=ET.parse(out).getroot()
  snets={frozenset((n.get('ref'),n.get('pin')) for n in net.findall('node')) for net in xml.findall('./nets/net')}
 bnets=collections.defaultdict(set)
 for ref,f in fps.items():
  for p in it(f,'pad'):
   if one(p,'net'):bnets[one(p,'net')[-1]].add((ref,p[1]))
 assert snets=={frozenset(v) for v in bnets.values()},'PCB/schematic pin-net partition differs'
 expected={'D1':'ANT_R1','D2':'ANT_R2','D3':'TXRX','D4':'TXRX','D5':'RIG_AB'}
 gerber=(ROOT/'manufacturing/P2-prep-01/RayRigAntSw-F_Cu.gbr').read_text()
 for ref,anode in expected.items():
  f=fps[ref];pads={x[1]:x for x in it(f,'pad')}
  assert one(pads['1'],'net')[-1]=='+12V' and one(pads['2'],'net')[-1]==anode
  for num,net in [('1','+12V'),('2',anode)]:
   m=re.search(r'%TO\.P,'+ref+','+num+r'(?:,[^*]*)?\*%\s*%TO\.N,([^*]+)\*%\s*X(-?\d+)Y(-?\d+)D03',gerber)
   assert m and m[1]==net,(ref,num,'Gerber polarity')
   x,y=map(float,one(f,'at')[1:3]);angle=math.radians(float(one(f,'at')[3]) if len(one(f,'at'))>3 else 0)
   px,py=map(float,one(pads[num],'at')[1:3]);gx=x+px*math.cos(angle)+py*math.sin(angle);gy=y-px*math.sin(angle)+py*math.cos(angle)
   assert abs(int(m[2])/1e6-gx)<1e-5 and abs(-int(m[3])/1e6-gy)<1e-5,(ref,num,'Gerber position')
 rows=list(csv.DictReader((ROOT/'bom/RayRigAntSw.csv').open(encoding='utf8')))
 refs={r.strip() for row in rows for r in row['Designator'].split(',')}
 assert refs==set(fps),'BOM coverage'
 for row in rows:
  rr=[r.strip() for r in row['Designator'].split(',')]
  assert int(row['Quantity'])==len(rr)
  if not row['Designator'].startswith('J9'):
   for ref in rr:
    assert row['Value']==prop(fps[ref],'Value')
    assert row['Footprint']==fps[ref][1]
 man=ROOT/'manufacturing/P2-prep-01'
 for suffix in ['F_Cu.gbr','B_Cu.gbr','F_Mask.gbr','B_Mask.gbr','F_Silkscreen.gbr','B_Silkscreen.gbr','Edge_Cuts.gbr','PTH.drl','NPTH.drl']:
  assert (man/('RayRigAntSw-'+suffix)).stat().st_size>100
 for f in man.glob('*.gbr'):assert 'P2-prep-01' in f.read_text()
 # Compare every round drilled pad/via center and diameter with Excellon output.
 expected_holes=[]
 for f in fps.values():
  x,y=map(float,one(f,'at')[1:3]);ang=math.radians(float(one(f,'at')[3]) if len(one(f,'at'))>3 else 0)
  for p in it(f,'pad'):
   drill=one(p,'drill')
   if not drill:continue
   assert drill[1]!='oval','Slot verification needs explicit extension'
   px,py=map(float,one(p,'at')[1:3])
   expected_holes.append((round(x+px*math.cos(ang)+py*math.sin(ang),3),round(y-px*math.sin(ang)+py*math.cos(ang),3),round(float(drill[1]),3)))
 for v in it(pcb,'via'):
  expected_holes.append((round(float(one(v,'at')[1]),3),round(float(one(v,'at')[2]),3),round(float(one(v,'drill')[1]),3)))
 actual_holes=[]
 for df in man.glob('*.drl'):
  tools={};diam=None
  for line in df.read_text().splitlines():
   m=re.fullmatch(r'T(\d+)C([\d.]+)',line)
   if m:tools[m[1]]=float(m[2]);continue
   m=re.fullmatch(r'T(\d+)',line)
   if m:diam=tools[m[1]];continue
   m=re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)',line)
   if m:actual_holes.append((round(float(m[1]),3),round(-float(m[2]),3),round(diam,3)))
 remaining=list(set(expected_holes))
 assert len(actual_holes)==len(remaining)
 for hole in actual_holes:
  match=next((h for h in remaining if abs(h[0]-hole[0])<=0.00101 and abs(h[1]-hole[1])<=0.00101 and h[2]==hole[2]),None)
  assert match is not None,'Excellon hole differs from board pads/vias'
  remaining.remove(match)
 assert (man/'RayRigAntSw-bom.csv').read_bytes()==(ROOT/'bom/RayRigAntSw.csv').read_bytes()
 for n in ['LICENSE','NOTICE']:assert (man/n).read_bytes()==(ROOT/n).read_bytes()
 drc=json.loads((ROOT/'docs/validation/drc.json').read_text())
 assert not drc['unconnected_items'] and not drc['schematic_parity']
 drc_counts=collections.Counter(x['type'] for x in drc['violations'])
 assert drc_counts['clearance']==4 and set(drc_counts)<= {'clearance','malformed_courtyard'}
 for x in drc['violations']:
  if x['type']=='malformed_courtyard':
   assert all(i['description'] in ['Footprint J6','Footprint J7'] for i in x['items'])
 erc=json.loads((ROOT/'docs/validation/erc.json').read_text())
 counts=collections.Counter(x['type'] for sh in erc['sheets'] for x in sh['violations'])
 assert counts=={'power_pin_not_driven':2,'pin_to_pin':6,'unconnected_wire_endpoint':1}
 result={'component_references':len(fps),'schematic_pcb_pin_net_partitions_equal':True,'local_library_resolution':True,'bom_reference_value_footprint_coverage':True,'all_five_diodes_source_and_gerber_net_and_position':True,'unconnected_pcb_items':0,'schematic_parity_issues':0,'retained_drc_clearance_errors':4,'retained_erc_findings':dict(counts)}
 result['retained_courtyard_findings']=drc_counts['malformed_courtyard']
 result['drill_centers_and_diameters_match']=True
 result['drilled_holes']=len(actual_holes)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--kicad-cli',default='kicad-cli');p.add_argument('--record',action='store_true');a=p.parse_args()
 r=check(a.kicad_cli)
 if a.record:(ROOT/'docs/validation/checks.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf8')
 manifest=ROOT/'SHA256SUMS'
 if manifest.exists() and not a.record:
  import runpy
  runpy.run_path(str(ROOT/'tools/integrity.py'))['verify'](ROOT)
 print(json.dumps(r,indent=2))

