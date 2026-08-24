import re, json, os
SP='/private/tmp/claude-501/-Users-amandachessell-Code-ODPi-egeria-docs-egeria-docs/4ede8936-3269-4824-8f08-06b13d6924bd/scratchpad'
OUT='/Users/amandachessell/Code/ODPi/egeria-docs/egeria-docs/site/snippets/design-patterns'
pats=json.load(open(SP+'/patterns.json'))
patlets=json.load(open(SP+'/patlets.json'))
outline=json.load(open(SP+'/outline.json'))
supp=json.load(open(SP+'/supplement.json'))

def unlig(t): return re.sub(r'\b([A-Za-z]*?(?:ffi|ffl|fi|fl|ff)) ([a-z]{2,})\b', r'\1\2', t)
def key(s): return re.sub(r"[^a-z0-9]","",s.lower())

# ---------- name fixes on patlets ----------
fixed=[]
for p in patlets:
    nm=supp['name_fixes'].get(p['name'], p['name'])
    if nm is None: continue
    p['name']=nm; fixed.append(p)
patlets=fixed
plby={}
for p in patlets: plby.setdefault(key(p['name']),p)

# ---------- chapters / groups ----------
CH=[(99,3,'People and Organizations'),(129,4,'Information Architecture'),(265,5,'Information at Rest'),
    (425,6,'Information in Motion'),(479,7,'Information Processing'),(563,8,'Information Protection'),
    (607,9,'Solutions for Information Management')]
def chap(pg):
    r=CH[0]
    for c in CH:
        if pg>=c[0]: r=c
    return r

fullnames={key(p['name']) for p in pats}
topgroup={}; cur=None
for pg,kind,txt in outline:
    if pg>672: break
    t=unlig(txt)
    if kind in ('GROUP','PATTERN') and t.endswith(' Patterns'):
        stem=t[:-len(' Patterns')]
        if key(stem) in fullnames: cur=stem
    elif kind=='PATTERN':
        topgroup.setdefault(key(t),cur)

# ---------- assemble the pattern catalogue ----------
catalog={}   # key -> record
for p in pats:
    k=key(p['name'])
    catalog[k]={'name':p['name'],'page':p['page'],'chapter':chap(p['page']),
                'group':topgroup.get(k),'sections':p['sections'],
                'patlet':plby.get(k),'full':True}
for p in patlets:
    k=key(p['name'])
    if k in catalog: continue
    catalog[k]={'name':p['name'],'page':p['page'],'chapter':chap(p['page']),
                'group':topgroup.get(k),'sections':{},'patlet':p,'full':False}
for e in supp['extra']:
    k=key(e['name'])
    if k in catalog: continue
    catalog[k]={'name':e['name'],'page':e['page'],'chapter':chap(e['page']),
                'group':e['group'],'sections':{},
                'patlet':{'problem':e['problem'],'solution':e['solution']},'full':False}

# patlet-only patterns inherit their group from the surrounding section
GROUPFIX={'informationworker':'Information User','informationsteward':'Information User',
 'informationgovernor':'Information User','informationowner':'Information User',
 'informationauditor':'Information User','dataqualityanalyst':'Information User',
 'businessanalyst':'Information User','datascientist':'Information User',
 'infrastructureoperator':'Information User',
 'sourcespecificpayload':'Information Element','targetspecificpayload':'Information Element',
 'canonicalbasedpayload':'Information Element',
 'completecoverage':'Information Collection','corecoverage':'Information Collection',
 'extendedcoverage':'Information Collection','localcoverage':'Information Collection',
 'staticstructure':'Information Entry','dynamicstructure':'Information Entry',
 'entrylevelstructure':'Information Entry','taggedmediastructure':'Information Entry',
 'locallocking':'Information Entry','distributedlocking':'Information Entry',
 'optimisticlocking':'Information Entry','lifecyclestates':'Information Entry',
 'uniqueentries':'Information Entry','deferredupdate':'Information Entry',
 'softdelete':'Information Entry','proxy':'Information Entry','provenance':'Information Entry',
 'historicalvalues':'Information Entry','relationships':'Information Entry',
 'informationcrawlingprocess':'Information Process','informationindexingprocess':'Information Process',
 'informationsearchprocess':'Information Process',
 'identityverification':'Information Guard','identitypropagation':'Information Guard',
 'trustednode':'Information Guard','functioncentricaccess':'Information Guard',
 'datacentricaccess':'Information Guard','separationofduties':'Information Guard',
 'encryptdata':'Information Guard','maskdata':'Information Guard','anonymizedata':'Information Guard',
 'physicalsecurityzone':'Information Guard','collectioncontrol':'Information Guard',
 'interactionanalysis':'Information Guard',
 'subjectareaprobe':'Information Probe','profilingruleprobe':'Information Probe',
 'informationflowprobe':'Information Probe','entryuniquenessprobe':'Information Probe',
 'accessauditingprobe':'Information Probe','operationalhealthprobe':'Information Probe',
 'sampledataprobe':'Information Probe','environmentprobe':'Information Probe'}
