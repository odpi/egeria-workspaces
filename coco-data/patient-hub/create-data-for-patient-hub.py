
import random
import uuid
import datetime
import os

random.seed(42)

# ── helpers ──────────────────────────────────────────────────────────────────
def uid():
    return str(uuid.uuid4())

def q(s):
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"

def qd(dt):
    if dt is None:
        return 'NULL'
    return "'" + dt.strftime('%Y-%m-%d %H:%M:%S+00') + "'"

def qdate(d):
    return "'" + d.strftime('%Y-%m-%d') + "'"

def rand_date(start, end):
    delta = end - start
    return start + datetime.timedelta(days=random.randint(0, delta.days))

def rand_ts(start, end):
    delta = int((end - start).total_seconds())
    return start + datetime.timedelta(seconds=random.randint(0, delta))

DB_START = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
DB_END   = datetime.datetime(2024, 12, 31, tzinfo=datetime.timezone.utc)

# ── file path helpers ─────────────────────────────────────────────────────────
IMAGE_BASE = '/data/hampton_hospital/images'
def img_path(patient_nhs, modality, study_date, seq):
    d = study_date.strftime('%Y/%m/%d')
    ext = {'CT':'dcm','MR':'dcm','CR':'dcm','DX':'dcm','US':'dcm',
           'PT':'dcm','NM':'dcm','MG':'dcm'}.get(modality,'dcm')
    return f"{IMAGE_BASE}/{modality}/{patient_nhs}/{d}/{seq:04d}.{ext}"

# ── departments ───────────────────────────────────────────────────────────────
DEPT_ID = {
    'oncology':   uid(),
    'surgery':    uid(),
    'haematology':uid(),
    'radiology':  uid(),
}
DEPT_ROWS = [
    (DEPT_ID['oncology'],    'Oncology',    'ONC',  'Main Building, Floor 2'),
    (DEPT_ID['surgery'],     'Surgery',     'SURG', 'Main Building, Floor 3'),
    (DEPT_ID['haematology'], 'Haematology', 'HAEM', 'Main Building, Floor 1'),
    (DEPT_ID['radiology'],   'Radiology',   'RAD',  'Imaging Wing, Floor 1'),
]

# ── staff ─────────────────────────────────────────────────────────────────────
# 15 staff across 4 departments, named + typed
STAFF = [
    # id, first, last, role, dept_key
    (uid(),'Grant',   'Able',      'Consultant',   'oncology'),
    (uid(),'Rachel',  'Holt',      'Consultant',   'oncology'),
    (uid(),'Marcus',  'Leigh',     'Consultant',   'haematology'),
    (uid(),'Julie',   'Stitched',  'Surgeon',      'surgery'),
    (uid(),'Omar',    'Farhan',    'Surgeon',      'surgery'),
    (uid(),'Claire',  'Bowden',    'Registrar',    'oncology'),
    (uid(),'Samuel',  'Okafor',    'Registrar',    'haematology'),
    (uid(),'Angela',  'Cummings',  'Nurse',        'oncology'),
    (uid(),'Tanya',   'Marsh',     'Nurse',        'oncology'),
    (uid(),'Priya',   'Nair',      'Nurse',        'haematology'),
    (uid(),'Leon',    'Frost',     'Nurse',        'surgery'),
    (uid(),'Wendy',   'Crane',     'Nurse',        'surgery'),
    (uid(),'Patrick', 'Doran',     'Radiologist',  'radiology'),
    (uid(),'Suki',    'Tanaka',    'Radiographer', 'radiology'),
    (uid(),'Daniel',  'Mwangi',    'Pharmacist',   'oncology'),
]
STAFF_IDS = [s[0] for s in STAFF]

# system actor for bootstrapping
SYSTEM_CLINICIAN = STAFF[0][0]  # Grant Able creates initial records

# ── patients ──────────────────────────────────────────────────────────────────
FIRST_NAMES_M = ['James','Oliver','Harry','Noah','George','Charlie','Jack','Alfie','Freddie','Archie',
                 'Henry','Thomas','William','Edward','Samuel','Benjamin','Michael','Daniel','Matthew','Ryan']
