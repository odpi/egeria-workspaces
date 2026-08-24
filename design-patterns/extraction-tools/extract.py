import re, json
SP='/private/tmp/claude-501/-Users-amandachessell-Code-ODPi-egeria-docs-egeria-docs/4ede8936-3269-4824-8f08-06b13d6924bd/scratchpad'
FIRST=99; LAST=672
pages=open(SP+'/poim_body.txt',encoding='utf-8',errors='replace').read().split('\f')
outline=json.load(open(SP+'/outline.json'))
captions=json.load(open(SP+'/captions.json'))

def unlig(t):
    return re.sub(r'\b([A-Za-z]*?(?:ffi|ffl|fi|fl|ff)) ([a-z]{2,})\b', r'\1\2', t)
def norm(s):
    s=s.replace('’',"'").replace('“','"').replace('”','"')
    return re.sub(r'\s+',' ',s).strip()

GROUPY=re.compile(r'(Patterns|Elements|Provisioning|Information)$')
by_page={}
for pg,kind,txt in outline:
    if pg>LAST: continue
    t=unlig(txt)
    if kind=='PATTERN' and t.endswith(' Patterns'): kind='GROUP'
    by_page.setdefault(pg,[]).append((kind,t))

DROP=re.compile(r'^(Chessell_Book\.indb|\d+/\d+/\d+\s)')
FIG=re.compile(r'^(Figure|Table)\s+\d+\.\d+')
BULLET=re.compile(r'^(•|\d+\.\s)')
LABEL=re.compile(r'^(Benefits|Liabilities)\s*:?$', re.I)

records=[]; cur_pat=None; cur_sub=None; cur_group=None; blocks=None

for i,ptxt in enumerate(pages):
    pg=FIRST+i
    if pg>LAST: break
    heads=list(by_page.get(pg,[]))
    caps=[norm(c) for c in captions.get(str(pg),[])]
    lines=[l for l in ptxt.split('\n') if not DROP.match(l.strip())]
    for j,l in enumerate(lines):          # drop running head
        if l.strip(): lines=lines[j+1:]; break
    for l in lines:
        if not l.strip(): continue
        ind=len(l)-len(l.lstrip()); s=norm(l)
        if s.isdigit(): continue
        if heads and (s==heads[0][1] or unlig(s)==heads[0][1]):
            kind,txt=heads.pop(0)
            if kind=='GROUP': cur_group=txt; cur_pat=None; cur_sub=None
            elif kind=='PATTERN':
                cur_pat=txt; cur_sub=None
                records.append({'name':txt,'group':cur_group,'page':pg,'sections':{}})
            else:
                cur_sub=txt; records[-1]['sections'][cur_sub]=[]
            blocks=records[-1]['sections'].get(cur_sub) if (cur_pat and cur_sub) else None
            continue
        if ind>=40: continue
        if FIG.match(s) and any(c.startswith(s[:40]) or s.startswith(c[:40]) for c in caps): continue
        if blocks is None: continue
        if BULLET.match(s) or LABEL.match(s):
            blocks.append(s)
        elif 20<=ind<=24 and blocks and not BULLET.match(blocks[-1]):
            blocks.append(s)
        elif not blocks:
            blocks.append(s)
        else:
            blocks[-1]=blocks[-1]+' '+s

for r in records:
    for k,v in list(r['sections'].items()):
        r['sections'][k]=[norm(re.sub(r'(\w)- (\w)', r'\1\2', p)) for p in v if p.strip()]
records=[r for r in records if r['sections']]
json.dump(records,open(SP+'/patterns.json','w'),indent=1)
from collections import Counter
print('records',len(records))
print('section histogram',sorted(Counter(len(r['sections']) for r in records).items()))
print('missing sections:',[(r['name'],sorted(set(['Context','Problem','Example','Forces','Solution','Consequences','Example Resolved','Known Uses','Related Patterns'])-set(r['sections']))) for r in records if len(r['sections'])<9][:15])
