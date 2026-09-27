-- Coco Pharmaceuticals Data Sharing Hub: one schema per strategic digital product.
-- GENERATED from coco-workbooks/1. coco-data-hub/strategic-digital-products/*.md
-- (Create Data Structure / Create Data Field / Link Data Field to Data Structure).
-- Do not edit by hand: change the product files and regenerate with
-- compose-configs/egeria-quickstart/bin/gen-coco-data-hub-sql.py.
-- Idempotent: every object is created only if it does not exist.

SET client_min_messages = warning;

-- ================================================================================================
-- research.md
-- ================================================================================================

-- New Product Definitions  (DigitalProduct::Coco::Product Definitions)
CREATE SCHEMA IF NOT EXISTS new_product_definitions;
GRANT ALL ON SCHEMA new_product_definitions TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA new_product_definitions IS 'The definition of a new product as it leaves development: its composition, the presentations it will be supplied in and the specification it must meet. It is the source the product master is created from.';

CREATE TABLE IF NOT EXISTS new_product_definitions.candidate_product_definition (
  product_code              varchar(20) NOT NULL,
  candidate_identifier      varchar(40) NOT NULL,
  product_name              varchar(120) NOT NULL,
  formulation_identifier    varchar(40) NOT NULL,
  active_ingredient_name    varchar(120) NOT NULL,
  product_strength          varchar(40),
  clinical_trial_identifier varchar(40),
  candidate_handover_date   date NOT NULL,
  CONSTRAINT candidate_product_definition_pk PRIMARY KEY (product_code)
);
COMMENT ON TABLE new_product_definitions.candidate_product_definition IS 'One row per product candidate handed over from development.';
COMMENT ON COLUMN new_product_definitions.candidate_product_definition.product_code IS 'The product code assigned on handover.';
COMMENT ON COLUMN new_product_definitions.candidate_product_definition.candidate_identifier IS 'The development identifier of the candidate.';
COMMENT ON COLUMN new_product_definitions.candidate_product_definition.product_name IS 'The proposed product name.';
COMMENT ON COLUMN new_product_definitions.candidate_product_definition.formulation_identifier IS 'The formulation developed.';
COMMENT ON COLUMN new_product_definitions.candidate_product_definition.active_ingredient_name IS 'The active ingredient.';
COMMENT ON COLUMN new_product_definitions.candidate_product_definition.product_strength IS 'The strength.';
COMMENT ON COLUMN new_product_definitions.candidate_product_definition.clinical_trial_identifier IS 'The trial that supports the product.';
COMMENT ON COLUMN new_product_definitions.candidate_product_definition.candidate_handover_date IS 'When development handed the definition over.';

CREATE TABLE IF NOT EXISTS new_product_definitions.product_presentation (
  pack_code        varchar(20) NOT NULL,
  product_code     varchar(20) NOT NULL,
  pack_description text NOT NULL,
  pack_quantity    integer NOT NULL,
  CONSTRAINT product_presentation_pk PRIMARY KEY (pack_code)
);
COMMENT ON TABLE new_product_definitions.product_presentation IS 'One row per presentation the product will be supplied in.';
COMMENT ON COLUMN new_product_definitions.product_presentation.pack_code IS 'The presentation''s pack code.';
COMMENT ON COLUMN new_product_definitions.product_presentation.product_code IS 'The product code assigned on handover.';
COMMENT ON COLUMN new_product_definitions.product_presentation.pack_description IS 'The presentation.';
COMMENT ON COLUMN new_product_definitions.product_presentation.pack_quantity IS 'Units per pack.';

CREATE TABLE IF NOT EXISTS new_product_definitions.product_specification (
  product_code                varchar(20) NOT NULL,
  test_code                   varchar(40) NOT NULL,
  specification_minimum_value varchar(60),
  specification_maximum_value varchar(60),
  test_unit                   varchar(20),
  CONSTRAINT product_specification_pk PRIMARY KEY (product_code, test_code)
);
COMMENT ON TABLE new_product_definitions.product_specification IS 'One row per specification limit the product must meet on release.';
COMMENT ON COLUMN new_product_definitions.product_specification.product_code IS 'The product code assigned on handover.';
COMMENT ON COLUMN new_product_definitions.product_specification.test_code IS 'The release test.';
COMMENT ON COLUMN new_product_definitions.product_specification.specification_minimum_value IS 'The lower limit.';
COMMENT ON COLUMN new_product_definitions.product_specification.specification_maximum_value IS 'The upper limit.';
COMMENT ON COLUMN new_product_definitions.product_specification.test_unit IS 'The unit.';

GRANT ALL ON ALL TABLES IN SCHEMA new_product_definitions TO egeria_admin, egeria_user, airflow_user;

-- Hospital Certifications  (DigitalProduct::Coco::Hospital Certifications)
CREATE SCHEMA IF NOT EXISTS hospital_certifications;
GRANT ALL ON SCHEMA hospital_certifications TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA hospital_certifications IS 'The certification of hospitals as clinical trial sites, including the evidence that site staff were trained on the protocol before they worked to it. Competency data is read here as compliance evidence.';

CREATE TABLE IF NOT EXISTS hospital_certifications.hospital_certification (
  hospital_identifier             varchar(40) NOT NULL,
  clinical_trial_identifier       varchar(40) NOT NULL,
  hospital_certification_date     date NOT NULL,
  hospital_certification_end_date date,
  hospital_certification_status   varchar(20) NOT NULL,
  hospital_certifier_identifier   varchar(40) NOT NULL,
  CONSTRAINT hospital_certification_pk PRIMARY KEY (hospital_identifier, clinical_trial_identifier)
);
COMMENT ON TABLE hospital_certifications.hospital_certification IS 'One row per hospital certified for a trial.';
COMMENT ON COLUMN hospital_certifications.hospital_certification.hospital_identifier IS 'The hospital.';
COMMENT ON COLUMN hospital_certifications.hospital_certification.clinical_trial_identifier IS 'The trial.';
COMMENT ON COLUMN hospital_certifications.hospital_certification.hospital_certification_date IS 'When certified.';
COMMENT ON COLUMN hospital_certifications.hospital_certification.hospital_certification_end_date IS 'When the certification lapses.';
COMMENT ON COLUMN hospital_certifications.hospital_certification.hospital_certification_status IS 'Certified, suspended or withdrawn.';
COMMENT ON COLUMN hospital_certifications.hospital_certification.hospital_certifier_identifier IS 'Who certified the site.';

CREATE TABLE IF NOT EXISTS hospital_certifications.site_staff_training_evidence (
  hospital_identifier       varchar(40) NOT NULL,
  clinical_trial_identifier varchar(40) NOT NULL,
  clinician_identifier      varchar(40) NOT NULL,
  protocol_identifier       varchar(40) NOT NULL,
  training_completed_date   date NOT NULL,
  training_expiry_date      date,
  CONSTRAINT site_staff_training_evidence_pk PRIMARY KEY (hospital_identifier, clinical_trial_identifier, clinician_identifier, protocol_identifier)
);
COMMENT ON TABLE hospital_certifications.site_staff_training_evidence IS 'One row per site staff member per protocol training completed.';
COMMENT ON COLUMN hospital_certifications.site_staff_training_evidence.hospital_identifier IS 'The site.';
COMMENT ON COLUMN hospital_certifications.site_staff_training_evidence.clinical_trial_identifier IS 'The trial.';
COMMENT ON COLUMN hospital_certifications.site_staff_training_evidence.clinician_identifier IS 'The staff member.';
COMMENT ON COLUMN hospital_certifications.site_staff_training_evidence.protocol_identifier IS 'The protocol trained on.';
COMMENT ON COLUMN hospital_certifications.site_staff_training_evidence.training_completed_date IS 'When training was completed.';
COMMENT ON COLUMN hospital_certifications.site_staff_training_evidence.training_expiry_date IS 'When the training lapses.';

GRANT ALL ON ALL TABLES IN SCHEMA hospital_certifications TO egeria_admin, egeria_user, airflow_user;

-- ================================================================================================
-- master-data-management.md
-- ================================================================================================

-- Product Master Data  (DigitalProduct::Coco::Product Master Data)
CREATE SCHEMA IF NOT EXISTS product_master_data;
GRANT ALL ON SCHEMA product_master_data TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA product_master_data IS 'The authoritative definition of every Coco Pharmaceuticals product: its identity, composition, presentations and pack configurations, the conditions it must be stored and shipped under, and the markets it is authorised for. Manufacturing, serialisation, distribution, sales and finance all read it and none of them own it.';

CREATE TABLE IF NOT EXISTS product_master_data.product_definition (
  product_code            varchar(20) NOT NULL,
  product_name            varchar(120) NOT NULL,
  product_description     text,
  product_type            varchar(40) NOT NULL,
  active_ingredient_name  varchar(120) NOT NULL,
  product_strength        varchar(40),
  product_current_status  varchar(20) NOT NULL,
  product_current_version varchar(20) NOT NULL,
  CONSTRAINT product_definition_pk PRIMARY KEY (product_code)
);
COMMENT ON TABLE product_master_data.product_definition IS 'One row per product, the attributes that identify it and describe what it is.';
COMMENT ON COLUMN product_master_data.product_definition.product_code IS 'The company''s unique code for the product.';
COMMENT ON COLUMN product_master_data.product_definition.product_name IS 'The product''s name as it appears on the label.';
COMMENT ON COLUMN product_master_data.product_definition.product_description IS 'What the product is and what it treats.';
COMMENT ON COLUMN product_master_data.product_definition.product_type IS 'Whether the product is a standard, personalised or investigational treatment.';
COMMENT ON COLUMN product_master_data.product_definition.active_ingredient_name IS 'The active ingredient responsible for the therapeutic effect.';
COMMENT ON COLUMN product_master_data.product_definition.product_strength IS 'The concentration or potency of the active ingredient.';
COMMENT ON COLUMN product_master_data.product_definition.product_current_status IS 'Whether the product is in development, marketed, suspended or withdrawn.';
COMMENT ON COLUMN product_master_data.product_definition.product_current_version IS 'The version of the product definition consuming systems should hold.';

CREATE TABLE IF NOT EXISTS product_master_data.pack_configuration (
  pack_code             varchar(20) NOT NULL,
  product_code          varchar(20) NOT NULL,
  pack_description      text,
  pack_quantity         integer NOT NULL,
  pack_destination_code varchar(8) NOT NULL,
  pack_serialised_flag  boolean NOT NULL,
  CONSTRAINT pack_configuration_pk PRIMARY KEY (pack_code)
);
COMMENT ON TABLE product_master_data.pack_configuration IS 'One row per saleable presentation of a product, the unit that carries a serial number.';
COMMENT ON COLUMN product_master_data.pack_configuration.pack_code IS 'The GTIN or company code of the pack presentation.';
COMMENT ON COLUMN product_master_data.pack_configuration.product_code IS 'The product the pack contains.';
COMMENT ON COLUMN product_master_data.pack_configuration.pack_description IS 'The presentation, for example thirty tablets in a blister pack.';
COMMENT ON COLUMN product_master_data.pack_configuration.pack_quantity IS 'The number of units of the product in the pack.';
COMMENT ON COLUMN product_master_data.pack_configuration.pack_destination_code IS 'The destination market the pack presentation is configured for.';
COMMENT ON COLUMN product_master_data.pack_configuration.pack_serialised_flag IS 'Whether packs of this presentation must carry a serial number.';

CREATE TABLE IF NOT EXISTS product_master_data.handling_requirement (
  product_code                        varchar(20) NOT NULL,
  product_storage_minimum_temperature double precision NOT NULL,
  product_storage_maximum_temperature double precision NOT NULL,
  product_hazard_code                 varchar(20),
  product_packaging_description       text,
  product_expiry_duration             integer NOT NULL,
  CONSTRAINT handling_requirement_pk PRIMARY KEY (product_code)
);
COMMENT ON TABLE product_master_data.handling_requirement IS 'One row per product, the storage and transport conditions it must be kept within.';
COMMENT ON COLUMN product_master_data.handling_requirement.product_code IS 'The product the requirement applies to.';
COMMENT ON COLUMN product_master_data.handling_requirement.product_storage_minimum_temperature IS 'The lowest temperature the product may be stored at, in degrees Celsius.';
COMMENT ON COLUMN product_master_data.handling_requirement.product_storage_maximum_temperature IS 'The highest temperature the product may be stored at, in degrees Celsius.';
COMMENT ON COLUMN product_master_data.handling_requirement.product_hazard_code IS 'The hazard classification of the product for transport, if any.';
COMMENT ON COLUMN product_master_data.handling_requirement.product_packaging_description IS 'The packaging required for transport.';
COMMENT ON COLUMN product_master_data.handling_requirement.product_expiry_duration IS 'The shelf life of the product from manufacture, in days.';

CREATE TABLE IF NOT EXISTS product_master_data.authorised_market_assignment (
  product_code             varchar(20) NOT NULL,
  market_code              varchar(8) NOT NULL,
  authorisation_identifier varchar(40) NOT NULL,
  authorisation_start_date date NOT NULL,
  authorisation_end_date   date,
  CONSTRAINT authorised_market_assignment_pk PRIMARY KEY (product_code, market_code)
);
COMMENT ON TABLE product_master_data.authorised_market_assignment IS 'One row per product per market it may be placed on.';
COMMENT ON COLUMN product_master_data.authorised_market_assignment.product_code IS 'The product.';
COMMENT ON COLUMN product_master_data.authorised_market_assignment.market_code IS 'The market the product is authorised for.';
COMMENT ON COLUMN product_master_data.authorised_market_assignment.authorisation_identifier IS 'The market authorisation the assignment relies on.';
COMMENT ON COLUMN product_master_data.authorised_market_assignment.authorisation_start_date IS 'When the product may first be placed on the market.';
COMMENT ON COLUMN product_master_data.authorised_market_assignment.authorisation_end_date IS 'When the authorisation lapses, if it does.';

GRANT ALL ON ALL TABLES IN SCHEMA product_master_data TO egeria_admin, egeria_user, airflow_user;

-- Product Change Notifications  (DigitalProduct::Coco::Product Change Notifications)
CREATE SCHEMA IF NOT EXISTS product_change_notifications;
GRANT ALL ON SCHEMA product_change_notifications TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA product_change_notifications IS 'Every change published from the product master, and the record of which consuming system has applied it and which has not. An inconsistent estate is only dangerous while nobody knows which copies are stale.';

CREATE TABLE IF NOT EXISTS product_change_notifications.product_change (
  product_change_identifier          varchar(40) NOT NULL,
  product_code                       varchar(20) NOT NULL,
  product_change_description         text NOT NULL,
  product_change_start_date          date NOT NULL,
  product_change_published_timestamp timestamptz NOT NULL,
  CONSTRAINT product_change_pk PRIMARY KEY (product_change_identifier)
);
COMMENT ON TABLE product_change_notifications.product_change IS 'One row per published change to a product attribute.';
COMMENT ON COLUMN product_change_notifications.product_change.product_change_identifier IS 'The unique identifier of the change.';
COMMENT ON COLUMN product_change_notifications.product_change.product_code IS 'The product changed.';
COMMENT ON COLUMN product_change_notifications.product_change.product_change_description IS 'Which attributes changed and to what.';
COMMENT ON COLUMN product_change_notifications.product_change.product_change_start_date IS 'When the change takes effect.';
COMMENT ON COLUMN product_change_notifications.product_change.product_change_published_timestamp IS 'When the change was published to consumers.';

CREATE TABLE IF NOT EXISTS product_change_notifications.distribution_receipt (
  product_change_identifier        varchar(40) NOT NULL,
  system_identifier                varchar(60) NOT NULL,
  product_change_applied_flag      boolean NOT NULL,
  product_change_applied_timestamp timestamptz,
  CONSTRAINT distribution_receipt_pk PRIMARY KEY (product_change_identifier, system_identifier)
);
COMMENT ON TABLE product_change_notifications.distribution_receipt IS 'One row per change per consuming system, recording whether it has been applied.';
COMMENT ON COLUMN product_change_notifications.distribution_receipt.product_change_identifier IS 'The change distributed.';
COMMENT ON COLUMN product_change_notifications.distribution_receipt.system_identifier IS 'The consuming system the change was sent to.';
COMMENT ON COLUMN product_change_notifications.distribution_receipt.product_change_applied_flag IS 'Whether the system has confirmed the change is applied.';
COMMENT ON COLUMN product_change_notifications.distribution_receipt.product_change_applied_timestamp IS 'When the system confirmed it.';

GRANT ALL ON ALL TABLES IN SCHEMA product_change_notifications TO egeria_admin, egeria_user, airflow_user;

-- Open Metadata Catalogue Holdings  (DigitalProduct::Coco::Open Metadata Catalogue Holdings)
CREATE SCHEMA IF NOT EXISTS open_metadata_catalogue_holdings;
GRANT ALL ON SCHEMA open_metadata_catalogue_holdings TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA open_metadata_catalogue_holdings IS 'What the open metadata catalogue knows about the estate: the assets it has catalogued, their classifications and owners, and the indicators that an asset holds personal data. It is the starting point for personal data discovery and for setting retention periods, because it describes what the company actually holds rather than what it believes it holds.';

CREATE TABLE IF NOT EXISTS open_metadata_catalogue_holdings.catalogued_asset (
  asset_identifier            varchar(40) NOT NULL,
  asset_name                  varchar(120) NOT NULL,
  asset_type                  varchar(60) NOT NULL,
  system_identifier           varchar(60),
  asset_owner_identifier      varchar(40),
  asset_personal_data_flag    boolean NOT NULL,
  asset_confidentiality_level varchar(20),
  CONSTRAINT catalogued_asset_pk PRIMARY KEY (asset_identifier)
);
COMMENT ON TABLE open_metadata_catalogue_holdings.catalogued_asset IS 'One row per asset in the catalogue.';
COMMENT ON COLUMN open_metadata_catalogue_holdings.catalogued_asset.asset_identifier IS 'The catalogue''s unique identifier for the asset.';
COMMENT ON COLUMN open_metadata_catalogue_holdings.catalogued_asset.asset_name IS 'The asset''s display name.';
COMMENT ON COLUMN open_metadata_catalogue_holdings.catalogued_asset.asset_type IS 'The open metadata type of the asset.';
COMMENT ON COLUMN open_metadata_catalogue_holdings.catalogued_asset.system_identifier IS 'The system that hosts the asset.';
COMMENT ON COLUMN open_metadata_catalogue_holdings.catalogued_asset.asset_owner_identifier IS 'The person or team accountable for the asset.';
COMMENT ON COLUMN open_metadata_catalogue_holdings.catalogued_asset.asset_personal_data_flag IS 'Whether the asset is classified as holding personal data.';
COMMENT ON COLUMN open_metadata_catalogue_holdings.catalogued_asset.asset_confidentiality_level IS 'The confidentiality classification of the asset.';

GRANT ALL ON ALL TABLES IN SCHEMA open_metadata_catalogue_holdings TO egeria_admin, egeria_user, airflow_user;

-- ================================================================================================
-- manufacturing.md
-- ================================================================================================

-- Personalised Manufacturing Schedule  (DigitalProduct::Coco::Personalised Manufacturing Schedule)
CREATE SCHEMA IF NOT EXISTS personalised_manufacturing_schedule;
GRANT ALL ON SCHEMA personalised_manufacturing_schedule TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA personalised_manufacturing_schedule IS 'Each accepted personalised order turned into a scheduled manufacturing slot, with the arriving patient material that fixes the deadline. Unlike batch scheduling it cannot defer or re-sequence freely, because the material has a viable life measured in days.';

CREATE TABLE IF NOT EXISTS personalised_manufacturing_schedule.manufacturing_slot (
  batch_identifier              varchar(40) NOT NULL,
  order_identifier              varchar(40) NOT NULL,
  patient_pseudonym_identifier  varchar(40) NOT NULL,
  product_code                  varchar(20) NOT NULL,
  slot_start_timestamp          timestamptz NOT NULL,
  slot_end_timestamp            timestamptz NOT NULL,
  patient_parameter_description text,
  slot_status                   varchar(20) NOT NULL,
  CONSTRAINT manufacturing_slot_pk PRIMARY KEY (batch_identifier)
);
COMMENT ON TABLE personalised_manufacturing_schedule.manufacturing_slot IS 'One row per scheduled slot for a personalised order.';
COMMENT ON COLUMN personalised_manufacturing_schedule.manufacturing_slot.batch_identifier IS 'The batch opened for the order.';
COMMENT ON COLUMN personalised_manufacturing_schedule.manufacturing_slot.order_identifier IS 'The order.';
COMMENT ON COLUMN personalised_manufacturing_schedule.manufacturing_slot.patient_pseudonym_identifier IS 'The patient, by pseudonym.';
COMMENT ON COLUMN personalised_manufacturing_schedule.manufacturing_slot.product_code IS 'The product.';
COMMENT ON COLUMN personalised_manufacturing_schedule.manufacturing_slot.slot_start_timestamp IS 'When manufacturing is scheduled to start.';
COMMENT ON COLUMN personalised_manufacturing_schedule.manufacturing_slot.slot_end_timestamp IS 'When it must finish.';
COMMENT ON COLUMN personalised_manufacturing_schedule.manufacturing_slot.patient_parameter_description IS 'The patient-specific parameters applied.';
COMMENT ON COLUMN personalised_manufacturing_schedule.manufacturing_slot.slot_status IS 'Scheduled, in progress, complete or cancelled.';

CREATE TABLE IF NOT EXISTS personalised_manufacturing_schedule.patient_material_receipt (
  shipment_identifier          varchar(40) NOT NULL,
  patient_pseudonym_identifier varchar(40) NOT NULL,
  shipment_delivery_timestamp  timestamptz NOT NULL,
  shipment_arrival_description text NOT NULL,
  sample_viable_duration       integer NOT NULL,
  CONSTRAINT patient_material_receipt_pk PRIMARY KEY (shipment_identifier)
);
COMMENT ON TABLE personalised_manufacturing_schedule.patient_material_receipt IS 'One row per consignment of patient material received at the manufacturing site.';
COMMENT ON COLUMN personalised_manufacturing_schedule.patient_material_receipt.shipment_identifier IS 'The consignment.';
COMMENT ON COLUMN personalised_manufacturing_schedule.patient_material_receipt.patient_pseudonym_identifier IS 'The patient, by pseudonym.';
COMMENT ON COLUMN personalised_manufacturing_schedule.patient_material_receipt.shipment_delivery_timestamp IS 'When it arrived.';
COMMENT ON COLUMN personalised_manufacturing_schedule.patient_material_receipt.shipment_arrival_description IS 'The condition on arrival.';
COMMENT ON COLUMN personalised_manufacturing_schedule.patient_material_receipt.sample_viable_duration IS 'The remaining viable life on arrival, in hours.';

GRANT ALL ON ALL TABLES IN SCHEMA personalised_manufacturing_schedule TO egeria_admin, egeria_user, airflow_user;

-- Batch Execution Records  (DigitalProduct::Coco::Batch Execution Records)
CREATE SCHEMA IF NOT EXISTS batch_execution_records;
GRANT ALL ON SCHEMA batch_execution_records TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA batch_execution_records IS 'The contemporaneous record of each production step: what was done, by whom, with which materials and on which equipment, together with the deviations raised during execution. It is the source of most of what ends up in the batch record.';

CREATE TABLE IF NOT EXISTS batch_execution_records.execution_step (
  batch_identifier               varchar(40) NOT NULL,
  execution_step_number          integer NOT NULL,
  execution_step_code            varchar(40) NOT NULL,
  execution_step_start_timestamp timestamptz NOT NULL,
  execution_step_end_timestamp   timestamptz NOT NULL,
  worker_pseudonym_identifier    varchar(40) NOT NULL,
  execution_step_signature       varchar(200) NOT NULL,
  execution_step_status          varchar(20) NOT NULL,
  CONSTRAINT execution_step_pk PRIMARY KEY (batch_identifier, execution_step_number)
);
COMMENT ON TABLE batch_execution_records.execution_step IS 'One row per production step performed for a batch.';
COMMENT ON COLUMN batch_execution_records.execution_step.batch_identifier IS 'The batch.';
COMMENT ON COLUMN batch_execution_records.execution_step.execution_step_number IS 'The step''s position in the process.';
COMMENT ON COLUMN batch_execution_records.execution_step.execution_step_code IS 'The step performed.';
COMMENT ON COLUMN batch_execution_records.execution_step.execution_step_start_timestamp IS 'When it started.';
COMMENT ON COLUMN batch_execution_records.execution_step.execution_step_end_timestamp IS 'When it finished.';
COMMENT ON COLUMN batch_execution_records.execution_step.worker_pseudonym_identifier IS 'The operator.';
COMMENT ON COLUMN batch_execution_records.execution_step.execution_step_signature IS 'The operator''s electronic signature.';
COMMENT ON COLUMN batch_execution_records.execution_step.execution_step_status IS 'Complete, complete with deviation, or aborted.';

CREATE TABLE IF NOT EXISTS batch_execution_records.material_usage (
  batch_identifier           varchar(40) NOT NULL,
  execution_step_number      integer NOT NULL,
  lot_identifier             varchar(40) NOT NULL,
  raw_material_code          varchar(20) NOT NULL,
  raw_material_used_quantity double precision NOT NULL,
  raw_material_used_unit     varchar(20) NOT NULL,
  CONSTRAINT material_usage_pk PRIMARY KEY (batch_identifier, execution_step_number, lot_identifier)
);
COMMENT ON TABLE batch_execution_records.material_usage IS 'One row per lot of material consumed in a step.';
COMMENT ON COLUMN batch_execution_records.material_usage.batch_identifier IS 'The batch.';
COMMENT ON COLUMN batch_execution_records.material_usage.execution_step_number IS 'The step.';
COMMENT ON COLUMN batch_execution_records.material_usage.lot_identifier IS 'The lot consumed.';
COMMENT ON COLUMN batch_execution_records.material_usage.raw_material_code IS 'The material.';
COMMENT ON COLUMN batch_execution_records.material_usage.raw_material_used_quantity IS 'The quantity consumed.';
COMMENT ON COLUMN batch_execution_records.material_usage.raw_material_used_unit IS 'The unit.';

CREATE TABLE IF NOT EXISTS batch_execution_records.equipment_usage (
  batch_identifier               varchar(40) NOT NULL,
  execution_step_number          integer NOT NULL,
  equipment_identifier           varchar(40) NOT NULL,
  equipment_qualified_status     varchar(20) NOT NULL,
  equipment_calibration_end_date date NOT NULL,
  CONSTRAINT equipment_usage_pk PRIMARY KEY (batch_identifier, execution_step_number, equipment_identifier)
);
COMMENT ON TABLE batch_execution_records.equipment_usage IS 'One row per piece of equipment used in a step, with its qualification status at the time.';
COMMENT ON COLUMN batch_execution_records.equipment_usage.batch_identifier IS 'The batch.';
COMMENT ON COLUMN batch_execution_records.equipment_usage.execution_step_number IS 'The step.';
COMMENT ON COLUMN batch_execution_records.equipment_usage.equipment_identifier IS 'The equipment.';
COMMENT ON COLUMN batch_execution_records.equipment_usage.equipment_qualified_status IS 'The qualification status read at the moment of use.';
COMMENT ON COLUMN batch_execution_records.equipment_usage.equipment_calibration_end_date IS 'When the calibration in force at use expires.';

GRANT ALL ON ALL TABLES IN SCHEMA batch_execution_records TO egeria_admin, egeria_user, airflow_user;

-- Process Parameter Time Series  (DigitalProduct::Coco::Process Parameter Time Series)
CREATE SCHEMA IF NOT EXISTS process_parameter_time_series;
GRANT ALL ON SCHEMA process_parameter_time_series TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA process_parameter_time_series IS 'The continuous record of critical process parameters captured from plant instrumentation, at a resolution nobody reads unless something went wrong, which is exactly when it cannot be recreated.';

CREATE TABLE IF NOT EXISTS process_parameter_time_series.process_parameter_reading (
  equipment_identifier            varchar(40) NOT NULL,
  process_parameter_code          varchar(40) NOT NULL,
  process_parameter_timestamp     timestamptz NOT NULL,
  batch_identifier                varchar(40),
  process_parameter_value         double precision NOT NULL,
  process_parameter_unit          varchar(20) NOT NULL,
  process_parameter_minimum_value double precision,
  process_parameter_maximum_value double precision,
  CONSTRAINT process_parameter_reading_pk PRIMARY KEY (equipment_identifier, process_parameter_code, process_parameter_timestamp)
);
COMMENT ON TABLE process_parameter_time_series.process_parameter_reading IS 'One row per instrument reading.';
COMMENT ON COLUMN process_parameter_time_series.process_parameter_reading.equipment_identifier IS 'The equipment instrumented.';
COMMENT ON COLUMN process_parameter_time_series.process_parameter_reading.process_parameter_code IS 'The parameter measured.';
COMMENT ON COLUMN process_parameter_time_series.process_parameter_reading.process_parameter_timestamp IS 'When measured.';
COMMENT ON COLUMN process_parameter_time_series.process_parameter_reading.batch_identifier IS 'The batch in progress when the reading was taken.';
COMMENT ON COLUMN process_parameter_time_series.process_parameter_reading.process_parameter_value IS 'The reading.';
COMMENT ON COLUMN process_parameter_time_series.process_parameter_reading.process_parameter_unit IS 'The unit.';
COMMENT ON COLUMN process_parameter_time_series.process_parameter_reading.process_parameter_minimum_value IS 'The lower validated limit.';
COMMENT ON COLUMN process_parameter_time_series.process_parameter_reading.process_parameter_maximum_value IS 'The upper validated limit.';

GRANT ALL ON ALL TABLES IN SCHEMA process_parameter_time_series TO egeria_admin, egeria_user, airflow_user;

-- Equipment Qualification Status  (DigitalProduct::Coco::Equipment Qualification Status)
CREATE SCHEMA IF NOT EXISTS equipment_qualification_status;
GRANT ALL ON SCHEMA equipment_qualification_status TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA equipment_qualification_status IS 'The qualification and calibration status of every piece of equipment used in production, consulted at the moment of use because a qualification that lapsed last week invalidates production that has already happened.';

CREATE TABLE IF NOT EXISTS equipment_qualification_status.equipment (
  equipment_identifier     varchar(40) NOT NULL,
  equipment_name           varchar(120) NOT NULL,
  equipment_type           varchar(60) NOT NULL,
  site_code                varchar(20) NOT NULL,
  equipment_current_status varchar(20) NOT NULL,
  CONSTRAINT equipment_pk PRIMARY KEY (equipment_identifier)
);
COMMENT ON TABLE equipment_qualification_status.equipment IS 'One row per piece of production equipment.';
COMMENT ON COLUMN equipment_qualification_status.equipment.equipment_identifier IS 'The equipment.';
COMMENT ON COLUMN equipment_qualification_status.equipment.equipment_name IS 'Its name.';
COMMENT ON COLUMN equipment_qualification_status.equipment.equipment_type IS 'Its type.';
COMMENT ON COLUMN equipment_qualification_status.equipment.site_code IS 'The site it is installed at.';
COMMENT ON COLUMN equipment_qualification_status.equipment.equipment_current_status IS 'In service, out of service or retired.';

CREATE TABLE IF NOT EXISTS equipment_qualification_status.qualification_status (
  equipment_identifier           varchar(40) NOT NULL,
  equipment_qualified_status     varchar(20) NOT NULL,
  equipment_qualified_date       date NOT NULL,
  equipment_qualified_end_date   date NOT NULL,
  equipment_calibration_date     date NOT NULL,
  equipment_calibration_end_date date NOT NULL,
  CONSTRAINT qualification_status_pk PRIMARY KEY (equipment_identifier)
);
COMMENT ON TABLE equipment_qualification_status.qualification_status IS 'One row per equipment, its current qualification and calibration validity.';
COMMENT ON COLUMN equipment_qualification_status.qualification_status.equipment_identifier IS 'The equipment.';
COMMENT ON COLUMN equipment_qualification_status.qualification_status.equipment_qualified_status IS 'Qualified, requalification due, or not qualified.';
COMMENT ON COLUMN equipment_qualification_status.qualification_status.equipment_qualified_date IS 'When last qualified.';
COMMENT ON COLUMN equipment_qualification_status.qualification_status.equipment_qualified_end_date IS 'When qualification lapses.';
COMMENT ON COLUMN equipment_qualification_status.qualification_status.equipment_calibration_date IS 'When last calibrated.';
COMMENT ON COLUMN equipment_qualification_status.qualification_status.equipment_calibration_end_date IS 'When calibration lapses.';

GRANT ALL ON ALL TABLES IN SCHEMA equipment_qualification_status TO egeria_admin, egeria_user, airflow_user;

-- Electronic Batch Records  (DigitalProduct::Coco::Electronic Batch Records)
CREATE SCHEMA IF NOT EXISTS electronic_batch_records;
GRANT ALL ON SCHEMA electronic_batch_records TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA electronic_batch_records IS 'The complete record of each batch assembled from every contributing system and held for the life of the obligation: execution, process parameters, laboratory results, deviation dispositions, excursion dispositions and signature authority, followed by the release authorisation once certified.';

CREATE TABLE IF NOT EXISTS electronic_batch_records.batch_record (
  batch_identifier             varchar(40) NOT NULL,
  product_code                 varchar(20) NOT NULL,
  patient_pseudonym_identifier varchar(40),
  batch_start_timestamp        timestamptz NOT NULL,
  batch_end_timestamp          timestamptz,
  batch_quantity               integer,
  batch_record_complete_flag   boolean NOT NULL,
  batch_certification_status   varchar(20) NOT NULL,
  CONSTRAINT batch_record_pk PRIMARY KEY (batch_identifier)
);
COMMENT ON TABLE electronic_batch_records.batch_record IS 'One row per batch.';
COMMENT ON COLUMN electronic_batch_records.batch_record.batch_identifier IS 'The batch.';
COMMENT ON COLUMN electronic_batch_records.batch_record.product_code IS 'The product.';
COMMENT ON COLUMN electronic_batch_records.batch_record.patient_pseudonym_identifier IS 'The patient, for a personalised batch.';
COMMENT ON COLUMN electronic_batch_records.batch_record.batch_start_timestamp IS 'When manufacturing started.';
COMMENT ON COLUMN electronic_batch_records.batch_record.batch_end_timestamp IS 'When it finished.';
COMMENT ON COLUMN electronic_batch_records.batch_record.batch_quantity IS 'The quantity produced.';
COMMENT ON COLUMN electronic_batch_records.batch_record.batch_record_complete_flag IS 'Whether every contributing section has been received.';
COMMENT ON COLUMN electronic_batch_records.batch_record.batch_certification_status IS 'Awaiting review, certified or rejected.';

CREATE TABLE IF NOT EXISTS electronic_batch_records.batch_record_section (
  batch_identifier                          varchar(40) NOT NULL,
  batch_record_section_reference_identifier varchar(40) NOT NULL,
  batch_record_section_type                 varchar(40) NOT NULL,
  system_identifier                         varchar(60) NOT NULL,
  batch_record_section_received_timestamp   timestamptz NOT NULL,
  CONSTRAINT batch_record_section_pk PRIMARY KEY (batch_identifier, batch_record_section_reference_identifier)
);
COMMENT ON TABLE electronic_batch_records.batch_record_section IS 'One row per contribution received from a source system for a batch.';
COMMENT ON COLUMN electronic_batch_records.batch_record_section.batch_identifier IS 'The batch.';
COMMENT ON COLUMN electronic_batch_records.batch_record_section.batch_record_section_reference_identifier IS 'The source record referenced.';
COMMENT ON COLUMN electronic_batch_records.batch_record_section.batch_record_section_type IS 'Execution, process parameters, laboratory results, deviation disposition, excursion disposition or signature authority.';
COMMENT ON COLUMN electronic_batch_records.batch_record_section.system_identifier IS 'The contributing system.';
COMMENT ON COLUMN electronic_batch_records.batch_record_section.batch_record_section_received_timestamp IS 'When received.';

CREATE TABLE IF NOT EXISTS electronic_batch_records.release_authorisation (
  batch_identifier           varchar(40) NOT NULL,
  market_code                varchar(8) NOT NULL,
  batch_released_quantity    integer NOT NULL,
  batch_certification_date   date NOT NULL,
  batch_certifier_identifier varchar(40) NOT NULL,
  CONSTRAINT release_authorisation_pk PRIMARY KEY (batch_identifier, market_code)
);
COMMENT ON TABLE electronic_batch_records.release_authorisation IS 'One row per certified batch per market, the quantities released.';
COMMENT ON COLUMN electronic_batch_records.release_authorisation.batch_identifier IS 'The batch.';
COMMENT ON COLUMN electronic_batch_records.release_authorisation.market_code IS 'The market released to.';
COMMENT ON COLUMN electronic_batch_records.release_authorisation.batch_released_quantity IS 'The quantity released to the market.';
COMMENT ON COLUMN electronic_batch_records.release_authorisation.batch_certification_date IS 'When certified.';
COMMENT ON COLUMN electronic_batch_records.release_authorisation.batch_certifier_identifier IS 'The Qualified Person.';

GRANT ALL ON ALL TABLES IN SCHEMA electronic_batch_records TO egeria_admin, egeria_user, airflow_user;

-- Serial Number Allocations  (DigitalProduct::Coco::Serial Number Allocations)
CREATE SCHEMA IF NOT EXISTS serial_number_allocations;
GRANT ALL ON SCHEMA serial_number_allocations TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA serial_number_allocations IS 'The unique identifiers issued for saleable packs, allocated per product, pack presentation and destination market before the line starts. Uniqueness is assured at generation, because a number issued twice cannot be corrected once packs are distributed.';

CREATE TABLE IF NOT EXISTS serial_number_allocations.serial_number_allocation (
  allocation_identifier   varchar(40) NOT NULL,
  product_code            varchar(20) NOT NULL,
  pack_code               varchar(20) NOT NULL,
  market_code             varchar(8) NOT NULL,
  allocation_start_number varchar(40) NOT NULL,
  allocation_end_number   varchar(40) NOT NULL,
  allocation_count        integer NOT NULL,
  allocation_timestamp    timestamptz NOT NULL,
  batch_identifier        varchar(40),
  CONSTRAINT serial_number_allocation_pk PRIMARY KEY (allocation_identifier)
);
COMMENT ON TABLE serial_number_allocations.serial_number_allocation IS 'One row per block of serial numbers allocated.';
COMMENT ON COLUMN serial_number_allocations.serial_number_allocation.allocation_identifier IS 'The allocation.';
COMMENT ON COLUMN serial_number_allocations.serial_number_allocation.product_code IS 'The product.';
COMMENT ON COLUMN serial_number_allocations.serial_number_allocation.pack_code IS 'The pack presentation.';
COMMENT ON COLUMN serial_number_allocations.serial_number_allocation.market_code IS 'The destination market.';
COMMENT ON COLUMN serial_number_allocations.serial_number_allocation.allocation_start_number IS 'The first serial number in the block.';
COMMENT ON COLUMN serial_number_allocations.serial_number_allocation.allocation_end_number IS 'The last serial number in the block.';
COMMENT ON COLUMN serial_number_allocations.serial_number_allocation.allocation_count IS 'The number of identifiers allocated.';
COMMENT ON COLUMN serial_number_allocations.serial_number_allocation.allocation_timestamp IS 'When allocated.';
COMMENT ON COLUMN serial_number_allocations.serial_number_allocation.batch_identifier IS 'The batch the block is reserved for.';

GRANT ALL ON ALL TABLES IN SCHEMA serial_number_allocations TO egeria_admin, egeria_user, airflow_user;

-- Commissioned Packs  (DigitalProduct::Coco::Commissioned Packs)
CREATE SCHEMA IF NOT EXISTS commissioned_packs;
GRANT ALL ON SCHEMA commissioned_packs TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA commissioned_packs IS 'Each pack that has had its identifier applied, verified and commissioned as a real, saleable object on the packaging line, and its assignment to a case. It works at line speed, which is why the identifiers had to be present before the line started.';

CREATE TABLE IF NOT EXISTS commissioned_packs.commissioned_pack (
  pack_serial_number          varchar(40) NOT NULL,
  pack_code                   varchar(20) NOT NULL,
  batch_identifier            varchar(40) NOT NULL,
  pack_expiry_date            date NOT NULL,
  pack_commissioned_timestamp timestamptz NOT NULL,
  pack_verified_flag          boolean NOT NULL,
  equipment_identifier        varchar(40) NOT NULL,
  CONSTRAINT commissioned_pack_pk PRIMARY KEY (pack_serial_number)
);
COMMENT ON TABLE commissioned_packs.commissioned_pack IS 'One row per pack commissioned.';
COMMENT ON COLUMN commissioned_packs.commissioned_pack.pack_serial_number IS 'The pack''s serial number.';
COMMENT ON COLUMN commissioned_packs.commissioned_pack.pack_code IS 'The presentation.';
COMMENT ON COLUMN commissioned_packs.commissioned_pack.batch_identifier IS 'The batch.';
COMMENT ON COLUMN commissioned_packs.commissioned_pack.pack_expiry_date IS 'The expiry printed on the pack.';
COMMENT ON COLUMN commissioned_packs.commissioned_pack.pack_commissioned_timestamp IS 'When commissioned.';
COMMENT ON COLUMN commissioned_packs.commissioned_pack.pack_verified_flag IS 'Whether the applied identifier was read back and verified.';
COMMENT ON COLUMN commissioned_packs.commissioned_pack.equipment_identifier IS 'The line.';

CREATE TABLE IF NOT EXISTS commissioned_packs.pack_to_case_assignment (
  pack_serial_number        varchar(40) NOT NULL,
  case_serial_number        varchar(40) NOT NULL,
  pack_aggregated_timestamp timestamptz NOT NULL,
  CONSTRAINT pack_to_case_assignment_pk PRIMARY KEY (pack_serial_number)
);
COMMENT ON TABLE commissioned_packs.pack_to_case_assignment IS 'One row per pack placed in a case.';
COMMENT ON COLUMN commissioned_packs.pack_to_case_assignment.pack_serial_number IS 'The pack.';
COMMENT ON COLUMN commissioned_packs.pack_to_case_assignment.case_serial_number IS 'The case it was placed in.';
COMMENT ON COLUMN commissioned_packs.pack_to_case_assignment.pack_aggregated_timestamp IS 'When.';

GRANT ALL ON ALL TABLES IN SCHEMA commissioned_packs TO egeria_admin, egeria_user, airflow_user;

-- Pack Aggregation Hierarchy  (DigitalProduct::Coco::Pack Aggregation Hierarchy)
CREATE SCHEMA IF NOT EXISTS pack_aggregation_hierarchy;
GRANT ALL ON SCHEMA pack_aggregation_hierarchy TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA pack_aggregation_hierarchy IS 'Which packs are in which case and which cases are on which pallet. The relationships allow a shipment to be verified without opening it and make a recall a query rather than a search.';

CREATE TABLE IF NOT EXISTS pack_aggregation_hierarchy.aggregation_relationship (
  aggregation_identifier           varchar(40) NOT NULL,
  aggregation_parent_serial_number varchar(40) NOT NULL,
  aggregation_parent_type          varchar(10) NOT NULL,
  aggregation_child_serial_number  varchar(40) NOT NULL,
  aggregation_child_type           varchar(10) NOT NULL,
  aggregation_timestamp            timestamptz NOT NULL,
  batch_identifier                 varchar(40) NOT NULL,
  CONSTRAINT aggregation_relationship_pk PRIMARY KEY (aggregation_identifier)
);
COMMENT ON TABLE pack_aggregation_hierarchy.aggregation_relationship IS 'One row per containment of one serialised unit in another.';
COMMENT ON COLUMN pack_aggregation_hierarchy.aggregation_relationship.aggregation_identifier IS 'The relationship.';
COMMENT ON COLUMN pack_aggregation_hierarchy.aggregation_relationship.aggregation_parent_serial_number IS 'The containing case or pallet.';
COMMENT ON COLUMN pack_aggregation_hierarchy.aggregation_relationship.aggregation_parent_type IS 'Case or pallet.';
COMMENT ON COLUMN pack_aggregation_hierarchy.aggregation_relationship.aggregation_child_serial_number IS 'The contained pack or case.';
COMMENT ON COLUMN pack_aggregation_hierarchy.aggregation_relationship.aggregation_child_type IS 'Pack or case.';
COMMENT ON COLUMN pack_aggregation_hierarchy.aggregation_relationship.aggregation_timestamp IS 'When recorded.';
COMMENT ON COLUMN pack_aggregation_hierarchy.aggregation_relationship.batch_identifier IS 'The batch.';

GRANT ALL ON ALL TABLES IN SCHEMA pack_aggregation_hierarchy TO egeria_admin, egeria_user, airflow_user;

-- Serialised Product Identifiers  (DigitalProduct::Coco::Serialised Product Identifiers)
CREATE SCHEMA IF NOT EXISTS serialised_product_identifiers;
GRANT ALL ON SCHEMA serialised_product_identifiers TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA serialised_product_identifiers IS 'The company''s own record of every identifier issued, commissioned, aggregated, shipped and decommissioned, and the alert dispositions that corrected it. It is the reconciliation point against the external verification systems, and the reason a discrepancy can be attributed rather than merely observed.';

CREATE TABLE IF NOT EXISTS serialised_product_identifiers.serialised_identifier (
  pack_serial_number               varchar(40) NOT NULL,
  product_code                     varchar(20) NOT NULL,
  pack_code                        varchar(20) NOT NULL,
  batch_identifier                 varchar(40) NOT NULL,
  pack_expiry_date                 date NOT NULL,
  market_code                      varchar(8) NOT NULL,
  pack_current_status              varchar(20) NOT NULL,
  aggregation_parent_serial_number varchar(40),
  warehouse_code                   varchar(20),
  CONSTRAINT serialised_identifier_pk PRIMARY KEY (pack_serial_number)
);
COMMENT ON TABLE serialised_product_identifiers.serialised_identifier IS 'One row per identifier, its current state.';
COMMENT ON COLUMN serialised_product_identifiers.serialised_identifier.pack_serial_number IS 'The identifier.';
COMMENT ON COLUMN serialised_product_identifiers.serialised_identifier.product_code IS 'The product.';
COMMENT ON COLUMN serialised_product_identifiers.serialised_identifier.pack_code IS 'The presentation.';
COMMENT ON COLUMN serialised_product_identifiers.serialised_identifier.batch_identifier IS 'The batch.';
COMMENT ON COLUMN serialised_product_identifiers.serialised_identifier.pack_expiry_date IS 'The expiry.';
COMMENT ON COLUMN serialised_product_identifiers.serialised_identifier.market_code IS 'The destination market.';
COMMENT ON COLUMN serialised_product_identifiers.serialised_identifier.pack_current_status IS 'Allocated, commissioned, aggregated, shipped, decommissioned or destroyed.';
COMMENT ON COLUMN serialised_product_identifiers.serialised_identifier.aggregation_parent_serial_number IS 'The case or pallet currently containing it.';
COMMENT ON COLUMN serialised_product_identifiers.serialised_identifier.warehouse_code IS 'The location, while in stock.';

CREATE TABLE IF NOT EXISTS serialised_product_identifiers.identifier_event (
  pack_serial_number   varchar(40) NOT NULL,
  pack_event_timestamp timestamptz NOT NULL,
  pack_event_type      varchar(20) NOT NULL,
  system_identifier    varchar(60) NOT NULL,
  alert_identifier     varchar(40),
  CONSTRAINT identifier_event_pk PRIMARY KEY (pack_serial_number, pack_event_timestamp)
);
COMMENT ON TABLE serialised_product_identifiers.identifier_event IS 'One row per change of state of an identifier.';
COMMENT ON COLUMN serialised_product_identifiers.identifier_event.pack_serial_number IS 'The identifier.';
COMMENT ON COLUMN serialised_product_identifiers.identifier_event.pack_event_timestamp IS 'When.';
COMMENT ON COLUMN serialised_product_identifiers.identifier_event.pack_event_type IS 'Commissioned, aggregated, shipped, verified, decommissioned, corrected.';
COMMENT ON COLUMN serialised_product_identifiers.identifier_event.system_identifier IS 'The system that reported the event.';
COMMENT ON COLUMN serialised_product_identifiers.identifier_event.alert_identifier IS 'The alert disposition that caused a correction, if any.';

GRANT ALL ON ALL TABLES IN SCHEMA serialised_product_identifiers TO egeria_admin, egeria_user, airflow_user;

-- Market Identifier Submissions  (DigitalProduct::Coco::Market Identifier Submissions)
CREATE SCHEMA IF NOT EXISTS market_identifier_submissions;
GRANT ALL ON SCHEMA market_identifier_submissions TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA market_identifier_submissions IS 'The identifier records uploaded to the national and regional verification systems of each destination market, together with the release authorisation each upload relied on. Destination determines the scheme, so the same production run may leave through several routes.';

CREATE TABLE IF NOT EXISTS market_identifier_submissions.identifier_submission (
  submission_identifier        varchar(40) NOT NULL,
  batch_identifier             varchar(40) NOT NULL,
  market_code                  varchar(8) NOT NULL,
  verification_scheme_code     varchar(20) NOT NULL,
  submission_timestamp         timestamptz NOT NULL,
  submission_count             integer NOT NULL,
  submission_acknowledged_flag boolean NOT NULL,
  batch_certification_date     date NOT NULL,
  CONSTRAINT identifier_submission_pk PRIMARY KEY (submission_identifier)
);
COMMENT ON TABLE market_identifier_submissions.identifier_submission IS 'One row per batch per market scheme uploaded to.';
COMMENT ON COLUMN market_identifier_submissions.identifier_submission.submission_identifier IS 'The upload.';
COMMENT ON COLUMN market_identifier_submissions.identifier_submission.batch_identifier IS 'The batch.';
COMMENT ON COLUMN market_identifier_submissions.identifier_submission.market_code IS 'The market.';
COMMENT ON COLUMN market_identifier_submissions.identifier_submission.verification_scheme_code IS 'The national or regional scheme.';
COMMENT ON COLUMN market_identifier_submissions.identifier_submission.submission_timestamp IS 'When uploaded.';
COMMENT ON COLUMN market_identifier_submissions.identifier_submission.submission_count IS 'The number of identifiers uploaded.';
COMMENT ON COLUMN market_identifier_submissions.identifier_submission.submission_acknowledged_flag IS 'Whether the scheme acknowledged the upload.';
COMMENT ON COLUMN market_identifier_submissions.identifier_submission.batch_certification_date IS 'The certification the upload relied on.';

GRANT ALL ON ALL TABLES IN SCHEMA market_identifier_submissions TO egeria_admin, egeria_user, airflow_user;

-- Market Verification Responses  (DigitalProduct::Coco::Market Verification Responses)
CREATE SCHEMA IF NOT EXISTS market_verification_responses;
GRANT ALL ON SCHEMA market_verification_responses TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA market_verification_responses IS 'What the national verification systems send back: verification results, decommissioning events, and the alerts raised when a pharmacy or trading partner scans an identifier that does not verify. The data originates outside the company, in systems that are opaque to it.';

CREATE TABLE IF NOT EXISTS market_verification_responses.verification_result (
  verification_event_identifier varchar(40) NOT NULL,
  pack_serial_number            varchar(40) NOT NULL,
  verification_scheme_code      varchar(20) NOT NULL,
  verification_event_type       varchar(20) NOT NULL,
  verification_event_timestamp  timestamptz NOT NULL,
  market_code                   varchar(8) NOT NULL,
  CONSTRAINT verification_result_pk PRIMARY KEY (verification_event_identifier)
);
COMMENT ON TABLE market_verification_responses.verification_result IS 'One row per verification or decommissioning event received.';
COMMENT ON COLUMN market_verification_responses.verification_result.verification_event_identifier IS 'The event.';
COMMENT ON COLUMN market_verification_responses.verification_result.pack_serial_number IS 'The identifier scanned.';
COMMENT ON COLUMN market_verification_responses.verification_result.verification_scheme_code IS 'The scheme reporting.';
COMMENT ON COLUMN market_verification_responses.verification_result.verification_event_type IS 'Verified, decommissioned, or failed.';
COMMENT ON COLUMN market_verification_responses.verification_result.verification_event_timestamp IS 'When.';
COMMENT ON COLUMN market_verification_responses.verification_result.market_code IS 'The market.';

CREATE TABLE IF NOT EXISTS market_verification_responses.verification_alert (
  alert_identifier           varchar(40) NOT NULL,
  pack_serial_number         varchar(40) NOT NULL,
  verification_scheme_code   varchar(20) NOT NULL,
  alert_type                 varchar(40) NOT NULL,
  alert_raised_timestamp     timestamptz NOT NULL,
  alert_reporter_description text NOT NULL,
  CONSTRAINT verification_alert_pk PRIMARY KEY (alert_identifier)
);
COMMENT ON TABLE market_verification_responses.verification_alert IS 'One row per alert raised by a scheme.';
COMMENT ON COLUMN market_verification_responses.verification_alert.alert_identifier IS 'The alert.';
COMMENT ON COLUMN market_verification_responses.verification_alert.pack_serial_number IS 'The identifier involved.';
COMMENT ON COLUMN market_verification_responses.verification_alert.verification_scheme_code IS 'The scheme.';
COMMENT ON COLUMN market_verification_responses.verification_alert.alert_type IS 'Unknown identifier, already decommissioned, expiry mismatch or other.';
COMMENT ON COLUMN market_verification_responses.verification_alert.alert_raised_timestamp IS 'When raised.';
COMMENT ON COLUMN market_verification_responses.verification_alert.alert_reporter_description IS 'The pharmacy or partner that scanned.';

GRANT ALL ON ALL TABLES IN SCHEMA market_verification_responses TO egeria_admin, egeria_user, airflow_user;

-- ================================================================================================
-- quality-systems.md
-- ================================================================================================

-- Consolidated Safety Reports  (DigitalProduct::Coco::Consolidated Safety Reports)
CREATE SCHEMA IF NOT EXISTS consolidated_safety_reports;
GRANT ALL ON SCHEMA consolidated_safety_reports TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA consolidated_safety_reports IS 'Every suspected adverse reaction registered at the single point of intake, whatever door it arrived through: a clinician''s report, a complaint with safety content or a trial site''s report. The statutory clock starts on first receipt anywhere in the company.';

CREATE TABLE IF NOT EXISTS consolidated_safety_reports.safety_report (
  safety_report_identifier         varchar(40) NOT NULL,
  safety_report_received_timestamp timestamptz NOT NULL,
  safety_report_source_type        varchar(20) NOT NULL,
  safety_report_source_identifier  varchar(40) NOT NULL,
  patient_pseudonym_identifier     varchar(40),
  product_code                     varchar(20) NOT NULL,
  batch_identifier                 varchar(40),
  clinical_trial_identifier        varchar(40),
  adverse_event_description        text NOT NULL,
  safety_case_identifier           varchar(40),
  CONSTRAINT safety_report_pk PRIMARY KEY (safety_report_identifier)
);
COMMENT ON TABLE consolidated_safety_reports.safety_report IS 'One row per suspected reaction registered.';
COMMENT ON COLUMN consolidated_safety_reports.safety_report.safety_report_identifier IS 'The report.';
COMMENT ON COLUMN consolidated_safety_reports.safety_report.safety_report_received_timestamp IS 'When first received anywhere in the company.';
COMMENT ON COLUMN consolidated_safety_reports.safety_report.safety_report_source_type IS 'Clinician, complaint, trial site, literature or other.';
COMMENT ON COLUMN consolidated_safety_reports.safety_report.safety_report_source_identifier IS 'The originating report or complaint.';
COMMENT ON COLUMN consolidated_safety_reports.safety_report.patient_pseudonym_identifier IS 'The patient or participant, by pseudonym.';
COMMENT ON COLUMN consolidated_safety_reports.safety_report.product_code IS 'The product.';
COMMENT ON COLUMN consolidated_safety_reports.safety_report.batch_identifier IS 'The batch, if known.';
COMMENT ON COLUMN consolidated_safety_reports.safety_report.clinical_trial_identifier IS 'The trial, for a site report.';
COMMENT ON COLUMN consolidated_safety_reports.safety_report.adverse_event_description IS 'The reaction as reported.';
COMMENT ON COLUMN consolidated_safety_reports.safety_report.safety_case_identifier IS 'The case opened from the report.';

GRANT ALL ON ALL TABLES IN SCHEMA consolidated_safety_reports TO egeria_admin, egeria_user, airflow_user;

-- Product Complaints  (DigitalProduct::Coco::Product Complaints)
CREATE SCHEMA IF NOT EXISTS product_complaints;
GRANT ALL ON SCHEMA product_complaints TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA product_complaints IS 'Complaints about product quality from pharmacies, distributors and patients, and the assessment that separates those which are also potential safety events from those which are not. The separation is deliberately generous.';

CREATE TABLE IF NOT EXISTS product_complaints.complaint (
  complaint_identifier         varchar(40) NOT NULL,
  complaint_received_timestamp timestamptz NOT NULL,
  complaint_reporter_type      varchar(20) NOT NULL,
  product_code                 varchar(20) NOT NULL,
  batch_identifier             varchar(40),
  pack_serial_number           varchar(40),
  complaint_description        text NOT NULL,
  complaint_current_status     varchar(20) NOT NULL,
  CONSTRAINT complaint_pk PRIMARY KEY (complaint_identifier)
);
COMMENT ON TABLE product_complaints.complaint IS 'One row per complaint received.';
COMMENT ON COLUMN product_complaints.complaint.complaint_identifier IS 'The complaint.';
COMMENT ON COLUMN product_complaints.complaint.complaint_received_timestamp IS 'When received.';
COMMENT ON COLUMN product_complaints.complaint.complaint_reporter_type IS 'Pharmacy, distributor, patient, healthcare professional.';
COMMENT ON COLUMN product_complaints.complaint.product_code IS 'The product.';
COMMENT ON COLUMN product_complaints.complaint.batch_identifier IS 'The batch, if known.';
COMMENT ON COLUMN product_complaints.complaint.pack_serial_number IS 'The pack, if known.';
COMMENT ON COLUMN product_complaints.complaint.complaint_description IS 'The complaint.';
COMMENT ON COLUMN product_complaints.complaint.complaint_current_status IS 'Open, under investigation, closed.';

CREATE TABLE IF NOT EXISTS product_complaints.complaint_safety_assessment (
  complaint_identifier           varchar(40) NOT NULL,
  complaint_safety_flag          boolean NOT NULL,
  complaint_assessor_identifier  varchar(40) NOT NULL,
  complaint_assessment_timestamp timestamptz NOT NULL,
  safety_report_identifier       varchar(40),
  CONSTRAINT complaint_safety_assessment_pk PRIMARY KEY (complaint_identifier)
);
COMMENT ON TABLE product_complaints.complaint_safety_assessment IS 'One row per complaint, whether it carries a potential safety event.';
COMMENT ON COLUMN product_complaints.complaint_safety_assessment.complaint_identifier IS 'The complaint.';
COMMENT ON COLUMN product_complaints.complaint_safety_assessment.complaint_safety_flag IS 'Whether it is also a suspected adverse reaction.';
COMMENT ON COLUMN product_complaints.complaint_safety_assessment.complaint_assessor_identifier IS 'Who assessed.';
COMMENT ON COLUMN product_complaints.complaint_safety_assessment.complaint_assessment_timestamp IS 'When.';
COMMENT ON COLUMN product_complaints.complaint_safety_assessment.safety_report_identifier IS 'The safety report raised, if any.';

GRANT ALL ON ALL TABLES IN SCHEMA product_complaints TO egeria_admin, egeria_user, airflow_user;

-- Pharmacovigilance Cases  (DigitalProduct::Coco::Pharmacovigilance Cases)
CREATE SCHEMA IF NOT EXISTS pharmacovigilance_cases;
GRANT ALL ON SCHEMA pharmacovigilance_cases TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA pharmacovigilance_cases IS 'The safety case from receipt through follow-up to closure, carrying the reporting clock that the regulators measure, with the narrative sent for assessment and the coded data that signal detection reads. Every other component in the safety chain either feeds it or reads from it.';

CREATE TABLE IF NOT EXISTS pharmacovigilance_cases.safety_case (
  safety_case_identifier         varchar(40) NOT NULL,
  safety_report_identifier       varchar(40) NOT NULL,
  safety_case_received_timestamp timestamptz NOT NULL,
  product_code                   varchar(20) NOT NULL,
  patient_pseudonym_identifier   varchar(40),
  safety_case_seriousness_code   varchar(20),
  safety_case_expectedness_code  varchar(20),
  safety_case_causality_code     varchar(20),
  safety_case_reporting_due_date date NOT NULL,
  safety_case_current_status     varchar(20) NOT NULL,
  CONSTRAINT safety_case_pk PRIMARY KEY (safety_case_identifier)
);
COMMENT ON TABLE pharmacovigilance_cases.safety_case IS 'One row per case.';
COMMENT ON COLUMN pharmacovigilance_cases.safety_case.safety_case_identifier IS 'The case.';
COMMENT ON COLUMN pharmacovigilance_cases.safety_case.safety_report_identifier IS 'The report it was opened from.';
COMMENT ON COLUMN pharmacovigilance_cases.safety_case.safety_case_received_timestamp IS 'The receipt timestamp the clock runs from.';
COMMENT ON COLUMN pharmacovigilance_cases.safety_case.product_code IS 'The product.';
COMMENT ON COLUMN pharmacovigilance_cases.safety_case.patient_pseudonym_identifier IS 'The patient, by pseudonym.';
COMMENT ON COLUMN pharmacovigilance_cases.safety_case.safety_case_seriousness_code IS 'Serious or non-serious, once assessed.';
COMMENT ON COLUMN pharmacovigilance_cases.safety_case.safety_case_expectedness_code IS 'Expected or unexpected, once assessed.';
COMMENT ON COLUMN pharmacovigilance_cases.safety_case.safety_case_causality_code IS 'The causality assessment.';
COMMENT ON COLUMN pharmacovigilance_cases.safety_case.safety_case_reporting_due_date IS 'When the regulatory report is due.';
COMMENT ON COLUMN pharmacovigilance_cases.safety_case.safety_case_current_status IS 'Open, awaiting assessment, follow-up, submitted, closed.';

CREATE TABLE IF NOT EXISTS pharmacovigilance_cases.case_narrative (
  safety_case_identifier              varchar(40) NOT NULL,
  safety_case_narrative_description   text NOT NULL,
  patient_birth_date                  date,
  patient_sex_code                    varchar(1),
  safety_case_concomitant_description text,
  CONSTRAINT case_narrative_pk PRIMARY KEY (safety_case_identifier)
);
COMMENT ON TABLE pharmacovigilance_cases.case_narrative IS 'One row per case, the narrative and patient context sent for medical assessment.';
COMMENT ON COLUMN pharmacovigilance_cases.case_narrative.safety_case_identifier IS 'The case.';
COMMENT ON COLUMN pharmacovigilance_cases.case_narrative.safety_case_narrative_description IS 'The clinical narrative.';
COMMENT ON COLUMN pharmacovigilance_cases.case_narrative.patient_birth_date IS 'The patient''s date of birth, where reported.';
COMMENT ON COLUMN pharmacovigilance_cases.case_narrative.patient_sex_code IS 'The patient''s sex, where reported.';
COMMENT ON COLUMN pharmacovigilance_cases.case_narrative.safety_case_concomitant_description IS 'Other treatments in use.';

CREATE TABLE IF NOT EXISTS pharmacovigilance_cases.case_follow_up (
  safety_case_identifier            varchar(40) NOT NULL,
  safety_case_follow_up_number      integer NOT NULL,
  safety_case_follow_up_date        date NOT NULL,
  safety_case_follow_up_description text NOT NULL,
  CONSTRAINT case_follow_up_pk PRIMARY KEY (safety_case_identifier, safety_case_follow_up_number)
);
COMMENT ON TABLE pharmacovigilance_cases.case_follow_up IS 'One row per follow-up action on a case.';
COMMENT ON COLUMN pharmacovigilance_cases.case_follow_up.safety_case_identifier IS 'The case.';
COMMENT ON COLUMN pharmacovigilance_cases.case_follow_up.safety_case_follow_up_number IS 'The follow-up''s sequence.';
COMMENT ON COLUMN pharmacovigilance_cases.case_follow_up.safety_case_follow_up_date IS 'When.';
COMMENT ON COLUMN pharmacovigilance_cases.case_follow_up.safety_case_follow_up_description IS 'What was requested or received.';

GRANT ALL ON ALL TABLES IN SCHEMA pharmacovigilance_cases TO egeria_admin, egeria_user, airflow_user;

-- Medical Assessments  (DigitalProduct::Coco::Medical Assessments)
CREATE SCHEMA IF NOT EXISTS medical_assessments;
GRANT ALL ON SCHEMA medical_assessments TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA medical_assessments IS 'The qualified medical judgement of seriousness, expectedness and causality for each case, and the coding of the event to the standard dictionary. It is the step that decides whether a report is expedited or periodic.';

CREATE TABLE IF NOT EXISTS medical_assessments.medical_assessment (
  safety_case_identifier           varchar(40) NOT NULL,
  safety_case_assessment_timestamp timestamptz NOT NULL,
  safety_case_assessor_identifier  varchar(40) NOT NULL,
  safety_case_seriousness_code     varchar(20) NOT NULL,
  safety_case_expectedness_code    varchar(20) NOT NULL,
  safety_case_causality_code       varchar(20) NOT NULL,
  safety_case_assessment_notes     text,
  CONSTRAINT medical_assessment_pk PRIMARY KEY (safety_case_identifier, safety_case_assessment_timestamp)
);
COMMENT ON TABLE medical_assessments.medical_assessment IS 'One row per assessment of a case.';
COMMENT ON COLUMN medical_assessments.medical_assessment.safety_case_identifier IS 'The case.';
COMMENT ON COLUMN medical_assessments.medical_assessment.safety_case_assessment_timestamp IS 'When.';
COMMENT ON COLUMN medical_assessments.medical_assessment.safety_case_assessor_identifier IS 'The assessing physician.';
COMMENT ON COLUMN medical_assessments.medical_assessment.safety_case_seriousness_code IS 'Serious or non-serious.';
COMMENT ON COLUMN medical_assessments.medical_assessment.safety_case_expectedness_code IS 'Expected or unexpected against the label.';
COMMENT ON COLUMN medical_assessments.medical_assessment.safety_case_causality_code IS 'The causality assessment.';
COMMENT ON COLUMN medical_assessments.medical_assessment.safety_case_assessment_notes IS 'The assessor''s reasoning.';

CREATE TABLE IF NOT EXISTS medical_assessments.coded_term (
  safety_case_identifier           varchar(40) NOT NULL,
  adverse_event_code               varchar(20) NOT NULL,
  adverse_event_dictionary_version varchar(10) NOT NULL,
  adverse_event_term_name          text NOT NULL,
  adverse_event_primary_flag       boolean NOT NULL,
  CONSTRAINT coded_term_pk PRIMARY KEY (safety_case_identifier, adverse_event_code)
);
COMMENT ON TABLE medical_assessments.coded_term IS 'One row per dictionary term coded against a case.';
COMMENT ON COLUMN medical_assessments.coded_term.safety_case_identifier IS 'The case.';
COMMENT ON COLUMN medical_assessments.coded_term.adverse_event_code IS 'The dictionary code.';
COMMENT ON COLUMN medical_assessments.coded_term.adverse_event_dictionary_version IS 'The dictionary version.';
COMMENT ON COLUMN medical_assessments.coded_term.adverse_event_term_name IS 'The term.';
COMMENT ON COLUMN medical_assessments.coded_term.adverse_event_primary_flag IS 'Whether this is the primary event.';

GRANT ALL ON ALL TABLES IN SCHEMA medical_assessments TO egeria_admin, egeria_user, airflow_user;

-- Safety Signals  (DigitalProduct::Coco::Safety Signals)
CREATE SCHEMA IF NOT EXISTS safety_signals;
GRANT ALL ON SCHEMA safety_signals TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA safety_signals IS 'The patterns found across accumulated cases that no single case shows, with the exposure denominators they were assessed against, and the referrals made to quality and to the authorisation register. A signal visible across trial and post-market data is invisible in either alone.';

CREATE TABLE IF NOT EXISTS safety_signals.safety_signal (
  signal_identifier         varchar(40) NOT NULL,
  signal_detected_date      date NOT NULL,
  product_code              varchar(20) NOT NULL,
  adverse_event_code        varchar(20) NOT NULL,
  signal_contributing_count integer NOT NULL,
  signal_description        text NOT NULL,
  signal_current_status     varchar(20) NOT NULL,
  signal_referral_type      varchar(20),
  CONSTRAINT safety_signal_pk PRIMARY KEY (signal_identifier)
);
COMMENT ON TABLE safety_signals.safety_signal IS 'One row per signal detected.';
COMMENT ON COLUMN safety_signals.safety_signal.signal_identifier IS 'The signal.';
COMMENT ON COLUMN safety_signals.safety_signal.signal_detected_date IS 'When detected.';
COMMENT ON COLUMN safety_signals.safety_signal.product_code IS 'The product.';
COMMENT ON COLUMN safety_signals.safety_signal.adverse_event_code IS 'The event term.';
COMMENT ON COLUMN safety_signals.safety_signal.signal_contributing_count IS 'The number of cases contributing.';
COMMENT ON COLUMN safety_signals.safety_signal.signal_description IS 'The pattern observed.';
COMMENT ON COLUMN safety_signals.safety_signal.signal_current_status IS 'Detected, under evaluation, confirmed, refuted.';
COMMENT ON COLUMN safety_signals.safety_signal.signal_referral_type IS 'Referred to quality, to authorisation, both or neither.';

CREATE TABLE IF NOT EXISTS safety_signals.exposure_denominator (
  product_code                varchar(20) NOT NULL,
  exposure_period_code        varchar(10) NOT NULL,
  exposure_count              integer NOT NULL,
  exposure_source_description text NOT NULL,
  CONSTRAINT exposure_denominator_pk PRIMARY KEY (product_code, exposure_period_code)
);
COMMENT ON TABLE safety_signals.exposure_denominator IS 'One row per product per period, the exposure the signal rate was measured against.';
COMMENT ON COLUMN safety_signals.exposure_denominator.product_code IS 'The product.';
COMMENT ON COLUMN safety_signals.exposure_denominator.exposure_period_code IS 'The period.';
COMMENT ON COLUMN safety_signals.exposure_denominator.exposure_count IS 'The estimated number of patients exposed.';
COMMENT ON COLUMN safety_signals.exposure_denominator.exposure_source_description IS 'How the estimate was derived.';

GRANT ALL ON ALL TABLES IN SCHEMA safety_signals TO egeria_admin, egeria_user, airflow_user;

-- Regulatory Safety Submissions  (DigitalProduct::Coco::Regulatory Safety Submissions)
CREATE SCHEMA IF NOT EXISTS regulatory_safety_submissions;
GRANT ALL ON SCHEMA regulatory_safety_submissions TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA regulatory_safety_submissions IS 'The expedited and periodic safety reports formatted and transmitted to the regulator of each market the product is authorised in, and the acknowledgement each received. An unacknowledged submission is not a submission.';

CREATE TABLE IF NOT EXISTS regulatory_safety_submissions.safety_submission (
  submission_identifier     varchar(40) NOT NULL,
  safety_case_identifier    varchar(40),
  product_code              varchar(20) NOT NULL,
  market_code               varchar(8) NOT NULL,
  submission_regulator_code varchar(20) NOT NULL,
  submission_type           varchar(20) NOT NULL,
  submission_due_date       date NOT NULL,
  submission_timestamp      timestamptz NOT NULL,
  submission_format_code    varchar(20) NOT NULL,
  CONSTRAINT safety_submission_pk PRIMARY KEY (submission_identifier)
);
COMMENT ON TABLE regulatory_safety_submissions.safety_submission IS 'One row per report submitted to a regulator.';
COMMENT ON COLUMN regulatory_safety_submissions.safety_submission.submission_identifier IS 'The submission.';
COMMENT ON COLUMN regulatory_safety_submissions.safety_submission.safety_case_identifier IS 'The case, for an expedited report.';
COMMENT ON COLUMN regulatory_safety_submissions.safety_submission.product_code IS 'The product.';
COMMENT ON COLUMN regulatory_safety_submissions.safety_submission.market_code IS 'The market.';
COMMENT ON COLUMN regulatory_safety_submissions.safety_submission.submission_regulator_code IS 'The regulator.';
COMMENT ON COLUMN regulatory_safety_submissions.safety_submission.submission_type IS 'Expedited or periodic.';
COMMENT ON COLUMN regulatory_safety_submissions.safety_submission.submission_due_date IS 'When due.';
COMMENT ON COLUMN regulatory_safety_submissions.safety_submission.submission_timestamp IS 'When transmitted.';
COMMENT ON COLUMN regulatory_safety_submissions.safety_submission.submission_format_code IS 'The format used.';

CREATE TABLE IF NOT EXISTS regulatory_safety_submissions.submission_acknowledgement (
  submission_acknowledgement_identifier varchar(60) NOT NULL,
  submission_identifier                 varchar(40) NOT NULL,
  submission_acknowledged_timestamp     timestamptz NOT NULL,
  submission_acknowledgement_status     varchar(20) NOT NULL,
  CONSTRAINT submission_acknowledgement_pk PRIMARY KEY (submission_acknowledgement_identifier)
);
COMMENT ON TABLE regulatory_safety_submissions.submission_acknowledgement IS 'One row per acknowledgement received.';
COMMENT ON COLUMN regulatory_safety_submissions.submission_acknowledgement.submission_acknowledgement_identifier IS 'The regulator''s reference.';
COMMENT ON COLUMN regulatory_safety_submissions.submission_acknowledgement.submission_identifier IS 'The submission.';
COMMENT ON COLUMN regulatory_safety_submissions.submission_acknowledgement.submission_acknowledged_timestamp IS 'When acknowledged.';
COMMENT ON COLUMN regulatory_safety_submissions.submission_acknowledgement.submission_acknowledgement_status IS 'Accepted, rejected or queried.';

GRANT ALL ON ALL TABLES IN SCHEMA regulatory_safety_submissions TO egeria_admin, egeria_user, airflow_user;

-- Laboratory Test Results  (DigitalProduct::Coco::Laboratory Test Results)
CREATE SCHEMA IF NOT EXISTS laboratory_test_results;
GRANT ALL ON SCHEMA laboratory_test_results TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA laboratory_test_results IS 'Sampling, testing and results for raw materials, in-process checks and finished product, compared against specification, and the certificates of analysis issued for release. Results are gates rather than reports: material cannot be issued and product cannot be released until the laboratory has answered.';

CREATE TABLE IF NOT EXISTS laboratory_test_results.sample (
  sample_identifier           varchar(40) NOT NULL,
  sample_type                 varchar(20) NOT NULL,
  lot_identifier              varchar(40),
  batch_identifier            varchar(40),
  sample_collection_timestamp timestamptz NOT NULL,
  sample_current_status       varchar(20) NOT NULL,
  CONSTRAINT sample_pk PRIMARY KEY (sample_identifier)
);
COMMENT ON TABLE laboratory_test_results.sample IS 'One row per sample taken for testing.';
COMMENT ON COLUMN laboratory_test_results.sample.sample_identifier IS 'The sample.';
COMMENT ON COLUMN laboratory_test_results.sample.sample_type IS 'Raw material, in-process or finished product.';
COMMENT ON COLUMN laboratory_test_results.sample.lot_identifier IS 'The material lot, for raw material.';
COMMENT ON COLUMN laboratory_test_results.sample.batch_identifier IS 'The batch, for in-process and finished product.';
COMMENT ON COLUMN laboratory_test_results.sample.sample_collection_timestamp IS 'When taken.';
COMMENT ON COLUMN laboratory_test_results.sample.sample_current_status IS 'Received, in test, complete.';

CREATE TABLE IF NOT EXISTS laboratory_test_results.test_result (
  test_result_identifier      varchar(40) NOT NULL,
  sample_identifier           varchar(40) NOT NULL,
  test_code                   varchar(40) NOT NULL,
  test_value                  varchar(60) NOT NULL,
  test_unit                   varchar(20),
  specification_minimum_value varchar(60),
  specification_maximum_value varchar(60),
  test_conformity_flag        boolean NOT NULL,
  test_completed_timestamp    timestamptz NOT NULL,
  test_analyst_identifier     varchar(40) NOT NULL,
  CONSTRAINT test_result_pk PRIMARY KEY (test_result_identifier)
);
COMMENT ON TABLE laboratory_test_results.test_result IS 'One row per test on a sample.';
COMMENT ON COLUMN laboratory_test_results.test_result.test_result_identifier IS 'The result.';
COMMENT ON COLUMN laboratory_test_results.test_result.sample_identifier IS 'The sample.';
COMMENT ON COLUMN laboratory_test_results.test_result.test_code IS 'The test.';
COMMENT ON COLUMN laboratory_test_results.test_result.test_value IS 'The result.';
COMMENT ON COLUMN laboratory_test_results.test_result.test_unit IS 'The unit.';
COMMENT ON COLUMN laboratory_test_results.test_result.specification_minimum_value IS 'The lower limit.';
COMMENT ON COLUMN laboratory_test_results.test_result.specification_maximum_value IS 'The upper limit.';
COMMENT ON COLUMN laboratory_test_results.test_result.test_conformity_flag IS 'Whether the result is within specification.';
COMMENT ON COLUMN laboratory_test_results.test_result.test_completed_timestamp IS 'When completed.';
COMMENT ON COLUMN laboratory_test_results.test_result.test_analyst_identifier IS 'The analyst.';

CREATE TABLE IF NOT EXISTS laboratory_test_results.certificate_of_analysis (
  certificate_identifier          varchar(40) NOT NULL,
  batch_identifier                varchar(40),
  lot_identifier                  varchar(40),
  certificate_date                date NOT NULL,
  certificate_conformity_flag     boolean NOT NULL,
  certificate_approver_identifier varchar(40) NOT NULL,
  CONSTRAINT certificate_of_analysis_pk PRIMARY KEY (certificate_identifier)
);
COMMENT ON TABLE laboratory_test_results.certificate_of_analysis IS 'One row per certificate issued for a batch or lot.';
COMMENT ON COLUMN laboratory_test_results.certificate_of_analysis.certificate_identifier IS 'The certificate.';
COMMENT ON COLUMN laboratory_test_results.certificate_of_analysis.batch_identifier IS 'The batch, for finished product.';
COMMENT ON COLUMN laboratory_test_results.certificate_of_analysis.lot_identifier IS 'The lot, for material.';
COMMENT ON COLUMN laboratory_test_results.certificate_of_analysis.certificate_date IS 'When issued.';
COMMENT ON COLUMN laboratory_test_results.certificate_of_analysis.certificate_conformity_flag IS 'Whether every test conformed.';
COMMENT ON COLUMN laboratory_test_results.certificate_of_analysis.certificate_approver_identifier IS 'Who approved the certificate.';

GRANT ALL ON ALL TABLES IN SCHEMA laboratory_test_results TO egeria_admin, egeria_user, airflow_user;

-- Deviations And CAPAs  (DigitalProduct::Coco::Deviations And CAPAs)
CREATE SCHEMA IF NOT EXISTS deviations_and_capas;
GRANT ALL ON SCHEMA deviations_and_capas TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA deviations_and_capas IS 'Departures from the approved process, their investigation and the corrective and preventive actions that follow, including the signals referred from safety. An open deviation is a gate on certification, so this sits inside the release flow rather than beside it.';

CREATE TABLE IF NOT EXISTS deviations_and_capas.deviation (
  deviation_identifier       varchar(40) NOT NULL,
  deviation_raised_timestamp timestamptz NOT NULL,
  deviation_source_type      varchar(20) NOT NULL,
  batch_identifier           varchar(40),
  product_code               varchar(20),
  signal_identifier          varchar(40),
  deviation_description      text NOT NULL,
  deviation_severity         varchar(20) NOT NULL,
  deviation_current_status   varchar(20) NOT NULL,
  CONSTRAINT deviation_pk PRIMARY KEY (deviation_identifier)
);
COMMENT ON TABLE deviations_and_capas.deviation IS 'One row per deviation raised.';
COMMENT ON COLUMN deviations_and_capas.deviation.deviation_identifier IS 'The deviation.';
COMMENT ON COLUMN deviations_and_capas.deviation.deviation_raised_timestamp IS 'When raised.';
COMMENT ON COLUMN deviations_and_capas.deviation.deviation_source_type IS 'Manufacturing execution, safety signal, audit or other.';
COMMENT ON COLUMN deviations_and_capas.deviation.batch_identifier IS 'The batch affected, if any.';
COMMENT ON COLUMN deviations_and_capas.deviation.product_code IS 'The product affected.';
COMMENT ON COLUMN deviations_and_capas.deviation.signal_identifier IS 'The safety signal referred, if any.';
COMMENT ON COLUMN deviations_and_capas.deviation.deviation_description IS 'The departure and its context.';
COMMENT ON COLUMN deviations_and_capas.deviation.deviation_severity IS 'Minor, major or critical.';
COMMENT ON COLUMN deviations_and_capas.deviation.deviation_current_status IS 'Open, under investigation, dispositioned, closed.';

CREATE TABLE IF NOT EXISTS deviations_and_capas.investigation (
  deviation_identifier                   varchar(40) NOT NULL,
  deviation_investigator_identifier      varchar(40) NOT NULL,
  deviation_investigation_completed_date date NOT NULL,
  deviation_root_cause_description       text NOT NULL,
  deviation_impact_description           text NOT NULL,
  deviation_disposition_status           varchar(40) NOT NULL,
  CONSTRAINT investigation_pk PRIMARY KEY (deviation_identifier)
);
COMMENT ON TABLE deviations_and_capas.investigation IS 'One row per deviation, the investigation outcome and impact on the batch.';
COMMENT ON COLUMN deviations_and_capas.investigation.deviation_identifier IS 'The deviation.';
COMMENT ON COLUMN deviations_and_capas.investigation.deviation_investigator_identifier IS 'Who investigated.';
COMMENT ON COLUMN deviations_and_capas.investigation.deviation_investigation_completed_date IS 'When.';
COMMENT ON COLUMN deviations_and_capas.investigation.deviation_root_cause_description IS 'The root cause found.';
COMMENT ON COLUMN deviations_and_capas.investigation.deviation_impact_description IS 'The impact on the batch.';
COMMENT ON COLUMN deviations_and_capas.investigation.deviation_disposition_status IS 'No impact, rework, reject, or release with justification.';

CREATE TABLE IF NOT EXISTS deviations_and_capas.corrective_action (
  corrective_action_identifier       varchar(40) NOT NULL,
  deviation_identifier               varchar(40) NOT NULL,
  corrective_action_type             varchar(20) NOT NULL,
  corrective_action_description      text NOT NULL,
  corrective_action_owner_identifier varchar(40) NOT NULL,
  corrective_action_due_date         date NOT NULL,
  corrective_action_current_status   varchar(20) NOT NULL,
  CONSTRAINT corrective_action_pk PRIMARY KEY (corrective_action_identifier)
);
COMMENT ON TABLE deviations_and_capas.corrective_action IS 'One row per corrective or preventive action.';
COMMENT ON COLUMN deviations_and_capas.corrective_action.corrective_action_identifier IS 'The action.';
COMMENT ON COLUMN deviations_and_capas.corrective_action.deviation_identifier IS 'The deviation it addresses.';
COMMENT ON COLUMN deviations_and_capas.corrective_action.corrective_action_type IS 'Corrective or preventive.';
COMMENT ON COLUMN deviations_and_capas.corrective_action.corrective_action_description IS 'The action.';
COMMENT ON COLUMN deviations_and_capas.corrective_action.corrective_action_owner_identifier IS 'Who owns it.';
COMMENT ON COLUMN deviations_and_capas.corrective_action.corrective_action_due_date IS 'When due.';
COMMENT ON COLUMN deviations_and_capas.corrective_action.corrective_action_current_status IS 'Open, complete, verified.';

GRANT ALL ON ALL TABLES IN SCHEMA deviations_and_capas TO egeria_admin, egeria_user, airflow_user;

-- Batch Certification Decisions  (DigitalProduct::Coco::Batch Certification Decisions)
CREATE SCHEMA IF NOT EXISTS batch_certification_decisions;
GRANT ALL ON SCHEMA batch_certification_decisions TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA batch_certification_decisions IS 'The review of each assembled batch record and the certification decision taken by a Qualified Person against the requirements of the destination market. It is the single human decision the whole chain exists to support, and it is market-specific.';

CREATE TABLE IF NOT EXISTS batch_certification_decisions.certification_decision (
  batch_identifier             varchar(40) NOT NULL,
  market_code                  varchar(8) NOT NULL,
  batch_certifier_identifier   varchar(40) NOT NULL,
  batch_certification_date     date NOT NULL,
  batch_certification_status   varchar(20) NOT NULL,
  batch_released_quantity      integer,
  batch_record_complete_flag   boolean NOT NULL,
  deviation_identifier         varchar(40),
  batch_certification_notes    text,
  shipment_storage_description text,
  CONSTRAINT certification_decision_pk PRIMARY KEY (batch_identifier, market_code)
);
COMMENT ON TABLE batch_certification_decisions.certification_decision IS 'One row per batch per market reviewed.';
COMMENT ON COLUMN batch_certification_decisions.certification_decision.batch_identifier IS 'The batch.';
COMMENT ON COLUMN batch_certification_decisions.certification_decision.market_code IS 'The market.';
COMMENT ON COLUMN batch_certification_decisions.certification_decision.batch_certifier_identifier IS 'The Qualified Person.';
COMMENT ON COLUMN batch_certification_decisions.certification_decision.batch_certification_date IS 'When decided.';
COMMENT ON COLUMN batch_certification_decisions.certification_decision.batch_certification_status IS 'Certified, rejected or held.';
COMMENT ON COLUMN batch_certification_decisions.certification_decision.batch_released_quantity IS 'The quantity released to the market.';
COMMENT ON COLUMN batch_certification_decisions.certification_decision.batch_record_complete_flag IS 'Whether the record reviewed was complete.';
COMMENT ON COLUMN batch_certification_decisions.certification_decision.deviation_identifier IS 'An open deviation that held the batch, if any.';
COMMENT ON COLUMN batch_certification_decisions.certification_decision.batch_certification_notes IS 'The reviewer''s findings.';
COMMENT ON COLUMN batch_certification_decisions.certification_decision.shipment_storage_description IS 'The storage conditions the released therapy must be shipped under.';

GRANT ALL ON ALL TABLES IN SCHEMA batch_certification_decisions TO egeria_admin, egeria_user, airflow_user;

-- Serialisation Alert Investigations  (DigitalProduct::Coco::Serialisation Alert Investigations)
CREATE SCHEMA IF NOT EXISTS serialisation_alert_investigations;
GRANT ALL ON SCHEMA serialisation_alert_investigations TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA serialisation_alert_investigations IS 'The investigation of verification alerts raised by pharmacies and trading partners, separating the company''s own data errors from genuine falsification signals, and the disposition returned to the serialisation repository. An alert not investigated is a falsification signal received and ignored.';

CREATE TABLE IF NOT EXISTS serialisation_alert_investigations.alert_investigation (
  alert_identifier                    varchar(40) NOT NULL,
  pack_serial_number                  varchar(40) NOT NULL,
  alert_investigator_identifier       varchar(40) NOT NULL,
  alert_investigation_start_timestamp timestamptz NOT NULL,
  alert_investigation_end_timestamp   timestamptz,
  alert_root_cause_type               varchar(40),
  alert_investigation_notes           text,
  alert_current_status                varchar(20) NOT NULL,
  CONSTRAINT alert_investigation_pk PRIMARY KEY (alert_identifier)
);
COMMENT ON TABLE serialisation_alert_investigations.alert_investigation IS 'One row per alert investigated.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_investigation.alert_identifier IS 'The alert.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_investigation.pack_serial_number IS 'The identifier.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_investigation.alert_investigator_identifier IS 'Who investigated.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_investigation.alert_investigation_start_timestamp IS 'When opened.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_investigation.alert_investigation_end_timestamp IS 'When closed.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_investigation.alert_root_cause_type IS 'Data error, scanning error, expired product, suspected falsification, other.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_investigation.alert_investigation_notes IS 'What was found.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_investigation.alert_current_status IS 'Open, closed, escalated.';

CREATE TABLE IF NOT EXISTS serialisation_alert_investigations.alert_disposition (
  alert_identifier             varchar(40) NOT NULL,
  alert_disposition_timestamp  timestamptz NOT NULL,
  alert_disposition_type       varchar(40) NOT NULL,
  alert_affected_count         integer NOT NULL,
  corrective_action_identifier varchar(40),
  CONSTRAINT alert_disposition_pk PRIMARY KEY (alert_identifier, alert_disposition_timestamp)
);
COMMENT ON TABLE serialisation_alert_investigations.alert_disposition IS 'One row per disposition returned for an alert.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_disposition.alert_identifier IS 'The alert.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_disposition.alert_disposition_timestamp IS 'When.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_disposition.alert_disposition_type IS 'Correct repository, decommission, recall, report to authority, no action.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_disposition.alert_affected_count IS 'The number of identifiers affected.';
COMMENT ON COLUMN serialisation_alert_investigations.alert_disposition.corrective_action_identifier IS 'The CAPA raised, if any.';

GRANT ALL ON ALL TABLES IN SCHEMA serialisation_alert_investigations TO egeria_admin, egeria_user, airflow_user;

-- Temperature Excursion Assessments  (DigitalProduct::Coco::Temperature Excursion Assessments)
CREATE SCHEMA IF NOT EXISTS temperature_excursion_assessments;
GRANT ALL ON SCHEMA temperature_excursion_assessments TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA temperature_excursion_assessments IS 'The assessment of each temperature excursion against the product''s stability data, and the disposition of the consignment. It runs before the goods are used rather than after, which is what distinguishes an assessment from a report.';

CREATE TABLE IF NOT EXISTS temperature_excursion_assessments.excursion_assessment (
  excursion_identifier                     varchar(40) NOT NULL,
  shipment_identifier                      varchar(40) NOT NULL,
  product_code                             varchar(20) NOT NULL,
  batch_identifier                         varchar(40) NOT NULL,
  excursion_assessor_identifier            varchar(40) NOT NULL,
  excursion_assessment_timestamp           timestamptz NOT NULL,
  excursion_stability_reference_identifier varchar(40) NOT NULL,
  excursion_disposition_status             varchar(20) NOT NULL,
  excursion_assessment_notes               text,
  CONSTRAINT excursion_assessment_pk PRIMARY KEY (excursion_identifier)
);
COMMENT ON TABLE temperature_excursion_assessments.excursion_assessment IS 'One row per excursion assessed.';
COMMENT ON COLUMN temperature_excursion_assessments.excursion_assessment.excursion_identifier IS 'The excursion.';
COMMENT ON COLUMN temperature_excursion_assessments.excursion_assessment.shipment_identifier IS 'The consignment.';
COMMENT ON COLUMN temperature_excursion_assessments.excursion_assessment.product_code IS 'The product.';
COMMENT ON COLUMN temperature_excursion_assessments.excursion_assessment.batch_identifier IS 'The batch.';
COMMENT ON COLUMN temperature_excursion_assessments.excursion_assessment.excursion_assessor_identifier IS 'Who assessed.';
COMMENT ON COLUMN temperature_excursion_assessments.excursion_assessment.excursion_assessment_timestamp IS 'When.';
COMMENT ON COLUMN temperature_excursion_assessments.excursion_assessment.excursion_stability_reference_identifier IS 'The stability study the assessment relies on.';
COMMENT ON COLUMN temperature_excursion_assessments.excursion_assessment.excursion_disposition_status IS 'Use, quarantine, reject.';
COMMENT ON COLUMN temperature_excursion_assessments.excursion_assessment.excursion_assessment_notes IS 'The reasoning.';

GRANT ALL ON ALL TABLES IN SCHEMA temperature_excursion_assessments TO egeria_admin, egeria_user, airflow_user;

-- Market Authorisations  (DigitalProduct::Coco::Market Authorisations)
CREATE SCHEMA IF NOT EXISTS market_authorisations;
GRANT ALL ON SCHEMA market_authorisations TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA market_authorisations IS 'Which product may be placed on which market, under which authorisation and subject to which conditions, and the label and authorisation changes that safety findings drive. Batch certification and serialisation routing both read it.';

CREATE TABLE IF NOT EXISTS market_authorisations.market_authorisation (
  authorisation_identifier     varchar(40) NOT NULL,
  product_code                 varchar(20) NOT NULL,
  market_code                  varchar(8) NOT NULL,
  authorisation_regulator_code varchar(20) NOT NULL,
  authorisation_start_date     date NOT NULL,
  authorisation_end_date       date,
  authorisation_current_status varchar(20) NOT NULL,
  signal_identifier            varchar(40),
  CONSTRAINT market_authorisation_pk PRIMARY KEY (authorisation_identifier)
);
COMMENT ON TABLE market_authorisations.market_authorisation IS 'One row per authorisation held.';
COMMENT ON COLUMN market_authorisations.market_authorisation.authorisation_identifier IS 'The authorisation.';
COMMENT ON COLUMN market_authorisations.market_authorisation.product_code IS 'The product.';
COMMENT ON COLUMN market_authorisations.market_authorisation.market_code IS 'The market.';
COMMENT ON COLUMN market_authorisations.market_authorisation.authorisation_regulator_code IS 'The granting regulator.';
COMMENT ON COLUMN market_authorisations.market_authorisation.authorisation_start_date IS 'When granted.';
COMMENT ON COLUMN market_authorisations.market_authorisation.authorisation_end_date IS 'When it lapses, if it does.';
COMMENT ON COLUMN market_authorisations.market_authorisation.authorisation_current_status IS 'Granted, suspended, varied, withdrawn.';
COMMENT ON COLUMN market_authorisations.market_authorisation.signal_identifier IS 'The safety signal behind the latest variation, if any.';

CREATE TABLE IF NOT EXISTS market_authorisations.authorisation_condition (
  authorisation_identifier              varchar(40) NOT NULL,
  authorisation_requirement_number      integer NOT NULL,
  authorisation_requirement_type        varchar(40) NOT NULL,
  authorisation_requirement_description text NOT NULL,
  authorisation_requirement_start_date  date NOT NULL,
  CONSTRAINT authorisation_condition_pk PRIMARY KEY (authorisation_identifier, authorisation_requirement_number)
);
COMMENT ON TABLE market_authorisations.authorisation_condition IS 'One row per condition or labelling requirement attached to an authorisation.';
COMMENT ON COLUMN market_authorisations.authorisation_condition.authorisation_identifier IS 'The authorisation.';
COMMENT ON COLUMN market_authorisations.authorisation_condition.authorisation_requirement_number IS 'The condition''s sequence.';
COMMENT ON COLUMN market_authorisations.authorisation_condition.authorisation_requirement_type IS 'Labelling, pack size, distribution, monitoring or other.';
COMMENT ON COLUMN market_authorisations.authorisation_condition.authorisation_requirement_description IS 'The condition.';
COMMENT ON COLUMN market_authorisations.authorisation_condition.authorisation_requirement_start_date IS 'When it took effect.';

GRANT ALL ON ALL TABLES IN SCHEMA market_authorisations TO egeria_admin, egeria_user, airflow_user;

-- Occupational Exposure Bands  (DigitalProduct::Coco::Occupational Exposure Bands)
CREATE SCHEMA IF NOT EXISTS occupational_exposure_bands;
GRANT ALL ON SCHEMA occupational_exposure_bands TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA occupational_exposure_bands IS 'Each substance assigned to an occupational exposure band and each band to a required containment level, revised as incidents reveal what the assessments missed. It is the rule set that turns a substance identity into a control requirement, and it is shared with transport classification rather than duplicated.';

CREATE TABLE IF NOT EXISTS occupational_exposure_bands.substance_exposure_band (
  substance_code         varchar(20) NOT NULL,
  substance_name         varchar(200) NOT NULL,
  substance_banding_code varchar(10) NOT NULL,
  substance_hazard_code  varchar(20) NOT NULL,
  substance_banding_date date NOT NULL,
  incident_identifier    varchar(40),
  CONSTRAINT substance_exposure_band_pk PRIMARY KEY (substance_code)
);
COMMENT ON TABLE occupational_exposure_bands.substance_exposure_band IS 'One row per substance, its band.';
COMMENT ON COLUMN occupational_exposure_bands.substance_exposure_band.substance_code IS 'The substance.';
COMMENT ON COLUMN occupational_exposure_bands.substance_exposure_band.substance_name IS 'Its name.';
COMMENT ON COLUMN occupational_exposure_bands.substance_exposure_band.substance_banding_code IS 'The band assigned.';
COMMENT ON COLUMN occupational_exposure_bands.substance_exposure_band.substance_hazard_code IS 'The hazard classification the assignment rests on.';
COMMENT ON COLUMN occupational_exposure_bands.substance_exposure_band.substance_banding_date IS 'When assigned or last revised.';
COMMENT ON COLUMN occupational_exposure_bands.substance_exposure_band.incident_identifier IS 'The incident that prompted the latest revision, if any.';

CREATE TABLE IF NOT EXISTS occupational_exposure_bands.band_containment_requirement (
  band_code                    varchar(10) NOT NULL,
  band_maximum_value           double precision NOT NULL,
  band_unit                    varchar(20) NOT NULL,
  band_containment_description text NOT NULL,
  CONSTRAINT band_containment_requirement_pk PRIMARY KEY (band_code)
);
COMMENT ON TABLE occupational_exposure_bands.band_containment_requirement IS 'One row per band, the limit and containment required.';
COMMENT ON COLUMN occupational_exposure_bands.band_containment_requirement.band_code IS 'The band.';
COMMENT ON COLUMN occupational_exposure_bands.band_containment_requirement.band_maximum_value IS 'The exposure limit.';
COMMENT ON COLUMN occupational_exposure_bands.band_containment_requirement.band_unit IS 'The unit of the limit.';
COMMENT ON COLUMN occupational_exposure_bands.band_containment_requirement.band_containment_description IS 'The containment required.';

GRANT ALL ON ALL TABLES IN SCHEMA occupational_exposure_bands TO egeria_admin, egeria_user, airflow_user;

-- Exposure Monitoring Results  (DigitalProduct::Coco::Exposure Monitoring Results)
CREATE SCHEMA IF NOT EXISTS exposure_monitoring_results;
GRANT ALL ON SCHEMA exposure_monitoring_results TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA exposure_monitoring_results IS 'Personal and static exposure measurements from monitoring campaigns, compared to the banded limits, against the workers and tasks monitored. An exposure that was not measured at the time cannot be measured later, so coverage matters as much as the readings.';

CREATE TABLE IF NOT EXISTS exposure_monitoring_results.monitoring_campaign (
  monitoring_campaign_identifier  varchar(40) NOT NULL,
  site_code                       varchar(20) NOT NULL,
  monitoring_campaign_start_date  date NOT NULL,
  monitoring_campaign_end_date    date NOT NULL,
  substance_code                  varchar(20) NOT NULL,
  monitoring_campaign_description text NOT NULL,
  CONSTRAINT monitoring_campaign_pk PRIMARY KEY (monitoring_campaign_identifier)
);
COMMENT ON TABLE exposure_monitoring_results.monitoring_campaign IS 'One row per monitoring campaign.';
COMMENT ON COLUMN exposure_monitoring_results.monitoring_campaign.monitoring_campaign_identifier IS 'The campaign.';
COMMENT ON COLUMN exposure_monitoring_results.monitoring_campaign.site_code IS 'The site.';
COMMENT ON COLUMN exposure_monitoring_results.monitoring_campaign.monitoring_campaign_start_date IS 'When it began.';
COMMENT ON COLUMN exposure_monitoring_results.monitoring_campaign.monitoring_campaign_end_date IS 'When it ended.';
COMMENT ON COLUMN exposure_monitoring_results.monitoring_campaign.substance_code IS 'The substance monitored.';
COMMENT ON COLUMN exposure_monitoring_results.monitoring_campaign.monitoring_campaign_description IS 'The tasks and locations covered.';

CREATE TABLE IF NOT EXISTS exposure_monitoring_results.exposure_measurement (
  exposure_reading_identifier    varchar(40) NOT NULL,
  monitoring_campaign_identifier varchar(40) NOT NULL,
  exposure_reading_type          varchar(10) NOT NULL,
  worker_pseudonym_identifier    varchar(40),
  exposure_reading_location      varchar(120),
  exposure_reading_timestamp     timestamptz NOT NULL,
  exposure_reading_value         double precision NOT NULL,
  band_maximum_value             double precision NOT NULL,
  exposure_limit_exceeded_flag   boolean NOT NULL,
  CONSTRAINT exposure_measurement_pk PRIMARY KEY (exposure_reading_identifier)
);
COMMENT ON TABLE exposure_monitoring_results.exposure_measurement IS 'One row per measurement.';
COMMENT ON COLUMN exposure_monitoring_results.exposure_measurement.exposure_reading_identifier IS 'The measurement.';
COMMENT ON COLUMN exposure_monitoring_results.exposure_measurement.monitoring_campaign_identifier IS 'The campaign.';
COMMENT ON COLUMN exposure_monitoring_results.exposure_measurement.exposure_reading_type IS 'Personal or static.';
COMMENT ON COLUMN exposure_monitoring_results.exposure_measurement.worker_pseudonym_identifier IS 'The worker, for a personal measurement.';
COMMENT ON COLUMN exposure_monitoring_results.exposure_measurement.exposure_reading_location IS 'Where, for a static measurement.';
COMMENT ON COLUMN exposure_monitoring_results.exposure_measurement.exposure_reading_timestamp IS 'When.';
COMMENT ON COLUMN exposure_monitoring_results.exposure_measurement.exposure_reading_value IS 'The exposure measured.';
COMMENT ON COLUMN exposure_monitoring_results.exposure_measurement.band_maximum_value IS 'The limit compared against.';
COMMENT ON COLUMN exposure_monitoring_results.exposure_measurement.exposure_limit_exceeded_flag IS 'Whether the limit was exceeded.';

GRANT ALL ON ALL TABLES IN SCHEMA exposure_monitoring_results TO egeria_admin, egeria_user, airflow_user;

-- Incidents And Near Misses  (DigitalProduct::Coco::Incidents And Near Misses)
CREATE SCHEMA IF NOT EXISTS incidents_and_near_misses;
GRANT ALL ON SCHEMA incidents_and_near_misses TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA incidents_and_near_misses IS 'Incidents, near misses and their investigations, with the substance or control implicated and the findings fed back into the exposure assessments. It is what makes the health surveillance chain a loop rather than a line.';

CREATE TABLE IF NOT EXISTS incidents_and_near_misses.incident (
  incident_identifier         varchar(40) NOT NULL,
  incident_type               varchar(20) NOT NULL,
  incident_timestamp          timestamptz NOT NULL,
  incident_reported_timestamp timestamptz NOT NULL,
  site_code                   varchar(20) NOT NULL,
  incident_location           varchar(120) NOT NULL,
  substance_code              varchar(20),
  worker_pseudonym_identifier varchar(40),
  incident_description        text NOT NULL,
  incident_severity           varchar(20) NOT NULL,
  CONSTRAINT incident_pk PRIMARY KEY (incident_identifier)
);
COMMENT ON TABLE incidents_and_near_misses.incident IS 'One row per incident or near miss reported.';
COMMENT ON COLUMN incidents_and_near_misses.incident.incident_identifier IS 'The incident.';
COMMENT ON COLUMN incidents_and_near_misses.incident.incident_type IS 'Incident or near miss.';
COMMENT ON COLUMN incidents_and_near_misses.incident.incident_timestamp IS 'When it occurred.';
COMMENT ON COLUMN incidents_and_near_misses.incident.incident_reported_timestamp IS 'When reported.';
COMMENT ON COLUMN incidents_and_near_misses.incident.site_code IS 'The site.';
COMMENT ON COLUMN incidents_and_near_misses.incident.incident_location IS 'Where.';
COMMENT ON COLUMN incidents_and_near_misses.incident.substance_code IS 'The substance implicated, if any.';
COMMENT ON COLUMN incidents_and_near_misses.incident.worker_pseudonym_identifier IS 'The worker affected, if any.';
COMMENT ON COLUMN incidents_and_near_misses.incident.incident_description IS 'What happened and the immediate response.';
COMMENT ON COLUMN incidents_and_near_misses.incident.incident_severity IS 'The assessed seriousness.';

CREATE TABLE IF NOT EXISTS incidents_and_near_misses.incident_investigation_finding (
  incident_identifier                 varchar(40) NOT NULL,
  incident_finding_number             integer NOT NULL,
  incident_finding_description        text NOT NULL,
  control_identifier                  varchar(40),
  incident_finding_action_description text,
  CONSTRAINT incident_investigation_finding_pk PRIMARY KEY (incident_identifier, incident_finding_number)
);
COMMENT ON TABLE incidents_and_near_misses.incident_investigation_finding IS 'One row per finding from an incident''s investigation.';
COMMENT ON COLUMN incidents_and_near_misses.incident_investigation_finding.incident_identifier IS 'The incident.';
COMMENT ON COLUMN incidents_and_near_misses.incident_investigation_finding.incident_finding_number IS 'The finding''s sequence.';
COMMENT ON COLUMN incidents_and_near_misses.incident_investigation_finding.incident_finding_description IS 'The finding.';
COMMENT ON COLUMN incidents_and_near_misses.incident_investigation_finding.control_identifier IS 'The control implicated, if any.';
COMMENT ON COLUMN incidents_and_near_misses.incident_investigation_finding.incident_finding_action_description IS 'The change to assessments or controls that follows.';

GRANT ALL ON ALL TABLES IN SCHEMA incidents_and_near_misses TO egeria_admin, egeria_user, airflow_user;

-- ================================================================================================
-- procurement.md
-- ================================================================================================

-- Supplier Master Data  (DigitalProduct::Coco::Supplier Master Data)
CREATE SCHEMA IF NOT EXISTS supplier_master_data;
GRANT ALL ON SCHEMA supplier_master_data TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA supplier_master_data IS 'The authoritative record of every third party the company transacts with: its identity, its screening status and risk rating, and the payment details it is paid to. The supplier fraud was possible because this record was not authoritative; making it so is the control.';

CREATE TABLE IF NOT EXISTS supplier_master_data.supplier (
  supplier_identifier     varchar(40) NOT NULL,
  supplier_name           varchar(200) NOT NULL,
  supplier_type           varchar(40) NOT NULL,
  supplier_country        varchar(60) NOT NULL,
  supplier_approved_flag  boolean NOT NULL,
  supplier_approved_date  date,
  supplier_current_status varchar(20) NOT NULL,
  CONSTRAINT supplier_pk PRIMARY KEY (supplier_identifier)
);
COMMENT ON TABLE supplier_master_data.supplier IS 'One row per approved third party.';
COMMENT ON COLUMN supplier_master_data.supplier.supplier_identifier IS 'The company''s unique identifier for the supplier.';
COMMENT ON COLUMN supplier_master_data.supplier.supplier_name IS 'The supplier''s legal name.';
COMMENT ON COLUMN supplier_master_data.supplier.supplier_type IS 'Material supplier, service provider, healthcare organisation or other.';
COMMENT ON COLUMN supplier_master_data.supplier.supplier_country IS 'The country of incorporation.';
COMMENT ON COLUMN supplier_master_data.supplier.supplier_approved_flag IS 'Whether the supplier has passed onboarding.';
COMMENT ON COLUMN supplier_master_data.supplier.supplier_approved_date IS 'When approval was granted.';
COMMENT ON COLUMN supplier_master_data.supplier.supplier_current_status IS 'Active, suspended or closed.';

CREATE TABLE IF NOT EXISTS supplier_master_data.supplier_risk_status (
  supplier_identifier      varchar(40) NOT NULL,
  supplier_screened_status varchar(20) NOT NULL,
  supplier_screened_date   date NOT NULL,
  supplier_rating          varchar(20) NOT NULL,
  screening_identifier     varchar(40) NOT NULL,
  anomaly_identifier       varchar(40),
  CONSTRAINT supplier_risk_status_pk PRIMARY KEY (supplier_identifier)
);
COMMENT ON TABLE supplier_master_data.supplier_risk_status IS 'One row per supplier, its current screening and risk position.';
COMMENT ON COLUMN supplier_master_data.supplier_risk_status.supplier_identifier IS 'The supplier.';
COMMENT ON COLUMN supplier_master_data.supplier_risk_status.supplier_screened_status IS 'Clear, match under review, or blocked.';
COMMENT ON COLUMN supplier_master_data.supplier_risk_status.supplier_screened_date IS 'When the supplier was last screened.';
COMMENT ON COLUMN supplier_master_data.supplier_risk_status.supplier_rating IS 'The assessed risk rating.';
COMMENT ON COLUMN supplier_master_data.supplier_risk_status.screening_identifier IS 'The screening result the status rests on.';
COMMENT ON COLUMN supplier_master_data.supplier_risk_status.anomaly_identifier IS 'An open concern raised by transaction monitoring, if any.';

CREATE TABLE IF NOT EXISTS supplier_master_data.supplier_payment_details (
  supplier_identifier              varchar(40) NOT NULL,
  bank_account_current_identifier  varchar(40) NOT NULL,
  bank_account_provider_name       varchar(120) NOT NULL,
  bank_account_country             varchar(60) NOT NULL,
  payment_detail_change_identifier varchar(40) NOT NULL,
  payment_detail_verified_date     date NOT NULL,
  CONSTRAINT supplier_payment_details_pk PRIMARY KEY (supplier_identifier)
);
COMMENT ON TABLE supplier_master_data.supplier_payment_details IS 'One row per supplier, the verified bank details it is paid to.';
COMMENT ON COLUMN supplier_master_data.supplier_payment_details.supplier_identifier IS 'The supplier.';
COMMENT ON COLUMN supplier_master_data.supplier_payment_details.bank_account_current_identifier IS 'The bank account, masked.';
COMMENT ON COLUMN supplier_master_data.supplier_payment_details.bank_account_provider_name IS 'The bank.';
COMMENT ON COLUMN supplier_master_data.supplier_payment_details.bank_account_country IS 'The country of the account.';
COMMENT ON COLUMN supplier_master_data.supplier_payment_details.payment_detail_change_identifier IS 'The verified change that set these details.';
COMMENT ON COLUMN supplier_master_data.supplier_payment_details.payment_detail_verified_date IS 'When the details were last independently verified.';

GRANT ALL ON ALL TABLES IN SCHEMA supplier_master_data TO egeria_admin, egeria_user, airflow_user;

-- Third Party Onboarding Cases  (DigitalProduct::Coco::Third Party Onboarding Cases)
CREATE SCHEMA IF NOT EXISTS third_party_onboarding_cases;
GRANT ALL ON SCHEMA third_party_onboarding_cases TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA third_party_onboarding_cases IS 'Every proposed third party driven through screening, risk assessment and approval to the creation of a supplier record. It is deliberately the only route to that record: a supplier created outside this flow is a supplier nothing has checked.';

CREATE TABLE IF NOT EXISTS third_party_onboarding_cases.onboarding_case (
  onboarding_case_identifier           varchar(40) NOT NULL,
  third_party_name                     varchar(200) NOT NULL,
  third_party_country                  varchar(60) NOT NULL,
  third_party_owner_description        text,
  onboarding_case_requester_identifier varchar(40) NOT NULL,
  onboarding_case_start_date           date NOT NULL,
  onboarding_case_current_status       varchar(20) NOT NULL,
  supplier_identifier                  varchar(40),
  CONSTRAINT onboarding_case_pk PRIMARY KEY (onboarding_case_identifier)
);
COMMENT ON TABLE third_party_onboarding_cases.onboarding_case IS 'One row per third party proposed for onboarding.';
COMMENT ON COLUMN third_party_onboarding_cases.onboarding_case.onboarding_case_identifier IS 'The unique identifier of the case.';
COMMENT ON COLUMN third_party_onboarding_cases.onboarding_case.third_party_name IS 'The proposed third party''s legal name.';
COMMENT ON COLUMN third_party_onboarding_cases.onboarding_case.third_party_country IS 'Its country of incorporation.';
COMMENT ON COLUMN third_party_onboarding_cases.onboarding_case.third_party_owner_description IS 'Its beneficial ownership as declared.';
COMMENT ON COLUMN third_party_onboarding_cases.onboarding_case.onboarding_case_requester_identifier IS 'Who proposed the third party.';
COMMENT ON COLUMN third_party_onboarding_cases.onboarding_case.onboarding_case_start_date IS 'When the case was opened.';
COMMENT ON COLUMN third_party_onboarding_cases.onboarding_case.onboarding_case_current_status IS 'Screening, risk assessment, approved, rejected.';
COMMENT ON COLUMN third_party_onboarding_cases.onboarding_case.supplier_identifier IS 'The supplier record created on approval.';

CREATE TABLE IF NOT EXISTS third_party_onboarding_cases.screening_request (
  screening_identifier          varchar(40) NOT NULL,
  onboarding_case_identifier    varchar(40) NOT NULL,
  screening_requested_timestamp timestamptz NOT NULL,
  screening_type                varchar(40) NOT NULL,
  supplier_rating               varchar(20),
  CONSTRAINT screening_request_pk PRIMARY KEY (screening_identifier)
);
COMMENT ON TABLE third_party_onboarding_cases.screening_request IS 'One row per screening submitted to the external service for a case.';
COMMENT ON COLUMN third_party_onboarding_cases.screening_request.screening_identifier IS 'The screening request.';
COMMENT ON COLUMN third_party_onboarding_cases.screening_request.onboarding_case_identifier IS 'The case.';
COMMENT ON COLUMN third_party_onboarding_cases.screening_request.screening_requested_timestamp IS 'When it was submitted.';
COMMENT ON COLUMN third_party_onboarding_cases.screening_request.screening_type IS 'Sanctions, politically exposed persons, adverse media, or all.';
COMMENT ON COLUMN third_party_onboarding_cases.screening_request.supplier_rating IS 'The risk rating assigned once the result was assessed.';

GRANT ALL ON ALL TABLES IN SCHEMA third_party_onboarding_cases TO egeria_admin, egeria_user, airflow_user;

-- Third Party Screening Results  (DigitalProduct::Coco::Third Party Screening Results)
CREATE SCHEMA IF NOT EXISTS third_party_screening_results;
GRANT ALL ON SCHEMA third_party_screening_results TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA third_party_screening_results IS 'The answers returned by the external screening service: matches against sanctions, politically exposed person and adverse media lists, with the risk indicators and the date each was given. Its answers age, which is why the chain re-screens rather than treating an onboarding result as permanent.';

CREATE TABLE IF NOT EXISTS third_party_screening_results.screening_result (
  screening_identifier  varchar(40) NOT NULL,
  third_party_name      varchar(200) NOT NULL,
  screening_date        date NOT NULL,
  screening_status      varchar(20) NOT NULL,
  screening_match_count integer NOT NULL,
  screening_rating      varchar(20),
  CONSTRAINT screening_result_pk PRIMARY KEY (screening_identifier)
);
COMMENT ON TABLE third_party_screening_results.screening_result IS 'One row per screening returned by the service.';
COMMENT ON COLUMN third_party_screening_results.screening_result.screening_identifier IS 'The screening request answered.';
COMMENT ON COLUMN third_party_screening_results.screening_result.third_party_name IS 'The name screened.';
COMMENT ON COLUMN third_party_screening_results.screening_result.screening_date IS 'When the service answered.';
COMMENT ON COLUMN third_party_screening_results.screening_result.screening_status IS 'Clear, potential match, confirmed match.';
COMMENT ON COLUMN third_party_screening_results.screening_result.screening_match_count IS 'The number of list entries matched.';
COMMENT ON COLUMN third_party_screening_results.screening_result.screening_rating IS 'The service''s overall risk indicator.';

CREATE TABLE IF NOT EXISTS third_party_screening_results.screening_match (
  screening_identifier        varchar(40) NOT NULL,
  screening_match_list_name   varchar(120) NOT NULL,
  screening_match_name        varchar(200) NOT NULL,
  screening_match_rating      varchar(20) NOT NULL,
  screening_match_description text,
  CONSTRAINT screening_match_pk PRIMARY KEY (screening_identifier, screening_match_list_name, screening_match_name)
);
COMMENT ON TABLE third_party_screening_results.screening_match IS 'One row per list entry matched by a screening.';
COMMENT ON COLUMN third_party_screening_results.screening_match.screening_identifier IS 'The screening.';
COMMENT ON COLUMN third_party_screening_results.screening_match.screening_match_list_name IS 'The sanctions, PEP or media list matched.';
COMMENT ON COLUMN third_party_screening_results.screening_match.screening_match_name IS 'The list entry''s name.';
COMMENT ON COLUMN third_party_screening_results.screening_match.screening_match_rating IS 'The strength of the match.';
COMMENT ON COLUMN third_party_screening_results.screening_match.screening_match_description IS 'Why the entry matched.';

GRANT ALL ON ALL TABLES IN SCHEMA third_party_screening_results TO egeria_admin, egeria_user, airflow_user;

-- Supplier Material Certificates  (DigitalProduct::Coco::Supplier Material Certificates)
CREATE SCHEMA IF NOT EXISTS supplier_material_certificates;
GRANT ALL ON SCHEMA supplier_material_certificates TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA supplier_material_certificates IS 'The certificates of analysis and conformity that accompany incoming material, held against the supplier and the lot they certify. The data originates outside the company, which is why it is verified on receipt rather than trusted on arrival.';

CREATE TABLE IF NOT EXISTS supplier_material_certificates.certificate_of_analysis (
  certificate_identifier      varchar(40) NOT NULL,
  supplier_identifier         varchar(40) NOT NULL,
  raw_material_code           varchar(20) NOT NULL,
  lot_identifier              varchar(40) NOT NULL,
  certificate_type            varchar(40) NOT NULL,
  certificate_date            date NOT NULL,
  certificate_conformity_flag boolean NOT NULL,
  CONSTRAINT certificate_of_analysis_pk PRIMARY KEY (certificate_identifier)
);
COMMENT ON TABLE supplier_material_certificates.certificate_of_analysis IS 'One row per certificate received with a lot of material.';
COMMENT ON COLUMN supplier_material_certificates.certificate_of_analysis.certificate_identifier IS 'The unique identifier of the certificate.';
COMMENT ON COLUMN supplier_material_certificates.certificate_of_analysis.supplier_identifier IS 'The supplier.';
COMMENT ON COLUMN supplier_material_certificates.certificate_of_analysis.raw_material_code IS 'The material certified.';
COMMENT ON COLUMN supplier_material_certificates.certificate_of_analysis.lot_identifier IS 'The supplier''s lot number.';
COMMENT ON COLUMN supplier_material_certificates.certificate_of_analysis.certificate_type IS 'Certificate of analysis or certificate of conformity.';
COMMENT ON COLUMN supplier_material_certificates.certificate_of_analysis.certificate_date IS 'When the supplier issued it.';
COMMENT ON COLUMN supplier_material_certificates.certificate_of_analysis.certificate_conformity_flag IS 'Whether the supplier declares the lot conforms to specification.';

CREATE TABLE IF NOT EXISTS supplier_material_certificates.certificate_test_result (
  certificate_identifier      varchar(40) NOT NULL,
  test_code                   varchar(40) NOT NULL,
  test_value                  varchar(60) NOT NULL,
  test_unit                   varchar(20),
  specification_minimum_value varchar(60),
  specification_maximum_value varchar(60),
  CONSTRAINT certificate_test_result_pk PRIMARY KEY (certificate_identifier, test_code)
);
COMMENT ON TABLE supplier_material_certificates.certificate_test_result IS 'One row per test reported on a certificate.';
COMMENT ON COLUMN supplier_material_certificates.certificate_test_result.certificate_identifier IS 'The certificate.';
COMMENT ON COLUMN supplier_material_certificates.certificate_test_result.test_code IS 'The test performed.';
COMMENT ON COLUMN supplier_material_certificates.certificate_test_result.test_value IS 'The result reported.';
COMMENT ON COLUMN supplier_material_certificates.certificate_test_result.test_unit IS 'The unit of the result.';
COMMENT ON COLUMN supplier_material_certificates.certificate_test_result.specification_minimum_value IS 'The lower specification limit.';
COMMENT ON COLUMN supplier_material_certificates.certificate_test_result.specification_maximum_value IS 'The upper specification limit.';

GRANT ALL ON ALL TABLES IN SCHEMA supplier_material_certificates TO egeria_admin, egeria_user, airflow_user;

-- Purchase Orders And Receipts  (DigitalProduct::Coco::Purchase Orders And Receipts)
CREATE SCHEMA IF NOT EXISTS purchase_orders_and_receipts;
GRANT ALL ON SCHEMA purchase_orders_and_receipts TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA purchase_orders_and_receipts IS 'The purchase orders raised against approved suppliers and the confirmations that the goods or services were received, which is what a supplier invoice must match before it can be paid.';

CREATE TABLE IF NOT EXISTS purchase_orders_and_receipts.purchase_order (
  order_identifier          varchar(40) NOT NULL,
  supplier_identifier       varchar(40) NOT NULL,
  order_date                date NOT NULL,
  order_total_amount        numeric(18,2) NOT NULL,
  order_currency_code       varchar(3) NOT NULL,
  order_approver_identifier varchar(40) NOT NULL,
  order_current_status      varchar(20) NOT NULL,
  CONSTRAINT purchase_order_pk PRIMARY KEY (order_identifier)
);
COMMENT ON TABLE purchase_orders_and_receipts.purchase_order IS 'One row per purchase order.';
COMMENT ON COLUMN purchase_orders_and_receipts.purchase_order.order_identifier IS 'The purchase order number.';
COMMENT ON COLUMN purchase_orders_and_receipts.purchase_order.supplier_identifier IS 'The supplier.';
COMMENT ON COLUMN purchase_orders_and_receipts.purchase_order.order_date IS 'When raised.';
COMMENT ON COLUMN purchase_orders_and_receipts.purchase_order.order_total_amount IS 'The ordered value.';
COMMENT ON COLUMN purchase_orders_and_receipts.purchase_order.order_currency_code IS 'The currency.';
COMMENT ON COLUMN purchase_orders_and_receipts.purchase_order.order_approver_identifier IS 'Who approved the order.';
COMMENT ON COLUMN purchase_orders_and_receipts.purchase_order.order_current_status IS 'Open, received, closed or cancelled.';

CREATE TABLE IF NOT EXISTS purchase_orders_and_receipts.goods_receipt_confirmation (
  goods_receipt_identifier varchar(40) NOT NULL,
  order_identifier         varchar(40) NOT NULL,
  line_item_number         integer NOT NULL,
  goods_receipt_date       date NOT NULL,
  goods_receipt_quantity   integer NOT NULL,
  CONSTRAINT goods_receipt_confirmation_pk PRIMARY KEY (goods_receipt_identifier, order_identifier, line_item_number)
);
COMMENT ON TABLE purchase_orders_and_receipts.goods_receipt_confirmation IS 'One row per confirmation that an order line has been received.';
COMMENT ON COLUMN purchase_orders_and_receipts.goods_receipt_confirmation.goods_receipt_identifier IS 'The receipt.';
COMMENT ON COLUMN purchase_orders_and_receipts.goods_receipt_confirmation.order_identifier IS 'The order received against.';
COMMENT ON COLUMN purchase_orders_and_receipts.goods_receipt_confirmation.line_item_number IS 'The order line.';
COMMENT ON COLUMN purchase_orders_and_receipts.goods_receipt_confirmation.goods_receipt_date IS 'When received.';
COMMENT ON COLUMN purchase_orders_and_receipts.goods_receipt_confirmation.goods_receipt_quantity IS 'The quantity confirmed received.';

GRANT ALL ON ALL TABLES IN SCHEMA purchase_orders_and_receipts TO egeria_admin, egeria_user, airflow_user;

-- ================================================================================================
-- warehouse.md
-- ================================================================================================

-- Goods Receipts  (DigitalProduct::Coco::Goods Receipts)
CREATE SCHEMA IF NOT EXISTS goods_receipts;
GRANT ALL ON SCHEMA goods_receipts TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA goods_receipts IS 'What physically arrived: each lot of material received, checked against the order and the supplier''s documentation, and what the inspection found. It is the point at which a supplier''s claim becomes the company''s record.';

CREATE TABLE IF NOT EXISTS goods_receipts.goods_receipt (
  goods_receipt_identifier varchar(40) NOT NULL,
  order_identifier         varchar(40) NOT NULL,
  supplier_identifier      varchar(40) NOT NULL,
  raw_material_code        varchar(20) NOT NULL,
  lot_identifier           varchar(40) NOT NULL,
  goods_receipt_date       date NOT NULL,
  goods_receipt_quantity   integer NOT NULL,
  warehouse_code           varchar(20) NOT NULL,
  certificate_identifier   varchar(40),
  CONSTRAINT goods_receipt_pk PRIMARY KEY (goods_receipt_identifier)
);
COMMENT ON TABLE goods_receipts.goods_receipt IS 'One row per lot received.';
COMMENT ON COLUMN goods_receipts.goods_receipt.goods_receipt_identifier IS 'The receipt.';
COMMENT ON COLUMN goods_receipts.goods_receipt.order_identifier IS 'The purchase order.';
COMMENT ON COLUMN goods_receipts.goods_receipt.supplier_identifier IS 'The supplier.';
COMMENT ON COLUMN goods_receipts.goods_receipt.raw_material_code IS 'The material.';
COMMENT ON COLUMN goods_receipts.goods_receipt.lot_identifier IS 'The supplier''s lot.';
COMMENT ON COLUMN goods_receipts.goods_receipt.goods_receipt_date IS 'When received.';
COMMENT ON COLUMN goods_receipts.goods_receipt.goods_receipt_quantity IS 'The quantity received.';
COMMENT ON COLUMN goods_receipts.goods_receipt.warehouse_code IS 'The receiving location.';
COMMENT ON COLUMN goods_receipts.goods_receipt.certificate_identifier IS 'The certificate that accompanied the lot.';

CREATE TABLE IF NOT EXISTS goods_receipts.receipt_inspection (
  goods_receipt_identifier           varchar(40) NOT NULL,
  goods_receipt_inspection_date      date NOT NULL,
  goods_receipt_inspector_identifier varchar(40) NOT NULL,
  goods_receipt_inspection_status    varchar(20) NOT NULL,
  goods_receipt_inspection_notes     text,
  CONSTRAINT receipt_inspection_pk PRIMARY KEY (goods_receipt_identifier, goods_receipt_inspection_date)
);
COMMENT ON TABLE goods_receipts.receipt_inspection IS 'One row per inspection of a received lot.';
COMMENT ON COLUMN goods_receipts.receipt_inspection.goods_receipt_identifier IS 'The receipt inspected.';
COMMENT ON COLUMN goods_receipts.receipt_inspection.goods_receipt_inspection_date IS 'When.';
COMMENT ON COLUMN goods_receipts.receipt_inspection.goods_receipt_inspector_identifier IS 'Who inspected.';
COMMENT ON COLUMN goods_receipts.receipt_inspection.goods_receipt_inspection_status IS 'Accepted, rejected or held.';
COMMENT ON COLUMN goods_receipts.receipt_inspection.goods_receipt_inspection_notes IS 'What was found.';

GRANT ALL ON ALL TABLES IN SCHEMA goods_receipts TO egeria_admin, egeria_user, airflow_user;

-- Material Quarantine Dispositions  (DigitalProduct::Coco::Material Quarantine Dispositions)
CREATE SCHEMA IF NOT EXISTS material_quarantine_dispositions;
GRANT ALL ON SCHEMA material_quarantine_dispositions TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA material_quarantine_dispositions IS 'Each lot held in quarantine, the tests requested for it, and the disposition that released it for use or rejected it. It is a system-enforced gate rather than a procedural one, because the failure it prevents is discovered in a finished batch.';

CREATE TABLE IF NOT EXISTS material_quarantine_dispositions.quarantine_record (
  lot_identifier                 varchar(40) NOT NULL,
  raw_material_code              varchar(20) NOT NULL,
  goods_receipt_identifier       varchar(40) NOT NULL,
  lot_quarantine_start_timestamp timestamptz NOT NULL,
  warehouse_code                 varchar(20) NOT NULL,
  lot_quantity                   integer NOT NULL,
  sample_identifier              varchar(40),
  lot_quarantine_status          varchar(20) NOT NULL,
  CONSTRAINT quarantine_record_pk PRIMARY KEY (lot_identifier)
);
COMMENT ON TABLE material_quarantine_dispositions.quarantine_record IS 'One row per lot placed in quarantine.';
COMMENT ON COLUMN material_quarantine_dispositions.quarantine_record.lot_identifier IS 'The lot.';
COMMENT ON COLUMN material_quarantine_dispositions.quarantine_record.raw_material_code IS 'The material.';
COMMENT ON COLUMN material_quarantine_dispositions.quarantine_record.goods_receipt_identifier IS 'The receipt that placed it.';
COMMENT ON COLUMN material_quarantine_dispositions.quarantine_record.lot_quarantine_start_timestamp IS 'When quarantine began.';
COMMENT ON COLUMN material_quarantine_dispositions.quarantine_record.warehouse_code IS 'The quarantine location.';
COMMENT ON COLUMN material_quarantine_dispositions.quarantine_record.lot_quantity IS 'The quantity held.';
COMMENT ON COLUMN material_quarantine_dispositions.quarantine_record.sample_identifier IS 'The sample sent for incoming testing.';
COMMENT ON COLUMN material_quarantine_dispositions.quarantine_record.lot_quarantine_status IS 'Held, released or rejected.';

CREATE TABLE IF NOT EXISTS material_quarantine_dispositions.release_disposition (
  lot_identifier            varchar(40) NOT NULL,
  lot_disposition_timestamp timestamptz NOT NULL,
  lot_disposition_status    varchar(20) NOT NULL,
  test_result_identifier    varchar(40) NOT NULL,
  lot_expiry_date           date,
  lot_released_quantity     integer,
  CONSTRAINT release_disposition_pk PRIMARY KEY (lot_identifier, lot_disposition_timestamp)
);
COMMENT ON TABLE material_quarantine_dispositions.release_disposition IS 'One row per disposition decision on a quarantined lot.';
COMMENT ON COLUMN material_quarantine_dispositions.release_disposition.lot_identifier IS 'The lot.';
COMMENT ON COLUMN material_quarantine_dispositions.release_disposition.lot_disposition_timestamp IS 'When decided.';
COMMENT ON COLUMN material_quarantine_dispositions.release_disposition.lot_disposition_status IS 'Released for use or rejected.';
COMMENT ON COLUMN material_quarantine_dispositions.release_disposition.test_result_identifier IS 'The laboratory result the decision rests on.';
COMMENT ON COLUMN material_quarantine_dispositions.release_disposition.lot_expiry_date IS 'The expiry assigned to the released lot.';
COMMENT ON COLUMN material_quarantine_dispositions.release_disposition.lot_released_quantity IS 'The quantity released.';

GRANT ALL ON ALL TABLES IN SCHEMA material_quarantine_dispositions TO egeria_admin, egeria_user, airflow_user;

-- Goods Inventory Stock  (DigitalProduct::Coco::Goods Inventory Stock)
CREATE SCHEMA IF NOT EXISTS goods_inventory_stock;
GRANT ALL ON SCHEMA goods_inventory_stock TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA goods_inventory_stock IS 'The stock of materials and finished goods at every location: the current position, the movements that produced it, and the issues of material to manufacturing with their quarantine status. It also carries serialised finished goods once they are commissioned.';

CREATE TABLE IF NOT EXISTS goods_inventory_stock.stock_position (
  product_code            varchar(20) NOT NULL,
  warehouse_code          varchar(20) NOT NULL,
  lot_identifier          varchar(40),
  stock_level             integer NOT NULL,
  stock_minimum_level     integer,
  stock_maximum_level     integer,
  stock_current_timestamp timestamptz NOT NULL,
  CONSTRAINT stock_position_pk PRIMARY KEY (product_code, warehouse_code)
);
COMMENT ON TABLE goods_inventory_stock.stock_position IS 'One row per material or product per location.';
COMMENT ON COLUMN goods_inventory_stock.stock_position.product_code IS 'The material or product.';
COMMENT ON COLUMN goods_inventory_stock.stock_position.warehouse_code IS 'The location.';
COMMENT ON COLUMN goods_inventory_stock.stock_position.lot_identifier IS 'The lot, where stock is lot-tracked.';
COMMENT ON COLUMN goods_inventory_stock.stock_position.stock_level IS 'Quantity on hand.';
COMMENT ON COLUMN goods_inventory_stock.stock_position.stock_minimum_level IS 'The reorder level.';
COMMENT ON COLUMN goods_inventory_stock.stock_position.stock_maximum_level IS 'The maximum holding.';
COMMENT ON COLUMN goods_inventory_stock.stock_position.stock_current_timestamp IS 'When the position was last updated.';

CREATE TABLE IF NOT EXISTS goods_inventory_stock.stock_movement (
  stock_movement_identifier varchar(40) NOT NULL,
  product_code              varchar(20) NOT NULL,
  lot_identifier            varchar(40),
  stock_movement_type       varchar(20) NOT NULL,
  stock_movement_quantity   integer NOT NULL,
  stock_movement_timestamp  timestamptz NOT NULL,
  warehouse_code            varchar(20) NOT NULL,
  CONSTRAINT stock_movement_pk PRIMARY KEY (stock_movement_identifier)
);
COMMENT ON TABLE goods_inventory_stock.stock_movement IS 'One row per movement of stock into, out of or between locations.';
COMMENT ON COLUMN goods_inventory_stock.stock_movement.stock_movement_identifier IS 'The movement.';
COMMENT ON COLUMN goods_inventory_stock.stock_movement.product_code IS 'The material or product.';
COMMENT ON COLUMN goods_inventory_stock.stock_movement.lot_identifier IS 'The lot.';
COMMENT ON COLUMN goods_inventory_stock.stock_movement.stock_movement_type IS 'Receipt, issue, transfer, adjustment or shipment.';
COMMENT ON COLUMN goods_inventory_stock.stock_movement.stock_movement_quantity IS 'The quantity moved.';
COMMENT ON COLUMN goods_inventory_stock.stock_movement.stock_movement_timestamp IS 'When.';
COMMENT ON COLUMN goods_inventory_stock.stock_movement.warehouse_code IS 'The location affected.';

CREATE TABLE IF NOT EXISTS goods_inventory_stock.material_issue (
  stock_movement_identifier    varchar(40) NOT NULL,
  batch_identifier             varchar(40) NOT NULL,
  raw_material_code            varchar(20) NOT NULL,
  lot_identifier               varchar(40) NOT NULL,
  raw_material_issued_quantity integer NOT NULL,
  lot_quarantine_status        varchar(20) NOT NULL,
  CONSTRAINT material_issue_pk PRIMARY KEY (stock_movement_identifier)
);
COMMENT ON TABLE goods_inventory_stock.material_issue IS 'One row per issue of material to a manufacturing batch.';
COMMENT ON COLUMN goods_inventory_stock.material_issue.stock_movement_identifier IS 'The issue movement.';
COMMENT ON COLUMN goods_inventory_stock.material_issue.batch_identifier IS 'The batch the material was issued to.';
COMMENT ON COLUMN goods_inventory_stock.material_issue.raw_material_code IS 'The material.';
COMMENT ON COLUMN goods_inventory_stock.material_issue.lot_identifier IS 'The lot issued.';
COMMENT ON COLUMN goods_inventory_stock.material_issue.raw_material_issued_quantity IS 'The quantity issued.';
COMMENT ON COLUMN goods_inventory_stock.material_issue.lot_quarantine_status IS 'The lot''s quarantine status at issue.';

GRANT ALL ON ALL TABLES IN SCHEMA goods_inventory_stock TO egeria_admin, egeria_user, airflow_user;

-- Hazardous Material Holdings  (DigitalProduct::Coco::Hazardous Material Holdings)
CREATE SCHEMA IF NOT EXISTS hazardous_material_holdings;
GRANT ALL ON SCHEMA hazardous_material_holdings TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA hazardous_material_holdings IS 'The hazardous substances the company holds, where and in what quantity, with the hazard data for each. It serves occupational health, dangerous goods transport and physical inventory tracking, which is exactly the kind of fact a supply chain view surfaces and a system inventory does not.';

CREATE TABLE IF NOT EXISTS hazardous_material_holdings.substance_holding (
  substance_code              varchar(20) NOT NULL,
  warehouse_code              varchar(20) NOT NULL,
  substance_quantity          double precision NOT NULL,
  substance_unit              varchar(20) NOT NULL,
  substance_form_description  text NOT NULL,
  substance_current_timestamp timestamptz NOT NULL,
  CONSTRAINT substance_holding_pk PRIMARY KEY (substance_code, warehouse_code)
);
COMMENT ON TABLE hazardous_material_holdings.substance_holding IS 'One row per substance per location.';
COMMENT ON COLUMN hazardous_material_holdings.substance_holding.substance_code IS 'The substance.';
COMMENT ON COLUMN hazardous_material_holdings.substance_holding.warehouse_code IS 'The location.';
COMMENT ON COLUMN hazardous_material_holdings.substance_holding.substance_quantity IS 'The quantity held.';
COMMENT ON COLUMN hazardous_material_holdings.substance_holding.substance_unit IS 'The unit of the quantity.';
COMMENT ON COLUMN hazardous_material_holdings.substance_holding.substance_form_description IS 'The physical form held, for example powder or solution.';
COMMENT ON COLUMN hazardous_material_holdings.substance_holding.substance_current_timestamp IS 'When the holding was last updated.';

CREATE TABLE IF NOT EXISTS hazardous_material_holdings.substance_hazard_data (
  substance_code               varchar(20) NOT NULL,
  substance_name               varchar(200) NOT NULL,
  substance_hazard_code        varchar(20) NOT NULL,
  substance_hazard_description text NOT NULL,
  substance_banding_code       varchar(10),
  substance_transport_code     varchar(20),
  CONSTRAINT substance_hazard_data_pk PRIMARY KEY (substance_code)
);
COMMENT ON TABLE hazardous_material_holdings.substance_hazard_data IS 'One row per substance, its hazard classification.';
COMMENT ON COLUMN hazardous_material_holdings.substance_hazard_data.substance_code IS 'The substance.';
COMMENT ON COLUMN hazardous_material_holdings.substance_hazard_data.substance_name IS 'The substance''s name.';
COMMENT ON COLUMN hazardous_material_holdings.substance_hazard_data.substance_hazard_code IS 'The hazard classification.';
COMMENT ON COLUMN hazardous_material_holdings.substance_hazard_data.substance_hazard_description IS 'The hazards the substance presents.';
COMMENT ON COLUMN hazardous_material_holdings.substance_hazard_data.substance_banding_code IS 'The occupational exposure band assigned, once assigned.';
COMMENT ON COLUMN hazardous_material_holdings.substance_hazard_data.substance_transport_code IS 'The transport classification, once derived.';

GRANT ALL ON ALL TABLES IN SCHEMA hazardous_material_holdings TO egeria_admin, egeria_user, airflow_user;

-- ================================================================================================
-- delivery.md
-- ================================================================================================

-- Patient Sample Consignments  (DigitalProduct::Coco::Patient Sample Consignments)
CREATE SCHEMA IF NOT EXISTS patient_sample_consignments;
GRANT ALL ON SCHEMA patient_sample_consignments TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA patient_sample_consignments IS 'The collection of patient material at the treating site and its transport, under temperature and time constraints, to the manufacturing site. It is the inbound half of a round trip that has a clock running from the moment the sample is taken.';

CREATE TABLE IF NOT EXISTS patient_sample_consignments.sample_consignment (
  shipment_identifier          varchar(40) NOT NULL,
  order_identifier             varchar(40) NOT NULL,
  patient_pseudonym_identifier varchar(40) NOT NULL,
  sample_collection_location   varchar(40) NOT NULL,
  sample_collection_timestamp  timestamptz NOT NULL,
  shipment_dispatch_timestamp  timestamptz NOT NULL,
  shipment_delivery_timestamp  timestamptz,
  sample_viable_duration       integer,
  shipment_arrival_description text,
  carrier_identifier           varchar(40) NOT NULL,
  CONSTRAINT sample_consignment_pk PRIMARY KEY (shipment_identifier)
);
COMMENT ON TABLE patient_sample_consignments.sample_consignment IS 'One row per consignment of patient material.';
COMMENT ON COLUMN patient_sample_consignments.sample_consignment.shipment_identifier IS 'The consignment.';
COMMENT ON COLUMN patient_sample_consignments.sample_consignment.order_identifier IS 'The order the material is for.';
COMMENT ON COLUMN patient_sample_consignments.sample_consignment.patient_pseudonym_identifier IS 'The patient, by pseudonym.';
COMMENT ON COLUMN patient_sample_consignments.sample_consignment.sample_collection_location IS 'Where collected.';
COMMENT ON COLUMN patient_sample_consignments.sample_consignment.sample_collection_timestamp IS 'When the sample was taken.';
COMMENT ON COLUMN patient_sample_consignments.sample_consignment.shipment_dispatch_timestamp IS 'When dispatched.';
COMMENT ON COLUMN patient_sample_consignments.sample_consignment.shipment_delivery_timestamp IS 'When it arrived at manufacturing.';
COMMENT ON COLUMN patient_sample_consignments.sample_consignment.sample_viable_duration IS 'The remaining viable life on arrival, in hours.';
COMMENT ON COLUMN patient_sample_consignments.sample_consignment.shipment_arrival_description IS 'The condition on arrival.';
COMMENT ON COLUMN patient_sample_consignments.sample_consignment.carrier_identifier IS 'The carrier.';

GRANT ALL ON ALL TABLES IN SCHEMA patient_sample_consignments TO egeria_admin, egeria_user, airflow_user;

-- Therapy Delivery Events  (DigitalProduct::Coco::Therapy Delivery Events)
CREATE SCHEMA IF NOT EXISTS therapy_delivery_events;
GRANT ALL ON SCHEMA therapy_delivery_events TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA therapy_delivery_events IS 'The finished therapy tracked from release to administration at the treating site, and the confirmation of arrival and administration reported back into the order. It closes the loop that the ordering portal opened.';

CREATE TABLE IF NOT EXISTS therapy_delivery_events.delivery_event (
  batch_identifier             varchar(40) NOT NULL,
  shipment_event_type          varchar(20) NOT NULL,
  shipment_event_timestamp     timestamptz NOT NULL,
  patient_pseudonym_identifier varchar(40) NOT NULL,
  order_identifier             varchar(40) NOT NULL,
  shipment_event_location      varchar(120),
  shipment_storage_description text,
  CONSTRAINT delivery_event_pk PRIMARY KEY (batch_identifier, shipment_event_type, shipment_event_timestamp)
);
COMMENT ON TABLE therapy_delivery_events.delivery_event IS 'One row per tracking event for a released therapy.';
COMMENT ON COLUMN therapy_delivery_events.delivery_event.batch_identifier IS 'The therapy.';
COMMENT ON COLUMN therapy_delivery_events.delivery_event.shipment_event_type IS 'Released, dispatched, in transit, delivered, administered.';
COMMENT ON COLUMN therapy_delivery_events.delivery_event.shipment_event_timestamp IS 'When.';
COMMENT ON COLUMN therapy_delivery_events.delivery_event.patient_pseudonym_identifier IS 'The patient, by pseudonym.';
COMMENT ON COLUMN therapy_delivery_events.delivery_event.order_identifier IS 'The order.';
COMMENT ON COLUMN therapy_delivery_events.delivery_event.shipment_event_location IS 'Where.';
COMMENT ON COLUMN therapy_delivery_events.delivery_event.shipment_storage_description IS 'The storage conditions the therapy must be kept under in transit.';

CREATE TABLE IF NOT EXISTS therapy_delivery_events.administration_confirmation (
  batch_identifier                   varchar(40) NOT NULL,
  patient_pseudonym_identifier       varchar(40) NOT NULL,
  treatment_administration_timestamp timestamptz NOT NULL,
  clinician_identifier               varchar(40) NOT NULL,
  order_identifier                   varchar(40) NOT NULL,
  CONSTRAINT administration_confirmation_pk PRIMARY KEY (batch_identifier)
);
COMMENT ON TABLE therapy_delivery_events.administration_confirmation IS 'One row per therapy confirmed administered.';
COMMENT ON COLUMN therapy_delivery_events.administration_confirmation.batch_identifier IS 'The therapy.';
COMMENT ON COLUMN therapy_delivery_events.administration_confirmation.patient_pseudonym_identifier IS 'The patient, by pseudonym.';
COMMENT ON COLUMN therapy_delivery_events.administration_confirmation.treatment_administration_timestamp IS 'When administered.';
COMMENT ON COLUMN therapy_delivery_events.administration_confirmation.clinician_identifier IS 'Who administered.';
COMMENT ON COLUMN therapy_delivery_events.administration_confirmation.order_identifier IS 'The order fulfilled.';

GRANT ALL ON ALL TABLES IN SCHEMA therapy_delivery_events TO egeria_admin, egeria_user, airflow_user;

-- Transport Classifications  (DigitalProduct::Coco::Transport Classifications)
CREATE SCHEMA IF NOT EXISTS transport_classifications;
GRANT ALL ON SCHEMA transport_classifications TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA transport_classifications IS 'The transport classification of each substance and product in each form it is shipped: UN number, packing group, labelling and the documentation set required. It is a library rather than a process because the same rules must give the same answer to despatch, to procurement and to the person signing the declaration.';

CREATE TABLE IF NOT EXISTS transport_classifications.transport_classification (
  transport_classification_identifier                varchar(40) NOT NULL,
  substance_code                                     varchar(20),
  product_code                                       varchar(20),
  substance_form_description                         text NOT NULL,
  transport_classification_code                      varchar(20) NOT NULL,
  transport_classification_packing_group_code        varchar(5),
  transport_classification_hazard_class_code         varchar(10) NOT NULL,
  transport_classification_labelling_description     text NOT NULL,
  transport_classification_documentation_description text NOT NULL,
  transport_classification_date                      date NOT NULL,
  CONSTRAINT transport_classification_pk PRIMARY KEY (transport_classification_identifier)
);
COMMENT ON TABLE transport_classifications.transport_classification IS 'One row per substance or product per shipped form.';
COMMENT ON COLUMN transport_classifications.transport_classification.transport_classification_identifier IS 'The unique identifier of the transport classification of a substance or product in a shipped form.';
COMMENT ON COLUMN transport_classifications.transport_classification.substance_code IS 'The substance, for hazardous materials.';
COMMENT ON COLUMN transport_classifications.transport_classification.product_code IS 'The product, for finished goods.';
COMMENT ON COLUMN transport_classifications.transport_classification.substance_form_description IS 'The form shipped.';
COMMENT ON COLUMN transport_classifications.transport_classification.transport_classification_code IS 'The UN number.';
COMMENT ON COLUMN transport_classifications.transport_classification.transport_classification_packing_group_code IS 'The packing group.';
COMMENT ON COLUMN transport_classifications.transport_classification.transport_classification_hazard_class_code IS 'The hazard class.';
COMMENT ON COLUMN transport_classifications.transport_classification.transport_classification_labelling_description IS 'The labelling required.';
COMMENT ON COLUMN transport_classifications.transport_classification.transport_classification_documentation_description IS 'The documentation set required.';
COMMENT ON COLUMN transport_classifications.transport_classification.transport_classification_date IS 'When derived.';

GRANT ALL ON ALL TABLES IN SCHEMA transport_classifications TO egeria_admin, egeria_user, airflow_user;

-- Dangerous Goods Consignment Records  (DigitalProduct::Coco::Dangerous Goods Consignment Records)
CREATE SCHEMA IF NOT EXISTS dangerous_goods_consignment_records;
GRANT ALL ON SCHEMA dangerous_goods_consignment_records TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA dangerous_goods_consignment_records IS 'The dangerous goods declaration and accompanying documents for each consignment, signed by a certificated person, with the certificate that authorised the signature. The shipper''s liability stays with the company however the carrier behaves afterwards.';

CREATE TABLE IF NOT EXISTS dangerous_goods_consignment_records.consignment_declaration (
  shipment_identifier              varchar(40) NOT NULL,
  shipment_dispatch_date           date NOT NULL,
  carrier_identifier               varchar(40) NOT NULL,
  shipment_ship_to_address         text NOT NULL,
  transport_classification_code    varchar(20) NOT NULL,
  shipment_quantity                double precision NOT NULL,
  shipment_unit                    varchar(20) NOT NULL,
  declaration_signatory_identifier varchar(40) NOT NULL,
  declaration_signed_timestamp     timestamptz NOT NULL,
  certificate_identifier           varchar(40) NOT NULL,
  CONSTRAINT consignment_declaration_pk PRIMARY KEY (shipment_identifier)
);
COMMENT ON TABLE dangerous_goods_consignment_records.consignment_declaration IS 'One row per dangerous goods consignment.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_declaration.shipment_identifier IS 'The consignment.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_declaration.shipment_dispatch_date IS 'When dispatched.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_declaration.carrier_identifier IS 'The carrier.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_declaration.shipment_ship_to_address IS 'The destination.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_declaration.transport_classification_code IS 'The UN number declared.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_declaration.shipment_quantity IS 'The quantity shipped.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_declaration.shipment_unit IS 'The unit.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_declaration.declaration_signatory_identifier IS 'The certificated signatory, by pseudonym.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_declaration.declaration_signed_timestamp IS 'When signed.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_declaration.certificate_identifier IS 'The signatory''s dangerous goods certificate.';

CREATE TABLE IF NOT EXISTS dangerous_goods_consignment_records.consignment_document (
  shipment_identifier varchar(40) NOT NULL,
  document_identifier varchar(60) NOT NULL,
  document_type       varchar(40) NOT NULL,
  document_date       date NOT NULL,
  CONSTRAINT consignment_document_pk PRIMARY KEY (shipment_identifier, document_identifier)
);
COMMENT ON TABLE dangerous_goods_consignment_records.consignment_document IS 'One row per document in the consignment''s documentation set.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_document.shipment_identifier IS 'The consignment.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_document.document_identifier IS 'The document.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_document.document_type IS 'Declaration, safety data sheet, handling instructions or other.';
COMMENT ON COLUMN dangerous_goods_consignment_records.consignment_document.document_date IS 'Its date.';

GRANT ALL ON ALL TABLES IN SCHEMA dangerous_goods_consignment_records TO egeria_admin, egeria_user, airflow_user;

-- In-Transit Temperature Readings  (DigitalProduct::Coco::In-Transit Temperature Readings)
CREATE SCHEMA IF NOT EXISTS in_transit_temperature_readings;
GRANT ALL ON SCHEMA in_transit_temperature_readings TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA in_transit_temperature_readings IS 'The readings from the loggers and live monitors travelling inside consignments: temperature, location and time. The devices are themselves dangerous goods, because they contain lithium batteries.';

CREATE TABLE IF NOT EXISTS in_transit_temperature_readings.temperature_reading (
  device_identifier          varchar(40) NOT NULL,
  device_reading_timestamp   timestamptz NOT NULL,
  shipment_identifier        varchar(40) NOT NULL,
  device_reading_temperature double precision NOT NULL,
  device_location            varchar(120),
  device_type                varchar(20) NOT NULL,
  CONSTRAINT temperature_reading_pk PRIMARY KEY (device_identifier, device_reading_timestamp)
);
COMMENT ON TABLE in_transit_temperature_readings.temperature_reading IS 'One row per reading from a device.';
COMMENT ON COLUMN in_transit_temperature_readings.temperature_reading.device_identifier IS 'The device.';
COMMENT ON COLUMN in_transit_temperature_readings.temperature_reading.device_reading_timestamp IS 'When.';
COMMENT ON COLUMN in_transit_temperature_readings.temperature_reading.shipment_identifier IS 'The consignment the device travelled with.';
COMMENT ON COLUMN in_transit_temperature_readings.temperature_reading.device_reading_temperature IS 'The temperature, in degrees Celsius.';
COMMENT ON COLUMN in_transit_temperature_readings.temperature_reading.device_location IS 'The device''s reported location, if it reports one.';
COMMENT ON COLUMN in_transit_temperature_readings.temperature_reading.device_type IS 'Logger or live monitor.';

GRANT ALL ON ALL TABLES IN SCHEMA in_transit_temperature_readings TO egeria_admin, egeria_user, airflow_user;

-- Cold Chain Transit Records  (DigitalProduct::Coco::Cold Chain Transit Records)
CREATE SCHEMA IF NOT EXISTS cold_chain_transit_records;
GRANT ALL ON SCHEMA cold_chain_transit_records TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA cold_chain_transit_records IS 'The temperature history of each consignment reconciled against the permitted range for the product shipped, and the excursions detected. A gap in the record is treated as an excursion, because an unmonitored interval cannot be shown to have been within range.';

CREATE TABLE IF NOT EXISTS cold_chain_transit_records.transit_temperature_record (
  shipment_identifier                   varchar(40) NOT NULL,
  product_code                          varchar(20) NOT NULL,
  batch_identifier                      varchar(40) NOT NULL,
  device_identifier                     varchar(40) NOT NULL,
  shipment_transit_start_timestamp      timestamptz NOT NULL,
  shipment_transit_end_timestamp        timestamptz NOT NULL,
  shipment_transit_minimum_temperature  double precision NOT NULL,
  shipment_transit_maximum_temperature  double precision NOT NULL,
  shipment_transit_record_complete_flag boolean NOT NULL,
  CONSTRAINT transit_temperature_record_pk PRIMARY KEY (shipment_identifier)
);
COMMENT ON TABLE cold_chain_transit_records.transit_temperature_record IS 'One row per consignment, the reconciled temperature history.';
COMMENT ON COLUMN cold_chain_transit_records.transit_temperature_record.shipment_identifier IS 'The consignment.';
COMMENT ON COLUMN cold_chain_transit_records.transit_temperature_record.product_code IS 'The product shipped.';
COMMENT ON COLUMN cold_chain_transit_records.transit_temperature_record.batch_identifier IS 'The batch.';
COMMENT ON COLUMN cold_chain_transit_records.transit_temperature_record.device_identifier IS 'The device the record came from.';
COMMENT ON COLUMN cold_chain_transit_records.transit_temperature_record.shipment_transit_start_timestamp IS 'When monitoring began.';
COMMENT ON COLUMN cold_chain_transit_records.transit_temperature_record.shipment_transit_end_timestamp IS 'When monitoring ended.';
COMMENT ON COLUMN cold_chain_transit_records.transit_temperature_record.shipment_transit_minimum_temperature IS 'The lowest temperature recorded.';
COMMENT ON COLUMN cold_chain_transit_records.transit_temperature_record.shipment_transit_maximum_temperature IS 'The highest temperature recorded.';
COMMENT ON COLUMN cold_chain_transit_records.transit_temperature_record.shipment_transit_record_complete_flag IS 'Whether the record has no gaps.';

CREATE TABLE IF NOT EXISTS cold_chain_transit_records.excursion_detection (
  excursion_identifier          varchar(40) NOT NULL,
  shipment_identifier           varchar(40) NOT NULL,
  excursion_start_timestamp     timestamptz NOT NULL,
  excursion_end_timestamp       timestamptz NOT NULL,
  excursion_duration            integer NOT NULL,
  excursion_maximum_temperature double precision NOT NULL,
  excursion_type                varchar(20) NOT NULL,
  CONSTRAINT excursion_detection_pk PRIMARY KEY (excursion_identifier)
);
COMMENT ON TABLE cold_chain_transit_records.excursion_detection IS 'One row per excursion detected in a consignment''s record.';
COMMENT ON COLUMN cold_chain_transit_records.excursion_detection.excursion_identifier IS 'The excursion.';
COMMENT ON COLUMN cold_chain_transit_records.excursion_detection.shipment_identifier IS 'The consignment.';
COMMENT ON COLUMN cold_chain_transit_records.excursion_detection.excursion_start_timestamp IS 'When the range was left.';
COMMENT ON COLUMN cold_chain_transit_records.excursion_detection.excursion_end_timestamp IS 'When it was regained.';
COMMENT ON COLUMN cold_chain_transit_records.excursion_detection.excursion_duration IS 'How long, in minutes.';
COMMENT ON COLUMN cold_chain_transit_records.excursion_detection.excursion_maximum_temperature IS 'The extreme temperature reached.';
COMMENT ON COLUMN cold_chain_transit_records.excursion_detection.excursion_type IS 'Temperature excursion or monitoring gap.';

GRANT ALL ON ALL TABLES IN SCHEMA cold_chain_transit_records TO egeria_admin, egeria_user, airflow_user;

-- Carrier Transit Events  (DigitalProduct::Coco::Carrier Transit Events)
CREATE SCHEMA IF NOT EXISTS carrier_transit_events;
GRANT ALL ON SCHEMA carrier_transit_events TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA carrier_transit_events IS 'The handover events, delays and delivery confirmations reported by carrier systems for each consignment. The company reads status from carriers and hands documentation to them, but has no visibility of what happens inside them.';

CREATE TABLE IF NOT EXISTS carrier_transit_events.transit_event (
  shipment_identifier                varchar(40) NOT NULL,
  shipment_transit_event_type        varchar(20) NOT NULL,
  shipment_transit_event_timestamp   timestamptz NOT NULL,
  carrier_identifier                 varchar(40) NOT NULL,
  shipment_transit_event_location    varchar(120),
  shipment_transit_event_description text,
  CONSTRAINT transit_event_pk PRIMARY KEY (shipment_identifier, shipment_transit_event_type, shipment_transit_event_timestamp)
);
COMMENT ON TABLE carrier_transit_events.transit_event IS 'One row per event reported by a carrier.';
COMMENT ON COLUMN carrier_transit_events.transit_event.shipment_identifier IS 'The consignment.';
COMMENT ON COLUMN carrier_transit_events.transit_event.shipment_transit_event_type IS 'Collected, handed over, delayed, delivered or exception.';
COMMENT ON COLUMN carrier_transit_events.transit_event.shipment_transit_event_timestamp IS 'When.';
COMMENT ON COLUMN carrier_transit_events.transit_event.carrier_identifier IS 'The carrier.';
COMMENT ON COLUMN carrier_transit_events.transit_event.shipment_transit_event_location IS 'Where.';
COMMENT ON COLUMN carrier_transit_events.transit_event.shipment_transit_event_description IS 'The carrier''s description.';

GRANT ALL ON ALL TABLES IN SCHEMA carrier_transit_events TO egeria_admin, egeria_user, airflow_user;

-- ================================================================================================
-- patient-treatment.md
-- ================================================================================================

-- Treatment Orders  (DigitalProduct::Coco::Treatment Orders)
CREATE SCHEMA IF NOT EXISTS treatment_orders;
GRANT ALL ON SCHEMA treatment_orders TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA treatment_orders IS 'The orders placed by treating clinicians for personalised therapies: the patient, the prescribing clinician, the product ordered and the sample collection it requires. It is the point at which a treatment decision made outside the company becomes an instruction inside it.';

CREATE TABLE IF NOT EXISTS treatment_orders.treatment_order (
  order_identifier     varchar(40) NOT NULL,
  order_date           date NOT NULL,
  patient_identifier   varchar(40) NOT NULL,
  clinician_identifier varchar(40) NOT NULL,
  hospital_identifier  varchar(40) NOT NULL,
  product_code         varchar(20) NOT NULL,
  order_quantity       integer NOT NULL,
  order_current_status varchar(20) NOT NULL,
  CONSTRAINT treatment_order_pk PRIMARY KEY (order_identifier)
);
COMMENT ON TABLE treatment_orders.treatment_order IS 'One row per order placed through the portal.';
COMMENT ON COLUMN treatment_orders.treatment_order.order_identifier IS 'The unique identifier of the order.';
COMMENT ON COLUMN treatment_orders.treatment_order.order_date IS 'When the order was placed.';
COMMENT ON COLUMN treatment_orders.treatment_order.patient_identifier IS 'The patient the therapy is for, as identified by the treating site.';
COMMENT ON COLUMN treatment_orders.treatment_order.clinician_identifier IS 'The prescribing clinician.';
COMMENT ON COLUMN treatment_orders.treatment_order.hospital_identifier IS 'The treating site.';
COMMENT ON COLUMN treatment_orders.treatment_order.product_code IS 'The product ordered.';
COMMENT ON COLUMN treatment_orders.treatment_order.order_quantity IS 'The number of doses ordered.';
COMMENT ON COLUMN treatment_orders.treatment_order.order_current_status IS 'Where the order is in its life.';

CREATE TABLE IF NOT EXISTS treatment_orders.sample_collection_request (
  order_identifier             varchar(40) NOT NULL,
  sample_collection_location   varchar(40) NOT NULL,
  sample_collection_start_date date NOT NULL,
  sample_collection_end_date   date NOT NULL,
  sample_material_type         varchar(60) NOT NULL,
  CONSTRAINT sample_collection_request_pk PRIMARY KEY (order_identifier)
);
COMMENT ON TABLE treatment_orders.sample_collection_request IS 'One row per request for patient material to be collected for an order.';
COMMENT ON COLUMN treatment_orders.sample_collection_request.order_identifier IS 'The order the sample is for.';
COMMENT ON COLUMN treatment_orders.sample_collection_request.sample_collection_location IS 'Where the material is to be collected.';
COMMENT ON COLUMN treatment_orders.sample_collection_request.sample_collection_start_date IS 'The earliest the material may be taken.';
COMMENT ON COLUMN treatment_orders.sample_collection_request.sample_collection_end_date IS 'The latest the material may be taken.';
COMMENT ON COLUMN treatment_orders.sample_collection_request.sample_material_type IS 'The material required from the patient.';

GRANT ALL ON ALL TABLES IN SCHEMA treatment_orders TO egeria_admin, egeria_user, airflow_user;

-- Clinician Adverse Reaction Reports  (DigitalProduct::Coco::Clinician Adverse Reaction Reports)
CREATE SCHEMA IF NOT EXISTS clinician_adverse_reaction_reports;
GRANT ALL ON SCHEMA clinician_adverse_reaction_reports TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA clinician_adverse_reaction_reports IS 'Suspected adverse reactions reported by treating clinicians through the ordering portal, identifying the patient by pseudonym and the product and batch involved. The data arrives through the same channel as orders but is of a different kind, and starts a different clock.';

CREATE TABLE IF NOT EXISTS clinician_adverse_reaction_reports.clinician_reaction_report (
  adverse_event_identifier        varchar(40) NOT NULL,
  adverse_event_reported_date     date NOT NULL,
  patient_pseudonym_identifier    varchar(40) NOT NULL,
  clinician_identifier            varchar(40) NOT NULL,
  product_code                    varchar(20) NOT NULL,
  batch_identifier                varchar(40),
  adverse_event_description       text NOT NULL,
  adverse_event_reported_severity varchar(20),
  CONSTRAINT clinician_reaction_report_pk PRIMARY KEY (adverse_event_identifier)
);
COMMENT ON TABLE clinician_adverse_reaction_reports.clinician_reaction_report IS 'One row per suspected reaction reported by a clinician.';
COMMENT ON COLUMN clinician_adverse_reaction_reports.clinician_reaction_report.adverse_event_identifier IS 'The unique identifier of the report.';
COMMENT ON COLUMN clinician_adverse_reaction_reports.clinician_reaction_report.adverse_event_reported_date IS 'When the clinician reported the reaction.';
COMMENT ON COLUMN clinician_adverse_reaction_reports.clinician_reaction_report.patient_pseudonym_identifier IS 'The patient, by pseudonym.';
COMMENT ON COLUMN clinician_adverse_reaction_reports.clinician_reaction_report.clinician_identifier IS 'The reporting clinician.';
COMMENT ON COLUMN clinician_adverse_reaction_reports.clinician_reaction_report.product_code IS 'The product suspected.';
COMMENT ON COLUMN clinician_adverse_reaction_reports.clinician_reaction_report.batch_identifier IS 'The batch administered, if known.';
COMMENT ON COLUMN clinician_adverse_reaction_reports.clinician_reaction_report.adverse_event_description IS 'The clinician''s description of the reaction.';
COMMENT ON COLUMN clinician_adverse_reaction_reports.clinician_reaction_report.adverse_event_reported_severity IS 'The severity as reported by the clinician.';

GRANT ALL ON ALL TABLES IN SCHEMA clinician_adverse_reaction_reports TO egeria_admin, egeria_user, airflow_user;

-- Patient Pseudonym Register  (DigitalProduct::Coco::Patient Pseudonym Register)
CREATE SCHEMA IF NOT EXISTS patient_pseudonym_register;
GRANT ALL ON SCHEMA patient_pseudonym_register TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA patient_pseudonym_register IS 'The link between a patient, the material taken from them and the therapy manufactured from it, issued as a pseudonym that every other system in the chain works from. Manufacturing can be certain it has the right material without ever holding the patient''s identity.';

CREATE TABLE IF NOT EXISTS patient_pseudonym_register.patient_pseudonym_link (
  patient_pseudonym_identifier       varchar(40) NOT NULL,
  order_identifier                   varchar(40) NOT NULL,
  patient_pseudonym_issued_timestamp timestamptz NOT NULL,
  product_code                       varchar(20) NOT NULL,
  patient_parameter_description      text,
  CONSTRAINT patient_pseudonym_link_pk PRIMARY KEY (patient_pseudonym_identifier)
);
COMMENT ON TABLE patient_pseudonym_register.patient_pseudonym_link IS 'One row per patient pseudonym issued for an order.';
COMMENT ON COLUMN patient_pseudonym_register.patient_pseudonym_link.patient_pseudonym_identifier IS 'The pseudonym issued.';
COMMENT ON COLUMN patient_pseudonym_register.patient_pseudonym_link.order_identifier IS 'The order the pseudonym was issued for.';
COMMENT ON COLUMN patient_pseudonym_register.patient_pseudonym_link.patient_pseudonym_issued_timestamp IS 'When the pseudonym was issued.';
COMMENT ON COLUMN patient_pseudonym_register.patient_pseudonym_link.product_code IS 'The product specified.';
COMMENT ON COLUMN patient_pseudonym_register.patient_pseudonym_link.patient_parameter_description IS 'The patient-specific parameters manufacturing must apply.';

CREATE TABLE IF NOT EXISTS patient_pseudonym_register.administration_record (
  batch_identifier                        varchar(40) NOT NULL,
  patient_pseudonym_identifier            varchar(40) NOT NULL,
  treatment_delivery_timestamp            timestamptz NOT NULL,
  treatment_administration_timestamp      timestamptz,
  treatment_administration_confirmed_flag boolean NOT NULL,
  CONSTRAINT administration_record_pk PRIMARY KEY (batch_identifier)
);
COMMENT ON TABLE patient_pseudonym_register.administration_record IS 'One row per therapy delivered and administered, closing the loop the order opened.';
COMMENT ON COLUMN patient_pseudonym_register.administration_record.batch_identifier IS 'The therapy administered.';
COMMENT ON COLUMN patient_pseudonym_register.administration_record.patient_pseudonym_identifier IS 'The patient, by pseudonym.';
COMMENT ON COLUMN patient_pseudonym_register.administration_record.treatment_delivery_timestamp IS 'When the therapy arrived at the treating site.';
COMMENT ON COLUMN patient_pseudonym_register.administration_record.treatment_administration_timestamp IS 'When the therapy was administered.';
COMMENT ON COLUMN patient_pseudonym_register.administration_record.treatment_administration_confirmed_flag IS 'Whether administration has been confirmed by the site.';

GRANT ALL ON ALL TABLES IN SCHEMA patient_pseudonym_register TO egeria_admin, egeria_user, airflow_user;

-- ================================================================================================
-- finance.md
-- ================================================================================================

-- Treatment Invoices  (DigitalProduct::Coco::Treatment Invoices)
CREATE SCHEMA IF NOT EXISTS treatment_invoices;
GRANT ALL ON SCHEMA treatment_invoices TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA treatment_invoices IS 'The invoices raised for fulfilled treatment orders and the revenue recognition data that accompanies them. It is where a clinical event becomes a financial one, and where the fulfilment record and the financial record must agree.';

CREATE TABLE IF NOT EXISTS treatment_invoices.invoice (
  invoice_number         varchar(40) NOT NULL,
  invoice_date           date NOT NULL,
  order_identifier       varchar(40) NOT NULL,
  customer_identifier    varchar(40) NOT NULL,
  invoice_total_amount   numeric(18,2) NOT NULL,
  invoice_currency_code  varchar(3) NOT NULL,
  invoice_due_date       date NOT NULL,
  invoice_current_status varchar(20) NOT NULL,
  CONSTRAINT invoice_pk PRIMARY KEY (invoice_number)
);
COMMENT ON TABLE treatment_invoices.invoice IS 'One row per invoice raised.';
COMMENT ON COLUMN treatment_invoices.invoice.invoice_number IS 'The invoice number.';
COMMENT ON COLUMN treatment_invoices.invoice.invoice_date IS 'When the invoice was raised.';
COMMENT ON COLUMN treatment_invoices.invoice.order_identifier IS 'The treatment order invoiced.';
COMMENT ON COLUMN treatment_invoices.invoice.customer_identifier IS 'The organisation invoiced.';
COMMENT ON COLUMN treatment_invoices.invoice.invoice_total_amount IS 'The invoiced value.';
COMMENT ON COLUMN treatment_invoices.invoice.invoice_currency_code IS 'The currency of the invoice.';
COMMENT ON COLUMN treatment_invoices.invoice.invoice_due_date IS 'When payment is due.';
COMMENT ON COLUMN treatment_invoices.invoice.invoice_current_status IS 'Whether the invoice is open, paid or credited.';

CREATE TABLE IF NOT EXISTS treatment_invoices.revenue_recognition (
  invoice_number           varchar(40) NOT NULL,
  revenue_recognition_date date NOT NULL,
  revenue_amount           numeric(18,2) NOT NULL,
  order_delivery_date      date NOT NULL,
  ledger_account_code      varchar(20) NOT NULL,
  CONSTRAINT revenue_recognition_pk PRIMARY KEY (invoice_number)
);
COMMENT ON TABLE treatment_invoices.revenue_recognition IS 'One row per invoice, the revenue recognised and the evidence it rests on.';
COMMENT ON COLUMN treatment_invoices.revenue_recognition.invoice_number IS 'The invoice.';
COMMENT ON COLUMN treatment_invoices.revenue_recognition.revenue_recognition_date IS 'When the revenue is recognised.';
COMMENT ON COLUMN treatment_invoices.revenue_recognition.revenue_amount IS 'The revenue recognised.';
COMMENT ON COLUMN treatment_invoices.revenue_recognition.order_delivery_date IS 'The delivery date the recognition relies on.';
COMMENT ON COLUMN treatment_invoices.revenue_recognition.ledger_account_code IS 'The revenue account posted to.';

GRANT ALL ON ALL TABLES IN SCHEMA treatment_invoices TO egeria_admin, egeria_user, airflow_user;

-- Subledger Postings  (DigitalProduct::Coco::Subledger Postings)
CREATE SCHEMA IF NOT EXISTS subledger_postings;
GRANT ALL ON SCHEMA subledger_postings TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA subledger_postings IS 'The transactions carried from the operational systems into the general ledger, batched per source feed and accounting period. Each feed is a place where a transaction can be dropped, duplicated or posted to the wrong period, so completeness is asserted per feed rather than in aggregate.';

CREATE TABLE IF NOT EXISTS subledger_postings.posting_batch (
  feed_identifier        varchar(40) NOT NULL,
  system_identifier      varchar(60) NOT NULL,
  accounting_period_code varchar(10) NOT NULL,
  feed_posted_timestamp  timestamptz NOT NULL,
  feed_line_count        integer NOT NULL,
  feed_total_amount      numeric(18,2) NOT NULL,
  feed_current_status    varchar(20) NOT NULL,
  CONSTRAINT posting_batch_pk PRIMARY KEY (feed_identifier)
);
COMMENT ON TABLE subledger_postings.posting_batch IS 'One row per batch of postings from one source feed for one period.';
COMMENT ON COLUMN subledger_postings.posting_batch.feed_identifier IS 'The unique identifier of the batch.';
COMMENT ON COLUMN subledger_postings.posting_batch.system_identifier IS 'The source system the feed comes from.';
COMMENT ON COLUMN subledger_postings.posting_batch.accounting_period_code IS 'The accounting period the batch belongs to.';
COMMENT ON COLUMN subledger_postings.posting_batch.feed_posted_timestamp IS 'When the batch was posted to the ledger.';
COMMENT ON COLUMN subledger_postings.posting_batch.feed_line_count IS 'The number of postings in the batch.';
COMMENT ON COLUMN subledger_postings.posting_batch.feed_total_amount IS 'The control total of the batch.';
COMMENT ON COLUMN subledger_postings.posting_batch.feed_current_status IS 'Whether the batch is pending, posted or rejected.';

CREATE TABLE IF NOT EXISTS subledger_postings.posting_line (
  feed_identifier        varchar(40) NOT NULL,
  posting_line_number    integer NOT NULL,
  ledger_account_code    varchar(20) NOT NULL,
  legal_entity_code      varchar(10) NOT NULL,
  transaction_identifier varchar(40) NOT NULL,
  posting_amount         numeric(18,2) NOT NULL,
  posting_currency_code  varchar(3) NOT NULL,
  CONSTRAINT posting_line_pk PRIMARY KEY (feed_identifier, posting_line_number)
);
COMMENT ON TABLE subledger_postings.posting_line IS 'One row per posting within a batch.';
COMMENT ON COLUMN subledger_postings.posting_line.feed_identifier IS 'The batch the posting belongs to.';
COMMENT ON COLUMN subledger_postings.posting_line.posting_line_number IS 'The position of the posting in the batch.';
COMMENT ON COLUMN subledger_postings.posting_line.ledger_account_code IS 'The account posted to.';
COMMENT ON COLUMN subledger_postings.posting_line.legal_entity_code IS 'The legal entity the posting belongs to.';
COMMENT ON COLUMN subledger_postings.posting_line.transaction_identifier IS 'The source transaction the posting represents.';
COMMENT ON COLUMN subledger_postings.posting_line.posting_amount IS 'The amount posted.';
COMMENT ON COLUMN subledger_postings.posting_line.posting_currency_code IS 'The currency of the amount.';

GRANT ALL ON ALL TABLES IN SCHEMA subledger_postings TO egeria_admin, egeria_user, airflow_user;

-- Manual Journal Approvals  (DigitalProduct::Coco::Manual Journal Approvals)
CREATE SCHEMA IF NOT EXISTS manual_journal_approvals;
GRANT ALL ON SCHEMA manual_journal_approvals TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA manual_journal_approvals IS 'Manual journal entries above the materiality threshold, together with the review and approval each received before it was posted. Manual adjustment is the segment of the close least covered by system controls and most able to change a reported figure.';

CREATE TABLE IF NOT EXISTS manual_journal_approvals.journal_entry (
  journal_entry_identifier          varchar(40) NOT NULL,
  accounting_period_code            varchar(10) NOT NULL,
  legal_entity_code                 varchar(10) NOT NULL,
  journal_entry_amount              numeric(18,2) NOT NULL,
  journal_entry_description         text NOT NULL,
  journal_entry_preparer_identifier varchar(40) NOT NULL,
  journal_entry_submitted_timestamp timestamptz NOT NULL,
  CONSTRAINT journal_entry_pk PRIMARY KEY (journal_entry_identifier)
);
COMMENT ON TABLE manual_journal_approvals.journal_entry IS 'One row per manual journal entry submitted for review.';
COMMENT ON COLUMN manual_journal_approvals.journal_entry.journal_entry_identifier IS 'The unique identifier of the entry.';
COMMENT ON COLUMN manual_journal_approvals.journal_entry.accounting_period_code IS 'The period the entry adjusts.';
COMMENT ON COLUMN manual_journal_approvals.journal_entry.legal_entity_code IS 'The entity the entry belongs to.';
COMMENT ON COLUMN manual_journal_approvals.journal_entry.journal_entry_amount IS 'The value of the adjustment.';
COMMENT ON COLUMN manual_journal_approvals.journal_entry.journal_entry_description IS 'The reason for the adjustment.';
COMMENT ON COLUMN manual_journal_approvals.journal_entry.journal_entry_preparer_identifier IS 'The person who prepared the entry.';
COMMENT ON COLUMN manual_journal_approvals.journal_entry.journal_entry_submitted_timestamp IS 'When the entry was submitted for review.';

CREATE TABLE IF NOT EXISTS manual_journal_approvals.journal_approval (
  journal_entry_identifier          varchar(40) NOT NULL,
  journal_entry_approval_timestamp  timestamptz NOT NULL,
  journal_entry_approver_identifier varchar(40) NOT NULL,
  journal_entry_approval_status     varchar(20) NOT NULL,
  journal_entry_approval_notes      text,
  CONSTRAINT journal_approval_pk PRIMARY KEY (journal_entry_identifier, journal_entry_approval_timestamp)
);
COMMENT ON TABLE manual_journal_approvals.journal_approval IS 'One row per review decision on a journal entry.';
COMMENT ON COLUMN manual_journal_approvals.journal_approval.journal_entry_identifier IS 'The entry reviewed.';
COMMENT ON COLUMN manual_journal_approvals.journal_approval.journal_entry_approval_timestamp IS 'When the decision was taken.';
COMMENT ON COLUMN manual_journal_approvals.journal_approval.journal_entry_approver_identifier IS 'The reviewer.';
COMMENT ON COLUMN manual_journal_approvals.journal_approval.journal_entry_approval_status IS 'Approved, rejected or returned for change.';
COMMENT ON COLUMN manual_journal_approvals.journal_approval.journal_entry_approval_notes IS 'The reviewer''s comments.';

GRANT ALL ON ALL TABLES IN SCHEMA manual_journal_approvals TO egeria_admin, egeria_user, airflow_user;

-- Consolidated Group Results  (DigitalProduct::Coco::Consolidated Group Results)
CREATE SCHEMA IF NOT EXISTS consolidated_group_results;
GRANT ALL ON SCHEMA consolidated_group_results TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA consolidated_group_results IS 'The trial balances of the US parent and the UK and EU subsidiaries, the intercompany eliminations and currency translations applied to them, and the consolidated statement lines that result. It is where several sets of books become one set of figures.';

CREATE TABLE IF NOT EXISTS consolidated_group_results.entity_trial_balance (
  legal_entity_code             varchar(10) NOT NULL,
  accounting_period_code        varchar(10) NOT NULL,
  ledger_account_code           varchar(20) NOT NULL,
  ledger_account_balance_amount numeric(18,2) NOT NULL,
  ledger_currency_code          varchar(3) NOT NULL,
  CONSTRAINT entity_trial_balance_pk PRIMARY KEY (legal_entity_code, accounting_period_code, ledger_account_code)
);
COMMENT ON TABLE consolidated_group_results.entity_trial_balance IS 'One row per account per legal entity per period.';
COMMENT ON COLUMN consolidated_group_results.entity_trial_balance.legal_entity_code IS 'The legal entity.';
COMMENT ON COLUMN consolidated_group_results.entity_trial_balance.accounting_period_code IS 'The period.';
COMMENT ON COLUMN consolidated_group_results.entity_trial_balance.ledger_account_code IS 'The account.';
COMMENT ON COLUMN consolidated_group_results.entity_trial_balance.ledger_account_balance_amount IS 'The closing balance in the entity''s currency.';
COMMENT ON COLUMN consolidated_group_results.entity_trial_balance.ledger_currency_code IS 'The entity''s reporting currency.';

CREATE TABLE IF NOT EXISTS consolidated_group_results.consolidation_adjustment (
  consolidation_adjustment_identifier  varchar(40) NOT NULL,
  accounting_period_code               varchar(10) NOT NULL,
  consolidation_adjustment_type        varchar(40) NOT NULL,
  legal_entity_code                    varchar(10) NOT NULL,
  ledger_account_code                  varchar(20) NOT NULL,
  consolidation_adjustment_amount      numeric(18,2) NOT NULL,
  consolidation_adjustment_description text NOT NULL,
  CONSTRAINT consolidation_adjustment_pk PRIMARY KEY (consolidation_adjustment_identifier)
);
COMMENT ON TABLE consolidated_group_results.consolidation_adjustment IS 'One row per elimination or translation adjustment applied during consolidation.';
COMMENT ON COLUMN consolidated_group_results.consolidation_adjustment.consolidation_adjustment_identifier IS 'The unique identifier of the adjustment.';
COMMENT ON COLUMN consolidated_group_results.consolidation_adjustment.accounting_period_code IS 'The period.';
COMMENT ON COLUMN consolidated_group_results.consolidation_adjustment.consolidation_adjustment_type IS 'Intercompany elimination, currency translation or other.';
COMMENT ON COLUMN consolidated_group_results.consolidation_adjustment.legal_entity_code IS 'The entity the adjustment applies to.';
COMMENT ON COLUMN consolidated_group_results.consolidation_adjustment.ledger_account_code IS 'The account adjusted.';
COMMENT ON COLUMN consolidated_group_results.consolidation_adjustment.consolidation_adjustment_amount IS 'The adjustment in group currency.';
COMMENT ON COLUMN consolidated_group_results.consolidation_adjustment.consolidation_adjustment_description IS 'The basis of the adjustment.';

CREATE TABLE IF NOT EXISTS consolidated_group_results.consolidated_statement_line (
  statement_line_identifier varchar(40) NOT NULL,
  accounting_period_code    varchar(10) NOT NULL,
  statement_line_code       varchar(20) NOT NULL,
  statement_segment_code    varchar(20),
  statement_line_amount     numeric(18,2) NOT NULL,
  CONSTRAINT consolidated_statement_line_pk PRIMARY KEY (statement_line_identifier)
);
COMMENT ON TABLE consolidated_group_results.consolidated_statement_line IS 'One row per line of the consolidated statements per period, with segment analysis.';
COMMENT ON COLUMN consolidated_group_results.consolidated_statement_line.statement_line_identifier IS 'The unique identifier of a line of the consolidated statements for a period and segment.';
COMMENT ON COLUMN consolidated_group_results.consolidated_statement_line.accounting_period_code IS 'The period.';
COMMENT ON COLUMN consolidated_group_results.consolidated_statement_line.statement_line_code IS 'The statement line.';
COMMENT ON COLUMN consolidated_group_results.consolidated_statement_line.statement_segment_code IS 'The business segment the line is analysed to.';
COMMENT ON COLUMN consolidated_group_results.consolidated_statement_line.statement_line_amount IS 'The consolidated amount in group currency.';

GRANT ALL ON ALL TABLES IN SCHEMA consolidated_group_results TO egeria_admin, egeria_user, airflow_user;

-- External Financial Disclosures  (DigitalProduct::Coco::External Financial Disclosures)
CREATE SCHEMA IF NOT EXISTS external_financial_disclosures;
GRANT ALL ON SCHEMA external_financial_disclosures TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA external_financial_disclosures IS 'The statements filed with regulators and published to the market, and the disclosures of transfers of value to healthcare professionals. Every figure must be resolvable back through the consolidation and the ledger to the transactions it was built from.';

CREATE TABLE IF NOT EXISTS external_financial_disclosures.disclosure_statement (
  disclosure_identifier        varchar(40) NOT NULL,
  disclosure_type              varchar(40) NOT NULL,
  accounting_period_code       varchar(10) NOT NULL,
  disclosure_regulator_code    varchar(20) NOT NULL,
  disclosure_filed_timestamp   timestamptz NOT NULL,
  disclosure_acknowledged_flag boolean NOT NULL,
  CONSTRAINT disclosure_statement_pk PRIMARY KEY (disclosure_identifier)
);
COMMENT ON TABLE external_financial_disclosures.disclosure_statement IS 'One row per statement or report filed.';
COMMENT ON COLUMN external_financial_disclosures.disclosure_statement.disclosure_identifier IS 'The unique identifier of the filing.';
COMMENT ON COLUMN external_financial_disclosures.disclosure_statement.disclosure_type IS 'Annual report, quarterly report, transfers of value disclosure or other.';
COMMENT ON COLUMN external_financial_disclosures.disclosure_statement.accounting_period_code IS 'The period the filing covers.';
COMMENT ON COLUMN external_financial_disclosures.disclosure_statement.disclosure_regulator_code IS 'The regulator or body the filing was made to.';
COMMENT ON COLUMN external_financial_disclosures.disclosure_statement.disclosure_filed_timestamp IS 'When the filing was made.';
COMMENT ON COLUMN external_financial_disclosures.disclosure_statement.disclosure_acknowledged_flag IS 'Whether the regulator has acknowledged receipt.';

CREATE TABLE IF NOT EXISTS external_financial_disclosures.disclosure_line_item (
  disclosure_identifier               varchar(40) NOT NULL,
  statement_line_code                 varchar(20) NOT NULL,
  disclosure_line_amount              numeric(18,2) NOT NULL,
  consolidation_adjustment_identifier varchar(40),
  CONSTRAINT disclosure_line_item_pk PRIMARY KEY (disclosure_identifier, statement_line_code)
);
COMMENT ON TABLE external_financial_disclosures.disclosure_line_item IS 'One row per figure in a filing, with its source.';
COMMENT ON COLUMN external_financial_disclosures.disclosure_line_item.disclosure_identifier IS 'The filing.';
COMMENT ON COLUMN external_financial_disclosures.disclosure_line_item.statement_line_code IS 'The statement line the figure reports.';
COMMENT ON COLUMN external_financial_disclosures.disclosure_line_item.disclosure_line_amount IS 'The figure disclosed.';
COMMENT ON COLUMN external_financial_disclosures.disclosure_line_item.consolidation_adjustment_identifier IS 'The consolidation adjustment the figure depends on, if any.';

GRANT ALL ON ALL TABLES IN SCHEMA external_financial_disclosures TO egeria_admin, egeria_user, airflow_user;

-- Financial Controls Evidence  (DigitalProduct::Coco::Financial Controls Evidence)
CREATE SCHEMA IF NOT EXISTS financial_controls_evidence;
GRANT ALL ON SCHEMA financial_controls_evidence TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA financial_controls_evidence IS 'The documentation and test evidence for the internal controls over financial reporting, and the reconciliations, approvals and checklist items produced by each close. The controls it evidences are controls over the close itself, so the repository is part of the chain rather than an audit of it.';

CREATE TABLE IF NOT EXISTS financial_controls_evidence.control_test_evidence (
  control_identifier          varchar(40) NOT NULL,
  accounting_period_code      varchar(10) NOT NULL,
  control_tested_date         date NOT NULL,
  control_tester_identifier   varchar(40) NOT NULL,
  control_tested_status       varchar(20) NOT NULL,
  control_evidence_identifier varchar(60) NOT NULL,
  CONSTRAINT control_test_evidence_pk PRIMARY KEY (control_identifier, accounting_period_code)
);
COMMENT ON TABLE financial_controls_evidence.control_test_evidence IS 'One row per test of a control in a period.';
COMMENT ON COLUMN financial_controls_evidence.control_test_evidence.control_identifier IS 'The control tested.';
COMMENT ON COLUMN financial_controls_evidence.control_test_evidence.accounting_period_code IS 'The period the test covers.';
COMMENT ON COLUMN financial_controls_evidence.control_test_evidence.control_tested_date IS 'When the test was performed.';
COMMENT ON COLUMN financial_controls_evidence.control_test_evidence.control_tester_identifier IS 'Who performed the test.';
COMMENT ON COLUMN financial_controls_evidence.control_test_evidence.control_tested_status IS 'Whether the control operated effectively.';
COMMENT ON COLUMN financial_controls_evidence.control_test_evidence.control_evidence_identifier IS 'The document holding the evidence.';

CREATE TABLE IF NOT EXISTS financial_controls_evidence.close_checklist_item (
  accounting_period_code                   varchar(10) NOT NULL,
  close_checklist_item_code                varchar(40) NOT NULL,
  close_checklist_item_completed_timestamp timestamptz,
  close_checklist_item_approver_identifier varchar(40),
  close_checklist_item_status              varchar(20) NOT NULL,
  CONSTRAINT close_checklist_item_pk PRIMARY KEY (accounting_period_code, close_checklist_item_code)
);
COMMENT ON TABLE financial_controls_evidence.close_checklist_item IS 'One row per step of the period-end close, its completion and approval.';
COMMENT ON COLUMN financial_controls_evidence.close_checklist_item.accounting_period_code IS 'The period closed.';
COMMENT ON COLUMN financial_controls_evidence.close_checklist_item.close_checklist_item_code IS 'The step.';
COMMENT ON COLUMN financial_controls_evidence.close_checklist_item.close_checklist_item_completed_timestamp IS 'When the step was completed.';
COMMENT ON COLUMN financial_controls_evidence.close_checklist_item.close_checklist_item_approver_identifier IS 'Who approved completion.';
COMMENT ON COLUMN financial_controls_evidence.close_checklist_item.close_checklist_item_status IS 'Not started, complete or approved.';

GRANT ALL ON ALL TABLES IN SCHEMA financial_controls_evidence TO egeria_admin, egeria_user, airflow_user;

-- Supplier Payment Detail Changes  (DigitalProduct::Coco::Supplier Payment Detail Changes)
CREATE SCHEMA IF NOT EXISTS supplier_payment_detail_changes;
GRANT ALL ON SCHEMA supplier_payment_detail_changes TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA supplier_payment_detail_changes IS 'Every change to a supplier''s bank details, treated as a controlled event with independent verification rather than as routine maintenance. This is where the payment flow has historically been attacked.';

CREATE TABLE IF NOT EXISTS supplier_payment_detail_changes.payment_detail_change (
  payment_detail_change_identifier           varchar(40) NOT NULL,
  supplier_identifier                        varchar(40) NOT NULL,
  payment_detail_change_requested_timestamp  timestamptz NOT NULL,
  payment_detail_change_requester_identifier varchar(40) NOT NULL,
  bank_account_previous_identifier           varchar(40),
  bank_account_current_identifier            varchar(40) NOT NULL,
  payment_detail_change_status               varchar(20) NOT NULL,
  CONSTRAINT payment_detail_change_pk PRIMARY KEY (payment_detail_change_identifier)
);
COMMENT ON TABLE supplier_payment_detail_changes.payment_detail_change IS 'One row per requested change to a supplier''s payment details.';
COMMENT ON COLUMN supplier_payment_detail_changes.payment_detail_change.payment_detail_change_identifier IS 'The unique identifier of the change request.';
COMMENT ON COLUMN supplier_payment_detail_changes.payment_detail_change.supplier_identifier IS 'The supplier.';
COMMENT ON COLUMN supplier_payment_detail_changes.payment_detail_change.payment_detail_change_requested_timestamp IS 'When the change was requested.';
COMMENT ON COLUMN supplier_payment_detail_changes.payment_detail_change.payment_detail_change_requester_identifier IS 'Who requested it.';
COMMENT ON COLUMN supplier_payment_detail_changes.payment_detail_change.bank_account_previous_identifier IS 'The bank account before the change, masked.';
COMMENT ON COLUMN supplier_payment_detail_changes.payment_detail_change.bank_account_current_identifier IS 'The bank account after the change, masked.';
COMMENT ON COLUMN supplier_payment_detail_changes.payment_detail_change.payment_detail_change_status IS 'Pending verification, verified, rejected.';

CREATE TABLE IF NOT EXISTS supplier_payment_detail_changes.verification_evidence (
  payment_detail_change_identifier          varchar(40) NOT NULL,
  payment_detail_change_verified_timestamp  timestamptz NOT NULL,
  payment_detail_change_verifier_identifier varchar(40) NOT NULL,
  payment_detail_change_channel_type        varchar(40) NOT NULL,
  payment_detail_change_verified_notes      text,
  CONSTRAINT verification_evidence_pk PRIMARY KEY (payment_detail_change_identifier, payment_detail_change_verified_timestamp)
);
COMMENT ON TABLE supplier_payment_detail_changes.verification_evidence IS 'One row per independent verification of a change.';
COMMENT ON COLUMN supplier_payment_detail_changes.verification_evidence.payment_detail_change_identifier IS 'The change verified.';
COMMENT ON COLUMN supplier_payment_detail_changes.verification_evidence.payment_detail_change_verified_timestamp IS 'When the verification was completed.';
COMMENT ON COLUMN supplier_payment_detail_changes.verification_evidence.payment_detail_change_verifier_identifier IS 'Who carried out the verification.';
COMMENT ON COLUMN supplier_payment_detail_changes.verification_evidence.payment_detail_change_channel_type IS 'The channel used, for example call-back to a known number.';
COMMENT ON COLUMN supplier_payment_detail_changes.verification_evidence.payment_detail_change_verified_notes IS 'What was confirmed and with whom.';

GRANT ALL ON ALL TABLES IN SCHEMA supplier_payment_detail_changes TO egeria_admin, egeria_user, airflow_user;

-- Supplier Payments  (DigitalProduct::Coco::Supplier Payments)
CREATE SCHEMA IF NOT EXISTS supplier_payments;
GRANT ALL ON SCHEMA supplier_payments TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA supplier_payments IS 'Supplier invoices matched to purchase orders and goods receipts, the payment authorisations that followed, and the instructions sent to the bank. Screening status and payment details are read at the moment of authorisation, the only moment at which either of them protects anything.';

CREATE TABLE IF NOT EXISTS supplier_payments.invoice_match (
  invoice_number           varchar(40) NOT NULL,
  supplier_identifier      varchar(40) NOT NULL,
  order_identifier         varchar(40) NOT NULL,
  goods_receipt_identifier varchar(40),
  invoice_total_amount     numeric(18,2) NOT NULL,
  invoice_currency_code    varchar(3) NOT NULL,
  invoice_match_status     varchar(20) NOT NULL,
  CONSTRAINT invoice_match_pk PRIMARY KEY (invoice_number, supplier_identifier)
);
COMMENT ON TABLE supplier_payments.invoice_match IS 'One row per supplier invoice, matched to the order and receipt it settles.';
COMMENT ON COLUMN supplier_payments.invoice_match.invoice_number IS 'The supplier''s invoice number.';
COMMENT ON COLUMN supplier_payments.invoice_match.supplier_identifier IS 'The supplier.';
COMMENT ON COLUMN supplier_payments.invoice_match.order_identifier IS 'The purchase order matched.';
COMMENT ON COLUMN supplier_payments.invoice_match.goods_receipt_identifier IS 'The goods receipt matched.';
COMMENT ON COLUMN supplier_payments.invoice_match.invoice_total_amount IS 'The invoiced amount.';
COMMENT ON COLUMN supplier_payments.invoice_match.invoice_currency_code IS 'The currency.';
COMMENT ON COLUMN supplier_payments.invoice_match.invoice_match_status IS 'Matched, variance or unmatched.';

CREATE TABLE IF NOT EXISTS supplier_payments.payment_instruction (
  payment_identifier              varchar(40) NOT NULL,
  supplier_identifier             varchar(40) NOT NULL,
  invoice_number                  varchar(40) NOT NULL,
  payment_amount                  numeric(18,2) NOT NULL,
  payment_currency_code           varchar(3) NOT NULL,
  payment_authoriser_identifier   varchar(40) NOT NULL,
  payment_authorised_timestamp    timestamptz NOT NULL,
  supplier_screened_status        varchar(20) NOT NULL,
  bank_account_current_identifier varchar(40) NOT NULL,
  ledger_account_code             varchar(20) NOT NULL,
  CONSTRAINT payment_instruction_pk PRIMARY KEY (payment_identifier)
);
COMMENT ON TABLE supplier_payments.payment_instruction IS 'One row per payment authorised and instructed to the bank.';
COMMENT ON COLUMN supplier_payments.payment_instruction.payment_identifier IS 'The unique identifier of the payment.';
COMMENT ON COLUMN supplier_payments.payment_instruction.supplier_identifier IS 'The payee.';
COMMENT ON COLUMN supplier_payments.payment_instruction.invoice_number IS 'The invoice settled.';
COMMENT ON COLUMN supplier_payments.payment_instruction.payment_amount IS 'The amount paid.';
COMMENT ON COLUMN supplier_payments.payment_instruction.payment_currency_code IS 'The currency.';
COMMENT ON COLUMN supplier_payments.payment_instruction.payment_authoriser_identifier IS 'Who authorised the payment.';
COMMENT ON COLUMN supplier_payments.payment_instruction.payment_authorised_timestamp IS 'When it was authorised.';
COMMENT ON COLUMN supplier_payments.payment_instruction.supplier_screened_status IS 'The supplier''s screening status at authorisation.';
COMMENT ON COLUMN supplier_payments.payment_instruction.bank_account_current_identifier IS 'The account paid, masked.';
COMMENT ON COLUMN supplier_payments.payment_instruction.ledger_account_code IS 'The cost coding of the payment.';

GRANT ALL ON ALL TABLES IN SCHEMA supplier_payments TO egeria_admin, egeria_user, airflow_user;

-- Payment Anomaly Findings  (DigitalProduct::Coco::Payment Anomaly Findings)
CREATE SCHEMA IF NOT EXISTS payment_anomaly_findings;
GRANT ALL ON SCHEMA payment_anomaly_findings TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA payment_anomaly_findings IS 'The patterns found across supplier payments and expense claims that no single transaction shows: duplicate payments, unusual supplier behaviour, and the concerns raised as a result. The fraud that motivated this chain was visible only across the whole flow.';

CREATE TABLE IF NOT EXISTS payment_anomaly_findings.anomaly_finding (
  anomaly_identifier          varchar(40) NOT NULL,
  anomaly_detected_timestamp  timestamptz NOT NULL,
  anomaly_type                varchar(40) NOT NULL,
  supplier_identifier         varchar(40),
  worker_pseudonym_identifier varchar(40),
  anomaly_description         text NOT NULL,
  anomaly_severity            varchar(20) NOT NULL,
  anomaly_current_status      varchar(20) NOT NULL,
  CONSTRAINT anomaly_finding_pk PRIMARY KEY (anomaly_identifier)
);
COMMENT ON TABLE payment_anomaly_findings.anomaly_finding IS 'One row per anomaly detected.';
COMMENT ON COLUMN payment_anomaly_findings.anomaly_finding.anomaly_identifier IS 'The unique identifier of the finding.';
COMMENT ON COLUMN payment_anomaly_findings.anomaly_finding.anomaly_detected_timestamp IS 'When it was detected.';
COMMENT ON COLUMN payment_anomaly_findings.anomaly_finding.anomaly_type IS 'Duplicate payment, split payment, new-supplier spike, claim pattern or other.';
COMMENT ON COLUMN payment_anomaly_findings.anomaly_finding.supplier_identifier IS 'The supplier implicated, if any.';
COMMENT ON COLUMN payment_anomaly_findings.anomaly_finding.worker_pseudonym_identifier IS 'The claimant implicated, if any.';
COMMENT ON COLUMN payment_anomaly_findings.anomaly_finding.anomaly_description IS 'What was observed.';
COMMENT ON COLUMN payment_anomaly_findings.anomaly_finding.anomaly_severity IS 'The assessed seriousness.';
COMMENT ON COLUMN payment_anomaly_findings.anomaly_finding.anomaly_current_status IS 'Open, under investigation, closed as false positive, confirmed.';

CREATE TABLE IF NOT EXISTS payment_anomaly_findings.monitored_transaction (
  anomaly_identifier     varchar(40) NOT NULL,
  transaction_identifier varchar(40) NOT NULL,
  transaction_type       varchar(20) NOT NULL,
  transaction_amount     numeric(18,2) NOT NULL,
  transaction_date       date NOT NULL,
  CONSTRAINT monitored_transaction_pk PRIMARY KEY (anomaly_identifier, transaction_identifier)
);
COMMENT ON TABLE payment_anomaly_findings.monitored_transaction IS 'One row per transaction contributing to a finding.';
COMMENT ON COLUMN payment_anomaly_findings.monitored_transaction.anomaly_identifier IS 'The finding.';
COMMENT ON COLUMN payment_anomaly_findings.monitored_transaction.transaction_identifier IS 'The payment or claim.';
COMMENT ON COLUMN payment_anomaly_findings.monitored_transaction.transaction_type IS 'Supplier payment or expense claim.';
COMMENT ON COLUMN payment_anomaly_findings.monitored_transaction.transaction_amount IS 'Its amount.';
COMMENT ON COLUMN payment_anomaly_findings.monitored_transaction.transaction_date IS 'Its date.';

GRANT ALL ON ALL TABLES IN SCHEMA payment_anomaly_findings TO egeria_admin, egeria_user, airflow_user;

-- Transfers Of Value  (DigitalProduct::Coco::Transfers Of Value)
CREATE SCHEMA IF NOT EXISTS transfers_of_value;
GRANT ALL ON SCHEMA transfers_of_value TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA transfers_of_value IS 'Payments and benefits provided to healthcare professionals and organisations, from whichever flow they originate, identified and recorded so that they can be disclosed. Reconstructing this afterwards from a general ledger is the failure it exists to prevent.';

CREATE TABLE IF NOT EXISTS transfers_of_value.transfer_of_value (
  transfer_of_value_identifier           varchar(40) NOT NULL,
  transfer_of_value_recipient_identifier varchar(40) NOT NULL,
  transfer_of_value_recipient_type       varchar(20) NOT NULL,
  transfer_of_value_type                 varchar(40) NOT NULL,
  transfer_of_value_description          text NOT NULL,
  transfer_of_value_amount               numeric(18,2) NOT NULL,
  transfer_of_value_currency_code        varchar(3) NOT NULL,
  transfer_of_value_date                 date NOT NULL,
  transaction_identifier                 varchar(40) NOT NULL,
  transfer_of_value_disclosed_flag       boolean NOT NULL,
  CONSTRAINT transfer_of_value_pk PRIMARY KEY (transfer_of_value_identifier)
);
COMMENT ON TABLE transfers_of_value.transfer_of_value IS 'One row per payment or benefit to a healthcare professional or organisation.';
COMMENT ON COLUMN transfers_of_value.transfer_of_value.transfer_of_value_identifier IS 'The unique identifier of the transfer.';
COMMENT ON COLUMN transfers_of_value.transfer_of_value.transfer_of_value_recipient_identifier IS 'The healthcare professional or organisation.';
COMMENT ON COLUMN transfers_of_value.transfer_of_value.transfer_of_value_recipient_type IS 'Individual professional or organisation.';
COMMENT ON COLUMN transfers_of_value.transfer_of_value.transfer_of_value_type IS 'Fee, hospitality, travel, grant or other.';
COMMENT ON COLUMN transfers_of_value.transfer_of_value.transfer_of_value_description IS 'The purpose of the transfer.';
COMMENT ON COLUMN transfers_of_value.transfer_of_value.transfer_of_value_amount IS 'The value transferred.';
COMMENT ON COLUMN transfers_of_value.transfer_of_value.transfer_of_value_currency_code IS 'The currency.';
COMMENT ON COLUMN transfers_of_value.transfer_of_value.transfer_of_value_date IS 'When it was provided.';
COMMENT ON COLUMN transfers_of_value.transfer_of_value.transaction_identifier IS 'The payment or expense claim it originated from.';
COMMENT ON COLUMN transfers_of_value.transfer_of_value.transfer_of_value_disclosed_flag IS 'Whether it has been included in a disclosure.';

GRANT ALL ON ALL TABLES IN SCHEMA transfers_of_value TO egeria_admin, egeria_user, airflow_user;

-- Expense Approvals  (DigitalProduct::Coco::Expense Approvals)
CREATE SCHEMA IF NOT EXISTS expense_approvals;
GRANT ALL ON SCHEMA expense_approvals TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA expense_approvals IS 'Expense claims routed for approval, the approver each was sent to and the decision taken, carried forward to payment. The approval is only worth anything if it is still attached to the claim when the payment is made.';

CREATE TABLE IF NOT EXISTS expense_approvals.expense_claim (
  claim_identifier            varchar(40) NOT NULL,
  worker_pseudonym_identifier varchar(40) NOT NULL,
  claim_submitted_timestamp   timestamptz NOT NULL,
  claim_total_amount          numeric(18,2) NOT NULL,
  claim_currency_code         varchar(3) NOT NULL,
  ledger_account_code         varchar(20) NOT NULL,
  claim_approver_identifier   varchar(40) NOT NULL,
  CONSTRAINT expense_claim_pk PRIMARY KEY (claim_identifier)
);
COMMENT ON TABLE expense_approvals.expense_claim IS 'One row per claim submitted for approval.';
COMMENT ON COLUMN expense_approvals.expense_claim.claim_identifier IS 'The unique identifier of the claim.';
COMMENT ON COLUMN expense_approvals.expense_claim.worker_pseudonym_identifier IS 'The claimant.';
COMMENT ON COLUMN expense_approvals.expense_claim.claim_submitted_timestamp IS 'When it was submitted.';
COMMENT ON COLUMN expense_approvals.expense_claim.claim_total_amount IS 'The value claimed.';
COMMENT ON COLUMN expense_approvals.expense_claim.claim_currency_code IS 'The currency.';
COMMENT ON COLUMN expense_approvals.expense_claim.ledger_account_code IS 'The cost coding.';
COMMENT ON COLUMN expense_approvals.expense_claim.claim_approver_identifier IS 'The approver it was routed to.';

CREATE TABLE IF NOT EXISTS expense_approvals.approval_decision (
  claim_identifier          varchar(40) NOT NULL,
  claim_approval_timestamp  timestamptz NOT NULL,
  claim_approver_identifier varchar(40) NOT NULL,
  claim_approval_status     varchar(20) NOT NULL,
  claim_approval_notes      text,
  CONSTRAINT approval_decision_pk PRIMARY KEY (claim_identifier, claim_approval_timestamp)
);
COMMENT ON TABLE expense_approvals.approval_decision IS 'One row per decision on a claim.';
COMMENT ON COLUMN expense_approvals.approval_decision.claim_identifier IS 'The claim.';
COMMENT ON COLUMN expense_approvals.approval_decision.claim_approval_timestamp IS 'When.';
COMMENT ON COLUMN expense_approvals.approval_decision.claim_approver_identifier IS 'Who decided.';
COMMENT ON COLUMN expense_approvals.approval_decision.claim_approval_status IS 'Approved, rejected or returned.';
COMMENT ON COLUMN expense_approvals.approval_decision.claim_approval_notes IS 'The approver''s comments.';

GRANT ALL ON ALL TABLES IN SCHEMA expense_approvals TO egeria_admin, egeria_user, airflow_user;

-- General Ledger Balances  (DigitalProduct::Coco::General Ledger Balances)
CREATE SCHEMA IF NOT EXISTS general_ledger_balances;
GRANT ALL ON SCHEMA general_ledger_balances TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA general_ledger_balances IS 'The general ledger of each legal entity: the transactions posted from every feed, adjustment and payment, and the account balances that result. It is the source of the entity trial balances that consolidation starts from and of the manual entries that review examines.';

CREATE TABLE IF NOT EXISTS general_ledger_balances.ledger_transaction (
  transaction_identifier       varchar(40) NOT NULL,
  legal_entity_code            varchar(10) NOT NULL,
  accounting_period_code       varchar(10) NOT NULL,
  ledger_account_code          varchar(20) NOT NULL,
  transaction_amount           numeric(18,2) NOT NULL,
  transaction_currency_code    varchar(3) NOT NULL,
  transaction_posted_timestamp timestamptz NOT NULL,
  feed_identifier              varchar(40),
  journal_entry_identifier     varchar(40),
  CONSTRAINT ledger_transaction_pk PRIMARY KEY (transaction_identifier)
);
COMMENT ON TABLE general_ledger_balances.ledger_transaction IS 'One row per transaction posted to the ledger.';
COMMENT ON COLUMN general_ledger_balances.ledger_transaction.transaction_identifier IS 'The unique identifier of the ledger transaction.';
COMMENT ON COLUMN general_ledger_balances.ledger_transaction.legal_entity_code IS 'The entity.';
COMMENT ON COLUMN general_ledger_balances.ledger_transaction.accounting_period_code IS 'The period.';
COMMENT ON COLUMN general_ledger_balances.ledger_transaction.ledger_account_code IS 'The account.';
COMMENT ON COLUMN general_ledger_balances.ledger_transaction.transaction_amount IS 'The amount.';
COMMENT ON COLUMN general_ledger_balances.ledger_transaction.transaction_currency_code IS 'The currency.';
COMMENT ON COLUMN general_ledger_balances.ledger_transaction.transaction_posted_timestamp IS 'When posted.';
COMMENT ON COLUMN general_ledger_balances.ledger_transaction.feed_identifier IS 'The feed batch it arrived in, if from a feed.';
COMMENT ON COLUMN general_ledger_balances.ledger_transaction.journal_entry_identifier IS 'The manual journal it arrived in, if manual.';

CREATE TABLE IF NOT EXISTS general_ledger_balances.ledger_account_balance (
  legal_entity_code             varchar(10) NOT NULL,
  accounting_period_code        varchar(10) NOT NULL,
  ledger_account_code           varchar(20) NOT NULL,
  ledger_account_name           varchar(120) NOT NULL,
  ledger_account_balance_amount numeric(18,2) NOT NULL,
  ledger_currency_code          varchar(3) NOT NULL,
  CONSTRAINT ledger_account_balance_pk PRIMARY KEY (legal_entity_code, accounting_period_code, ledger_account_code)
);
COMMENT ON TABLE general_ledger_balances.ledger_account_balance IS 'One row per account per entity per period.';
COMMENT ON COLUMN general_ledger_balances.ledger_account_balance.legal_entity_code IS 'The entity.';
COMMENT ON COLUMN general_ledger_balances.ledger_account_balance.accounting_period_code IS 'The period.';
COMMENT ON COLUMN general_ledger_balances.ledger_account_balance.ledger_account_code IS 'The account.';
COMMENT ON COLUMN general_ledger_balances.ledger_account_balance.ledger_account_name IS 'The account''s name.';
COMMENT ON COLUMN general_ledger_balances.ledger_account_balance.ledger_account_balance_amount IS 'The closing balance.';
COMMENT ON COLUMN general_ledger_balances.ledger_account_balance.ledger_currency_code IS 'The currency.';

GRANT ALL ON ALL TABLES IN SCHEMA general_ledger_balances TO egeria_admin, egeria_user, airflow_user;

-- Employee Expense Claims  (DigitalProduct::Coco::Employee Expense Claims)
CREATE SCHEMA IF NOT EXISTS employee_expense_claims;
GRANT ALL ON SCHEMA employee_expense_claims TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA employee_expense_claims IS 'The claims employees submit for expenses incurred, line by line with their supporting evidence, and the record of which workers may claim against which cost centres. It is the entry point of the expense payment chain and a source of transfers of value that disclosure must catch.';

CREATE TABLE IF NOT EXISTS employee_expense_claims.claim_submission (
  claim_identifier            varchar(40) NOT NULL,
  worker_pseudonym_identifier varchar(40) NOT NULL,
  claim_submitted_timestamp   timestamptz NOT NULL,
  claim_total_amount          numeric(18,2) NOT NULL,
  claim_currency_code         varchar(3) NOT NULL,
  claim_current_status        varchar(20) NOT NULL,
  CONSTRAINT claim_submission_pk PRIMARY KEY (claim_identifier)
);
COMMENT ON TABLE employee_expense_claims.claim_submission IS 'One row per claim as submitted by the claimant.';
COMMENT ON COLUMN employee_expense_claims.claim_submission.claim_identifier IS 'The unique identifier of the claim.';
COMMENT ON COLUMN employee_expense_claims.claim_submission.worker_pseudonym_identifier IS 'The claimant.';
COMMENT ON COLUMN employee_expense_claims.claim_submission.claim_submitted_timestamp IS 'When submitted.';
COMMENT ON COLUMN employee_expense_claims.claim_submission.claim_total_amount IS 'The total claimed.';
COMMENT ON COLUMN employee_expense_claims.claim_submission.claim_currency_code IS 'The currency.';
COMMENT ON COLUMN employee_expense_claims.claim_submission.claim_current_status IS 'Draft, submitted, approved, paid or rejected.';

CREATE TABLE IF NOT EXISTS employee_expense_claims.claim_line (
  claim_identifier                varchar(40) NOT NULL,
  claim_line_number               integer NOT NULL,
  claim_line_type                 varchar(40) NOT NULL,
  claim_line_date                 date NOT NULL,
  claim_line_amount               numeric(18,2) NOT NULL,
  claim_line_description          text NOT NULL,
  claim_line_recipient_identifier varchar(40),
  claim_line_evidence_identifier  varchar(60),
  CONSTRAINT claim_line_pk PRIMARY KEY (claim_identifier, claim_line_number)
);
COMMENT ON TABLE employee_expense_claims.claim_line IS 'One row per expense within a claim.';
COMMENT ON COLUMN employee_expense_claims.claim_line.claim_identifier IS 'The claim.';
COMMENT ON COLUMN employee_expense_claims.claim_line.claim_line_number IS 'The position of the line in the claim.';
COMMENT ON COLUMN employee_expense_claims.claim_line.claim_line_type IS 'Travel, hospitality, accommodation or other.';
COMMENT ON COLUMN employee_expense_claims.claim_line.claim_line_date IS 'When the expense was incurred.';
COMMENT ON COLUMN employee_expense_claims.claim_line.claim_line_amount IS 'The amount.';
COMMENT ON COLUMN employee_expense_claims.claim_line.claim_line_description IS 'What the expense was for.';
COMMENT ON COLUMN employee_expense_claims.claim_line.claim_line_recipient_identifier IS 'The healthcare professional entertained, if any.';
COMMENT ON COLUMN employee_expense_claims.claim_line.claim_line_evidence_identifier IS 'The receipt or other evidence attached.';

CREATE TABLE IF NOT EXISTS employee_expense_claims.claimant_cost_centre (
  worker_pseudonym_identifier varchar(40) NOT NULL,
  cost_centre_code            varchar(20) NOT NULL,
  claim_approver_identifier   varchar(40) NOT NULL,
  claim_maximum_amount        numeric(18,2),
  CONSTRAINT claimant_cost_centre_pk PRIMARY KEY (worker_pseudonym_identifier, cost_centre_code)
);
COMMENT ON TABLE employee_expense_claims.claimant_cost_centre IS 'One row per worker per cost centre they may claim against, with the approver and spending authority.';
COMMENT ON COLUMN employee_expense_claims.claimant_cost_centre.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN employee_expense_claims.claimant_cost_centre.cost_centre_code IS 'The cost centre.';
COMMENT ON COLUMN employee_expense_claims.claimant_cost_centre.claim_approver_identifier IS 'The approver for the worker''s claims.';
COMMENT ON COLUMN employee_expense_claims.claimant_cost_centre.claim_maximum_amount IS 'The spending authority applying to the worker.';

GRANT ALL ON ALL TABLES IN SCHEMA employee_expense_claims TO egeria_admin, egeria_user, airflow_user;

-- ================================================================================================
-- people-systems.md
-- ================================================================================================

-- Worker Master Data  (DigitalProduct::Coco::Worker Master Data)
CREATE SCHEMA IF NOT EXISTS worker_master_data;
GRANT ALL ON SCHEMA worker_master_data TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA worker_master_data IS 'The authoritative record of every worker, employees and contractors alike, and the assignment of each to a role, an entity, a cost centre and a reporting line. It is the anchor that qualification, health surveillance, access and payroll records are all held against.';

CREATE TABLE IF NOT EXISTS worker_master_data.worker (
  worker_pseudonym_identifier varchar(40) NOT NULL,
  worker_type                 varchar(20) NOT NULL,
  legal_entity_code           varchar(10) NOT NULL,
  site_code                   varchar(20) NOT NULL,
  worker_hire_date            date NOT NULL,
  worker_leave_date           date,
  worker_current_status       varchar(20) NOT NULL,
  CONSTRAINT worker_pk PRIMARY KEY (worker_pseudonym_identifier)
);
COMMENT ON TABLE worker_master_data.worker IS 'One row per worker, identified by pseudonym to every consuming system.';
COMMENT ON COLUMN worker_master_data.worker.worker_pseudonym_identifier IS 'The worker''s pseudonym.';
COMMENT ON COLUMN worker_master_data.worker.worker_type IS 'Employee or contractor.';
COMMENT ON COLUMN worker_master_data.worker.legal_entity_code IS 'The employing entity.';
COMMENT ON COLUMN worker_master_data.worker.site_code IS 'The primary site.';
COMMENT ON COLUMN worker_master_data.worker.worker_hire_date IS 'When the worker joined.';
COMMENT ON COLUMN worker_master_data.worker.worker_leave_date IS 'When they left, once they have.';
COMMENT ON COLUMN worker_master_data.worker.worker_current_status IS 'Active, on leave, left.';

CREATE TABLE IF NOT EXISTS worker_master_data.worker_assignment (
  worker_pseudonym_identifier       varchar(40) NOT NULL,
  role_code                         varchar(40) NOT NULL,
  role_name                         varchar(120) NOT NULL,
  cost_centre_code                  varchar(20) NOT NULL,
  manager_pseudonym_identifier      varchar(40),
  worker_assignment_start_date      date NOT NULL,
  worker_spending_maximum_amount    numeric(18,2),
  worker_hazard_profile_description text,
  CONSTRAINT worker_assignment_pk PRIMARY KEY (worker_pseudonym_identifier)
);
COMMENT ON TABLE worker_master_data.worker_assignment IS 'One row per worker, their current role, cost centre and reporting line.';
COMMENT ON COLUMN worker_master_data.worker_assignment.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN worker_master_data.worker_assignment.role_code IS 'The role.';
COMMENT ON COLUMN worker_master_data.worker_assignment.role_name IS 'The role''s name.';
COMMENT ON COLUMN worker_master_data.worker_assignment.cost_centre_code IS 'The cost centre.';
COMMENT ON COLUMN worker_master_data.worker_assignment.manager_pseudonym_identifier IS 'The reporting manager.';
COMMENT ON COLUMN worker_master_data.worker_assignment.worker_assignment_start_date IS 'When the assignment began.';
COMMENT ON COLUMN worker_master_data.worker_assignment.worker_spending_maximum_amount IS 'The worker''s spending authority.';
COMMENT ON COLUMN worker_master_data.worker_assignment.worker_hazard_profile_description IS 'The substances and tasks the role exposes the worker to.';

GRANT ALL ON ALL TABLES IN SCHEMA worker_master_data TO egeria_admin, egeria_user, airflow_user;

-- Worker Lifecycle Events  (DigitalProduct::Coco::Worker Lifecycle Events)
CREATE SCHEMA IF NOT EXISTS worker_lifecycle_events;
GRANT ALL ON SCHEMA worker_lifecycle_events TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA worker_lifecycle_events IS 'Every joining, moving or leaving event, distributed to each system that must act on it, and the record of which have. The leaver case is the one that matters: access outlives employment by exactly this chain''s delay.';

CREATE TABLE IF NOT EXISTS worker_lifecycle_events.worker_event (
  worker_event_identifier       varchar(40) NOT NULL,
  worker_pseudonym_identifier   varchar(40) NOT NULL,
  worker_event_type             varchar(10) NOT NULL,
  worker_event_start_date       date NOT NULL,
  worker_event_raised_timestamp timestamptz NOT NULL,
  role_code                     varchar(40),
  worker_event_description      text NOT NULL,
  CONSTRAINT worker_event_pk PRIMARY KEY (worker_event_identifier)
);
COMMENT ON TABLE worker_lifecycle_events.worker_event IS 'One row per joiner, mover or leaver event.';
COMMENT ON COLUMN worker_lifecycle_events.worker_event.worker_event_identifier IS 'The event.';
COMMENT ON COLUMN worker_lifecycle_events.worker_event.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN worker_lifecycle_events.worker_event.worker_event_type IS 'Joiner, mover or leaver.';
COMMENT ON COLUMN worker_lifecycle_events.worker_event.worker_event_start_date IS 'The effective date.';
COMMENT ON COLUMN worker_lifecycle_events.worker_event.worker_event_raised_timestamp IS 'When the event was raised.';
COMMENT ON COLUMN worker_lifecycle_events.worker_event.role_code IS 'The new role, for a joiner or mover.';
COMMENT ON COLUMN worker_lifecycle_events.worker_event.worker_event_description IS 'The change.';

CREATE TABLE IF NOT EXISTS worker_lifecycle_events.event_distribution_status (
  worker_event_identifier        varchar(40) NOT NULL,
  system_identifier              varchar(60) NOT NULL,
  worker_event_sent_timestamp    timestamptz NOT NULL,
  worker_event_applied_flag      boolean NOT NULL,
  worker_event_applied_timestamp timestamptz,
  CONSTRAINT event_distribution_status_pk PRIMARY KEY (worker_event_identifier, system_identifier)
);
COMMENT ON TABLE worker_lifecycle_events.event_distribution_status IS 'One row per event per consuming system.';
COMMENT ON COLUMN worker_lifecycle_events.event_distribution_status.worker_event_identifier IS 'The event.';
COMMENT ON COLUMN worker_lifecycle_events.event_distribution_status.system_identifier IS 'The system notified.';
COMMENT ON COLUMN worker_lifecycle_events.event_distribution_status.worker_event_sent_timestamp IS 'When notified.';
COMMENT ON COLUMN worker_lifecycle_events.event_distribution_status.worker_event_applied_flag IS 'Whether the system has confirmed acting on it.';
COMMENT ON COLUMN worker_lifecycle_events.event_distribution_status.worker_event_applied_timestamp IS 'When confirmed.';

GRANT ALL ON ALL TABLES IN SCHEMA worker_lifecycle_events TO egeria_admin, egeria_user, airflow_user;

-- Access Entitlements  (DigitalProduct::Coco::Access Entitlements)
CREATE SCHEMA IF NOT EXISTS access_entitlements;
GRANT ALL ON SCHEMA access_entitlements TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA access_entitlements IS 'The accounts and entitlements created, changed and removed for each worker in response to worker events, and the data ownership assignments recorded in the open metadata catalogue. It is driven from the worker record rather than from requests, because an access removal that depends on somebody remembering to ask does not happen.';

CREATE TABLE IF NOT EXISTS access_entitlements.account (
  user_account_identifier     varchar(60) NOT NULL,
  worker_pseudonym_identifier varchar(40) NOT NULL,
  system_identifier           varchar(60) NOT NULL,
  user_account_start_date     date NOT NULL,
  user_account_end_date       date,
  user_account_current_status varchar(20) NOT NULL,
  worker_event_identifier     varchar(40) NOT NULL,
  CONSTRAINT account_pk PRIMARY KEY (user_account_identifier)
);
COMMENT ON TABLE access_entitlements.account IS 'One row per account held by a worker in a system.';
COMMENT ON COLUMN access_entitlements.account.user_account_identifier IS 'The account.';
COMMENT ON COLUMN access_entitlements.account.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN access_entitlements.account.system_identifier IS 'The system.';
COMMENT ON COLUMN access_entitlements.account.user_account_start_date IS 'When created.';
COMMENT ON COLUMN access_entitlements.account.user_account_end_date IS 'When removed, once removed.';
COMMENT ON COLUMN access_entitlements.account.user_account_current_status IS 'Active, suspended, removed.';
COMMENT ON COLUMN access_entitlements.account.worker_event_identifier IS 'The worker event that last changed it.';

CREATE TABLE IF NOT EXISTS access_entitlements.entitlement (
  user_account_identifier     varchar(60) NOT NULL,
  entitlement_code            varchar(60) NOT NULL,
  entitlement_description     text NOT NULL,
  entitlement_start_date      date NOT NULL,
  entitlement_end_date        date,
  entitlement_data_owner_flag boolean NOT NULL,
  CONSTRAINT entitlement_pk PRIMARY KEY (user_account_identifier, entitlement_code)
);
COMMENT ON TABLE access_entitlements.entitlement IS 'One row per entitlement granted to an account.';
COMMENT ON COLUMN access_entitlements.entitlement.user_account_identifier IS 'The account.';
COMMENT ON COLUMN access_entitlements.entitlement.entitlement_code IS 'The entitlement.';
COMMENT ON COLUMN access_entitlements.entitlement.entitlement_description IS 'What it permits.';
COMMENT ON COLUMN access_entitlements.entitlement.entitlement_start_date IS 'When granted.';
COMMENT ON COLUMN access_entitlements.entitlement.entitlement_end_date IS 'When revoked, once revoked.';
COMMENT ON COLUMN access_entitlements.entitlement.entitlement_data_owner_flag IS 'Whether the entitlement makes the worker a data owner in the catalogue.';

GRANT ALL ON ALL TABLES IN SCHEMA access_entitlements TO egeria_admin, egeria_user, airflow_user;

-- Payroll Results  (DigitalProduct::Coco::Payroll Results)
CREATE SCHEMA IF NOT EXISTS payroll_results;
GRANT ALL ON SCHEMA payroll_results TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA payroll_results IS 'The remuneration calculated and paid in each payroll run, in several countries under several sets of rules from one worker record, and the postings to the ledger by entity. It is the pay data that statutory reporting and pay equity analysis are built from.';

CREATE TABLE IF NOT EXISTS payroll_results.payroll_run (
  payroll_run_identifier   varchar(40) NOT NULL,
  legal_entity_code        varchar(10) NOT NULL,
  payroll_period_code      varchar(10) NOT NULL,
  payroll_run_date         date NOT NULL,
  payroll_run_count        integer NOT NULL,
  payroll_run_total_amount numeric(18,2) NOT NULL,
  payroll_currency_code    varchar(3) NOT NULL,
  CONSTRAINT payroll_run_pk PRIMARY KEY (payroll_run_identifier)
);
COMMENT ON TABLE payroll_results.payroll_run IS 'One row per payroll run.';
COMMENT ON COLUMN payroll_results.payroll_run.payroll_run_identifier IS 'The run.';
COMMENT ON COLUMN payroll_results.payroll_run.legal_entity_code IS 'The entity paid.';
COMMENT ON COLUMN payroll_results.payroll_run.payroll_period_code IS 'The pay period.';
COMMENT ON COLUMN payroll_results.payroll_run.payroll_run_date IS 'When run.';
COMMENT ON COLUMN payroll_results.payroll_run.payroll_run_count IS 'The number of workers paid.';
COMMENT ON COLUMN payroll_results.payroll_run.payroll_run_total_amount IS 'The total remuneration.';
COMMENT ON COLUMN payroll_results.payroll_run.payroll_currency_code IS 'The currency.';

CREATE TABLE IF NOT EXISTS payroll_results.payroll_posting (
  payroll_run_identifier      varchar(40) NOT NULL,
  worker_pseudonym_identifier varchar(40) NOT NULL,
  payroll_gross_amount        numeric(18,2) NOT NULL,
  payroll_employer_amount     numeric(18,2) NOT NULL,
  payroll_net_amount          numeric(18,2) NOT NULL,
  cost_centre_code            varchar(20) NOT NULL,
  ledger_account_code         varchar(20) NOT NULL,
  CONSTRAINT payroll_posting_pk PRIMARY KEY (payroll_run_identifier, worker_pseudonym_identifier)
);
COMMENT ON TABLE payroll_results.payroll_posting IS 'One row per worker per run, the remuneration and employer costs.';
COMMENT ON COLUMN payroll_results.payroll_posting.payroll_run_identifier IS 'The run.';
COMMENT ON COLUMN payroll_results.payroll_posting.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN payroll_results.payroll_posting.payroll_gross_amount IS 'Gross remuneration.';
COMMENT ON COLUMN payroll_results.payroll_posting.payroll_employer_amount IS 'Employer costs.';
COMMENT ON COLUMN payroll_results.payroll_posting.payroll_net_amount IS 'Net paid.';
COMMENT ON COLUMN payroll_results.payroll_posting.cost_centre_code IS 'The cost centre charged.';
COMMENT ON COLUMN payroll_results.payroll_posting.ledger_account_code IS 'The account posted to.';

GRANT ALL ON ALL TABLES IN SCHEMA payroll_results TO egeria_admin, egeria_user, airflow_user;

-- Corporate Directory Entries  (DigitalProduct::Coco::Corporate Directory Entries)
CREATE SCHEMA IF NOT EXISTS corporate_directory_entries;
GRANT ALL ON SCHEMA corporate_directory_entries TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA corporate_directory_entries IS 'The searchable directory of people, roles, locations and reporting lines that the rest of the organisation uses. It is downstream of the worker record and is frequently the first place a stale joiner or leaver event becomes visible to everybody.';

CREATE TABLE IF NOT EXISTS corporate_directory_entries.directory_entry (
  worker_pseudonym_identifier       varchar(40) NOT NULL,
  person_first_name                 varchar(80) NOT NULL,
  person_last_name                  varchar(80) NOT NULL,
  role_name                         varchar(120) NOT NULL,
  department_name                   varchar(120) NOT NULL,
  site_code                         varchar(20) NOT NULL,
  manager_pseudonym_identifier      varchar(40),
  person_work_phone_number          varchar(30),
  directory_entry_current_timestamp timestamptz NOT NULL,
  CONSTRAINT directory_entry_pk PRIMARY KEY (worker_pseudonym_identifier)
);
COMMENT ON TABLE corporate_directory_entries.directory_entry IS 'One row per worker in the directory.';
COMMENT ON COLUMN corporate_directory_entries.directory_entry.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN corporate_directory_entries.directory_entry.person_first_name IS 'Given name.';
COMMENT ON COLUMN corporate_directory_entries.directory_entry.person_last_name IS 'Family name.';
COMMENT ON COLUMN corporate_directory_entries.directory_entry.role_name IS 'The role.';
COMMENT ON COLUMN corporate_directory_entries.directory_entry.department_name IS 'The department.';
COMMENT ON COLUMN corporate_directory_entries.directory_entry.site_code IS 'The location.';
COMMENT ON COLUMN corporate_directory_entries.directory_entry.manager_pseudonym_identifier IS 'The reporting manager.';
COMMENT ON COLUMN corporate_directory_entries.directory_entry.person_work_phone_number IS 'Work telephone.';
COMMENT ON COLUMN corporate_directory_entries.directory_entry.directory_entry_current_timestamp IS 'When the entry was last updated from the worker record.';

GRANT ALL ON ALL TABLES IN SCHEMA corporate_directory_entries TO egeria_admin, egeria_user, airflow_user;

-- Role Competency Requirements  (DigitalProduct::Coco::Role Competency Requirements)
CREATE SCHEMA IF NOT EXISTS role_competency_requirements;
GRANT ALL ON SCHEMA role_competency_requirements TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA role_competency_requirements IS 'What competencies each regulated role requires and how often each must be refreshed. It is the specification the competency chain is judged against, and it changes when a process or a regulation changes rather than when a person does.';

CREATE TABLE IF NOT EXISTS role_competency_requirements.role_competency_requirement (
  role_code                   varchar(40) NOT NULL,
  competency_code             varchar(40) NOT NULL,
  competency_name             varchar(120) NOT NULL,
  competency_description      text NOT NULL,
  competency_refresh_duration integer NOT NULL,
  competency_regulated_flag   boolean NOT NULL,
  role_requirement_start_date date NOT NULL,
  CONSTRAINT role_competency_requirement_pk PRIMARY KEY (role_code, competency_code)
);
COMMENT ON TABLE role_competency_requirements.role_competency_requirement IS 'One row per role per competency required.';
COMMENT ON COLUMN role_competency_requirements.role_competency_requirement.role_code IS 'The role.';
COMMENT ON COLUMN role_competency_requirements.role_competency_requirement.competency_code IS 'The competency.';
COMMENT ON COLUMN role_competency_requirements.role_competency_requirement.competency_name IS 'Its name.';
COMMENT ON COLUMN role_competency_requirements.role_competency_requirement.competency_description IS 'What the competency covers.';
COMMENT ON COLUMN role_competency_requirements.role_competency_requirement.competency_refresh_duration IS 'How often it must be refreshed, in months.';
COMMENT ON COLUMN role_competency_requirements.role_competency_requirement.competency_regulated_flag IS 'Whether a regulation requires it.';
COMMENT ON COLUMN role_competency_requirements.role_competency_requirement.role_requirement_start_date IS 'When the requirement took effect.';

GRANT ALL ON ALL TABLES IN SCHEMA role_competency_requirements TO egeria_admin, egeria_user, airflow_user;

-- Training Completions  (DigitalProduct::Coco::Training Completions)
CREATE SCHEMA IF NOT EXISTS training_completions;
GRANT ALL ON SCHEMA training_completions TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA training_completions IS 'Training delivered, completion and assessment recorded, and refreshers scheduled for lapsing qualifications. Its output is evidence consumed by two regulated processes, which is a heavier duty than the system was originally bought for.';

CREATE TABLE IF NOT EXISTS training_completions.training_completion (
  training_completion_identifier varchar(40) NOT NULL,
  worker_pseudonym_identifier    varchar(40) NOT NULL,
  training_course_code           varchar(40) NOT NULL,
  competency_code                varchar(40) NOT NULL,
  training_completed_date        date NOT NULL,
  training_expiry_date           date,
  CONSTRAINT training_completion_pk PRIMARY KEY (training_completion_identifier)
);
COMMENT ON TABLE training_completions.training_completion IS 'One row per worker per training course completed.';
COMMENT ON COLUMN training_completions.training_completion.training_completion_identifier IS 'The completion.';
COMMENT ON COLUMN training_completions.training_completion.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN training_completions.training_completion.training_course_code IS 'The course.';
COMMENT ON COLUMN training_completions.training_completion.competency_code IS 'The competency the course evidences.';
COMMENT ON COLUMN training_completions.training_completion.training_completed_date IS 'When completed.';
COMMENT ON COLUMN training_completions.training_completion.training_expiry_date IS 'When the training lapses.';

CREATE TABLE IF NOT EXISTS training_completions.assessment_result (
  training_completion_identifier    varchar(40) NOT NULL,
  training_assessment_date          date NOT NULL,
  training_assessment_value         double precision NOT NULL,
  training_assessment_minimum_value double precision NOT NULL,
  training_assessment_passed_flag   boolean NOT NULL,
  CONSTRAINT assessment_result_pk PRIMARY KEY (training_completion_identifier, training_assessment_date)
);
COMMENT ON TABLE training_completions.assessment_result IS 'One row per assessment taken.';
COMMENT ON COLUMN training_completions.assessment_result.training_completion_identifier IS 'The completion assessed.';
COMMENT ON COLUMN training_completions.assessment_result.training_assessment_date IS 'When assessed.';
COMMENT ON COLUMN training_completions.assessment_result.training_assessment_value IS 'The score.';
COMMENT ON COLUMN training_completions.assessment_result.training_assessment_minimum_value IS 'The pass mark.';
COMMENT ON COLUMN training_completions.assessment_result.training_assessment_passed_flag IS 'Whether the worker passed.';

CREATE TABLE IF NOT EXISTS training_completions.refresher_schedule (
  worker_pseudonym_identifier varchar(40) NOT NULL,
  competency_code             varchar(40) NOT NULL,
  training_due_date           date NOT NULL,
  training_course_code        varchar(40) NOT NULL,
  training_scheduled_date     date,
  CONSTRAINT refresher_schedule_pk PRIMARY KEY (worker_pseudonym_identifier, competency_code, training_due_date)
);
COMMENT ON TABLE training_completions.refresher_schedule IS 'One row per refresher scheduled for a lapsing qualification.';
COMMENT ON COLUMN training_completions.refresher_schedule.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN training_completions.refresher_schedule.competency_code IS 'The competency lapsing.';
COMMENT ON COLUMN training_completions.refresher_schedule.training_due_date IS 'When it must be completed.';
COMMENT ON COLUMN training_completions.refresher_schedule.training_course_code IS 'The refresher course.';
COMMENT ON COLUMN training_completions.refresher_schedule.training_scheduled_date IS 'When it is scheduled.';

GRANT ALL ON ALL TABLES IN SCHEMA training_completions TO egeria_admin, egeria_user, airflow_user;

-- Worker Qualifications  (DigitalProduct::Coco::Worker Qualifications)
CREATE SCHEMA IF NOT EXISTS worker_qualifications;
GRANT ALL ON SCHEMA worker_qualifications TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA worker_qualifications IS 'The authoritative statement of what each worker is currently qualified to do, with the evidence and the expiry, read by manufacturing, shipping, drug development and the batch record as compliance evidence. A local copy that has drifted is worse than no copy at all.';

CREATE TABLE IF NOT EXISTS worker_qualifications.worker_qualification (
  worker_pseudonym_identifier    varchar(40) NOT NULL,
  competency_code                varchar(40) NOT NULL,
  competency_name                varchar(120) NOT NULL,
  qualification_start_date       date NOT NULL,
  qualification_expiry_date      date NOT NULL,
  qualification_current_status   varchar(20) NOT NULL,
  training_completion_identifier varchar(40) NOT NULL,
  certificate_identifier         varchar(40),
  role_code                      varchar(40) NOT NULL,
  CONSTRAINT worker_qualification_pk PRIMARY KEY (worker_pseudonym_identifier, competency_code)
);
COMMENT ON TABLE worker_qualifications.worker_qualification IS 'One row per worker per competency held.';
COMMENT ON COLUMN worker_qualifications.worker_qualification.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN worker_qualifications.worker_qualification.competency_code IS 'The competency.';
COMMENT ON COLUMN worker_qualifications.worker_qualification.competency_name IS 'Its name.';
COMMENT ON COLUMN worker_qualifications.worker_qualification.qualification_start_date IS 'When gained.';
COMMENT ON COLUMN worker_qualifications.worker_qualification.qualification_expiry_date IS 'When it lapses.';
COMMENT ON COLUMN worker_qualifications.worker_qualification.qualification_current_status IS 'Current, lapsing, lapsed.';
COMMENT ON COLUMN worker_qualifications.worker_qualification.training_completion_identifier IS 'The training completion that evidences it.';
COMMENT ON COLUMN worker_qualifications.worker_qualification.certificate_identifier IS 'The external certificate, where one exists.';
COMMENT ON COLUMN worker_qualifications.worker_qualification.role_code IS 'The role the qualification was gained for.';

GRANT ALL ON ALL TABLES IN SCHEMA worker_qualifications TO egeria_admin, egeria_user, airflow_user;

-- Qualification Expiry Warnings  (DigitalProduct::Coco::Qualification Expiry Warnings)
CREATE SCHEMA IF NOT EXISTS qualification_expiry_warnings;
GRANT ALL ON SCHEMA qualification_expiry_warnings TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA qualification_expiry_warnings IS 'Warnings raised for qualifications approaching or past expiry, sent to the processes that depend on them before rather than after. Currency is the property the competency chain is actually judged on.';

CREATE TABLE IF NOT EXISTS qualification_expiry_warnings.qualification_expiry_warning (
  qualification_warning_identifier       varchar(40) NOT NULL,
  worker_pseudonym_identifier            varchar(40) NOT NULL,
  competency_code                        varchar(40) NOT NULL,
  qualification_expiry_date              date NOT NULL,
  qualification_warning_raised_timestamp timestamptz NOT NULL,
  qualification_warning_type             varchar(20) NOT NULL,
  training_due_date                      date NOT NULL,
  CONSTRAINT qualification_expiry_warning_pk PRIMARY KEY (qualification_warning_identifier)
);
COMMENT ON TABLE qualification_expiry_warnings.qualification_expiry_warning IS 'One row per warning raised.';
COMMENT ON COLUMN qualification_expiry_warnings.qualification_expiry_warning.qualification_warning_identifier IS 'The warning.';
COMMENT ON COLUMN qualification_expiry_warnings.qualification_expiry_warning.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN qualification_expiry_warnings.qualification_expiry_warning.competency_code IS 'The competency.';
COMMENT ON COLUMN qualification_expiry_warnings.qualification_expiry_warning.qualification_expiry_date IS 'When it lapses.';
COMMENT ON COLUMN qualification_expiry_warnings.qualification_expiry_warning.qualification_warning_raised_timestamp IS 'When the warning was raised.';
COMMENT ON COLUMN qualification_expiry_warnings.qualification_expiry_warning.qualification_warning_type IS 'Approaching expiry or expired.';
COMMENT ON COLUMN qualification_expiry_warnings.qualification_expiry_warning.training_due_date IS 'The deadline set for the refresher.';

GRANT ALL ON ALL TABLES IN SCHEMA qualification_expiry_warnings TO egeria_admin, egeria_user, airflow_user;

-- Health Surveillance Records  (DigitalProduct::Coco::Health Surveillance Records)
CREATE SCHEMA IF NOT EXISTS health_surveillance_records;
GRANT ALL ON SCHEMA health_surveillance_records TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA health_surveillance_records IS 'The enrolment of each worker in health surveillance according to their exposure profile, and the results of surveillance appointments, exposure measurements and exposure incidents held against the individual. The record belongs to the person it describes rather than to the company.';

CREATE TABLE IF NOT EXISTS health_surveillance_records.surveillance_enrolment (
  worker_pseudonym_identifier       varchar(40) NOT NULL,
  surveillance_enrollment_date      date NOT NULL,
  role_code                         varchar(40) NOT NULL,
  worker_hazard_profile_description text NOT NULL,
  surveillance_frequency            integer NOT NULL,
  surveillance_current_status       varchar(20) NOT NULL,
  CONSTRAINT surveillance_enrolment_pk PRIMARY KEY (worker_pseudonym_identifier)
);
COMMENT ON TABLE health_surveillance_records.surveillance_enrolment IS 'One row per worker enrolled in surveillance.';
COMMENT ON COLUMN health_surveillance_records.surveillance_enrolment.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN health_surveillance_records.surveillance_enrolment.surveillance_enrollment_date IS 'When enrolled.';
COMMENT ON COLUMN health_surveillance_records.surveillance_enrolment.role_code IS 'The role that required enrolment.';
COMMENT ON COLUMN health_surveillance_records.surveillance_enrolment.worker_hazard_profile_description IS 'The exposure profile enrolment was based on.';
COMMENT ON COLUMN health_surveillance_records.surveillance_enrolment.surveillance_frequency IS 'How often appointments are due, in months.';
COMMENT ON COLUMN health_surveillance_records.surveillance_enrolment.surveillance_current_status IS 'Enrolled, lapsed, ended.';

CREATE TABLE IF NOT EXISTS health_surveillance_records.surveillance_result (
  surveillance_result_identifier         varchar(40) NOT NULL,
  worker_pseudonym_identifier            varchar(40) NOT NULL,
  surveillance_result_type               varchar(20) NOT NULL,
  surveillance_result_date               date NOT NULL,
  exposure_reading_identifier            varchar(40),
  incident_identifier                    varchar(40),
  surveillance_result_description        text NOT NULL,
  surveillance_result_action_description text,
  CONSTRAINT surveillance_result_pk PRIMARY KEY (surveillance_result_identifier)
);
COMMENT ON TABLE health_surveillance_records.surveillance_result IS 'One row per surveillance appointment, measurement or incident recorded against a worker.';
COMMENT ON COLUMN health_surveillance_records.surveillance_result.surveillance_result_identifier IS 'The record.';
COMMENT ON COLUMN health_surveillance_records.surveillance_result.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN health_surveillance_records.surveillance_result.surveillance_result_type IS 'Appointment, exposure measurement or exposure incident.';
COMMENT ON COLUMN health_surveillance_records.surveillance_result.surveillance_result_date IS 'When.';
COMMENT ON COLUMN health_surveillance_records.surveillance_result.exposure_reading_identifier IS 'The measurement, for a measurement.';
COMMENT ON COLUMN health_surveillance_records.surveillance_result.incident_identifier IS 'The incident, for an incident.';
COMMENT ON COLUMN health_surveillance_records.surveillance_result.surveillance_result_description IS 'The finding.';
COMMENT ON COLUMN health_surveillance_records.surveillance_result.surveillance_result_action_description IS 'Any action required.';

GRANT ALL ON ALL TABLES IN SCHEMA health_surveillance_records TO egeria_admin, egeria_user, airflow_user;

-- Long Term Health Archive  (DigitalProduct::Coco::Long Term Health Archive)
CREATE SCHEMA IF NOT EXISTS long_term_health_archive;
GRANT ALL ON SCHEMA long_term_health_archive TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA long_term_health_archive IS 'Health surveillance and exposure records retained for forty years from the last entry, across every system migration in that period. Its requirement is not storage but interpretability: a record that survives and can no longer be read is the same failure as one that was lost.';

CREATE TABLE IF NOT EXISTS long_term_health_archive.archived_health_record (
  health_record_identifier       varchar(40) NOT NULL,
  worker_pseudonym_identifier    varchar(40) NOT NULL,
  surveillance_result_identifier varchar(40) NOT NULL,
  health_record_archived_date    date NOT NULL,
  health_record_format_code      varchar(20) NOT NULL,
  health_record_archive_end_date date NOT NULL,
  health_record_readable_flag    boolean NOT NULL,
  CONSTRAINT archived_health_record_pk PRIMARY KEY (health_record_identifier)
);
COMMENT ON TABLE long_term_health_archive.archived_health_record IS 'One row per record archived.';
COMMENT ON COLUMN long_term_health_archive.archived_health_record.health_record_identifier IS 'The archived record.';
COMMENT ON COLUMN long_term_health_archive.archived_health_record.worker_pseudonym_identifier IS 'The worker.';
COMMENT ON COLUMN long_term_health_archive.archived_health_record.surveillance_result_identifier IS 'The surveillance record archived.';
COMMENT ON COLUMN long_term_health_archive.archived_health_record.health_record_archived_date IS 'When archived.';
COMMENT ON COLUMN long_term_health_archive.archived_health_record.health_record_format_code IS 'The format the record is held in.';
COMMENT ON COLUMN long_term_health_archive.archived_health_record.health_record_archive_end_date IS 'When retention ends.';
COMMENT ON COLUMN long_term_health_archive.archived_health_record.health_record_readable_flag IS 'Whether the record was readable at the last verification.';

GRANT ALL ON ALL TABLES IN SCHEMA long_term_health_archive TO egeria_admin, egeria_user, airflow_user;

-- ================================================================================================
-- privacy-operations.md
-- ================================================================================================

-- Data Subject Rights Requests  (DigitalProduct::Coco::Data Subject Rights Requests)
CREATE SCHEMA IF NOT EXISTS data_subject_rights_requests;
GRANT ALL ON SCHEMA data_subject_rights_requests TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA data_subject_rights_requests IS 'Requests from data subjects received through every channel the company offers, with the statutory clock that starts on receipt, and the response assembled for each. An email to a site address counts exactly as much as a submission through the portal.';

CREATE TABLE IF NOT EXISTS data_subject_rights_requests.rights_request (
  rights_request_identifier         varchar(40) NOT NULL,
  rights_request_received_timestamp timestamptz NOT NULL,
  rights_request_channel_type       varchar(20) NOT NULL,
  rights_request_type               varchar(20) NOT NULL,
  data_subject_type                 varchar(20) NOT NULL,
  data_subject_claimed_name         varchar(200) NOT NULL,
  rights_request_description        text NOT NULL,
  rights_request_due_date           date NOT NULL,
  rights_request_current_status     varchar(20) NOT NULL,
  CONSTRAINT rights_request_pk PRIMARY KEY (rights_request_identifier)
);
COMMENT ON TABLE data_subject_rights_requests.rights_request IS 'One row per request received.';
COMMENT ON COLUMN data_subject_rights_requests.rights_request.rights_request_identifier IS 'The request.';
COMMENT ON COLUMN data_subject_rights_requests.rights_request.rights_request_received_timestamp IS 'When first received anywhere in the company.';
COMMENT ON COLUMN data_subject_rights_requests.rights_request.rights_request_channel_type IS 'Portal, email, letter, telephone or other.';
COMMENT ON COLUMN data_subject_rights_requests.rights_request.rights_request_type IS 'Access, rectification, erasure, objection, portability or restriction.';
COMMENT ON COLUMN data_subject_rights_requests.rights_request.data_subject_type IS 'Patient, worker, healthcare professional, other.';
COMMENT ON COLUMN data_subject_rights_requests.rights_request.data_subject_claimed_name IS 'The name the requester gave.';
COMMENT ON COLUMN data_subject_rights_requests.rights_request.rights_request_description IS 'What was asked for.';
COMMENT ON COLUMN data_subject_rights_requests.rights_request.rights_request_due_date IS 'The statutory deadline.';
COMMENT ON COLUMN data_subject_rights_requests.rights_request.rights_request_current_status IS 'Received, verifying, in progress, responded, closed.';

CREATE TABLE IF NOT EXISTS data_subject_rights_requests.request_response (
  rights_request_identifier           varchar(40) NOT NULL,
  rights_request_response_timestamp   timestamptz NOT NULL,
  rights_request_response_description text NOT NULL,
  rights_request_responder_identifier varchar(40) NOT NULL,
  rights_request_refused_flag         boolean NOT NULL,
  CONSTRAINT request_response_pk PRIMARY KEY (rights_request_identifier, rights_request_response_timestamp)
);
COMMENT ON TABLE data_subject_rights_requests.request_response IS 'One row per response sent to a requester.';
COMMENT ON COLUMN data_subject_rights_requests.request_response.rights_request_identifier IS 'The request.';
COMMENT ON COLUMN data_subject_rights_requests.request_response.rights_request_response_timestamp IS 'When the response was sent.';
COMMENT ON COLUMN data_subject_rights_requests.request_response.rights_request_response_description IS 'The response, the actions taken and the reasons.';
COMMENT ON COLUMN data_subject_rights_requests.request_response.rights_request_responder_identifier IS 'Who sent it.';
COMMENT ON COLUMN data_subject_rights_requests.request_response.rights_request_refused_flag IS 'Whether any part of the request was refused.';

GRANT ALL ON ALL TABLES IN SCHEMA data_subject_rights_requests TO egeria_admin, egeria_user, airflow_user;

-- Requester Identity Verifications  (DigitalProduct::Coco::Requester Identity Verifications)
CREATE SCHEMA IF NOT EXISTS requester_identity_verifications;
GRANT ALL ON SCHEMA requester_identity_verifications TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA requester_identity_verifications IS 'The verification that a requester is who they claim to be, proportionate to what they are asking for. It is the step that stops the rights process from becoming an attack on the data it is meant to protect.';

CREATE TABLE IF NOT EXISTS requester_identity_verifications.identity_verification (
  rights_request_identifier                    varchar(40) NOT NULL,
  rights_request_verified_timestamp            timestamptz NOT NULL,
  rights_request_verified_method_code          varchar(40) NOT NULL,
  rights_request_verified_evidence_description text NOT NULL,
  rights_request_verified_status               varchar(20) NOT NULL,
  rights_request_verifier_identifier           varchar(40) NOT NULL,
  data_subject_identifier                      varchar(40),
  CONSTRAINT identity_verification_pk PRIMARY KEY (rights_request_identifier, rights_request_verified_timestamp)
);
COMMENT ON TABLE requester_identity_verifications.identity_verification IS 'One row per verification performed.';
COMMENT ON COLUMN requester_identity_verifications.identity_verification.rights_request_identifier IS 'The request.';
COMMENT ON COLUMN requester_identity_verifications.identity_verification.rights_request_verified_timestamp IS 'When verified.';
COMMENT ON COLUMN requester_identity_verifications.identity_verification.rights_request_verified_method_code IS 'The method used.';
COMMENT ON COLUMN requester_identity_verifications.identity_verification.rights_request_verified_evidence_description IS 'The evidence offered and accepted.';
COMMENT ON COLUMN requester_identity_verifications.identity_verification.rights_request_verified_status IS 'Verified, failed, insufficient.';
COMMENT ON COLUMN requester_identity_verifications.identity_verification.rights_request_verifier_identifier IS 'Who verified.';
COMMENT ON COLUMN requester_identity_verifications.identity_verification.data_subject_identifier IS 'The verified subject''s identifier in the relevant register.';

GRANT ALL ON ALL TABLES IN SCHEMA requester_identity_verifications TO egeria_admin, egeria_user, airflow_user;

-- Record Of Processing Activities  (DigitalProduct::Coco::Record Of Processing Activities)
CREATE SCHEMA IF NOT EXISTS record_of_processing_activities;
GRANT ALL ON SCHEMA record_of_processing_activities TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA record_of_processing_activities IS 'What personal data the company processes, for what purpose, under what lawful basis, and in which systems and processors it is held. It is what tells the rights chain where to look, so its accuracy is tested every time a request is answered.';

CREATE TABLE IF NOT EXISTS record_of_processing_activities.processing_activity (
  processing_activity_identifier          varchar(40) NOT NULL,
  processing_activity_name                varchar(120) NOT NULL,
  processing_activity_purpose_description text NOT NULL,
  processing_activity_basis_code          varchar(40) NOT NULL,
  data_subject_type                       varchar(20) NOT NULL,
  processing_activity_data_description    text NOT NULL,
  processing_activity_owner_identifier    varchar(40) NOT NULL,
  processing_activity_current_timestamp   timestamptz NOT NULL,
  CONSTRAINT processing_activity_pk PRIMARY KEY (processing_activity_identifier)
);
COMMENT ON TABLE record_of_processing_activities.processing_activity IS 'One row per processing activity.';
COMMENT ON COLUMN record_of_processing_activities.processing_activity.processing_activity_identifier IS 'The activity.';
COMMENT ON COLUMN record_of_processing_activities.processing_activity.processing_activity_name IS 'Its name.';
COMMENT ON COLUMN record_of_processing_activities.processing_activity.processing_activity_purpose_description IS 'The purpose.';
COMMENT ON COLUMN record_of_processing_activities.processing_activity.processing_activity_basis_code IS 'The lawful basis.';
COMMENT ON COLUMN record_of_processing_activities.processing_activity.data_subject_type IS 'The category of data subject.';
COMMENT ON COLUMN record_of_processing_activities.processing_activity.processing_activity_data_description IS 'The categories of personal data.';
COMMENT ON COLUMN record_of_processing_activities.processing_activity.processing_activity_owner_identifier IS 'The accountable owner.';
COMMENT ON COLUMN record_of_processing_activities.processing_activity.processing_activity_current_timestamp IS 'When last reviewed.';

CREATE TABLE IF NOT EXISTS record_of_processing_activities.processing_system (
  processing_activity_system_identifier varchar(40) NOT NULL,
  processing_activity_identifier        varchar(40) NOT NULL,
  system_identifier                     varchar(60),
  supplier_identifier                   varchar(40),
  retention_category_code               varchar(40) NOT NULL,
  system_reconciled_flag                boolean NOT NULL,
  CONSTRAINT processing_system_pk PRIMARY KEY (processing_activity_system_identifier)
);
COMMENT ON TABLE record_of_processing_activities.processing_system IS 'One row per system or processor holding data for an activity.';
COMMENT ON COLUMN record_of_processing_activities.processing_system.processing_activity_system_identifier IS 'The unique identifier of the entry for one system or processor holding data for a processing activity.';
COMMENT ON COLUMN record_of_processing_activities.processing_system.processing_activity_identifier IS 'The activity.';
COMMENT ON COLUMN record_of_processing_activities.processing_system.system_identifier IS 'The system, for internal holdings.';
COMMENT ON COLUMN record_of_processing_activities.processing_system.supplier_identifier IS 'The processor, for external holdings.';
COMMENT ON COLUMN record_of_processing_activities.processing_system.retention_category_code IS 'The retention category of the data held.';
COMMENT ON COLUMN record_of_processing_activities.processing_system.system_reconciled_flag IS 'Whether discovery found a discrepancy against this entry.';

GRANT ALL ON ALL TABLES IN SCHEMA record_of_processing_activities TO egeria_admin, egeria_user, airflow_user;

-- Personal Data Discovery Findings  (DigitalProduct::Coco::Personal Data Discovery Findings)
CREATE SCHEMA IF NOT EXISTS personal_data_discovery_findings;
GRANT ALL ON SCHEMA personal_data_discovery_findings TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA personal_data_discovery_findings IS 'What the survey of systems and stores actually found: personal data holdings by system, and the discrepancies between them and the record of processing. The register describes what the company believes it processes; this describes what it actually holds.';

CREATE TABLE IF NOT EXISTS personal_data_discovery_findings.discovered_holding (
  holding_identifier             varchar(40) NOT NULL,
  asset_identifier               varchar(40) NOT NULL,
  system_identifier              varchar(60) NOT NULL,
  data_subject_type              varchar(20) NOT NULL,
  holding_data_description       text NOT NULL,
  holding_discovered_timestamp   timestamptz NOT NULL,
  processing_activity_identifier varchar(40),
  CONSTRAINT discovered_holding_pk PRIMARY KEY (holding_identifier)
);
COMMENT ON TABLE personal_data_discovery_findings.discovered_holding IS 'One row per personal data holding found.';
COMMENT ON COLUMN personal_data_discovery_findings.discovered_holding.holding_identifier IS 'The holding.';
COMMENT ON COLUMN personal_data_discovery_findings.discovered_holding.asset_identifier IS 'The catalogued asset.';
COMMENT ON COLUMN personal_data_discovery_findings.discovered_holding.system_identifier IS 'The system.';
COMMENT ON COLUMN personal_data_discovery_findings.discovered_holding.data_subject_type IS 'The category of data subject the data concerns.';
COMMENT ON COLUMN personal_data_discovery_findings.discovered_holding.holding_data_description IS 'The personal data found.';
COMMENT ON COLUMN personal_data_discovery_findings.discovered_holding.holding_discovered_timestamp IS 'When found.';
COMMENT ON COLUMN personal_data_discovery_findings.discovered_holding.processing_activity_identifier IS 'The activity it reconciles to, if any.';

CREATE TABLE IF NOT EXISTS personal_data_discovery_findings.register_discrepancy (
  discrepancy_identifier         varchar(40) NOT NULL,
  holding_identifier             varchar(40),
  processing_activity_identifier varchar(40),
  discrepancy_type               varchar(40) NOT NULL,
  discrepancy_description        text NOT NULL,
  discrepancy_current_status     varchar(40) NOT NULL,
  CONSTRAINT register_discrepancy_pk PRIMARY KEY (discrepancy_identifier)
);
COMMENT ON TABLE personal_data_discovery_findings.register_discrepancy IS 'One row per difference between what was found and what the register says.';
COMMENT ON COLUMN personal_data_discovery_findings.register_discrepancy.discrepancy_identifier IS 'The discrepancy.';
COMMENT ON COLUMN personal_data_discovery_findings.register_discrepancy.holding_identifier IS 'The holding, for data found but not registered.';
COMMENT ON COLUMN personal_data_discovery_findings.register_discrepancy.processing_activity_identifier IS 'The activity, for data registered but not found.';
COMMENT ON COLUMN personal_data_discovery_findings.register_discrepancy.discrepancy_type IS 'Unregistered holding, missing holding, category mismatch.';
COMMENT ON COLUMN personal_data_discovery_findings.register_discrepancy.discrepancy_description IS 'The difference.';
COMMENT ON COLUMN personal_data_discovery_findings.register_discrepancy.discrepancy_current_status IS 'Open, register corrected, holding removed, accepted.';

GRANT ALL ON ALL TABLES IN SCHEMA personal_data_discovery_findings TO egeria_admin, egeria_user, airflow_user;

-- Rights Fulfilment Actions  (DigitalProduct::Coco::Rights Fulfilment Actions)
CREATE SCHEMA IF NOT EXISTS rights_fulfilment_actions;
GRANT ALL ON SCHEMA rights_fulfilment_actions TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA rights_fulfilment_actions IS 'Each verified request fanned out to every system and processor holding the person''s data, what came back, and the erasure, rectification and objection decisions driven onward to the systems that must act on them. It is the component that turns a register into an answer.';

CREATE TABLE IF NOT EXISTS rights_fulfilment_actions.fulfilment_request (
  rights_request_identifier                 varchar(40) NOT NULL,
  data_subject_identifier                   varchar(40) NOT NULL,
  data_subject_type                         varchar(20) NOT NULL,
  rights_request_type                       varchar(20) NOT NULL,
  rights_request_fulfilment_start_timestamp timestamptz NOT NULL,
  rights_request_fulfilment_count           integer NOT NULL,
  rights_request_fulfilment_status          varchar(20) NOT NULL,
  CONSTRAINT fulfilment_request_pk PRIMARY KEY (rights_request_identifier)
);
COMMENT ON TABLE rights_fulfilment_actions.fulfilment_request IS 'One row per verified request taken into fulfilment.';
COMMENT ON COLUMN rights_fulfilment_actions.fulfilment_request.rights_request_identifier IS 'The request.';
COMMENT ON COLUMN rights_fulfilment_actions.fulfilment_request.data_subject_identifier IS 'The verified subject.';
COMMENT ON COLUMN rights_fulfilment_actions.fulfilment_request.data_subject_type IS 'The category of subject.';
COMMENT ON COLUMN rights_fulfilment_actions.fulfilment_request.rights_request_type IS 'The right exercised.';
COMMENT ON COLUMN rights_fulfilment_actions.fulfilment_request.rights_request_fulfilment_start_timestamp IS 'When fulfilment began.';
COMMENT ON COLUMN rights_fulfilment_actions.fulfilment_request.rights_request_fulfilment_count IS 'The number of systems and processors asked.';
COMMENT ON COLUMN rights_fulfilment_actions.fulfilment_request.rights_request_fulfilment_status IS 'In progress, awaiting responses, decided, complete.';

CREATE TABLE IF NOT EXISTS rights_fulfilment_actions.system_action (
  system_action_identifier          varchar(40) NOT NULL,
  rights_request_identifier         varchar(40) NOT NULL,
  system_identifier                 varchar(60),
  supplier_identifier               varchar(40),
  system_action_type                varchar(20) NOT NULL,
  system_action_requested_timestamp timestamptz NOT NULL,
  system_action_completed_timestamp timestamptz,
  system_action_status              varchar(20) NOT NULL,
  retention_obligation_identifier   varchar(40),
  CONSTRAINT system_action_pk PRIMARY KEY (system_action_identifier)
);
COMMENT ON TABLE rights_fulfilment_actions.system_action IS 'One row per system or processor per request.';
COMMENT ON COLUMN rights_fulfilment_actions.system_action.system_action_identifier IS 'The unique identifier of the action requested of one system or processor for a request.';
COMMENT ON COLUMN rights_fulfilment_actions.system_action.rights_request_identifier IS 'The request.';
COMMENT ON COLUMN rights_fulfilment_actions.system_action.system_identifier IS 'The system, for internal holdings.';
COMMENT ON COLUMN rights_fulfilment_actions.system_action.supplier_identifier IS 'The processor, for external holdings.';
COMMENT ON COLUMN rights_fulfilment_actions.system_action.system_action_type IS 'Locate, disclose, rectify, erase, restrict.';
COMMENT ON COLUMN rights_fulfilment_actions.system_action.system_action_requested_timestamp IS 'When asked.';
COMMENT ON COLUMN rights_fulfilment_actions.system_action.system_action_completed_timestamp IS 'When answered.';
COMMENT ON COLUMN rights_fulfilment_actions.system_action.system_action_status IS 'Requested, completed, refused, no data held.';
COMMENT ON COLUMN rights_fulfilment_actions.system_action.retention_obligation_identifier IS 'The retention obligation that overrode an erasure, if any.';

GRANT ALL ON ALL TABLES IN SCHEMA rights_fulfilment_actions TO egeria_admin, egeria_user, airflow_user;

-- Retention Obligations  (DigitalProduct::Coco::Retention Obligations)
CREATE SCHEMA IF NOT EXISTS retention_obligations;
GRANT ALL ON SCHEMA retention_obligations TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA retention_obligations IS 'The retention obligation attaching to each category of personal data, and the basis that lets it override a request to be forgotten. Clinical trial records, employment decisions and health surveillance all outrank erasure, and the chain has to know that per holding rather than in general.';

CREATE TABLE IF NOT EXISTS retention_obligations.retention_obligation (
  retention_obligation_identifier  varchar(40) NOT NULL,
  retention_category_code          varchar(40) NOT NULL,
  retention_category_description   text NOT NULL,
  retention_duration               integer NOT NULL,
  retention_basis_description      text NOT NULL,
  retention_overrides_erasure_flag boolean NOT NULL,
  retention_obligation_start_date  date NOT NULL,
  CONSTRAINT retention_obligation_pk PRIMARY KEY (retention_obligation_identifier)
);
COMMENT ON TABLE retention_obligations.retention_obligation IS 'One row per retention category.';
COMMENT ON COLUMN retention_obligations.retention_obligation.retention_obligation_identifier IS 'The obligation.';
COMMENT ON COLUMN retention_obligations.retention_obligation.retention_category_code IS 'The category of data.';
COMMENT ON COLUMN retention_obligations.retention_obligation.retention_category_description IS 'What the category covers.';
COMMENT ON COLUMN retention_obligations.retention_obligation.retention_duration IS 'How long the data must be kept, in months.';
COMMENT ON COLUMN retention_obligations.retention_obligation.retention_basis_description IS 'The regulation or contract that requires it.';
COMMENT ON COLUMN retention_obligations.retention_obligation.retention_overrides_erasure_flag IS 'Whether the obligation overrides a request for erasure.';
COMMENT ON COLUMN retention_obligations.retention_obligation.retention_obligation_start_date IS 'When the obligation took effect.';

GRANT ALL ON ALL TABLES IN SCHEMA retention_obligations TO egeria_admin, egeria_user, airflow_user;

-- Retention Period Assignments  (DigitalProduct::Coco::Retention Period Assignments)
CREATE SCHEMA IF NOT EXISTS retention_period_assignments;
GRANT ALL ON SCHEMA retention_period_assignments TO egeria_admin, egeria_user, airflow_user;
COMMENT ON SCHEMA retention_period_assignments IS 'The retention period set on each catalogued asset: the basis it was set under and the dates on which the asset is to be archived and deleted. It is the point at which a retention obligation becomes an instruction attached to a specific holding.';

CREATE TABLE IF NOT EXISTS retention_period_assignments.retention_period_assignment (
  asset_identifier                varchar(40) NOT NULL,
  retention_obligation_identifier varchar(40) NOT NULL,
  retention_basis_description     text NOT NULL,
  retention_archive_date          date NOT NULL,
  retention_delete_date           date NOT NULL,
  retention_assigned_timestamp    timestamptz NOT NULL,
  retention_assigner_identifier   varchar(40) NOT NULL,
  CONSTRAINT retention_period_assignment_pk PRIMARY KEY (asset_identifier)
);
COMMENT ON TABLE retention_period_assignments.retention_period_assignment IS 'One row per asset with a retention period set.';
COMMENT ON COLUMN retention_period_assignments.retention_period_assignment.asset_identifier IS 'The catalogued asset.';
COMMENT ON COLUMN retention_period_assignments.retention_period_assignment.retention_obligation_identifier IS 'The obligation applied.';
COMMENT ON COLUMN retention_period_assignments.retention_period_assignment.retention_basis_description IS 'The basis recorded on the asset.';
COMMENT ON COLUMN retention_period_assignments.retention_period_assignment.retention_archive_date IS 'When the asset is to be archived.';
COMMENT ON COLUMN retention_period_assignments.retention_period_assignment.retention_delete_date IS 'When it is to be deleted.';
COMMENT ON COLUMN retention_period_assignments.retention_period_assignment.retention_assigned_timestamp IS 'When the period was set.';
COMMENT ON COLUMN retention_period_assignments.retention_period_assignment.retention_assigner_identifier IS 'Who set it.';

GRANT ALL ON ALL TABLES IN SCHEMA retention_period_assignments TO egeria_admin, egeria_user, airflow_user;