FIRST_NAMES_F = ['Olivia','Amelia','Isla','Sophia','Emily','Grace','Lily','Ella','Mia','Isabella',
                 'Poppy','Ava','Evie','Charlotte','Sophie','Hannah','Lucy','Freya','Zoe','Chloe']
LAST_NAMES    = ['Smith','Jones','Williams','Taylor','Brown','Davies','Evans','Wilson','Thomas','Roberts',
                 'Johnson','Lewis','Walker','Robinson','Wood','Thompson','White','Hughes','Martin','Clarke',
                 'Jackson','Harris','Turner','Cooper','Hill','Ward','Morris','Rogers','Cook','Patterson',
                 'Bailey','Bell','Cox','Howard','Butler','Barnes','Henderson','Fisher','Ross','Richards']
BLOOD_TYPES = ['A+','A-','B+','B-','AB+','AB-','O+','O-']

CANCER_TYPES = [
    'Non-Hodgkin lymphoma','Hodgkin lymphoma','Acute myeloid leukaemia',
    'Chronic lymphocytic leukaemia','Breast cancer','Colorectal cancer',
    'Lung cancer','Ovarian cancer','Prostate cancer','Cervical cancer',
]

ALLERGIES_LIST = [
    None, None, None,  # most patients have no recorded allergy
    'Penicillin', 'Sulfonamides', 'Aspirin', 'Codeine', 'Latex',
    'Iodine contrast', 'Methotrexate',
]

patients = []
used_nhs = set()
used_names = set()

def gen_nhs():
    while True:
        n = ''.join([str(random.randint(0,9)) for _ in range(10)])
        if n not in used_nhs:
            used_nhs.add(n)
            return n

for i in range(100):
    sex = random.choice(['Male','Female'])
    fn  = random.choice(FIRST_NAMES_M if sex=='Male' else FIRST_NAMES_F)
    ln  = random.choice(LAST_NAMES)
    # ensure unique full names
    while (fn,ln) in used_names:
        fn = random.choice(FIRST_NAMES_M if sex=='Male' else FIRST_NAMES_F)
        ln = random.choice(LAST_NAMES)
    used_names.add((fn,ln))

    dob = rand_date(datetime.date(1945,1,1), datetime.date(1985,12,31))
    nhs = gen_nhs()
    bt  = random.choice(BLOOD_TYPES)
    allergy = random.choice(ALLERGIES_LIST)
    cancer  = random.choice(CANCER_TYPES)

    # treatment window: 9 months to 2 years, starting somewhere in first 3 years
    tx_start = rand_ts(DB_START, datetime.datetime(2023,3,1,tzinfo=datetime.timezone.utc))
    tx_months = random.randint(9, 24)
    tx_end   = tx_start + datetime.timedelta(days=30*tx_months)
    if tx_end > DB_END:
        tx_end = DB_END

    patients.append({
        'id': uid(), 'nhs': nhs, 'first': fn, 'last': ln,
        'dob': dob, 'sex': sex, 'bt': bt, 'allergy': allergy,
        'cancer': cancer, 'tx_start': tx_start, 'tx_end': tx_end,
    })

# ── build SQL ─────────────────────────────────────────────────────────────────
lines = []
A = lines.append

A("-- ============================================================")
A("-- Hampton Hospital – Patient Record Data Hub")
A("-- Sample data load: 5-year oncology dataset")
A("-- Generated for testing purposes")
A("-- ============================================================")
A("")
A("BEGIN;")
A("")
A("-- ── Session context (system bootstrap clinician) ─────────────")
A(f"SET LOCAL app.current_clinician_id = '{SYSTEM_CLINICIAN}';")
A("SET LOCAL app.ip_address            = '10.0.0.1';")
A("SET LOCAL app.application_name      = 'DataLoad';")
A("")

