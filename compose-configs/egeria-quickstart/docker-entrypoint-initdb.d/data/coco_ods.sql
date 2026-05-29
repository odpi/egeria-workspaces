

DROP SEQUENCE IF EXISTS supplier_invoices_supplier_id_seq;
CREATE SEQUENCE supplier_invoices_supplier_id_seq INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1  NO CYCLE;
DROP SEQUENCE IF EXISTS supplier_invoices_supplier_id_seq1;
CREATE SEQUENCE supplier_invoices_supplier_id_seq1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1  NO CYCLE;
DROP TABLE IF EXISTS categories;
CREATE TABLE categories (category_id SMALLINT NOT NULL, category_name CHARACTER VARYING(15) NOT NULL, description TEXT, picture BYTEA, CONSTRAINT pk_categories PRIMARY KEY (category_id));
INSERT INTO categories (category_id, category_name, description, picture) VALUES 
(1000, 'OTC Pain', 'Over the counter pain medications', null),
(2000, 'ColdFlu', 'Over the counter cold and flu remedies', null),
(4000, 'BP', 'Prescription Blood Pressue Medications', null),
(3000, 'Allergy', 'Over the counter allergy medica6tions', null),
(5000, 'Chol', 'Prescription Cholesterol Lowering Medications', null),
(6000, 'PresBThin', 'Prescription Blood Thinners', null),
(7000, 'BonDen', 'Prescription Hormone Replacement Therapies', null),
(9000, 'TRIAL', 'Clinical Trial Controlled Prescriptions', null);
DROP TABLE IF EXISTS coco_locations;
CREATE TABLE coco_locations (location_id NUMERIC DEFAULT 0 NOT NULL, location_name CHARACTER VARYING(50) NOT NULL, building_name CHARACTER VARYING(50), street_number NUMERIC, street_name CHARACTER VARYING(50), district CHARACTER VARYING(50), city CHARACTER VARYING(50), area CHARACTER VARYING(30), country CHARACTER VARYING(50));
INSERT INTO coco_locations (location_id, location_name, building_name, street_number, street_name, district, city, area, country) VALUES 
(1, 'Amsterdam', null, 1833, 'Wilhelmdreef', 'Amsterdam-Zuidoost', 'Amsterdam', 'North Holland', 'Netherlands'),
(2, 'London', null, 32, 'Wibble Rd', 'Corterville', 'London', 'Greater London', 'United Kingdon'),
(3, 'New York', null, 27, 'Code St', 'Harlem', 'New York', 'NY', 'United States'),
(4, 'Hampton Hospital', 'Oncology Unit 1, Hampton Hospital', null, 'Nightingale St', 'Harlem', 'New York', 'NY', 'United States'),
(5, 'Austin', null, 10000, '38th St', 'Austin', 'Austin', 'TX', 'United States'),
(6, 'Winchester', null, 1, 'Eagles Nest', 'Winchester', 'Hampshire', 'Winchester', 'United Kingdom'),
(7, 'Kansas City', 'Coco Distribution Center', 1200, 'Industrial Parkway', 'Industrial Park', 'Kansas City', 'KS', 'United States'),
(8, 'Edmonton', null, 10828, '102 Ave NW', null, 'Edmonton', 'Alberta', 'Canada'),
(9, 'Bucharest', null, 500, 'Calea Victoriei', 'Sector 1', 'Bucharest', 'Bucharest', 'Romania');
DROP TABLE IF EXISTS customer_customer_demo;
CREATE TABLE customer_customer_demo (customer_id CHARACTER(1) NOT NULL, customer_type_id CHARACTER(1) NOT NULL, CONSTRAINT pk_customer_customer_demo PRIMARY KEY (customer_id, customer_type_id));
DROP TABLE IF EXISTS customer_demographics;
CREATE TABLE customer_demographics (customer_type_id CHARACTER(1) NOT NULL, customer_desc TEXT, CONSTRAINT pk_customer_demographics PRIMARY KEY (customer_type_id));
DROP TABLE IF EXISTS customer_travel;
CREATE TABLE customer_travel (company_name CHARACTER VARYING(40), customer_city CHARACTER VARYING(15), ofc CHARACTER VARYING(15), last_name CHARACTER VARYING(20), distance NUMERIC, travel_type TEXT, emissions NUMERIC, "date" DATE);
INSERT INTO customer_travel (company_name, customer_city, ofc, last_name, distance, travel_type, emissions, date) VALUES 
('Around the Horn', 'London', 'Corterville', 'Salle', null, 'Public', null, '2022-03-11'),
('Great Lakes Market', 'Eugene', 'Harlem', 'Hopeful', null, 'Air', 362, '2022-03-10'),
('RainForest Medical Resources', 'Elgin', 'Harlem', 'Deal', null, 'Air', 182, '2022-03-24'),
('Island Pharmacy', 'Cowes', 'Corterville', 'Salle', null, 'Car', null, '2022-03-14'),
('Natural Remedies', 'London', 'Corterville', 'Salle', null, 'Public', null, '2022-03-24'),
('Cut Price Meds', 'London', 'Corterville', 'Salle', null, 'Public', null, '2022-03-28'),
('A Shot in the Arm', 'London', 'Corterville', 'Salle', null, 'Public', null, '2022-04-05'),
('Lazy K CBD', 'Walla Walla', 'Harlem', 'Deal', null, 'Air', 300, '2022-04-11'),
('Hippy Drug Store', 'San Francisco', 'Harlem', 'Hopeful', null, 'Air', 348, '2022-05-02'),
('Lonesome Pine Brewery and Pharmacy', 'Portland', 'Harlem', 'Deal', null, 'Air', 250, '2022-05-16'),
('Gap Medical', 'London', 'Corterville', 'Salle', null, 'Public', null, '2022-04-05'),
('Old World Pharamcy', 'Anchorage', 'Harlem', 'Deal', null, 'Air', 386, '2022-06-06'),
('Rattlesnake Canyon Medicines', 'Albuquerque', 'Harlem', 'Hopeful', null, 'Air', 227, '2022-06-13'),
('Save-a-lot Medical', 'Boise', 'Harlem', 'Deal', null, 'Air', 301, '2022-06-27'),
('Seven Seas Solutions', 'London', 'Corterville', 'Salle', null, 'Public', null, '2022-06-06'),
('Split Rail Chemists', 'Lander', 'Harlem', 'Deal', null, 'Air', 294, '2022-06-20'),
('The Big Prescription', 'Portland', 'Harlem', 'Hopeful', null, 'Air', 250, '2022-07-11'),
('The Crack Box', 'Butte', 'Harlem', 'Deal', null, 'Air', 289, '2022-07-25'),
('Trail''s Head Gourmet Drugs', 'Kirkland', 'Harlem', 'Deal', null, 'Air', 230, '2022-08-01'),
('White Clover Medicinals', 'Seattle', 'Harlem', 'Hopeful', null, 'AIr', 245, '2022-08-15');
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (customer_id CHARACTER VARYING(20) NOT NULL, company_name CHARACTER VARYING(40) NOT NULL, contact_name CHARACTER VARYING(30), contact_title CHARACTER VARYING(30), address CHARACTER VARYING(60), city CHARACTER VARYING(15), region CHARACTER VARYING(15), postal_code CHARACTER VARYING(10), country CHARACTER VARYING(15), phone CHARACTER VARYING(24), fax CHARACTER VARYING(24), CONSTRAINT pk_customers PRIMARY KEY (customer_id));
INSERT INTO customers (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) VALUES 
('AROUT', 'Around the Horn', 'Julian and Sandy', 'Sales Representative', '120 Hanover Sq.', 'London', null, 'WA1 1DP', 'UK', '(171) 555-7788', '(171) 555-6750'),
('GREAL', 'Great Lakes Market', 'Ander D Counter', 'General Manager', '2732 Baker Blvd.', 'Eugene', 'OR', '97403', 'USA', '(503) 555-7555', null),
('RUMOUR', 'RainForest Medical Resources', 'Yoshi Latimer', 'Pharmacy Manager', 'City Center Plaza 516 Main St.', 'Elgin', 'OR', '97827', 'USA', '(503) 555-6874', '(503) 555-2376'),
('ISLAT', 'Island Pharmacy', 'Gordon Bennett', 'Pharmacy Manager', 'Garden House Crowther Way', 'Cowes', 'Isle of Wight', 'PO31 7PJ', 'UK', '(198) 555-8888', null),
('NATR', 'Natural Remedies', 'Fergus Fungi', 'Sales Representative', 'Fauntleroy Circus', 'London', null, 'EC2 5NT', 'UK', '(171) 555-1212', null),
('3RDMAN', 'Cut Price Meds', 'Harry Lime', 'Sales Representative', 'Berkeley Gardens 12  Brewery', 'London', null, 'WX1 6LT', 'UK', '(171) 555-2282', '(171) 555-9199'),
('ASIA', 'A Shot in the Arm', 'Hypo Dermic', 'Chief Pharmacist', '35 King George', 'London', null, 'WX3 6FW', 'UK', '(171) 555-0297', '(171) 555-3373'),
('LAZYK', 'Lazy K CBD', 'John Steel', 'Pharmacist', '12 Orchestra Terrace', 'Walla Walla', 'WA', '99362', 'USA', '(509) 555-7969', '(509) 555-6221'),
('HIPS', 'Hippy Drug Store', 'Jaime Yorres', 'Owner', '87 Polk St. Suite 5', 'San Francisco', 'CA', '94117', 'USA', '(415) 555-5938', null),
('LONEP', 'Lonesome Pine Brewery and Pharmacy', 'Tim E Leer', 'Manager', '89 Chiaroscuro Rd.', 'Portland', 'OR', '97219', 'USA', '(503) 555-9573', '(503) 555-9646'),
('GAPM', 'Gap Medical', 'Cumberland Gap', 'Buyer', 'South House 300 Queensbridge', 'London', null, 'SW7 1RZ', 'UK', '(171) 555-7733', '(171) 555-2530'),
('OLDY', 'Old World Pharamcy', 'Golda Mine', 'Pharmacist, Assayer', '2743 Bering St.', 'Anchorage', 'AK', '99508', 'USA', '(907) 555-7584', '(907) 555-2880'),
('RATTC', 'Rattlesnake Canyon Medicines', 'N Diamond', 'Pharmacist', '2817 Milton Dr.', 'Albuquerque', 'NM', '87110', 'USA', '(505) 555-5939', '(505) 555-3620'),
('SAVEA', 'Save-a-lot Medical', 'Jose Pavarotti', 'Owner', '187 Suffolk Ln.', 'Boise', 'ID', '83720', 'USA', '(208) 555-8097', null),
('SEVES', 'Seven Seas Solutions', 'Hari Kari', 'Pharmacy Buyer', '90 Wadhurst Rd.', 'London', null, 'OX15 4NB', 'UK', '(171) 555-1717', '(171) 555-5646'),
('SPLIR', 'Split Rail Chemists', 'Art Braunschweiger', 'Chief Buyer', 'P.O. Box 555', 'Lander', 'WY', '82520', 'USA', '(307) 555-4680', '(307) 555-6525'),
('THEBI', 'The Big Prescription', 'Letitia S Down', 'Owner', '89 Jefferson Way Suite 2', 'Portland', 'OR', '97201', 'USA', '(503) 555-3612', null),
('THECR', 'The Crack Box', 'Liu Wong', 'Pharmacist', '55 Grizzly Peak Rd.', 'Butte', 'MT', '59801', 'USA', '(406) 555-5834', '(406) 555-8083'),
('TRAIH', 'Trail''s Head Gourmet Drugs', 'Helvetius Nagy', 'Customer Service Manager', '722 DaVinci Blvd.', 'Kirkland', 'WA', '98034', 'USA', '(206) 555-8257', '(206) 555-2174'),
('WHITC', 'White Clover Medicinals', 'Karl Jablonski', 'Owner', '305 - 14th Ave. S. Suite 3B', 'Seattle', 'WA', '98128', 'USA', '(206) 555-4112', '(206) 555-4115');
DROP TABLE IF EXISTS employee_territories;
CREATE TABLE employee_territories (employee_id SMALLINT NOT NULL, territory_id CHARACTER VARYING(20) NOT NULL, CONSTRAINT pk_employee_territories PRIMARY KEY (employee_id, territory_id));
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (employee_id NUMERIC NOT NULL, last_name CHARACTER VARYING(20) NOT NULL, first_name CHARACTER VARYING(10) NOT NULL, title CHARACTER VARYING(30), title_of_courtesy CHARACTER VARYING(25), birth_date DATE, hire_date DATE, address CHARACTER VARYING(60), city CHARACTER VARYING(15), region CHARACTER VARYING(15), postal_code CHARACTER VARYING(10), country CHARACTER VARYING(15), home_phone CHARACTER VARYING(24), extension CHARACTER VARYING(4), photo BYTEA, notes TEXT, reports_to SMALLINT, photo_path CHARACTER VARYING(255), job_description CHARACTER VARYING(20), location_code INTEGER, mobile_phone CHARACTER VARYING(20), work_phone CHARACTER VARYING(20), employee_status CHARACTER VARYING(2), employee_level INTEGER, department INTEGER, leaving_date DATE, rehire CHARACTER VARYING(2), prior_service_credit NUMERIC, CONSTRAINT pk_employees PRIMARY KEY (employee_id));
INSERT INTO employees (employee_id, last_name, first_name, title, title_of_courtesy, birth_date, hire_date, address, city, region, postal_code, country, home_phone, extension, photo, notes, reports_to, photo_path, job_description, location_code, mobile_phone, work_phone, employee_status, employee_level, department, leaving_date, rehire, prior_service_credit) VALUES 
(921848, 'Leftie', 'Reddy', 'Procurement Manager', 'Mr', '1968-09-02', '2021-01-01', '32 Wibble Rd', 'Corterville', '1', null, 'UK', null, null, null, null, null, null, 'Procurement', 2, null, null, 'L', 3, 6877, '2021-05-15', 'N', null),
(338575, 'Tasker', 'Polly', 'IT Project Leader', 'Ms', '1979-11-11', '2022-04-01', '32 Wibble Rd', 'Corterville', '1', null, 'Netherland', null, null, null, null, null, null, null, 1, null, null, 'A', 7, 2373, null, null, null),
(296776, 'Keeper', 'Jules', 'Chief Data Officer', 'Dr', '1998-07-09', '2022-03-01', '32 Wibble Rd', 'Corterville', '1', null, 'UK', null, null, null, null, null, null, null, 2, null, null, 'A', 8, 5656, null, null, null),
(896522, 'Tally', 'Tom', 'AC Manager, Fin HQ', 'Mr', '1998-05-13', '2020-07-10', '32 Wibble Rd', 'Corterville', '1', null, 'UK', null, null, null, null, null, null, null, 2, null, null, 'A', 7, 6788, null, null, null),
(209482, 'Tidy', 'Tanya', 'Data Steward', 'Dr', '2000-04-26', '2015-04-01', '27 Code St', 'Harlem', '2', null, 'USA', null, null, null, null, null, null, null, 3, null, null, 'A', 2, 4051, null, null, null),
(139870, 'Broker', 'Faith', 'HR & Compliance Dir', 'Ms', '1996-12-03', '2018-02-01', '1833 Wilhelmdreef', 'Amsterdam', '1', null, 'Netherland', null, null, null, null, null, null, null, 1, null, null, 'A', 8, 2373, null, null, null),
(457911, 'Counter', 'Sally', 'Payment Clerk', 'Ms', '2001-02-10', '2012-05-01', '32 Wibble Rd', 'Corterville', '1', null, 'UK', null, null, null, null, null, null, null, 2, null, null, 'A', 2, 6877, null, null, null),
(818928, 'Stage', 'Lemmie', 'DataStage Specialist', 'Mr', '2001-05-10', '2019-05-01', '1833 Wilhelmdreef', 'Amsterdam', '1', null, 'Netherland', null, null, null, null, null, null, null, 1, null, null, 'A', 4, 3082, null, null, null),
(144994, 'Hopeful', 'Harry', 'Sales Specialist, NY', 'Mr', '1995-09-15', '2012-05-01', '27 Code St', 'Harlem', '2', null, 'USA', null, null, null, null, null, null, null, 3, null, null, 'A', 6, 2343, null, null, null),
(324713, 'Overview', 'Erin', 'Information Architect', 'Ms', '2000-09-03', '2019-05-01', '32 Wibble Rd', 'Corterville', '1', null, 'UK', null, null, null, null, null, null, null, 2, null, null, 'A', 7, 7432, null, null, null),
(199995, 'Geeke', 'Gary', 'IT Infrstructure Lead', 'Mr', '2000-10-01', '2020-05-01', '1833 Wilhelmdreef', 'Amsterdam', '1', null, 'Netherland', null, null, null, null, null, null, null, 1, null, null, 'A', 6, 3082, null, null, null),
(986419, 'Profile', 'Peter', 'Information Analyst', 'Mr', '2001-06-15', '2015-05-01', '32 Wibble Rd', 'Corterville', '1', null, 'UK', null, null, null, null, null, null, null, 2, null, null, 'A', 5, 7432, null, null, null),
(328080, 'Quartile', 'Callie', 'Data Scientist', 'Dr', '1995-01-01', '2012-03-01', '27 Code St', 'Harlem', '2', null, 'USA', null, null, null, null, null, null, null, 3, null, null, 'A', 5, 4051, null, null, null),
(133777, 'Now', 'Zac', 'Founder', 'Dr', '1990-10-11', '2010-01-01', '27 Code St.', 'Harlem', '2', null, 'USA', null, null, null, null, null, null, null, 3, null, null, 'A', 9, 9999, null, null, null),
(439222, 'Starter', 'Steve', 'Founder', 'Mr', '1992-07-10', '2010-01-01', '1833 Wilhelmdreef', 'Amsterdam', '1', null, 'Netherland', null, null, null, null, null, null, null, 1, null, null, 'A', 9, 9999, null, null, null),
(371803, 'Daring', 'Terri', 'Founder', 'Ms', '1995-01-10', '2010-01-01', '32 Wibble Rd', 'Corterville', '1', null, 'UK', null, null, null, null, null, null, null, 2, null, null, 'A', 9, 9999, null, null, null),
(302145, 'Tube', 'Tessa', 'Lead Researcher', 'Dr', '1998-07-15', '2010-10-10', '27 Code St', 'Harlem', '2', null, 'USA', null, null, null, null, null, null, null, 3, null, null, 'A', 7, 2343, null, null, null),
(188888, 'Mint', 'Reggie', 'CFO', 'Mr', '1994-08-31', '2018-01-01', '32 Wibble Rd', 'Corterville', '1', null, 'UK', null, null, null, null, null, null, null, 2, null, null, 'A', 8, 5656, null, null, null),
(549922, 'Zeller', 'Maura', 'Sales', 'Dr', '1985-02-14', '2012-01-01', '1833 Wilhelmdreef', 'Amsterdam', '1', null, 'Netherland', null, null, null, null, null, null, 'Sales', 1, null, null, 'A', 7, 7432, null, null, null),
(254678, 'Salle', 'Hugo', 'Sales', 'Mr', '1989-06-10', '2013-02-01', '32 Wibble Rd', 'Corterville', '1', null, 'UK', null, null, null, null, null, null, 'Sales', 1, null, null, 'A', 7, 7432, null, null, null),
(549032, 'Deal', 'Margo', 'Sales', 'Ms', '1995-09-14', '2016-01-01', '27 Code St.', 'Harlem', '2', null, 'USA', null, null, null, null, null, null, 'Sales', 2, null, null, 'A', 7, 7432, null, null, null);
DROP TABLE IF EXISTS order_details;
CREATE TABLE order_details (order_id SMALLINT NOT NULL, product_id SMALLINT NOT NULL, unit_price REAL NOT NULL, quantity SMALLINT NOT NULL, discount REAL NOT NULL, CONSTRAINT pk_order_details PRIMARY KEY (order_id, product_id));
INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount) VALUES 
(10, 2050, 30.0, 5, 5.0),
(10, 3000, 50.0, 2, 0.0),
(10, 1000, 10.0, 100, 7.0),
(90, 1010, 25.0, 25, 7.0),
(90, 1000, 25.0, 10, 2.5);
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (order_id SMALLINT NOT NULL, customer_id CHARACTER VARYING(20), employee_id NUMERIC, order_date DATE, required_date DATE, shipped_date DATE, ship_via SMALLINT, freight REAL, ship_name CHARACTER VARYING(40), ship_address CHARACTER VARYING(60), ship_city CHARACTER VARYING(15), ship_region CHARACTER VARYING(15), ship_postal_code CHARACTER VARYING(10), ship_country CHARACTER VARYING(15), CONSTRAINT pk_orders PRIMARY KEY (order_id));
INSERT INTO orders (order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country) VALUES 
(10, 'AROUT', 144994, '2022-06-01', '2022-06-10', '2022-06-06', 4, null, 'Julian', '120 Hanover Square', 'London', '1', 'WA1 1DP', 'UK'),
(90, 'THECR', 144994, '2022-05-22', '2022-07-01', null, 2, null, 'Liu Wong', '55 Grizzly Peak Rd.', 'Butte', '2', '59801', 'USA');
DROP TABLE IF EXISTS products;
CREATE TABLE products (product_id SMALLINT NOT NULL, product_name CHARACTER VARYING(40) NOT NULL, supplier_id SMALLINT, category_id SMALLINT, quantity_per_unit CHARACTER VARYING(20), unit_price REAL, units_in_stock SMALLINT, units_on_order SMALLINT, reorder_level SMALLINT, discontinued INTEGER NOT NULL, unit_dosage CHARACTER VARYING(10), replacement CHARACTER VARYING(40), CONSTRAINT pk_products PRIMARY KEY (product_id));
INSERT INTO products (product_id, product_name, supplier_id, category_id, quantity_per_unit, unit_price, units_in_stock, units_on_order, reorder_level, discontinued, unit_dosage, replacement) VALUES 
(4010, 'Toprol-XL', 3000, 6000, '30', 40.0, 0, 10, 8, 0, '25mg', null),
(1000, 'Asprin', 1000, 1000, '250', 10.0, 10000, 100, 500, 0, '81mg', null),
(1010, 'Asprin', 1000, 1000, '250', 25.0, 500, 0, 25, 0, '250mg', null),
(2050, 'Plavix', 2000, 5000, '30', 20.0, 100, 0, 5, 0, '75mg', null),
(2000, 'Norvasc', 3000, 6000, '30', 40.0, 100, 10, 10, 0, '10mg', null),
(2010, 'Norvasc', 3000, 6000, '30', 30.0, 80, 8, 10, 0, '5mg', null),
(3000, 'Cozaar', 2000, 5000, '30', 50.0, 50, 10, 10, 0, '100mg', null),
(4000, 'Toprol-XL', 3000, 6000, '30', 65.0, 20, 5, 5, 0, '50mg', null),
(5000, 'Crestor', 1000, 5000, '30', 15.0, 250, 0, 20, 0, '5mg', null),
(9000, 'Cisplatin', 2000, 9000, '25', 120.0, 50, 0, 2, 0, '50mg', null);
DROP TABLE IF EXISTS region;
CREATE TABLE region (region_id SMALLINT NOT NULL, region_description CHARACTER VARYING(30) NOT NULL, CONSTRAINT pk_region PRIMARY KEY (region_id));
INSERT INTO region (region_id, region_description) VALUES 
(1, 'Europe, Middle East'),
(2, 'North America'),
(3, 'Asia Pacifric'),
(4, 'South and Central America'),
(5, 'Africa'),
(6, 'India Region');
DROP TABLE IF EXISTS shippers;
CREATE TABLE shippers (shipper_id SMALLINT NOT NULL, company_name CHARACTER VARYING(40) NOT NULL, phone CHARACTER VARYING(24), CONSTRAINT pk_shippers PRIMARY KEY (shipper_id));
INSERT INTO shippers (shipper_id, company_name, phone) VALUES 
(1, 'Speedy Express', '(503) 555-9831'),
(2, 'United Package', '(503) 555-3199'),
(3, 'Federal Shipping', '(503) 555-9931'),
(4, 'Alliance Shippers', '1-800-222-0451'),
(5, 'UPS', '1-800-782-7892'),
(6, 'DHL', '1-800-225-5345');
DROP TABLE IF EXISTS sites;
CREATE TABLE sites (site_id SMALLINT NOT NULL, site_name CHARACTER VARYING(50) NOT NULL, country CHARACTER VARYING(25) NOT NULL, mfg_area NUMERIC, mfg_kwh NUMERIC, rsch_area NUMERIC, rsch_kwh NUMERIC, ofc_area NUMERIC, ofc_kwh NUMERIC, dat_area NUMERIC, data_kwh NUMERIC, dep_area NUMERIC, dep_kwh NUMERIC, total_area NUMERIC, num_workers SMALLINT, num_vehicles SMALLINT, region CHARACTER VARYING(25));
COMMENT ON TABLE sites IS 'Information about each site';
COMMENT ON COLUMN sites.site_id IS 'Unique ID of a site';
COMMENT ON COLUMN sites.country IS 'The country the site is in';
COMMENT ON COLUMN sites.mfg_area IS 'measured in square feet';
COMMENT ON COLUMN sites.rsch_area IS 'measured in square feet';
COMMENT ON COLUMN sites.ofc_area IS 'measured in square feet';
COMMENT ON COLUMN sites.dat_area IS 'measured in square feet';
COMMENT ON COLUMN sites.dep_area IS 'measured in square feet';
COMMENT ON COLUMN sites.total_area IS 'measured in square feet';
INSERT INTO sites (site_id, site_name, country, mfg_area, mfg_kwh, rsch_area, rsch_kwh, ofc_area, ofc_kwh, dat_area, data_kwh, dep_area, dep_kwh, total_area, num_workers, num_vehicles, region) VALUES 
(1, 'Amsterdam', 'NL', 0, 0, 5000, 250000, 5000, 75000, 500, 300000, 1000, 12000, 12000, 50, null, 'Netherlands'),
(2, 'London', 'UK', 0, 0, 3000, 150000, 5000, 75000, 0, 0, 0, 0, 8000, 32, null, 'UK'),
(3, 'New York', 'US', 0, 0, 4000, 200000, 5000, 75000, 1000, 600000, 0, 0, 10000, 30, null, 'USA'),
(6, 'Winchester', 'UK', 20000, 1400000, 0, 0, 7000, 105000, 1000, 600000, 12000, 144000, 40000, 60, null, 'UK'),
(7, 'Kansas CIty', 'US', 0, 0, 0, 0, 1500, 22500, 0, 0, 18500, 222000, 20000, 10, null, 'USA'),
(8, 'Edmonton', 'CA', 20000, 1400000, 0, 0, 6000, 90000, 1000, 600000, 13000, 156000, 30000, 30, null, 'Alberta'),
(9, 'Bucharest', 'RO', 6000, 420000, 0, 0, 6000, 70000, 0, 0, 0, 0, 12000, 25, null, 'Romania'),
(5, 'Austin', 'US', 4500, 315000, 0, 0, 5000, 75000, 500, 300000, 0, 0, 10000, 30, null, 'ERCOT');
DROP TABLE IF EXISTS supplier_invoice_details;
CREATE TABLE supplier_invoice_details (invoice_number NUMERIC NOT NULL, line_number NUMERIC NOT NULL, product_id NUMERIC, dedlivery_date DATE NOT NULL, quantity_received NUMERIC NOT NULL, item_amount MONEY NOT NULL);
DROP TABLE IF EXISTS supplier_invoices;
CREATE TABLE supplier_invoices (supplier_id SMALLINT DEFAULT nextval('supplier_invoices_supplier_id_seq1'::regclass) NOT NULL, supply_order_number NUMERIC NOT NULL, invoice_amount MONEY NOT NULL, invoice_number NUMERIC NOT NULL, invoice_date DATE NOT NULL);
INSERT INTO supplier_invoices (supplier_id, supply_order_number, invoice_amount, invoice_number, invoice_date) VALUES 
(4000, 1234, '$100,000.00', 10, '2022-06-01'),
(4000, 1235, '$120,000.00', 10, '2022-07-01'),
(4000, 1236, '$98,000.00', 10, '2022-08-01'),
(4000, 1001, '$80,000.00', 10, '2022-05-01'),
(4000, 1000, '$50,000.00', 10, '2022-04-01');
DROP TABLE IF EXISTS suppliers;
CREATE TABLE suppliers (supplier_id SMALLINT NOT NULL, company_name CHARACTER VARYING(40) NOT NULL, contact_name CHARACTER VARYING(30), contact_title CHARACTER VARYING(30), address CHARACTER VARYING(60), city CHARACTER VARYING(15), region CHARACTER VARYING(15), postal_code CHARACTER VARYING(10), country CHARACTER VARYING(15), phone CHARACTER VARYING(24), fax CHARACTER VARYING(24), homepage TEXT, CONSTRAINT pk_suppliers PRIMARY KEY (supplier_id));
INSERT INTO suppliers (supplier_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax, homepage) VALUES 
(7000, 'BASE', 'Gretta Grunt', 'Sales Biologist', 'Am Wiesenhang 30,', 'Berlin', '1', '82396', 'Germany', '49-30-77-461-5846', null, null),
(8000, 'Lushplanet', 'Felicity Flower', 'Botanical Sales', '2915 Kazi St', 'Jonesboro', '2', '72401', 'USA', '1-870-934-8394', null, null),
(9000, 'Worldwide Excipients', 'Pakit Fuller', 'Sales', '81 Central Market', 'Mumbai', '6', '110052', 'India', '91-385-821-0056', null, null),
(1000, 'Generic Medicines Ltd', 'Peter Pill', 'Sales', '1000 Saville Row', 'London', '1', 'EC1 4SD', 'UK', '44-171-555-2222', null, null),
(2000, 'Texas Tablets', 'Tex Roper', 'Sales Representative', '1000 Congress Dr', 'Austin', '2', '78700', 'USA', '1-512-555-2223', null, null),
(3000, 'Groote Generics', 'Oom Poul', 'President', '1000 Kruger Straat', 'Amsterdam', '1', '1011 NK', 'Netherland', '31-20-555-2224', null, null),
(4000, 'Worldwide Fleet Supplies', 'Grady Gas', 'Client Executive', '999 Refinery Ln', 'Houston', '2', '77001', 'USA', '1-281-555-6789', null, null),
(5000, 'Amazon Botanicals', 'Hibisco Flor', 'Pharma Supplies Rep', 'Rua Felicity Flores', 'Rio De Janeiro', '4', '23060-0987', 'Brazil', '55-215-140-5555', null, null),
(6000, 'Southern Gas and Electric', 'Patsy Power', 'Commercial Sales', '99 Generator Place', 'Manchester', '1', 'NH 03100', 'UK', '44-161-555-4321', null, null),
(6001, 'NLE', 'Piet Power', 'Client Sales', 'Reguliersdwarstraat', 'Amsterdam', '1', '1017 BM', 'Netherland', '31-88-730-67307', null, null),
(6002, 'Austin Energy', 'Tex Power', 'Commercial Accounts Executive', '2 Kramer Lane', 'Austin', '2', '78758', 'USA', '1-512-494-9400', null, null),
(10000, 'Petes Office Supplies', 'Peter Piper', 'Commercial Sales Manager', 'Hamnterinalen 58a', 'Nynashamn', '1', '149 30', 'Sweden', '08-670-29-41', null, null);
DROP TABLE IF EXISTS supplies;
CREATE TABLE supplies (supply_id NUMERIC, supply_name CHARACTER VARYING(40), supplier_id NUMERIC, volume_units NUMERIC, units_on_hand NUMERIC, reorder_level NUMERIC, unit_type CHARACTER VARYING(20));
INSERT INTO supplies (supply_id, supply_name, supplier_id, volume_units, units_on_hand, reorder_level, unit_type) VALUES 
(20, 'Plastic Pill Bottles', 1000, 100, 2000, 2000, 'Cases'),
(21, 'Glass Vials', 1000, 100, 500, 500, 'Cases'),
(22, 'Aluminum Foil', 1000, 500, 20000, 20000, 'Meters'),
(23, 'Cotton Wool', 1000, 100, 1000, 1000, 'Kilograms'),
(24, 'Cardboard Shipping Boxes', 1000, 100, 1000, 2000, 'Cases'),
(40, 'cephalexin', 7000, 10, 25, 25, 'Kilograms'),
(41, 'penicillin', 7000, 500, 2000, 1500, 'Kilograms'),
(42, 'Ampicillin', 7000, 100, 400, 250, 'Kilograms'),
(50, 'Botanical supplies', 8000, 1, 5, 3, 'Cases'),
(30, 'Polymers', 1000, 5, 250, 200, 'Metric Tonnes'),
(71, 'Office Supplies', 10000, null, null, null, 'Various'),
(11001, 'Power Supply UK', 6000, null, null, null, 'Monthly KWH'),
(11002, 'Power Supply Netherland', 6001, null, null, null, 'Monthly KWH'),
(11003, 'Power Supply Austin', 6002, null, null, null, 'Monthly KWH'),
(10, 'Gasoline USA', 4000, 1, 500, 500, 'US Galons'),
(11, 'Diesel USA', 4000, 1, 750, 750, 'US Galons'),
(12, 'Petroleum Netherland', 4000, 1, 1000, 1000, 'Liters'),
(13, 'Diesel Netherland', 4000, 1, 800, 800, 'Liters'),
(70, 'Computer Paper', 10000, 10, 200, 250, 'Boxes');
DROP TABLE IF EXISTS supply_order_details;
CREATE TABLE supply_order_details (supply_order_number NUMERIC NOT NULL, product_id NUMERIC NOT NULL, unit_price MONEY NOT NULL, supply_order_qty NUMERIC NOT NULL, item_total_price MONEY NOT NULL);
INSERT INTO supply_order_details (supply_order_number, product_id, unit_price, supply_order_qty, item_total_price) VALUES 
(9001, 10, '$3.00', 5000, '$15,000.00'),
(9001, 11, '$3.50', 2000, '$7,000.00');
DROP TABLE IF EXISTS supply_orders;
CREATE TABLE supply_orders (supply_order_number NUMERIC, supply_id NUMERIC, employee_id NUMERIC, order_date DATE, requested_delivery_date DATE, ship_to_address CHARACTER VARYING(32), supplier_reference CHARACTER VARYING(20));
INSERT INTO supply_orders (supply_order_number, supply_id, employee_id, order_date, requested_delivery_date, ship_to_address, supplier_reference) VALUES 
(1001, 10, 896552, '2022-04-01', '2022-04-15', '1200 Industrial Parkway', 'Monthly_Gasoline'),
(1000, 10, 896552, '2022-03-01', '2022-03-15', '1200 Industrial Parkway', 'Monthly_Gasoline');
DROP TABLE IF EXISTS territories;
CREATE TABLE territories (territory_id CHARACTER VARYING(20) NOT NULL, territory_description CHARACTER VARYING(40) NOT NULL, region_id SMALLINT NOT NULL, CONSTRAINT pk_territories PRIMARY KEY (territory_id));
INSERT INTO territories (territory_id, territory_description, region_id) VALUES 
('01730', 'Bedford', 1),
('02139', 'Cambridge', 1),
('02184', 'Braintree', 1),
('06897', 'Wilton', 1),
('60179', 'Hoffman Estates', 2),
('60601', 'Chicago', 2),
('80202', 'Denver', 2),
('80909', 'Colorado Springs', 2),
('85014', 'Phoenix', 2),
('85251', 'Scottsdale', 2),
('90405', 'Santa Monica', 2),
('94025', 'Menlo Park', 2),
('94105', 'San Francisco', 2),
('95008', 'Campbell', 2),
('95054', 'Santa Clara', 2),
('95060', 'Santa Cruz', 2),
('98004', 'Bellevue', 2),
('98052', 'Redmond', 2),
('98104', 'Seattle', 2),
('01581', 'Westboro', 2),
('01833', 'Georgetown', 2),
('02116', 'Boston', 2),
('02903', 'Providence', 2),
('03049', 'Hollis', 1),
('03801', 'Portsmouth', 1),
('07960', 'Morristown', 2),
('08837', 'Edison', 2),
('10019', 'New York', 2),
('10038', 'New York', 2),
('11747', 'Mellvile', 2),
('14450', 'Fairport', 2),
('19428', 'Philadelphia', 2),
('19713', 'Neward', 2),
('20852', 'Rockville', 2),
('27403', 'Greensboro', 2),
('27511', 'Cary', 2),
('29202', 'Columbia', 2),
('30346', 'Atlanta', 2),
('31406', 'Savannah', 2),
('32859', 'Orlando', 2),
('33607', 'Tampa', 2),
('40222', 'Louisville', 2),
('44122', 'Beachwood', 2),
('45839', 'Findlay', 2),
('48075', 'Southfield', 2),
('48084', 'Troy', 2),
('48304', 'Bloomfield Hills', 2),
('53404', 'Racine', 2),
('55113', 'Roseville', 2),
('55439', 'Minneapolis', 2),
('72716', 'Bentonville', 2),
('75234', 'Dallas', 2),
('78759', 'Austin', 2);
DROP TABLE IF EXISTS units_by_location;
CREATE TABLE units_by_location (location_id NUMERIC, department_name CHARACTER VARYING(32), department_number NUMERIC);
INSERT INTO units_by_location (location_id, department_name, department_number) VALUES 
(8, 'Hazardous_Waste_Managemnt', 9999),
(5, 'Legal', 9995),
(5, 'Sales', 9996),
(5, 'Executives', 2),
(6, 'Executives', 1),
(6, 'Product_Research', 9990),
(6, 'Clinical_Trials', 9992),
(6, 'HR', 9993),
(6, 'Sales', 9994),
(7, 'Distribution', 9991),
(4, 'Clinical_trials', 9997),
(4, 'Product_Research', 9998),
(3, 'Sales', 9980),
(2, 'Sales', 9981),
(2, 'Marketing', 9982),
(2, 'HR', 9983),
(1, 'HR', 9984),
(1, 'Sales', 9985),
(1, 'Executive', 9986),
(1, 'Sustainability', 9987),
(1, 'Distribution', 9988);
DROP TABLE IF EXISTS us_states;
CREATE TABLE us_states (state_id SMALLINT NOT NULL, state_name CHARACTER VARYING(100), state_abbr CHARACTER VARYING(2), state_region CHARACTER VARYING(50), CONSTRAINT pk_usstates PRIMARY KEY (state_id));
INSERT INTO us_states (state_id, state_name, state_abbr, state_region) VALUES 
(1, 'Alabama', 'AL', 'south'),
(2, 'Alaska', 'AK', 'north'),
(3, 'Arizona', 'AZ', 'west'),
(4, 'Arkansas', 'AR', 'south'),
(5, 'California', 'CA', 'west'),
(6, 'Colorado', 'CO', 'west'),
(7, 'Connecticut', 'CT', 'east'),
(8, 'Delaware', 'DE', 'east'),
(9, 'District of Columbia', 'DC', 'east'),
(10, 'Florida', 'FL', 'south'),
(11, 'Georgia', 'GA', 'south'),
(12, 'Hawaii', 'HI', 'west'),
(13, 'Idaho', 'ID', 'midwest'),
(14, 'Illinois', 'IL', 'midwest'),
(15, 'Indiana', 'IN', 'midwest'),
(16, 'Iowa', 'IO', 'midwest'),
(17, 'Kansas', 'KS', 'midwest'),
(18, 'Kentucky', 'KY', 'south'),
(19, 'Louisiana', 'LA', 'south'),
(20, 'Maine', 'ME', 'north'),
(21, 'Maryland', 'MD', 'east'),
(22, 'Massachusetts', 'MA', 'north'),
(23, 'Michigan', 'MI', 'north'),
(24, 'Minnesota', 'MN', 'north'),
(25, 'Mississippi', 'MS', 'south'),
(26, 'Missouri', 'MO', 'south'),
(27, 'Montana', 'MT', 'west'),
(28, 'Nebraska', 'NE', 'midwest'),
(29, 'Nevada', 'NV', 'west'),
(30, 'New Hampshire', 'NH', 'east'),
(31, 'New Jersey', 'NJ', 'east'),
(32, 'New Mexico', 'NM', 'west'),
(33, 'New York', 'NY', 'east'),
(34, 'North Carolina', 'NC', 'east'),
(35, 'North Dakota', 'ND', 'midwest'),
(36, 'Ohio', 'OH', 'midwest'),
(37, 'Oklahoma', 'OK', 'midwest'),
(38, 'Oregon', 'OR', 'west'),
(39, 'Pennsylvania', 'PA', 'east'),
(40, 'Rhode Island', 'RI', 'east'),
(41, 'South Carolina', 'SC', 'east'),
(42, 'South Dakota', 'SD', 'midwest'),
(43, 'Tennessee', 'TN', 'midwest'),
(44, 'Texas', 'TX', 'west'),
(45, 'Utah', 'UT', 'west'),
(46, 'Vermont', 'VT', 'east'),
(47, 'Virginia', 'VA', 'east'),
(48, 'Washington', 'WA', 'west'),
(49, 'West Virginia', 'WV', 'south'),
(50, 'Wisconsin', 'WI', 'midwest'),
(51, 'Wyoming', 'WY', 'west');
ALTER TABLE "customer_customer_demo" ADD CONSTRAINT fk_customer_customer_demo_customer_demographics FOREIGN KEY ("customer_type_id") REFERENCES "customer_demographics" ("customer_type_id");
ALTER TABLE "customer_customer_demo" ADD CONSTRAINT fk_customer_customer_demo_customers FOREIGN KEY ("customer_id") REFERENCES "customers" ("customer_id");
ALTER TABLE "employee_territories" ADD CONSTRAINT fk_employee_territories_employees FOREIGN KEY ("employee_id") REFERENCES "employees" ("employee_id");
ALTER TABLE "employee_territories" ADD CONSTRAINT fk_employee_territories_territories FOREIGN KEY ("territory_id") REFERENCES "territories" ("territory_id");
ALTER TABLE "order_details" ADD CONSTRAINT fk_order_details_orders FOREIGN KEY ("order_id") REFERENCES "orders" ("order_id");
ALTER TABLE "order_details" ADD CONSTRAINT fk_order_details_products FOREIGN KEY ("product_id") REFERENCES "products" ("product_id");
ALTER TABLE "orders" ADD CONSTRAINT fk_orders_customers FOREIGN KEY ("customer_id") REFERENCES "customers" ("customer_id");
ALTER TABLE "orders" ADD CONSTRAINT fk_orders_employees FOREIGN KEY ("employee_id") REFERENCES "employees" ("employee_id");
ALTER TABLE "orders" ADD CONSTRAINT fk_orders_shippers FOREIGN KEY ("ship_via") REFERENCES "shippers" ("shipper_id");
ALTER TABLE "products" ADD CONSTRAINT fk_products_categories FOREIGN KEY ("category_id") REFERENCES "categories" ("category_id");
ALTER TABLE "products" ADD CONSTRAINT fk_products_suppliers FOREIGN KEY ("supplier_id") REFERENCES "suppliers" ("supplier_id");
ALTER TABLE "territories" ADD CONSTRAINT fk_territories_region FOREIGN KEY ("region_id") REFERENCES "region" ("region_id");