for k,g in GROUPFIX.items():
    if k in catalog and not catalog[k]['group']: catalog[k]['group']=g

json.dump({k:{kk:vv for kk,vv in v.items() if kk!='sections'} for k,v in catalog.items()},
          open(SP+'/catalog_meta.json','w'),indent=1)
print('catalog size',len(catalog))
print('full',sum(1 for v in catalog.values() if v['full']),'patlet-only',sum(1 for v in catalog.values() if not v['full']))
nogroup=[v['name'] for v in catalog.values() if not v['group']]
print('no group (%d):'%len(nogroup),nogroup)

# =====================================================================
# small-caps reference detection
# =====================================================================
NAMEIDX={}
for k,v in catalog.items():
    toks=[t for t in re.split(r'[^A-Za-z0-9]+', v['name']) if t]
    NAMEIDX[tuple(t.upper() for t in toks)]=k
MAXLEN=max(len(t) for t in NAMEIDX)
STOP={'MCHS','IT','ETL','SQL','XML','JSON','API','APIS','CRM','ERP','UML','IBM','OK'}
RUN=re.compile(r"\b[A-Z][A-Z'\-]+(?:\s+[A-Z][A-Z'\-]+)*\b")

def refs(text):
    found=[]
    for m in RUN.finditer(text):
        toks=[t for t in re.split(r"[^A-Z']+", m.group(0)) if len(t)>=2 and t not in STOP]
        i=0
        while i<len(toks):
            hit=None
            for n in range(min(MAXLEN,len(toks)-i),0,-1):
                cand=tuple(toks[i:i+n])
                for c in (cand, cand[:-1]+(cand[-1].rstrip('S'),), cand[:-1]+(cand[-1]+'S',)):
                    if c in NAMEIDX and (n>1 or len(c[0])>=5):
                        hit=(NAMEIDX[c],n); break
                if hit: break
            if hit:
                if hit[0] not in found: found.append(hit[0])
                i+=hit[1]
            else: i+=1
    return found

# =====================================================================
# section -> attribute helpers
# =====================================================================
def smallcaps_to_title(text):
    """The book sets pattern names in small capitals; render them in title case."""
    def fix(m):
        run=m.group(0)
        toks=[t for t in re.split(r"\s+", run) if t]
        if len(toks)==1 and (toks[0] in STOP or len(toks[0])<5): return run
        if all(t in STOP for t in toks): return run
        return ' '.join(t if t in STOP else
                        '-'.join(w.capitalize() for w in t.split('-')) for t in toks)
    return RUN.sub(fix, text)

def debullet(s):
    return re.sub(r'^(•\s*|\d+\.\s+)','',s).strip()
def is_bullet(s):
    return bool(re.match(r'^(•|\d+\.\s)', s))

def consequences(blocks):
    ben=[]; lia=[]; mode=None; loose=[]
    for b in blocks:
        t=debullet(b)
        m=re.match(r'^(Benefits?|Liabilities?)\s*[:—–-]\s*(.*)$', t, re.I)
        if m:
            mode='b' if m.group(1).lower().startswith('benefit') else 'l'
            rest=m.group(2).strip()
            if rest: (ben if mode=='b' else lia).append(rest)
            continue
        if mode=='b': ben.append(t)
        elif mode=='l': lia.append(t)
        else: loose.append(t)
    if loose and not ben and not lia: ben=loose
    elif loose: ben=loose+ben
    return ben,lia

def paras(blocks):
    out=[]
    for b in blocks:
        b=smallcaps_to_title(b)
        m=re.match(r'^(\d+)\.\s+(.*)$', b, re.S)
        if m: out.append(m.group(1)+'. '+m.group(2).strip())
        elif is_bullet(b): out.append('- '+debullet(b))
        else: out.append(b)
    # blank line between blocks, except between consecutive list items
    res=[]
    for i,t in enumerate(out):
        if i and not (re.match(r'^(- |\d+\. )',t) and re.match(r'^(- |\d+\. )',out[i-1])):
            res.append('')
        res.append(t)
    return res

