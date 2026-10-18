-- system-qualified-name: SoftwareServer::SYS-007::Microsoft 365
-- Microsoft 365 - Bucharest.  Microsoft 365 (Exchange Online) tenant ekgpharma.ro.  Mailboxes are provisioned directly
-- from Workday over Graph (cloud-only; not synchronised from Active Directory), so leavers' mailboxes are converted to
-- shared mailboxes by the same flow.  Its tables feed Corporate Directory Entries (mailbox users).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS microsoft_365;
COMMENT ON SCHEMA microsoft_365 IS 'Microsoft 365 (EKG): Exchange Online recipient properties as exported by the daily Get-EXORecipient job.';

CREATE TABLE IF NOT EXISTS microsoft_365.exo_recipient (
  externaldirectoryobjectid uuid NOT NULL,
  primarysmtpaddress        varchar(120) NOT NULL,
  firstname                 varchar(80),
  lastname                  varchar(80),
  displayname               varchar(160),
  title                     varchar(120),
  department                varchar(120),
  office                    varchar(120),
  phone                     varchar(30),
  manager                   varchar(120),
  customattribute1          varchar(20),
  recipienttypedetails      varchar(40) NOT NULL,
  isdirsynced               boolean NOT NULL,
  whenchanged               timestamptz NOT NULL,
  CONSTRAINT exo_recipient_pk PRIMARY KEY (externaldirectoryobjectid)
);
COMMENT ON TABLE microsoft_365.exo_recipient IS 'Exchange Online recipients (customattribute1 = Workday employee ID written by the provisioning integration).';