# ── departments (head_clinician_id set later via UPDATE) ──────────────────────
A("-- ── Departments ──────────────────────────────────────────────")
for dept_id, dname, dcode, dloc in DEPT_ROWS:
    A(f"INSERT INTO department (department_id, name, code, location, created_by, created_at)")
    A(f"  VALUES ({q(dept_id)}, {q(dname)}, {q(dcode)}, {q(dloc)}, {q(SYSTEM_CLINICIAN)}, '2019-12-01 08:00:00+00');")
A("")

# ── clinicians ────────────────────────────────────────────────────────────────
A("-- ── Clinicians ───────────────────────────────────────────────")
for cid, cfirst, clast, crole, cdept in STAFF:
    dept_id = DEPT_ID[cdept]
    gmc = str(random.randint(1000000,9999999)) if crole in ('Consultant','Surgeon','Registrar','Radiologist') else None
    A(f"INSERT INTO clinician (clinician_id, first_name, last_name, role, department_id, gmc_number, created_by, created_at)")
    A(f"  VALUES ({q(cid)}, {q(cfirst)}, {q(clast)}, {q(crole)}, {q(dept_id)}, {q(gmc)}, {q(SYSTEM_CLINICIAN)}, '2019-12-01 08:00:00+00');")
A("")

# set department heads
dept_heads = {
    'oncology':    STAFF[0][0],    # Grant Able
    'surgery':     STAFF[3][0],    # Julie Stitched
    'haematology': STAFF[2][0],    # Marcus Leigh
    'radiology':   STAFF[12][0],   # Patrick Doran
}
A("-- ── Department heads ─────────────────────────────────────────")
for dkey, hid in dept_heads.items():
    A(f"UPDATE department SET head_clinician_id = {q(hid)}, updated_by = {q(SYSTEM_CLINICIAN)}, updated_at = '2019-12-15 08:00:00+00'")
    A(f"  WHERE department_id = {q(DEPT_ID[dkey])};")
A("")

# ── patients ──────────────────────────────────────────────────────────────────
A("-- ── Patients ─────────────────────────────────────────────────")
for p in patients:
    postcode_letters = random.choice(['SW','NW','SE','NE','WC','EC','W','N','S','E'])
    postcode = f"{postcode_letters}{random.randint(1,20)} {random.randint(1,9)}{random.choice('ABCDEFGHJKLMNPQRSTUVWXY')}{random.choice('ABCDEFGHJKLMNPQRSTUVWXY')}"
    phone = f"07{random.randint(100,999)} {random.randint(100000,999999)}"
    addr = f"{random.randint(1,200)} {random.choice(['High Street','Church Lane','Oak Avenue','Mill Road','Station Road','Park Close'])}, London"
    A(f"INSERT INTO patient (patient_id, nhs_number, first_name, last_name, date_of_birth, sex, address, postcode, phone, blood_type, allergies, created_by, created_at)")
    A(f"  VALUES ({q(p['id'])}, {q(p['nhs'])}, {q(p['first'])}, {q(p['last'])}, {qdate(p['dob'])}, {q(p['sex'])}, {q(addr)}, {q(postcode)}, {q(phone)}, {q(p['bt'])}, {q(p['allergy'])}, {q(SYSTEM_CLINICIAN)}, {qd(p['tx_start'])});")
A("")

# ── clinical data per patient ─────────────────────────────────────────────────
A("-- ── Clinical data ────────────────────────────────────────────")