def listify(blocks):
    out=[]
    for b in blocks:
        t=debullet(b)
        if t: out.append('- '+re.sub(r'\s+',' ',smallcaps_to_title(t)))
    return out

LEGAL=("Extracted from *Patterns of Information Management* by Mandy Chessell and Harald C. Smith, "
       "IBM Press, 2013, ISBN-13: 978-0-13-315550-1, Chapter {ch}, \"{title}\".  "
       "© Copyright 2013 by International Business Machines Corporation.  All rights reserved.")

def block(title, body):
    if not body: return ''
    if isinstance(body,list): body='\n'.join(body)
    return '### %s\n\n%s\n\n' % (title, body.strip())

def qn(name): return 'DesignPattern::'+name

def render(rec):
    s=rec['sections']; pl=rec['patlet']; chn,cht=rec['chapter'][1],rec['chapter'][2]
    desc=''
    if pl and pl.get('solution'): desc=smallcaps_to_title(pl['solution'])
    elif s.get('Solution'): desc=smallcaps_to_title(s['Solution'][0])
    prob=paras(s.get('Problem',[]))
    if not prob and pl and pl.get('problem'): prob=[smallcaps_to_title(pl['problem'])]
    ben,lia=consequences([smallcaps_to_title(x) for x in s.get('Consequences',[])])
    out=['## Create Design Pattern\n> Create or updates a design pattern.\n\n']
    out.append(block('Display Name', rec['name']))
    out.append(block('Qualified Name', qn(rec['name'])))
    out.append(block('Category', rec['group']+' Patterns'))
    out.append(block('Description', desc))
    out.append(block('Legal', LEGAL.format(ch=chn,title=cht)))
    out.append(block('Context', paras(s.get('Context',[]))))
    out.append(block('Problem Statement', prob))
    out.append(block('Problem Example', paras(s.get('Example',[]))))
    out.append(block('Forces', listify(s.get('Forces',[]))))
    soldesc=paras(s.get('Solution',[]))
    if not soldesc and pl and pl.get('solution'): soldesc=[smallcaps_to_title(pl['solution'])]
    out.append(block('Solution Description', soldesc))
    out.append(block('Solution Example', paras(s.get('Example Resolved',[]))))
    out.append(block('Benefits', ['- '+b for b in ben]))
    out.append(block('Liabilities', ['- '+l for l in lia]))
    out.append(block('Usage', paras(s.get('Known Uses',[]))))
    kw=['- Patterns of Information Management','- '+rec['group'],'- '+cht]
    out.append(block('Search Keywords', kw))
    out.append(block('Version Identifier','1.0'))
    out.append(block('Status','ACTIVE'))
    return ''.join(out)+'____\n\n'

# =====================================================================
# links
# =====================================================================
def sentences(blocks):
    out=[]
    for b in blocks:
        for s in re.split(r'(?<=[.?!])\s+(?=[A-Z“"(])', debullet(b)):
            s=s.strip()
            if s: out.append(s)
    return out

def ref_sentences(blocks):
    """map referenced pattern key -> first sentence mentioning it"""
    res={}
    for s in sentences(blocks):
        for k in refs(s):
            res.setdefault(k, s)
    return res

leads={}
for k,v in catalog.items():
    if v['group'] and key(v['group'])==k: leads[key(v['group'])]=k

spec=[]      # (general, specialized)
for k,v in sorted(catalog.items(), key=lambda x:(x[1]['page'])):
    lk=leads.get(key(v['group'] or ''))
    if lk and lk!=k: spec.append((lk,k))
specset={(a,b) for a,b in spec}

nested=[]; related=[]
seen_rel=set()
for k,v in sorted(catalog.items(), key=lambda x:(x[1]['page'])):
    sec=v['sections']
    for t,s in ref_sentences(sec.get('Solution',[])).items():
        if t==k or (k,t) in specset or (t,k) in specset: continue
        nested.append((k,t,smallcaps_to_title(s)))
    for t,s in ref_sentences(sec.get('Related Patterns',[])).items():
        if t==k: continue
        pair=tuple(sorted((k,t)))
        if pair in seen_rel or (k,t) in specset or (t,k) in specset: continue
        seen_rel.add(pair)
        related.append((k,t,smallcaps_to_title(s)))
nestset={(a,b) for a,b,_ in nested}
related=[(a,b,s) for a,b,s in related if (a,b) not in nestset and (b,a) not in nestset]

