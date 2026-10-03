-- system-qualified-name: SoftwareServer::SYS-008::Active Directory
-- Active Directory - Bucharest.  On-premises Active Directory (EKG.LOCAL) for all EKG user accounts and the groups
-- that authorise SAP, MES, LIMS, Empower, Maximo and the WMS over LDAP.  Accounts are created and disabled from
-- helpdesk tickets, not from Workday.  Its tables feed Access Entitlements and Corporate Directory Entries (staff
-- without a mailbox).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS active_directory;
COMMENT ON SCHEMA active_directory IS 'Active Directory (EKG): user, group and linked-value group membership attributes as exported by the nightly LDAP dump (lower-case attribute names).';

CREATE TABLE IF NOT EXISTS active_directory.ad_user (
  objectguid                 uuid NOT NULL,
  samaccountname             varchar(20) NOT NULL,
  userprincipalname          varchar(120) NOT NULL,
  givenname                  varchar(80),
  sn                         varchar(80),
  displayname                varchar(160),
  title                      varchar(120),
  department                 varchar(120),
  company                    varchar(120),
  physicaldeliveryofficename varchar(120),
  telephonenumber            varchar(30),
  employeeid                 varchar(20),
  manager                    varchar(255),
  distinguishedname          varchar(255) NOT NULL,
  useraccountcontrol         integer NOT NULL,
  whencreated                timestamptz NOT NULL,
  whenchanged                timestamptz NOT NULL,
  accountexpires             bigint NOT NULL,
  mail                       varchar(120),
  extensionattribute10       varchar(60),
  CONSTRAINT ad_user_pk PRIMARY KEY (objectguid)
);
COMMENT ON TABLE active_directory.ad_user IS 'User objects (employeeid = Workday employee ID; extensionattribute10 = the Workday event quoted on the helpdesk ticket that created the account; mail is set only for staff with a Microsoft 365 mailbox).';