CANCER_DRUGS = {
    'Non-Hodgkin lymphoma':         ['R-CHOP chemotherapy','Rituximab infusion','Bendamustine infusion'],
    'Hodgkin lymphoma':             ['ABVD chemotherapy','Brentuximab vedotin infusion','Nivolumab infusion'],
    'Acute myeloid leukaemia':      ['Cytarabine infusion','Daunorubicin infusion','Venetoclax oral'],
    'Chronic lymphocytic leukaemia':['Ibrutinib oral','Acalabrutinib oral','Obinutuzumab infusion'],
    'Breast cancer':                ['Trastuzumab infusion','Docetaxel infusion','Capecitabine oral'],
    'Colorectal cancer':            ['FOLFOX chemotherapy','Bevacizumab infusion','Cetuximab infusion'],
    'Lung cancer':                  ['Pembrolizumab infusion','Carboplatin infusion','Pemetrexed infusion'],
    'Ovarian cancer':               ['Carboplatin infusion','Paclitaxel infusion','Bevacizumab infusion'],
    'Prostate cancer':              ['Enzalutamide oral','Abiraterone oral','Docetaxel infusion'],
    'Cervical cancer':              ['Cisplatin infusion','Bevacizumab infusion','Pembrolizumab infusion'],
}

IMAGING_BY_CANCER = {
    'Non-Hodgkin lymphoma':         [('CT','Chest/Abdomen/Pelvis'),('PT','Whole body')],
    'Hodgkin lymphoma':             [('CT','Chest/Abdomen/Pelvis'),('PT','Whole body')],
    'Acute myeloid leukaemia':      [('CT','Chest'),('MR','Brain')],
    'Chronic lymphocytic leukaemia':[('CT','Chest/Abdomen'),('US','Abdomen')],
    'Breast cancer':                [('MG','Bilateral breast'),('MR','Breast'),('CR','Chest')],
    'Colorectal cancer':            [('CT','Chest/Abdomen/Pelvis'),('MR','Pelvis')],
    'Lung cancer':                  [('CT','Chest'),('PT','Whole body'),('CR','Chest')],
    'Ovarian cancer':               [('CT','Abdomen/Pelvis'),('MR','Pelvis'),('US','Pelvis')],
    'Prostate cancer':              [('MR','Pelvis'),('NM','Bone scan'),('CT','Chest/Abdomen/Pelvis')],
    'Cervical cancer':              [('MR','Pelvis'),('CT','Chest/Abdomen/Pelvis'),('PT','Whole body')],
}

DICOM_INSTITUTIONS = ['Hampton Hospital Radiology', 'Hampton Hospital Imaging Centre']
FMT = 'DICOM'

total_visits = 0
total_treatments = 0
total_measurements = 0
total_labs = 0
total_images = 0

