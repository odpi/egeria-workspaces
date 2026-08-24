import re, json, os
exec(open('/private/tmp/claude-501/-Users-amandachessell-Code-ODPi-egeria-docs-egeria-docs/4ede8936-3269-4824-8f08-06b13d6924bd/scratchpad/build.py').read())
rows=json.load(open(SP+'/glossary_rows.json'))
def fixcaps(s):
    for _ in range(6): s=re.sub(r'(?<![A-Z])([A-Z]) ([A-Z]{2,})', r'\1\2', s)
    return re.sub(r'\s+',' ',s).strip()

ALIAS={'informationanalyticsnode':'informationanalysisnode','lookuptables':'lookuptablenode',
       'informationreporting':'informationreportingprocess','informationcontext':None,
       'informationqualityremediationprocess':'informationremediationprocess',
       'informationreengineeringsteps':'informationreengineeringstep',
       'archivingprocess':'informationarchivingprocess','evergreeningprocess':'informationevergreeningprocess',
       'informationanalytics':'informationanalysisnode',
       'informationcontent':'informationcontentnode','informationmirrornode':'informationmirrorstore',
       'operationalstatusnode':'operationalstatusstore'}
unres=[]
def resolve(rel):
    r=fixcaps(rel); out=[]
    for part in re.split(r'\s*,\s*', r):
        part=part.strip()
        if not part: continue
        got=refs(part)
        if got:
            for g in got:
                if g not in out: out.append(g)
        else:
            k=key(part)
            k=ALIAS.get(k,k)
            if k and k in catalog and k not in out: out.append(k)
            elif part: unres.append(part)
    return out

GSLUG='PatternsOfInformationManagement'
LEGAL_G=("Extracted from the Glossary (Appendix 1) of *Patterns of Information Management* by "
 "Mandy Chessell and Harald C. Smith, IBM Press, 2013, ISBN-13: 978-0-13-315550-1.  "
 "© Copyright 2013 by International Business Machines Corporation.  All rights reserved.")

o=[HDR,
 "**Glossary of the Patterns of Information Management**\n\n"
 "Appendix 1 of *Patterns of Information Management* is a three-column table of Topic,\n"
 "Description and Related Patterns.  Each topic becomes a glossary term; the Related Patterns\n"
 "column becomes a `Link Semantic Assignment` onto the design pattern created by the chapter\n"
 "files in this directory.\n\n____\n\n"]
o.append('## Create Glossary\n> Creates or updates a glossary — a collection of related terms for a specific domain or purpose.\n\n')
o.append(block('Display Name','Glossary for the Patterns of Information Management'))
o.append(block('Qualified Name','Glossary::'+GSLUG))
o.append(block('Language','English'))
o.append(block('Category','Patterns of Information Management'))
o.append(block('Description','The terminology used by the Patterns of Information Management pattern language, as defined in Appendix 1 of the book.  Each term is linked to the design patterns that work with the concept it names.'))
o.append(block('Usage','Use this glossary to interpret the design patterns loaded from *Patterns of Information Management*.'))
o.append(block('Purpose','To define the vocabulary shared by the 232 design patterns in the Patterns of Information Management pattern language.'))
o.append(block('Legal',LEGAL_G))
o.append(block('Search Keywords',['- Patterns of Information Management','- Information Management','- Information Architecture']))
o.append(block('Authors',['- Mandy Chessell','- Harald C. Smith']))
o.append(block('Version Identifier','1.0'))
o.append(block('Status','ACTIVE'))
o.append('____\n\n')

links=[]
nterm=0
for r in rows:
    topic=re.sub(r'\s+',' ',r['topic']).strip()
    if not topic: continue
    nterm+=1
    tqn='GlossaryTerm::%s::%s'%(GSLUG,topic)
    o.append('## Create Glossary Term\n> Creates or updates a glossary term — a concept, phrase, or word defined within a glossary.\n\n')
    o.append(block('Display Name',topic))
    o.append(block('Glossary Name',['- Glossary::'+GSLUG]))
    o.append(block('Qualified Name',tqn))
    o.append(block('Summary',smallcaps_to_title(r['desc'])))
    o.append(block('Category','Patterns of Information Management'))
    o.append(block('Legal',LEGAL_G))
    rel=resolve(r['rel'])
    if rel:
        names=[catalog[k]['name'] for k in rel]
        o.append(block('Usage','Used by the following design pattern%s: %s.'
                       % ('' if len(names)==1 else 's', ', '.join(names))))
    o.append(block('Version Identifier','1.0'))
    o.append(block('Status','ACTIVE'))
    o.append('____\n\n')
    for k in rel:
        links.append((tqn,topic,k))

for tqn,topic,k in links:
    o.append('## Link Semantic Assignment\n> Create a SemanticAssignment relationship (0370) between an existing element and a glossary term, indicating the data matches the term meaning.\n\n')
    o.append(block('Target Element',qn(catalog[k]['name'])))
    o.append(block('Glossary Term',tqn))
    o.append(block('Label','Glossary Definition'))
    o.append(block('Description','The %s design pattern works with the concept named by the glossary term "%s".'%(catalog[k]['name'],topic)))
    o.append('____\n\n')

body=''.join(o)
open(os.path.join(OUT,'poim-glossary.md'),'w').write(body)
print('terms',nterm,'semantic assignments',len(links))
print('unresolved pattern references:',sorted(set(unres)))
