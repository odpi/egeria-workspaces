import re, json
from collections import Counter, defaultdict
SP='/private/tmp/claude-501/-Users-amandachessell-Code-ODPi-egeria-docs-egeria-docs/4ede8936-3269-4824-8f08-06b13d6924bd/scratchpad'
xml=open(SP+'/poim_body.xml',encoding='utf-8',errors='replace').read()
fonts={m.group(1):(int(m.group(2)),m.group(3).split('+')[-1]) for m in re.finditer(r'<fontspec id="(\d+)" size="(\d+)" family="([^"]+)"',xml)}
def clean(t):
    return re.sub(r'<[^>]+>','',t).replace('’',"'").replace('“','"').replace('”','"')

def join_lines(els):
    """group elements into visual lines by top, join with soft-hyphen removal"""
    lines=defaultdict(list)
    for e in els: lines[e['top']].append(e)
    outl=[]
    for top in sorted(lines):
        s=''.join(x['raw'] for x in sorted(lines[top],key=lambda x:x['left']))
        outl.append(s.strip())
    res=''
    for s in outl:
        if not s: continue
        if res.endswith('-'): res=res[:-1]+s
        elif res: res=res+' '+s
        else: res=s
    return re.sub(r'\s+',' ',res).strip()

rows_all=[]
for pm in re.finditer(r'<page number="(\d+)"(.*?)</page>',xml,re.S):
    pg=int(pm.group(1)); els=[]
    for m in re.finditer(r'<text top="(\d+)" left="(\d+)" width="(\d+)" height="(\d+)" font="(\d+)">(.*?)</text>', pm.group(2), re.S):
        sz,fam=fonts[m.group(5)]
        if not fam.startswith('TimesLTStd') or sz!=14: continue
        raw=clean(m.group(6))
        if not raw.strip(): continue
        els.append({'top':int(m.group(1)),'left':int(m.group(2)),'raw':raw})
    if len(els)<6: continue
    cnt=Counter(e['left'] for e in els)
    cols=[]
    for l in sorted(cnt):
        if cnt[l]>=3 and not (cols and l-cols[-1]<=12): cols.append(l)
    if len(cols)<3: continue
    namecol,probcol,solcol=cols[0],cols[1],cols[-1]
    if not (probcol-namecol>50 and solcol-probcol>80): continue
    def colof(e):
        c=cols[0]
        for m_ in cols:
            if e['left']>=m_-6: c=m_
        return c
    nametops=sorted(set(e['top'] for e in els if colof(e)==namecol))
    probstarts=sorted(set(e['top'] for e in els if colof(e)==probcol
                          and e['raw'].startswith(' ') and len(e['raw'].strip())>3))
    if not nametops or not probstarts: continue
    probtops=set(e['top'] for e in els if colof(e)==probcol)
    starts=[]
    for ps in probstarts:
        blockstarts={t for i,t in enumerate(nametops) if i==0 or t-nametops[i-1]>25}
        cand=[t for t in nametops if ps-22<=t<=ps+6 and (t>=ps-2 or t in blockstarts)]
        cand=[t for t in cand if not starts or t>starts[-1]]
        starts.append(min(cand) if cand else ps)
    starts=sorted(set(starts))
    bounds=starts+[10**6]
    for i,st in enumerate(starts):
        en=bounds[i+1]
        buckets={namecol:[],probcol:[],solcol:[]}
        for e in els:
            if st-2<=e['top']<en-2:
                c=colof(e)
                if c in buckets: buckets[c].append(e)
        rows_all.append({'page':pg,'name':join_lines(buckets[namecol]),
                         'problem':join_lines(buckets[probcol]),'solution':join_lines(buckets[solcol])})

def fixcaps(s):
    for _ in range(6): s=re.sub(r'(?<![A-Z])([A-Z]) ([A-Z]{2,})', r'\1\2', s)
    return re.sub(r'\s+',' ',s).strip()
def title(n):
    return ' '.join('-'.join(p.capitalize() for p in w.split('-')) if w.isupper() else w for w in n.split(' '))
res=[]
for r in rows_all:
    nm=fixcaps(r['name'])
    if not nm or not re.match(r"^[A-Z][A-Z\-' ]{3,}$", nm): continue
    prob=fixcaps(r['problem']); sol=fixcaps(r['solution'])
    if len(prob)<15 or len(sol)<15: continue
    res.append({'page':r['page'],'name':title(nm),'raw':nm,'problem':prob,'solution':sol})
json.dump(res,open(SP+'/patlets.json','w'),indent=1)
print('patlet rows',len(res),'distinct',len(set(r['name'] for r in res)))