for p in patients:
    pid      = p['id']
    nhs      = p['nhs']
    cancer   = p['cancer']
    tx_start = p['tx_start']
    tx_end   = p['tx_end']
    duration_days = (tx_end - tx_start).days

    # Assign a primary consultant (oncology or haematology depending on cancer type)
    haem_cancers = {'Non-Hodgkin lymphoma','Hodgkin lymphoma','Acute myeloid leukaemia','Chronic lymphocytic leukaemia'}
    if cancer in haem_cancers:
        primary_consultants = [s[0] for s in STAFF if s[3] in ('Consultant','Registrar') and s[4]=='haematology']
        primary_dept = DEPT_ID['haematology']
        lab_panels = ['FBC','U&E','Bone marrow biopsy panel','LFT']
    else:
        primary_consultants = [s[0] for s in STAFF if s[3] in ('Consultant','Registrar') and s[4]=='oncology']
        primary_dept = DEPT_ID['oncology']
        lab_panels = ['FBC','U&E','LFT','Tumour markers']

    consultant = random.choice(primary_consultants)
    nurses     = [s[0] for s in STAFF if s[3]=='Nurse']
    surgeons   = [s[0] for s in STAFF if s[3]=='Surgeon']
    radiologist= STAFF[12][0]  # Patrick Doran
    drugs      = CANCER_DRUGS[cancer]

    # ── Build treatment bursts ────────────────────────────────────
    # ~4-8 bursts of 6 weeks each across the treatment window
    num_bursts = random.randint(4, 7)
    burst_starts = sorted(random.sample(
        range(0, max(1, duration_days - 42)),
        min(num_bursts, max(1, duration_days - 42))
    ))

    visit_counter = 0
    image_seq     = 1

    for burst_start_day in burst_starts:
        burst_start_ts = tx_start + datetime.timedelta(days=burst_start_day)
        num_weeks = random.randint(4, 6)

        for week in range(num_weeks):
            visit_day = burst_start_ts + datetime.timedelta(days=week*7 + random.randint(0,2))
            if visit_day >= tx_end or visit_day >= DB_END:
                break

            visit_id   = uid()
            visit_type = random.choices(['Outpatient','Inpatient','Day case'], weights=[60,20,20])[0]
            admitted   = visit_day
            hours_in   = 2 if visit_type=='Outpatient' else (random.randint(12,72) if visit_type=='Inpatient' else 6)
            discharged = admitted + datetime.timedelta(hours=hours_in)
            attending  = consultant
            visit_dept = primary_dept
            reason     = f"{cancer} – scheduled {'treatment' if week%3!=2 else 'review'} visit"
            dnotes     = f"Patient tolerated treatment. Next {'bloods' if week%2==0 else 'imaging'} due."

            A(f"INSERT INTO visit (visit_id, patient_id, department_id, attending_clinician_id, admitted_at, discharged_at, visit_type, reason, discharge_notes, created_by, created_at)")
            A(f"  VALUES ({q(visit_id)}, {q(pid)}, {q(visit_dept)}, {q(attending)}, {qd(admitted)}, {qd(discharged)}, {q(visit_type)}, {q(reason)}, {q(dnotes)}, {q(attending)}, {qd(admitted)});")
            total_visits += 1

            # ── treatment ──────────────────────────────────────────
            drug = random.choice(drugs)
            tx_id = uid()
            tx_type = 'Infusion' if 'infusion' in drug.lower() else ('Oral medication' if 'oral' in drug.lower() else 'Chemotherapy')
            nurse = random.choice(nurses)
            A(f"INSERT INTO treatment (treatment_id, visit_id, department_id, clinician_id, treatment_type, description, notes, performed_at, created_by, created_at)")
            A(f"  VALUES ({q(tx_id)}, {q(visit_id)}, {q(visit_dept)}, {q(nurse)}, {q(tx_type)}, {q(drug)}, {q(f'Administered by nursing staff. Patient tolerated well.')}, {qd(admitted + datetime.timedelta(minutes=30))}, {q(nurse)}, {qd(admitted)});")
            total_treatments += 1

            # occasional surgical review
            if visit_type=='Inpatient' and random.random()<0.25:
                surg_id = uid()
                surgeon = random.choice(surgeons)
                A(f"INSERT INTO treatment (treatment_id, visit_id, department_id, clinician_id, treatment_type, description, notes, performed_at, created_by, created_at)")
                A(f"  VALUES ({q(surg_id)}, {q(visit_id)}, {q(DEPT_ID['surgery'])}, {q(surgeon)}, 'Surgical review', 'Surgical assessment and wound review', 'No immediate surgical intervention required.', {qd(admitted + datetime.timedelta(hours=2))}, {q(surgeon)}, {qd(admitted)});")
                total_treatments += 1

            # ── measurements ───────────────────────────────────────
            m_ts = admitted + datetime.timedelta(minutes=15)
            weight = round(random.uniform(55, 95), 1)
            meas = [
                ('Weight',    weight,                    'kg'),
                ('Height',    round(random.uniform(155,185),1), 'cm'),
                ('Systolic BP', random.randint(100,150), 'mmHg'),
                ('Diastolic BP',random.randint(60,95),   'mmHg'),
                ('Heart rate',  random.randint(55,100),  'bpm'),
                ('Temperature', round(random.uniform(36.2,37.5),1), '°C'),
                ('SpO2',        random.randint(94,100),  '%'),
                ('ECOG score',  random.randint(0,3),     'scale'),
            ]
            for mtype, mval, munit in meas:
                mid = uid()
                A(f"INSERT INTO measurement (measurement_id, visit_id, clinician_id, measured_at, type, value, unit, created_by, created_at)")
                A(f"  VALUES ({q(mid)}, {q(visit_id)}, {q(nurse)}, {qd(m_ts)}, {q(mtype)}, {mval}, {q(munit)}, {q(nurse)}, {qd(admitted)});")
                m_ts += datetime.timedelta(minutes=2)
                total_measurements += 1

            # ── lab results ────────────────────────────────────────
            collected_ts = admitted + datetime.timedelta(minutes=10)
            resulted_ts  = admitted + datetime.timedelta(hours=4)
            panel = random.choice(lab_panels)

            lab_analytes = {
                'FBC':  [('Haemoglobin',random.uniform(90,155),'g/L','130-170'),
                         ('White cell count',random.uniform(2.5,12.0),'10⁹/L','4.0-11.0'),
                         ('Platelets',random.randint(80,400),'10⁹/L','150-400'),
                         ('Neutrophils',random.uniform(1.5,8.0),'10⁹/L','1.8-7.5')],
                'U&E':  [('Sodium',random.randint(130,148),'mmol/L','133-146'),
                         ('Potassium',round(random.uniform(3.2,5.5),1),'mmol/L','3.5-5.3'),
                         ('Creatinine',random.randint(50,140),'µmol/L','62-106'),
                         ('Urea',round(random.uniform(2.5,10.0),1),'mmol/L','2.5-7.8')],
                'LFT':  [('ALT',random.randint(10,80),'IU/L','7-56'),
                         ('AST',random.randint(10,60),'IU/L','10-40'),
                         ('Bilirubin',random.randint(3,30),'µmol/L','3-21'),
                         ('Albumin',random.randint(28,45),'g/L','35-50')],
                'Tumour markers': [('CA-125',round(random.uniform(5,500),1),'U/mL','<35'),
                                   ('CEA',round(random.uniform(1,50),1),'µg/L','<5'),
                                   ('AFP',round(random.uniform(1,200),1),'µg/L','<10')],
                'Bone marrow biopsy panel': [('Blast percentage',round(random.uniform(0,30),1),'%','<5'),
                                              ('Cellularity',round(random.uniform(30,95),1),'%','30-70')],
            }.get(panel, [('Haemoglobin',random.uniform(100,150),'g/L','130-170')])

            for analyte, val, unit_l, ref in lab_analytes:
                rid = uid()
                val_r = round(float(val), 2)
                # determine flag
                try:
                    lo, hi = ref.replace('<','0-').split('-')
                    lo_f, hi_f = float(lo.replace('<','')), float(hi)
                    flag = 'H' if val_r > hi_f else ('L' if val_r < lo_f else None)
                except Exception:
                    flag = None
                A(f"INSERT INTO lab_result (result_id, visit_id, clinician_id, sample_type, collected_at, resulted_at, panel, analyte, value, unit, reference_range, flag, created_by, created_at)")
                A(f"  VALUES ({q(rid)}, {q(visit_id)}, {q(consultant)}, {q('Blood' if panel!='Bone marrow biopsy panel' else 'Bone marrow')}, {qd(collected_ts)}, {qd(resulted_ts)}, {q(panel)}, {q(analyte)}, {val_r}, {q(unit_l)}, {q(ref)}, {q(flag)}, {q(consultant)}, {qd(admitted)});")
                total_labs += 1

            # ── medical images (first visit of each burst + every 3rd week) ──
            if week == 0 or week % 3 == 0:
                imaging_options = IMAGING_BY_CANCER.get(cancer, [('CT','Chest')])
                modality, body_part = random.choice(imaging_options)
                study_uid  = uid()
                series_uid = uid()
                sop_uid    = uid()
                acc_no     = f"ACC{nhs[:5]}{image_seq:04d}"
                fpath      = img_path(nhs, modality, admitted, image_seq)
                # rough size by modality
                sizes = {'CT':524288000,'MR':209715200,'CR':16777216,'DX':16777216,
                         'US':5242880,'PT':104857600,'NM':52428800,'MG':33554432}
                fsize = sizes.get(modality,16777216) + random.randint(-2000000,2000000)

                rpt_ts = admitted + datetime.timedelta(hours=random.randint(4,24))
                report = f"Staging CT {body_part}. {random.choice(['No significant interval change.','Partial response to treatment noted.','Stable disease.','Mild progression at primary site.','Lymph node burden reduced.'])} Radiologist review complete."

                A(f"INSERT INTO medical_image (image_id, visit_id, clinician_id, modality, body_part, captured_at, file_path, file_format, file_size_bytes, dicom_study_uid, dicom_series_uid, dicom_sop_uid, dicom_patient_id, dicom_accession_no, dicom_institution, report, report_by, created_by, created_at)")
                A(f"  VALUES ({q(uid())}, {q(visit_id)}, {q(radiologist)}, {q(modality)}, {q(body_part)}, {qd(admitted + datetime.timedelta(hours=1))}, {q(fpath)}, {q(FMT)}, {fsize}, {q(study_uid)}, {q(series_uid)}, {q(sop_uid)}, {q(nhs)}, {q(acc_no)}, {q(random.choice(DICOM_INSTITUTIONS))}, {q(report)}, {q('Dr P Doran FRCR – Hampton Hospital Radiology')}, {q(radiologist)}, {qd(rpt_ts)});")
                image_seq += 1
                total_images += 1

            visit_counter += 1

    # ── inter-burst medication visits (about monthly between bursts) ───────────
    # Simple outpatient medication reviews
    cur = tx_start + datetime.timedelta(days=random.randint(5,14))
    while cur < tx_end:
        # skip if within a burst
        cur += datetime.timedelta(days=random.randint(25,35))
        if cur >= tx_end:
            break
        visit_id = uid()
        drug = random.choice(drugs)
        admitted = cur
        discharged = cur + datetime.timedelta(hours=2)
        A(f"INSERT INTO visit (visit_id, patient_id, department_id, attending_clinician_id, admitted_at, discharged_at, visit_type, reason, discharge_notes, created_by, created_at)")
        A(f"  VALUES ({q(visit_id)}, {q(pid)}, {q(primary_dept)}, {q(consultant)}, {qd(admitted)}, {qd(discharged)}, 'Outpatient', {q(f'{cancer} – medication review')}, 'Medication review completed. Continue current regimen.', {q(consultant)}, {qd(admitted)});")
        total_visits += 1

        med_id = uid()
        A(f"INSERT INTO treatment (treatment_id, visit_id, department_id, clinician_id, treatment_type, description, notes, performed_at, created_by, created_at)")
        A(f"  VALUES ({q(med_id)}, {q(visit_id)}, {q(primary_dept)}, {q(random.choice(nurses))}, 'Oral medication', {q(drug)}, 'Prescription issued. Patient counselled on side effects.', {qd(admitted + datetime.timedelta(minutes=20))}, {q(consultant)}, {qd(admitted)});")
        total_treatments += 1

A("")
A("COMMIT;")
A("")
A("-- ── Summary ──────────────────────────────────────────────────")
A(f"-- Departments:   {len(DEPT_ROWS)}")
A(f"-- Clinicians:    {len(STAFF)}")
A(f"-- Patients:      {len(patients)}")
A(f"-- Visits:        {total_visits}")
A(f"-- Treatments:    {total_treatments}")
A(f"-- Measurements:  {total_measurements}")
A(f"-- Lab results:   {total_labs}")
A(f"-- Medical images:{total_images}")

sql = '\n'.join(lines)
with open('/mnt/user-data/outputs/hampton_hospital_data_load.sql', 'w') as f:
    f.write(sql)

print(f"Done. Lines: {len(lines)}")
print(f"Departments:  {len(DEPT_ROWS)}")
print(f"Clinicians:   {len(STAFF)}")
print(f"Patients:     {len(patients)}")
print(f"Visits:       {total_visits}")
print(f"Treatments:   {total_treatments}")
print(f"Measurements: {total_measurements}")
print(f"Lab results:  {total_labs}")
print(f"Images:       {total_images}")