INSERT INTO microsoft_365.exo_recipient (externaldirectoryobjectid, primarysmtpaddress, firstname, lastname, displayname, title, department, office, phone, manager, customattribute1, recipienttypedetails, isdirsynced, whenchanged) VALUES
('03653cff-6371-1560-3074-bb5501bff288', 'andrei.munteanu@ekgpharma.ro', 'Andrei', 'Munteanu', 'Andrei Munteanu', 'Director General', 'Conducere', 'Fabrica București', '+40 21 318 4101', NULL, '20011', 'UserMailbox', FALSE, '2012-02-01 18:30:00+00'),
('205fdc1a-22b3-0427-1b1e-2807738c0110', 'gheorghe.radu@ekgpharma.ro', 'Gheorghe', 'Radu', 'Gheorghe Radu', 'Director Financiar', 'Financiar-contabilitate', 'Fabrica București', '+40 21 318 4114', 'andrei.munteanu@ekgpharma.ro', '20014', 'UserMailbox', FALSE, '2013-05-06 18:30:00+00'),
('c4311d01-f603-a4b5-2a1d-8f36bf0812b8', 'nicoleta.oprea@ekgpharma.ro', 'Nicoleta', 'Oprea', 'Nicoleta Oprea', 'Director Calitate și Persoană Calificată', 'Asigurarea calității', 'Fabrica București', '+40 21 318 4117', 'andrei.munteanu@ekgpharma.ro', '20017', 'UserMailbox', FALSE, '2014-09-01 18:30:00+00'),
('4fa7f7cd-ed56-82e6-bc1d-7a55918a5ba4', 'florin.stoica@ekgpharma.ro', 'Florin', 'Stoica', 'Florin Stoica', 'Director Producție', 'Producție sterile', 'Fabrica București', '+40 21 318 4121', 'andrei.munteanu@ekgpharma.ro', '20021', 'UserMailbox', FALSE, '2015-03-02 18:30:00+00'),
('e86bbf01-2c9e-590b-ebfc-8be7391aacf7', 'adina.petre@ekgpharma.ro', 'Adina', 'Petre', 'Adina Petre', 'Manager Afaceri de Reglementare și Juridic', 'Afaceri de reglementare', 'Fabrica București', '+40 21 318 4123', 'andrei.munteanu@ekgpharma.ro', '20023', 'UserMailbox', FALSE, '2016-01-11 18:30:00+00'),
('bafb7530-6a24-f0dc-260a-42b3b18d30c8', 'cristian.lungu@ekgpharma.ro', 'Cristian', 'Lungu', 'Cristian Lungu', 'Manager Vânzări', 'Vânzări și marketing', 'Fabrica București', '+40 21 318 4126', 'andrei.munteanu@ekgpharma.ro', '20026', 'UserMailbox', FALSE, '2016-10-03 18:30:00+00'),
('b46b64bd-678a-8b19-2015-c51c25f4db16', 'luminita.chiriac@ekgpharma.ro', 'Luminița', 'Chiriac', 'Luminița Chiriac', 'Director Resurse Umane', 'Resurse umane', 'Fabrica București', '+40 21 318 4129', 'andrei.munteanu@ekgpharma.ro', '20029', 'UserMailbox', FALSE, '2017-04-18 18:30:00+00'),
('c833cdcf-a3f8-b0f6-998c-268cc7683253', 'mihai.constantin@ekgpharma.ro', 'Mihai', 'Constantin', 'Mihai Constantin', 'Manager IT', 'IT', 'Fabrica București', '+40 21 318 4131', 'gheorghe.radu@ekgpharma.ro', '20031', 'UserMailbox', FALSE, '2017-08-01 18:30:00+00'),
('76486722-ca0d-af07-c5d3-33d385827ae6', 'lucian.preda@ekgpharma.ro', 'Lucian', 'Preda', 'Lucian Preda', 'Inginer Infrastructură IT', 'IT', 'Fabrica București', '+40 21 318 4133', 'mihai.constantin@ekgpharma.ro', '20033', 'UserMailbox', FALSE, '2018-02-12 18:30:00+00'),
('d07c4b4d-f9e6-96ef-680a-882a3dd26f29', 'mihaela.apostol@ekgpharma.ro', 'Mihaela', 'Apostol', 'Mihaela Apostol', 'Contabil Șef', 'Financiar-contabilitate', 'Fabrica București', '+40 21 318 4135', 'gheorghe.radu@ekgpharma.ro', '20035', 'UserMailbox', FALSE, '2018-06-04 18:30:00+00'),
('789a880f-9bc3-991e-1c09-b78876fba7b9', 'simona.florescu@ekgpharma.ro', 'Simona', 'Florescu', 'Simona Florescu', 'Controller Financiar', 'Financiar-contabilitate', 'Fabrica București', '+40 21 318 4138', 'gheorghe.radu@ekgpharma.ro', '20038', 'UserMailbox', FALSE, '2019-01-14 18:30:00+00'),
('ab2baf3c-10dd-8851-6cc8-19a18c6727b0', 'marian.bucur@ekgpharma.ro', 'Marian', 'Bucur', 'Marian Bucur', 'Manager Mentenanță și Utilități', 'Mentenanță și inginerie', 'Fabrica București', '+40 21 318 4140', 'florin.stoica@ekgpharma.ro', '20040', 'UserMailbox', FALSE, '2015-11-02 18:30:00+00'),
('9d709920-da0c-2777-7167-7d5ddc16ac7d', 'ciprian.tudor@ekgpharma.ro', 'Ciprian', 'Tudor', 'Ciprian Tudor', 'Manager Lanț de Aprovizionare', 'Depozit și logistică', 'Fabrica București', '+40 21 318 4142', 'gheorghe.radu@ekgpharma.ro', '20042', 'UserMailbox', FALSE, '2016-05-16 18:30:00+00'),
('ed6bc3e7-d667-ac42-d6d8-1416503fdcfb', 'sorin.matei@ekgpharma.ro', 'Sorin', 'Matei', 'Sorin Matei', 'Specialist Securitate IT', 'IT', 'Fabrica București', '+40 21 318 4144', 'mihai.constantin@ekgpharma.ro', '20044', 'UserMailbox', FALSE, '2020-03-02 18:30:00+00'),
('e3e9dcff-573d-adaf-6647-17a2c67a3743', 'roxana.dumitrescu@ekgpharma.ro', 'Roxana', 'Dumitrescu', 'Roxana Dumitrescu', 'Specialist Marketing', 'Vânzări și marketing', 'Fabrica București', '+40 21 318 4146', 'cristian.lungu@ekgpharma.ro', '20046', 'UserMailbox', FALSE, '2021-06-07 18:30:00+00'),
('60162f6f-ccbc-d52a-ea2d-529b04ecc0ee', 'sebastian.vasile@ekgpharma.ro', 'Sebastian', 'Vasile', 'Sebastian Vasile', 'Analist Control Calitate', 'Control calitate', 'Fabrica București', '+40 21 318 4149', 'nicoleta.oprea@ekgpharma.ro', '20049', 'SharedMailbox', FALSE, '2026-07-31 18:30:00+00'),
('a9d8cab9-7d42-136d-f123-357ed407876a', 'elena.popescu@ekgpharma.ro', 'Elena', 'Popescu', 'Elena Popescu', 'Analist Control Calitate', 'Control calitate', 'Fabrica București', '+40 21 318 4152', 'nicoleta.oprea@ekgpharma.ro', '20052', 'UserMailbox', FALSE, '2018-10-15 18:30:00+00'),
('6ab573d7-8d6f-16a2-b68b-a569659f001f', 'ioana.stan@ekgpharma.ro', 'Ioana', 'Stan', 'Ioana Stan', 'Analist Microbiologie', 'Control calitate', 'Fabrica București', '+40 21 318 4155', 'nicoleta.oprea@ekgpharma.ro', '20055', 'UserMailbox', FALSE, '2020-02-17 18:30:00+00'),
('8fc4ab1c-e262-da91-fc7e-d555145c7e39', 'vlad.georgescu@ekgpharma.ro', 'Vlad', 'Georgescu', 'Vlad Georgescu', 'Șef de Tură Producție', 'Producție sterile', 'Fabrica București', '+40 21 318 4166', 'florin.stoica@ekgpharma.ro', '20066', 'UserMailbox', FALSE, '2016-09-05 18:30:00+00'),
('4cd738aa-8e71-4334-2c61-39f77f06bdae', 'raluca.enache@ekgpharma.ro', 'Raluca', 'Enache', 'Raluca Enache', 'Specialist Asigurarea Calității', 'Asigurarea calității', 'Fabrica București', '+40 21 318 4169', 'nicoleta.oprea@ekgpharma.ro', '20069', 'UserMailbox', FALSE, '2019-05-13 18:30:00+00'),
('62ebddcd-60e1-717d-5ece-5c66cf7dbf2a', 'oana.nistor@ekgpharma.ro', 'Oana', 'Nistor', 'Oana Nistor', 'Contabil Furnizori', 'Financiar-contabilitate', 'Fabrica București', '+40 21 318 4175', 'mihaela.apostol@ekgpharma.ro', '20075', 'UserMailbox', FALSE, '2021-02-01 18:30:00+00'),
('88a06652-4000-bd59-dce8-8cae7fbe2c80', 'gabriela.toma@ekgpharma.ro', 'Gabriela', 'Toma', 'Gabriela Toma', 'Responsabil Farmacovigilență', 'Afaceri de reglementare', 'Fabrica București', '+40 21 318 4181', 'adina.petre@ekgpharma.ro', '20081', 'UserMailbox', FALSE, '2022-09-12 18:30:00+00'),
('9e766631-db46-08b6-e576-09277fab8401', 'irina.moldovan@ekgpharma.ro', 'Irina', 'Moldovan', 'Irina Moldovan', 'Analist Control Calitate', 'Control calitate', 'Fabrica București', '+40 21 318 4184', 'nicoleta.oprea@ekgpharma.ro', '20084', 'UserMailbox', FALSE, '2026-09-01 18:30:00+00'),
('e0033966-b294-216c-518c-8c171111ef14', 'paul.neagu.ext@ekgpharma.ro', 'Paul', 'Neagu', 'Paul Neagu', 'Consultant Validare', 'Mentenanță și inginerie', 'Fabrica București', NULL, 'marian.bucur@ekgpharma.ro', 'C0012', 'UserMailbox', FALSE, '2026-06-15 18:30:00+00')
ON CONFLICT DO NOTHING;

-- Custom attributes written by the Workday worker feed (subscription apply script buc_microsoft_365__worker_master_data).
ALTER TABLE microsoft_365.exo_recipient ADD COLUMN IF NOT EXISTS customattribute2 varchar(20);
ALTER TABLE microsoft_365.exo_recipient ADD COLUMN IF NOT EXISTS customattribute3 varchar(40);
ALTER TABLE microsoft_365.exo_recipient ADD COLUMN IF NOT EXISTS customattribute4 varchar(40);
COMMENT ON COLUMN microsoft_365.exo_recipient.customattribute2 IS 'CustomAttribute2: Workday cost centre (used by address-book policies and dynamic distribution groups).';
COMMENT ON COLUMN microsoft_365.exo_recipient.customattribute3 IS 'CustomAttribute3: Workday job profile.';
COMMENT ON COLUMN microsoft_365.exo_recipient.customattribute4 IS 'CustomAttribute4: Workday worker status (active, on leave, left YYYY-MM-DD).';

GRANT USAGE ON SCHEMA microsoft_365 TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA microsoft_365 TO egeria_user, airflow_user;