print('links: specialized=%d nested=%d related=%d' % (len(spec),len(nested),len(related)))

def trim(s,n=600):
    s=re.sub(r'\s+',' ',s).strip()
    return s if len(s)<=n else s[:n].rsplit(' ',1)[0]+'...'

def linkblock(cmd, desc, fields, label, text):
    o=['## %s\n> %s\n\n' % (cmd,desc)]
    for t,v in fields: o.append(block(t,v))
    o.append(block('Label',label))
    o.append(block('Description',trim(text)))
    return ''.join(o)+'____\n\n'

# =====================================================================
# emit files
# =====================================================================
HDR=("<!-- SPDX-License-Identifier: CC-BY-4.0 -->\n"
     "<!-- Copyright Contributors to the ODPi Egeria project. -->\n\n")
SLUG={3:'people-and-organizations',4:'information-architecture',5:'information-at-rest',
      6:'information-in-motion',7:'information-processing',8:'information-protection',
      9:'solutions-for-information-management'}
INTRO=("**{title}**\n\n"
 "Dr.Egeria commands for the design patterns in Chapter {n}, \"{title}\", of *Patterns of\n"
 "Information Management* by Mandy Chessell and Harald C. Smith (IBM Press, 2013).\n"
 "The book sets each pattern's identifier in small capitals; those small-capital names are used\n"
 "here as the display names, and as the reference names in "
 "[poim-pattern-links.md](poim-pattern-links.md).\n"
 "{note}\n____\n\n")
PATLET_NOTE=("\nPatterns marked as summarised below are described in the book by a patlet table only\n"
 "(icon, name, problem, solution) rather than a full pattern description, so they carry a\n"
 "Description, Problem Statement and Solution Description but no Context, Forces, examples\n"
 "or consequences.\n")

files={}
for n in sorted(SLUG):
    recs=[v for v in catalog.values() if v['chapter'][1]==n]
    recs.sort(key=lambda r:(r['page'],r['name']))
    title=[c[2] for c in CH if c[1]==n][0]
    note=PATLET_NOTE if any(not r['full'] for r in recs) else ''
    body=HDR+INTRO.format(title=title,n=n,note=note)+''.join(render(r) for r in recs)
    files['poim-ch%d-%s.md'%(n,SLUG[n])]=body

# links file
lp=[HDR,
 "**Links between the Patterns of Information Management**\n\n"
 "Three kinds of link are generated from the book:\n\n"
 "- **Specialized** — every pattern group has a *lead pattern* that \"describes the core principles\n"
 "  and capabilities of the group\"; the other patterns in the group \"enhance one or more\n"
 "  characteristics of the lead pattern to support a more specialized situation\" (Chapter 1).\n"
 "- **Nested** — a pattern used as a component in the solution of another pattern.  Chapter 1:\n"
 "  \"a pattern can be used as a component in the solution described by another pattern.  When\n"
 "  this occurs, the icon of the pattern is used in the solution diagram of the consuming pattern.\"\n"
 "  These are taken from the small-capital references in each pattern's Solution section.\n"
 "- **Related** — the cross-references in each pattern's *Related Patterns* section.\n\n"
 "____\n\n"]
for a,b in spec:
    lp.append(linkblock('Link Specialized Design Patterns','Nest specialized design patterns.',
        [('General Design Pattern',qn(catalog[a]['name'])),
         ('Specialized Design Pattern',qn(catalog[b]['name']))],
        'Pattern Group',
        '%s is a member of the %s pattern group, whose lead pattern is %s.'
        % (catalog[b]['name'],catalog[b]['group'],catalog[a]['name'])))
for a,b,s in nested:
    lp.append(linkblock('Link Nested Design Patterns','Nest two design patterns.',
        [('Parent Design Pattern',qn(catalog[a]['name'])),
         ('Nested Design Pattern',qn(catalog[b]['name']))],
        'Solution Component', s))
for a,b,s in related:
    lp.append(linkblock('Link Related Design Patterns','Link related design patterns.',
        [('Design Pattern 1',qn(catalog[a]['name'])),
         ('Design Pattern 2',qn(catalog[b]['name']))],
        'Related Pattern', s))
files['poim-pattern-links.md']=''.join(lp)

for fn,body in files.items():
    open(os.path.join(OUT,fn),'w').write(body)
    print('%-52s %8d bytes  %4d commands' % (fn,len(body),body.count('\n## ')+body.startswith('## ')))
