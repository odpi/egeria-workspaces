import re, json
from collections import Counter, defaultdict
SP='/private/tmp/claude-501/-Users-amandachessell-Code-ODPi-egeria-docs-egeria-docs/4ede8936-3269-4824-8f08-06b13d6924bd/scratchpad'
xml=open(SP+'/gloss.xml',encoding='utf-8',errors='replace').read()
fonts={m.group(1):(int(m.group(2)),m.group(3).split('+')[-1]) for m in re.finditer(r'<fontspec id="(\d+)" size="(\d+)" family="([^"]+)"',xml)}
def clean(t): return re.sub(r'<[^>]+>','',t).replace('’',"'").replace('“','"').replace('”','"')
def join_lines(els):
    lines=defaultdict(list)
    for e in els: lines[e['top']].append(e)
    res=''
    for top in sorted(lines):
        s=''.join(x['raw'] for x in sorted(lines[top],key=lambda x:x['left'])).strip()
        if not s: continue
        if res.endswith('-'): res=res[:-1]+s
        elif res: res=res+' '+s
        else: res=s
    return re.sub(r'\s+',' ',res).strip()

rows=[]
for pm in re.finditer(r'<page number="(\d+)"(.*?)</page>',xml,re.S):
    els=[]
    for m in re.finditer(r'<text top="(\d+)" left="(\d+)"[^>]*font="(\d+)">(.*?)</text>', pm.group(2), re.S):
        sz,fam=fonts[m.group(3)]
        if not fam.startswith('TimesLTStd') or sz!=14: continue
        raw=clean(m.group(4))
        if raw.strip(): els.append({'top':int(m.group(1)),'left':int(m.group(2)),'raw':raw})
    if len(els)<6: continue
    cnt=Counter(e['left'] for e in els); cols=[]
    for l in sorted(cnt):
        if cnt[l]>=3 and not (cols and l-cols[-1]<=12): cols.append(l)
    if len(cols)<3: continue
    topic,desc,rel=cols[0],cols[1],cols[-1]
    def colof(e):
        c=cols[0]
        for m_ in cols:
            if e['left']>=m_-6: c=m_
        return c
    tops=sorted(set(e['top'] for e in els if colof(e)==topic))
    desctops=set(e['top'] for e in els if colof(e)==desc)
    probstarts=sorted(set(e['top'] for e in els if colof(e)==desc
                          and e['raw'].startswith(' ') and len(e['raw'].strip())>3))
    starts=sorted(set(probstarts))
    b=starts+[10**6]
    for i,st in enumerate(starts):
        en=b[i+1]; buck={topic:[],desc:[],rel:[]}
        for e in els:
            if st-2<=e['top']<en-2:
                c=colof(e)
                if c in buck: buck[c].append(e)
        rows.append({'topic':join_lines(buck[topic]),'desc':join_lines(buck[desc]),'rel':join_lines(buck[rel])})
rows=[r for r in rows if r['topic'] and r['topic'] not in ('Topic',) and len(r['desc'])>10]
json.dump(rows,open(SP+'/glossary_rows.json','w'),indent=1)
print('terms',len(rows))
for r in rows[:4]: print(' ',r['topic'],'|',r['desc'][:60],'|',r['rel'])
