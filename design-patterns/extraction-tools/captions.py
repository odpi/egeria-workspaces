import re, json
from collections import defaultdict
SP='/private/tmp/claude-501/-Users-amandachessell-Code-ODPi-egeria-docs-egeria-docs/4ede8936-3269-4824-8f08-06b13d6924bd/scratchpad'
xml=open(SP+'/poim_body.xml',encoding='utf-8',errors='replace').read()
fonts={m.group(1):(int(m.group(2)),m.group(3).split('+')[-1]) for m in re.finditer(r'<fontspec id="(\d+)" size="(\d+)" family="([^"]+)"',xml)}
caps=defaultdict(list)
for pm in re.finditer(r'<page number="(\d+)"(.*?)</page>',xml,re.S):
    pg=int(pm.group(1)); lines=defaultdict(list)
    for m in re.finditer(r'<text top="(\d+)" left="(\d+)"[^>]*font="(\d+)">(.*?)</text>', pm.group(2), re.S):
        sz,fam=fonts[m.group(3)]
        if not fam.startswith('HelveticaLTStd'): continue
        t=re.sub(r'<[^>]+>','',m.group(4))
        if t.strip(): lines[int(m.group(1))].append((int(m.group(2)),t))
    for top in sorted(lines):
        s=''.join(x[1] for x in sorted(lines[top]))
        s=re.sub(r'\s+',' ',s).replace('’',"'").strip()
        if re.match(r'^(Figure|Table)\s+\d+\.\d+', s): caps[pg].append(s)
json.dump({str(k):v for k,v in caps.items()},open(SP+'/captions.json','w'),indent=1)
print('pages with captions',len(caps),'total',sum(len(v) for v in caps.values()))
print(caps[383], caps[377])