INSERT INTO active_directory.ad_user (objectguid, samaccountname, userprincipalname, givenname, sn, displayname, title, department, company, physicaldeliveryofficename, telephonenumber, employeeid, manager, distinguishedname, useraccountcontrol, whencreated, whenchanged, accountexpires, mail, extensionattribute10) VALUES
('045dae99-6feb-c23c-6a64-6c554233fe1e', 'amunteanu', 'amunteanu@ekg.local', 'Andrei', 'Munteanu', 'Andrei Munteanu', 'Director General', 'Conducere', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4101', '20011', NULL, 'CN=Andrei Munteanu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2012-01-29 14:20:00+00', '2012-02-01 14:20:00+00', 9223372036854775807, 'andrei.munteanu@ekgpharma.ro', 'EVT-RO-2012-0001'),
('fd5db688-2aa5-ad4c-1bdb-64b17472267f', 'gradu', 'gradu@ekg.local', 'Gheorghe', 'Radu', 'Gheorghe Radu', 'Director Financiar', 'Financiar-contabilitate', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4114', '20014', 'CN=Andrei Munteanu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Gheorghe Radu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2013-05-03 14:20:00+00', '2013-05-06 14:20:00+00', 9223372036854775807, 'gheorghe.radu@ekgpharma.ro', 'EVT-RO-2013-0002'),
('0e41f1a6-9a26-5ab9-aa52-c3e076d4e598', 'noprea', 'noprea@ekg.local', 'Nicoleta', 'Oprea', 'Nicoleta Oprea', 'Director Calitate și Persoană Calificată', 'Asigurarea calității', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4117', '20017', 'CN=Andrei Munteanu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Nicoleta Oprea,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2014-08-29 14:20:00+00', '2014-09-01 14:20:00+00', 9223372036854775807, 'nicoleta.oprea@ekgpharma.ro', 'EVT-RO-2014-0003'),
('472541c9-257c-2010-80a1-bf3eb861e16b', 'fstoica', 'fstoica@ekg.local', 'Florin', 'Stoica', 'Florin Stoica', 'Director Producție', 'Producție sterile', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4121', '20021', 'CN=Andrei Munteanu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Florin Stoica,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2015-02-27 14:20:00+00', '2015-03-02 14:20:00+00', 9223372036854775807, 'florin.stoica@ekgpharma.ro', 'EVT-RO-2015-0004'),
('2e1a239a-fcdc-f164-ae3c-8d3241944469', 'apetre', 'apetre@ekg.local', 'Adina', 'Petre', 'Adina Petre', 'Manager Afaceri de Reglementare și Juridic', 'Afaceri de reglementare', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4123', '20023', 'CN=Andrei Munteanu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Adina Petre,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2016-01-08 14:20:00+00', '2016-01-11 14:20:00+00', 9223372036854775807, 'adina.petre@ekgpharma.ro', 'EVT-RO-2016-0006'),
('6c61116c-2578-4582-7f91-7746cbbca2be', 'clungu', 'clungu@ekg.local', 'Cristian', 'Lungu', 'Cristian Lungu', 'Manager Vânzări', 'Vânzări și marketing', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4126', '20026', 'CN=Andrei Munteanu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Cristian Lungu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2016-09-30 14:20:00+00', '2016-10-03 14:20:00+00', 9223372036854775807, 'cristian.lungu@ekgpharma.ro', 'EVT-RO-2016-0009'),
('e90fe7a9-88e2-e5d1-2182-54ad529f4788', 'lchiriac', 'lchiriac@ekg.local', 'Luminița', 'Chiriac', 'Luminița Chiriac', 'Director Resurse Umane', 'Resurse umane', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4129', '20029', 'CN=Andrei Munteanu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Luminita Chiriac,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2017-04-15 14:20:00+00', '2017-04-18 14:20:00+00', 9223372036854775807, 'luminita.chiriac@ekgpharma.ro', 'EVT-RO-2017-0010'),
('ca219cb7-0113-272d-a9e3-4e147266bb35', 'mconstantin', 'mconstantin@ekg.local', 'Mihai', 'Constantin', 'Mihai Constantin', 'Manager IT', 'IT', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4131', '20031', 'CN=Gheorghe Radu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Mihai Constantin,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2017-07-29 14:20:00+00', '2017-08-01 14:20:00+00', 9223372036854775807, 'mihai.constantin@ekgpharma.ro', 'EVT-RO-2017-0011'),
('73abb4ec-ed66-6d48-976e-b1b0985d4ae1', 'lpreda', 'lpreda@ekg.local', 'Lucian', 'Preda', 'Lucian Preda', 'Inginer Infrastructură IT', 'IT', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4133', '20033', 'CN=Mihai Constantin,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Lucian Preda,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2018-02-09 14:20:00+00', '2018-02-12 14:20:00+00', 9223372036854775807, 'lucian.preda@ekgpharma.ro', 'EVT-RO-2018-0013'),
('9b7420e1-8120-a13e-f61b-d22e640d8722', 'mapostol', 'mapostol@ekg.local', 'Mihaela', 'Apostol', 'Mihaela Apostol', 'Contabil Șef', 'Financiar-contabilitate', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4135', '20035', 'CN=Gheorghe Radu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Mihaela Apostol,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2018-06-01 14:20:00+00', '2018-06-04 14:20:00+00', 9223372036854775807, 'mihaela.apostol@ekgpharma.ro', 'EVT-RO-2018-0015'),
('ecc3ac1b-6e5a-2229-3bce-b9f61344de99', 'sflorescu', 'sflorescu@ekg.local', 'Simona', 'Florescu', 'Simona Florescu', 'Controller Financiar', 'Financiar-contabilitate', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4138', '20038', 'CN=Gheorghe Radu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Simona Florescu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2019-01-11 14:20:00+00', '2019-01-14 14:20:00+00', 9223372036854775807, 'simona.florescu@ekgpharma.ro', 'EVT-RO-2019-0017'),
('33e09dd2-a741-56e7-7446-b876308abb10', 'mbucur', 'mbucur@ekg.local', 'Marian', 'Bucur', 'Marian Bucur', 'Manager Mentenanță și Utilități', 'Mentenanță și inginerie', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4140', '20040', 'CN=Florin Stoica,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Marian Bucur,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2015-10-30 14:20:00+00', '2015-11-02 14:20:00+00', 9223372036854775807, 'marian.bucur@ekgpharma.ro', 'EVT-RO-2015-0005'),
('2d862d58-984a-56eb-49c6-cd90b85f2d85', 'ctudor', 'ctudor@ekg.local', 'Ciprian', 'Tudor', 'Ciprian Tudor', 'Manager Lanț de Aprovizionare', 'Depozit și logistică', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4142', '20042', 'CN=Gheorghe Radu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Ciprian Tudor,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2016-05-13 14:20:00+00', '2016-05-16 14:20:00+00', 9223372036854775807, 'ciprian.tudor@ekgpharma.ro', 'EVT-RO-2016-0007'),
('efc5b107-a42f-2a58-777b-f12fdbef3893', 'smatei', 'smatei@ekg.local', 'Sorin', 'Matei', 'Sorin Matei', 'Specialist Securitate IT', 'IT', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4144', '20044', 'CN=Mihai Constantin,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Sorin Matei,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2020-02-28 14:20:00+00', '2020-03-02 14:20:00+00', 9223372036854775807, 'sorin.matei@ekgpharma.ro', 'EVT-RO-2020-0022'),
('3e809e4b-3e57-9873-2765-4e1893e6a2ee', 'rdumitrescu', 'rdumitrescu@ekg.local', 'Roxana', 'Dumitrescu', 'Roxana Dumitrescu', 'Specialist Marketing', 'Vânzări și marketing', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4146', '20046', 'CN=Cristian Lungu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Roxana Dumitrescu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2021-06-04 14:20:00+00', '2021-06-07 14:20:00+00', 9223372036854775807, 'roxana.dumitrescu@ekgpharma.ro', 'EVT-RO-2021-0025'),
('812cbd24-40ad-155c-10bb-6b2ed6801250', 'svasile', 'svasile@ekg.local', 'Sebastian', 'Vasile', 'Sebastian Vasile', 'Analist Control Calitate', 'Control calitate', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4149', '20049', 'CN=Nicoleta Oprea,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Sebastian Vasile,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2019-08-30 14:20:00+00', '2019-09-02 14:20:00+00', 9223372036854775807, 'sebastian.vasile@ekgpharma.ro', 'EVT-RO-2019-0020'),
('8165e734-b1ef-9727-1905-818055c2658d', 'epopescu', 'epopescu@ekg.local', 'Elena', 'Popescu', 'Elena Popescu', 'Analist Control Calitate', 'Control calitate', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4152', '20052', 'CN=Nicoleta Oprea,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Elena Popescu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2018-10-12 14:20:00+00', '2018-10-15 14:20:00+00', 9223372036854775807, 'elena.popescu@ekgpharma.ro', 'EVT-RO-2018-0016'),
('62371cff-559c-7450-8211-9f0ad8dcba96', 'istan', 'istan@ekg.local', 'Ioana', 'Stan', 'Ioana Stan', 'Analist Microbiologie', 'Control calitate', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4155', '20055', 'CN=Nicoleta Oprea,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Ioana Stan,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2020-02-14 14:20:00+00', '2020-02-17 14:20:00+00', 9223372036854775807, 'ioana.stan@ekgpharma.ro', 'EVT-RO-2020-0021'),
('d16f7c67-3bfa-b47e-3b45-28943a90c089', 'bionescu', 'bionescu@ekg.local', 'Bogdan', 'Ionescu', 'Bogdan Ionescu', 'Operator Producție Sterile', 'Producție sterile', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', NULL, '20058', 'CN=Vlad Georgescu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Bogdan Ionescu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2019-03-29 14:20:00+00', '2019-04-01 14:20:00+00', 9223372036854775807, NULL, 'EVT-RO-2019-0018'),
('77b643a4-3081-1409-9c86-3e1e875097d5', 'adinu', 'adinu@ekg.local', 'Alexandru', 'Dinu', 'Alexandru Dinu', 'Operator Producție Sterile', 'Laborator ser autolog', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', NULL, '20061', 'CN=Florin Stoica,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Alexandru Dinu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2020-07-03 14:20:00+00', '2026-08-03 10:12:00+00', 9223372036854775807, NULL, 'EVT-RO-2020-0023'),
('b3d8878c-7269-d02e-95f9-f22e69d753c1', 'cmarin', 'cmarin@ekg.local', 'Cătălina', 'Marin', 'Cătălina Marin', 'Specialist Laborator Ser Autolog', 'Laborator ser autolog', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', NULL, '20063', 'CN=Florin Stoica,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Catalina Marin,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2022-01-07 14:20:00+00', '2022-01-10 14:20:00+00', 9223372036854775807, NULL, 'EVT-RO-2022-0026'),
('a7b0bd32-830b-d550-9255-b8548230f1a2', 'vgeorgescu', 'vgeorgescu@ekg.local', 'Vlad', 'Georgescu', 'Vlad Georgescu', 'Șef de Tură Producție', 'Producție sterile', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4166', '20066', 'CN=Florin Stoica,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Vlad Georgescu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2016-09-02 14:20:00+00', '2016-09-05 14:20:00+00', 9223372036854775807, 'vlad.georgescu@ekgpharma.ro', 'EVT-RO-2016-0008'),
('e0e1544c-3252-f339-3e9f-349139f1ef61', 'renache', 'renache@ekg.local', 'Raluca', 'Enache', 'Raluca Enache', 'Specialist Asigurarea Calității', 'Asigurarea calității', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4169', '20069', 'CN=Nicoleta Oprea,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Raluca Enache,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2019-05-10 14:20:00+00', '2019-05-13 14:20:00+00', 9223372036854775807, 'raluca.enache@ekgpharma.ro', 'EVT-RO-2019-0019'),
('93dd42f8-d978-4690-0ece-857ddbf20f7a', 'dilie', 'dilie@ekg.local', 'Dan', 'Ilie', 'Dan Ilie', 'Operator Depozit și Expediții ADR', 'Depozit și logistică', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', NULL, '20072', 'CN=Ciprian Tudor,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Dan Ilie,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2018-03-16 14:20:00+00', '2018-03-19 14:20:00+00', 9223372036854775807, NULL, 'EVT-RO-2018-0014'),
('c4af9f05-7a64-4bea-6c5c-45b9f7d9d1be', 'onistor', 'onistor@ekg.local', 'Oana', 'Nistor', 'Oana Nistor', 'Contabil Furnizori', 'Financiar-contabilitate', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4175', '20075', 'CN=Mihaela Apostol,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Oana Nistor,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2021-01-29 14:20:00+00', '2021-02-01 14:20:00+00', 9223372036854775807, 'oana.nistor@ekgpharma.ro', 'EVT-RO-2021-0024'),
('644959cd-9e43-d828-3ff9-c58f6512b3a4', 'rstoian', 'rstoian@ekg.local', 'Radu', 'Stoian', 'Radu Stoian', 'Tehnician Mentenanță și Metrologie', 'Mentenanță și inginerie', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', NULL, '20078', 'CN=Marian Bucur,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Radu Stoian,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2017-11-17 14:20:00+00', '2017-11-20 14:20:00+00', 9223372036854775807, NULL, 'EVT-RO-2017-0012'),
('f41957f0-8498-2d93-a4d3-9608d7108b0a', 'gtoma', 'gtoma@ekg.local', 'Gabriela', 'Toma', 'Gabriela Toma', 'Responsabil Farmacovigilență', 'Afaceri de reglementare', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4181', '20081', 'CN=Adina Petre,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Gabriela Toma,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2022-09-09 14:20:00+00', '2022-09-12 14:20:00+00', 9223372036854775807, 'gabriela.toma@ekgpharma.ro', 'EVT-RO-2022-0027'),
('e1ef25e5-a542-1271-acd7-1f76179f5905', 'imoldovan', 'imoldovan@ekg.local', 'Irina', 'Moldovan', 'Irina Moldovan', 'Analist Control Calitate', 'Control calitate', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', '+40 21 318 4184', '20084', 'CN=Nicoleta Oprea,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Irina Moldovan,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2026-08-29 14:20:00+00', '2026-09-01 14:20:00+00', 9223372036854775807, 'irina.moldovan@ekgpharma.ro', 'EVT-RO-2026-0030'),
('e01c0c35-d5a4-dfd3-dfae-6941a58103ab', 'spavel', 'spavel@ekg.local', 'Ștefan', 'Pavel', 'Ștefan Pavel', 'Operator Producție Sterile', 'Producție sterile', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', NULL, '20086', 'CN=Vlad Georgescu,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Stefan Pavel,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 512, '2023-03-03 14:20:00+00', '2023-03-06 14:20:00+00', 9223372036854775807, NULL, 'EVT-RO-2023-0028'),
('8aadf84a-b789-12ab-d4c9-dcf35d558f0e', 'pneagu.ext', 'pneagu.ext@ekg.local', 'Paul', 'Neagu', 'Paul Neagu', 'Consultant Validare', 'Mentenanță și inginerie', 'EKG Pharmaceuticals S.R.L.', 'Fabrica București', NULL, 'C0012', 'CN=Marian Bucur,OU=Utilizatori,OU=Bucuresti,DC=ekg,DC=local', 'CN=Paul Neagu,OU=Externi,OU=Bucuresti,DC=ekg,DC=local', 512, '2026-06-12 14:20:00+00', '2026-06-15 14:20:00+00', 134431488000000000, 'paul.neagu.ext@ekgpharma.ro', 'EVT-RO-2026-0029'),
('784da46c-7e75-9361-1ef6-af89c9f59ff4', 'svc_sap_sso', 'svc_sap_sso@ekg.local', NULL, NULL, 'Cont serviciu SAP Kerberos', NULL, 'IT', 'EKG Pharmaceuticals S.R.L.', NULL, NULL, NULL, NULL, 'CN=svc_sap_sso,OU=Servicii,OU=Bucuresti,DC=ekg,DC=local', 66048, '2019-03-04 10:00:00+00', '2025-11-12 08:30:00+00', 9223372036854775807, NULL, NULL),
('ff874cbf-87bf-e4c2-4856-f84e4b776782', 'svc_mes_ldap', 'svc_mes_ldap@ekg.local', NULL, NULL, 'Cont serviciu Opcenter LDAP bind', NULL, 'IT', 'EKG Pharmaceuticals S.R.L.', NULL, NULL, NULL, NULL, 'CN=svc_mes_ldap,OU=Servicii,OU=Bucuresti,DC=ekg,DC=local', 66048, '2019-03-04 10:00:00+00', '2025-11-12 08:30:00+00', 9223372036854775807, NULL, NULL)
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS active_directory.ad_group (
  objectguid          uuid NOT NULL,
  samaccountname      varchar(64) NOT NULL,
  description         varchar(255),
  distinguishedname   varchar(255) NOT NULL,
  grouptype           integer NOT NULL,
  extensionattribute1 varchar(60),
  whencreated         timestamptz NOT NULL,
  CONSTRAINT ad_group_pk PRIMARY KEY (objectguid)
);
COMMENT ON TABLE active_directory.ad_group IS 'Security groups (extensionattribute1 = DATA-OWNER marks data ownership groups).';

INSERT INTO active_directory.ad_group (objectguid, samaccountname, description, distinguishedname, grouptype, extensionattribute1, whencreated) VALUES
('49133f95-b598-ba15-4bbc-58bd2b4ff874', 'GG-SAP-SSO', 'Autentificare unică SAP S/4HANA (Kerberos)', 'CN=GG-SAP-SSO,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, NULL, '2019-03-04 10:00:00+00'),
('c28eedb5-6687-3e80-c47e-b4c5c9d32ba8', 'GG-MES-Operatori', 'Opcenter MES - operatori producție', 'CN=GG-MES-Operatori,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, NULL, '2019-03-04 10:00:00+00'),
('09e01ebd-898c-436a-483a-8d24eb51b6f2', 'GG-MES-SerAutolog', 'Opcenter MES - laborator ser autolog', 'CN=GG-MES-SerAutolog,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, NULL, '2019-03-04 10:00:00+00'),
('eea5947f-8de4-6eb8-1790-bc3396cf7fe7', 'GG-MES-Supervizori', 'Opcenter MES - șefi de tură și verificare', 'CN=GG-MES-Supervizori,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, NULL, '2019-03-04 10:00:00+00'),
('12d91360-367f-d708-e7cf-d6b782894777', 'GG-LIMS-Analisti', 'LabWare LIMS - analiști CC', 'CN=GG-LIMS-Analisti,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, NULL, '2019-03-04 10:00:00+00'),
('91911c5f-c57a-1d57-04c4-1cd703dfe341', 'GG-LIMS-Aprobare', 'LabWare LIMS - aprobare rezultate și certificate', 'CN=GG-LIMS-Aprobare,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, NULL, '2019-03-04 10:00:00+00'),
('f26897c9-f4a6-2723-df39-eede0e6a18f1', 'GG-Empower-Analisti', 'Empower 3 - analiști cromatografie', 'CN=GG-Empower-Analisti,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, NULL, '2019-03-04 10:00:00+00'),
('ed31cf0b-ee82-e604-60aa-169a935ae8f1', 'GG-Maximo-Tehnicieni', 'Maximo - tehnicieni mentenanță', 'CN=GG-Maximo-Tehnicieni,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, NULL, '2019-03-04 10:00:00+00'),
('402757d9-e6e0-7c54-c51b-7e43c12cb581', 'GG-WMS-Depozit', 'WMS intern - operatori depozit', 'CN=GG-WMS-Depozit,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, NULL, '2019-03-04 10:00:00+00'),
('118aa8fd-7158-0b6e-6fa6-9fda25dd806d', 'GG-VPN-Acces', 'Acces VPN de la distanță', 'CN=GG-VPN-Acces,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, NULL, '2019-03-04 10:00:00+00'),
('fddf2dd1-d282-4065-cc7d-e860969947f3', 'DO-SAP-Furnizori', 'Proprietar date: fișa furnizori SAP', 'CN=DO-SAP-Furnizori,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, 'DATA-OWNER', '2019-03-04 10:00:00+00'),
('d2f33080-2b10-976e-846d-66185ee1a858', 'DO-LIMS-Rezultate', 'Proprietar date: rezultate de laborator', 'CN=DO-LIMS-Rezultate,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, 'DATA-OWNER', '2019-03-04 10:00:00+00'),
('436f0512-ee6e-d605-0089-a012db185fab', 'DO-Workday-Angajati', 'Proprietar date: fișa angajaților', 'CN=DO-Workday-Angajati,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, 'DATA-OWNER', '2019-03-04 10:00:00+00'),
('cc04ac17-b76d-8e59-9058-db6d72368a11', 'DO-MES-Loturi', 'Proprietar date: înregistrări de lot', 'CN=DO-MES-Loturi,OU=Grupuri,OU=Bucuresti,DC=ekg,DC=local', -2147483646, 'DATA-OWNER', '2019-03-04 10:00:00+00')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS active_directory.ad_group_member (
  group_objectguid        uuid NOT NULL,
  member_objectguid       uuid NOT NULL,
  originating_create_time timestamptz NOT NULL,
  originating_delete_time timestamptz,
  CONSTRAINT ad_group_member_pk PRIMARY KEY (group_objectguid, member_objectguid)
);
COMMENT ON TABLE active_directory.ad_group_member IS 'Group membership with linked-value replication metadata (create/delete times).';

INSERT INTO active_directory.ad_group_member (group_objectguid, member_objectguid, originating_create_time, originating_delete_time) VALUES
('49133f95-b598-ba15-4bbc-58bd2b4ff874', '045dae99-6feb-c23c-6a64-6c554233fe1e', '2019-03-04 10:00:00+00', NULL),
('49133f95-b598-ba15-4bbc-58bd2b4ff874', 'fd5db688-2aa5-ad4c-1bdb-64b17472267f', '2019-03-04 10:00:00+00', NULL),
('49133f95-b598-ba15-4bbc-58bd2b4ff874', '472541c9-257c-2010-80a1-bf3eb861e16b', '2019-03-04 10:00:00+00', NULL),
('49133f95-b598-ba15-4bbc-58bd2b4ff874', '9b7420e1-8120-a13e-f61b-d22e640d8722', '2019-03-04 10:00:00+00', NULL),
('49133f95-b598-ba15-4bbc-58bd2b4ff874', 'ecc3ac1b-6e5a-2229-3bce-b9f61344de99', '2019-03-04 10:00:00+00', NULL),
('49133f95-b598-ba15-4bbc-58bd2b4ff874', '2d862d58-984a-56eb-49c6-cd90b85f2d85', '2019-03-04 10:00:00+00', NULL),
('49133f95-b598-ba15-4bbc-58bd2b4ff874', 'c4af9f05-7a64-4bea-6c5c-45b9f7d9d1be', '2021-01-30 15:00:00+00', NULL),
('49133f95-b598-ba15-4bbc-58bd2b4ff874', '33e09dd2-a741-56e7-7446-b876308abb10', '2019-03-04 10:00:00+00', NULL),
('49133f95-b598-ba15-4bbc-58bd2b4ff874', '0e41f1a6-9a26-5ab9-aa52-c3e076d4e598', '2019-03-04 10:00:00+00', NULL),
('c28eedb5-6687-3e80-c47e-b4c5c9d32ba8', 'd16f7c67-3bfa-b47e-3b45-28943a90c089', '2019-03-30 15:00:00+00', NULL),
('c28eedb5-6687-3e80-c47e-b4c5c9d32ba8', 'e01c0c35-d5a4-dfd3-dfae-6941a58103ab', '2023-03-04 15:00:00+00', NULL),
('c28eedb5-6687-3e80-c47e-b4c5c9d32ba8', '77b643a4-3081-1409-9c86-3e1e875097d5', '2020-07-04 15:00:00+00', NULL),
('09e01ebd-898c-436a-483a-8d24eb51b6f2', 'b3d8878c-7269-d02e-95f9-f22e69d753c1', '2022-01-08 15:00:00+00', NULL),
('09e01ebd-898c-436a-483a-8d24eb51b6f2', '77b643a4-3081-1409-9c86-3e1e875097d5', '2026-08-03 10:12:00+00', NULL),
('eea5947f-8de4-6eb8-1790-bc3396cf7fe7', 'a7b0bd32-830b-d550-9255-b8548230f1a2', '2019-03-04 10:00:00+00', NULL),
('eea5947f-8de4-6eb8-1790-bc3396cf7fe7', 'e0e1544c-3252-f339-3e9f-349139f1ef61', '2019-05-11 15:00:00+00', NULL),
('12d91360-367f-d708-e7cf-d6b782894777', '8165e734-b1ef-9727-1905-818055c2658d', '2019-03-04 10:00:00+00', NULL),
('12d91360-367f-d708-e7cf-d6b782894777', '62371cff-559c-7450-8211-9f0ad8dcba96', '2020-02-15 15:00:00+00', NULL),
('12d91360-367f-d708-e7cf-d6b782894777', '812cbd24-40ad-155c-10bb-6b2ed6801250', '2019-08-31 15:00:00+00', NULL),
('12d91360-367f-d708-e7cf-d6b782894777', 'e1ef25e5-a542-1271-acd7-1f76179f5905', '2026-08-30 15:00:00+00', NULL),
('91911c5f-c57a-1d57-04c4-1cd703dfe341', '0e41f1a6-9a26-5ab9-aa52-c3e076d4e598', '2019-03-04 10:00:00+00', NULL),
('91911c5f-c57a-1d57-04c4-1cd703dfe341', 'e0e1544c-3252-f339-3e9f-349139f1ef61', '2019-05-11 15:00:00+00', NULL),
('f26897c9-f4a6-2723-df39-eede0e6a18f1', '8165e734-b1ef-9727-1905-818055c2658d', '2019-03-04 10:00:00+00', NULL),
('f26897c9-f4a6-2723-df39-eede0e6a18f1', '812cbd24-40ad-155c-10bb-6b2ed6801250', '2019-08-31 15:00:00+00', NULL),
('f26897c9-f4a6-2723-df39-eede0e6a18f1', 'e1ef25e5-a542-1271-acd7-1f76179f5905', '2026-08-30 15:00:00+00', NULL),
('ed31cf0b-ee82-e604-60aa-169a935ae8f1', '644959cd-9e43-d828-3ff9-c58f6512b3a4', '2019-03-04 10:00:00+00', NULL),
('ed31cf0b-ee82-e604-60aa-169a935ae8f1', '33e09dd2-a741-56e7-7446-b876308abb10', '2019-03-04 10:00:00+00', NULL),
('ed31cf0b-ee82-e604-60aa-169a935ae8f1', '8aadf84a-b789-12ab-d4c9-dcf35d558f0e', '2026-06-13 15:00:00+00', NULL),
('402757d9-e6e0-7c54-c51b-7e43c12cb581', '93dd42f8-d978-4690-0ece-857ddbf20f7a', '2019-03-04 10:00:00+00', NULL),
('402757d9-e6e0-7c54-c51b-7e43c12cb581', '2d862d58-984a-56eb-49c6-cd90b85f2d85', '2019-03-04 10:00:00+00', NULL),
('118aa8fd-7158-0b6e-6fa6-9fda25dd806d', '045dae99-6feb-c23c-6a64-6c554233fe1e', '2019-03-04 10:00:00+00', NULL),
('118aa8fd-7158-0b6e-6fa6-9fda25dd806d', 'fd5db688-2aa5-ad4c-1bdb-64b17472267f', '2019-03-04 10:00:00+00', NULL),
('118aa8fd-7158-0b6e-6fa6-9fda25dd806d', '6c61116c-2578-4582-7f91-7746cbbca2be', '2019-03-04 10:00:00+00', NULL),
('118aa8fd-7158-0b6e-6fa6-9fda25dd806d', 'ca219cb7-0113-272d-a9e3-4e147266bb35', '2019-03-04 10:00:00+00', NULL),
('118aa8fd-7158-0b6e-6fa6-9fda25dd806d', '73abb4ec-ed66-6d48-976e-b1b0985d4ae1', '2019-03-04 10:00:00+00', NULL),
('118aa8fd-7158-0b6e-6fa6-9fda25dd806d', 'efc5b107-a42f-2a58-777b-f12fdbef3893', '2020-02-29 15:00:00+00', NULL),
('118aa8fd-7158-0b6e-6fa6-9fda25dd806d', '8aadf84a-b789-12ab-d4c9-dcf35d558f0e', '2026-06-13 15:00:00+00', NULL),
('fddf2dd1-d282-4065-cc7d-e860969947f3', 'fd5db688-2aa5-ad4c-1bdb-64b17472267f', '2019-03-04 10:00:00+00', NULL),
('d2f33080-2b10-976e-846d-66185ee1a858', '0e41f1a6-9a26-5ab9-aa52-c3e076d4e598', '2019-03-04 10:00:00+00', NULL),
('436f0512-ee6e-d605-0089-a012db185fab', 'e90fe7a9-88e2-e5d1-2182-54ad529f4788', '2019-03-04 10:00:00+00', NULL),
('cc04ac17-b76d-8e59-9058-db6d72368a11', '472541c9-257c-2010-80a1-bf3eb861e16b', '2019-03-04 10:00:00+00', NULL)
ON CONFLICT DO NOTHING;

-- Attributes written by the Workday worker feed (subscription apply script buc_active_directory__worker_master_data).
ALTER TABLE active_directory.ad_user ADD COLUMN IF NOT EXISTS employeetype varchar(40);
ALTER TABLE active_directory.ad_user ADD COLUMN IF NOT EXISTS departmentnumber varchar(20);
ALTER TABLE active_directory.ad_user ADD COLUMN IF NOT EXISTS extensionattribute11 varchar(60);
ALTER TABLE active_directory.ad_user ADD COLUMN IF NOT EXISTS extensionattribute12 varchar(60);
COMMENT ON COLUMN active_directory.ad_user.employeetype IS 'employeeType: employee / contractor, from the Workday worker feed.';
COMMENT ON COLUMN active_directory.ad_user.departmentnumber IS 'departmentNumber: the Workday cost centre.';
COMMENT ON COLUMN active_directory.ad_user.extensionattribute11 IS 'Workday worker status (active, on leave, left YYYY-MM-DD); a leaver whose account is still enabled is picked up by the IAM deprovisioning review.';
COMMENT ON COLUMN active_directory.ad_user.extensionattribute12 IS 'Workday job profile of the primary position.';

GRANT USAGE ON SCHEMA active_directory TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA active_directory TO egeria_user, airflow_user;
