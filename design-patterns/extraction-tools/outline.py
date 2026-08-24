import re, json
SP='/private/tmp/claude-501/-Users-amandachessell-Code-ODPi-egeria-docs-egeria-docs/4ede8936-3269-4824-8f08-06b13d6924bd/scratchpad'
xml=open(SP+'/poim_body.xml',encoding='utf-8',errors='replace').read()
fonts={m.group(1):(int(m.group(2)),m.group(3)) for m in re.finditer(r'<fontspec id="(\d+)" size="(\d+)" family="([^"]+)"',xml)}
SUBS={'Context','Problem','Example','Forces','Solution','Consequences','Example Resolved','Known Uses','Related Patterns'}
out=[]
for pm in re.finditer(r'<page number="(\d+)"(.*?)</page>',xml,re.S):
    pg=int(pm.group(1))
    for m in re.finditer(r'<text top="(\d+)"[^>]*font="(\d+)">(.*?)</text>', pm.group(2), re.S):
        sz,fam=fonts[m.group(2)]
        if 'HelveticaNeue' not in fam or 'Bd' not in fam: continue
        t=re.sub(r'<[^>]+>','',m.group(3))
        t=re.sub(r'\s+',' ',t).strip()
        if not t or t.isdigit(): continue
        if sz==18: out.append((pg,'GROUP',t))
        elif sz==17 and t!='H A P T E R': out.append((pg,'PATTERN',t))
        elif sz==15: out.append((pg,'SUB' if t in SUBS else 'SUB?',t))
json.dump(out,open(SP+'/outline.json','w'))
print('groups',sum(1 for x in out if x[1]=='GROUP'))
print('patterns',sum(1 for x in out if x[1]=='PATTERN'))
print('subs',sum(1 for x in out if x[1]=='SUB'))
print('other subs',sorted(set(x[2] for x in out if x[1]=='SUB?'))[:60])
