-- system-qualified-name: SoftwareServer::AUS-SYS-042::SN-ETL-AU-20200901
-- Informatica IDMC - Austin.  Informatica Intelligent Data Management Cloud for Austin: the mapping tasks that
-- propagate MDM golden records to SAP, Salesforce, Ariba and Manhattan WMS.  Its activity log feeds Product Change
-- Notifications (distribution receipts).
-- Loaded by init_coco_systems.sql.  Idempotent: safe to run again.

CREATE SCHEMA IF NOT EXISTS informatica_idmc;
COMMENT ON SCHEMA informatica_idmc IS 'Informatica IDMC Data Integration (Austin org): task run activity log as landed by the monitoring API.';

CREATE TABLE IF NOT EXISTS informatica_idmc.activity_log (
  run_id              bigint NOT NULL,
  object_name         varchar(120) NOT NULL,
  object_type         varchar(10) NOT NULL,
  start_time          timestamptz NOT NULL,
  end_time            timestamptz,
  state               integer NOT NULL,
  success_target_rows integer NOT NULL,
  failed_target_rows  integer NOT NULL,
  error_msg           text,
  runtime_params      jsonb NOT NULL,
  CONSTRAINT activity_log_pk PRIMARY KEY (run_id)
);
COMMENT ON TABLE informatica_idmc.activity_log IS 'Task run activity log (state 1 success, 2 warning, 3 failed); runtime parameters carry the change reference and target.';

INSERT INTO informatica_idmc.activity_log (run_id, object_name, object_type, start_time, end_time, state, success_target_rows, failed_target_rows, error_msg, runtime_params) VALUES
(3300017, 'mt_Product_Golden_To_SAP_S4', 'MTT', '2026-02-20 16:05:00+00', '2026-02-20 16:07:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0007", "$$Target$$": "SAP_S4"}'),
(3300034, 'mt_Product_Golden_To_SFDC', 'MTT', '2026-02-20 16:08:00+00', '2026-02-20 16:11:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0007", "$$Target$$": "SFDC"}'),
(3300051, 'mt_Product_Golden_To_ARIBA', 'MTT', '2026-02-20 16:11:00+00', '2026-02-20 16:15:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0007", "$$Target$$": "ARIBA"}'),
(3300068, 'mt_Product_Golden_To_MANH_WMS', 'MTT', '2026-02-20 16:14:00+00', '2026-02-20 16:19:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0007", "$$Target$$": "MANH_WMS"}'),
(3300085, 'mt_Product_Golden_To_SAP_S4', 'MTT', '2026-05-08 14:35:00+00', '2026-05-08 14:37:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0009", "$$Target$$": "SAP_S4"}'),
(3300102, 'mt_Product_Golden_To_SFDC', 'MTT', '2026-05-08 14:38:00+00', '2026-05-08 14:40:00+00', 3, 0, 1, 'Salesforce API limit exceeded', '{"$$ChangeRef$$": "PCN-26-0009", "$$Target$$": "SFDC"}'),
(3300119, 'mt_Product_Golden_To_SFDC', 'MTT', '2026-05-08 20:38:00+00', '2026-05-08 20:41:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0009", "$$Target$$": "SFDC"}'),
(3300136, 'mt_Product_Golden_To_ARIBA', 'MTT', '2026-05-08 14:41:00+00', '2026-05-08 14:45:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0009", "$$Target$$": "ARIBA"}'),
(3300153, 'mt_Product_Golden_To_MANH_WMS', 'MTT', '2026-05-08 14:44:00+00', '2026-05-08 14:49:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0009", "$$Target$$": "MANH_WMS"}'),
(3300170, 'mt_Product_Golden_To_SAP_S4', 'MTT', '2026-06-24 11:15:00+00', '2026-06-24 11:17:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0011", "$$Target$$": "SAP_S4"}'),
(3300187, 'mt_Product_Golden_To_SFDC', 'MTT', '2026-06-24 11:18:00+00', '2026-06-24 11:21:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0011", "$$Target$$": "SFDC"}'),
(3300204, 'mt_Product_Golden_To_ARIBA', 'MTT', '2026-06-24 11:21:00+00', '2026-06-24 11:25:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0011", "$$Target$$": "ARIBA"}'),
(3300221, 'mt_Product_Golden_To_MANH_WMS', 'MTT', '2026-06-24 11:24:00+00', '2026-06-24 11:29:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0011", "$$Target$$": "MANH_WMS"}'),
(3300238, 'mt_Product_Golden_To_SAP_S4', 'MTT', '2026-08-12 09:50:00+00', '2026-08-12 09:52:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0014", "$$Target$$": "SAP_S4"}'),
(3300255, 'mt_Product_Golden_To_SFDC', 'MTT', '2026-08-12 09:53:00+00', '2026-08-12 09:56:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0014", "$$Target$$": "SFDC"}'),
(3300272, 'mt_Product_Golden_To_ARIBA', 'MTT', '2026-08-12 09:56:00+00', '2026-08-12 10:00:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0014", "$$Target$$": "ARIBA"}'),
(3300289, 'mt_Product_Golden_To_MANH_WMS', 'MTT', '2026-08-12 09:59:00+00', '2026-08-12 10:04:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0014", "$$Target$$": "MANH_WMS"}'),
(3300306, 'mt_Product_Golden_To_SAP_S4', 'MTT', '2026-09-18 15:25:00+00', '2026-09-18 15:27:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0016", "$$Target$$": "SAP_S4"}'),
(3300323, 'mt_Product_Golden_To_SFDC', 'MTT', '2026-09-18 15:28:00+00', '2026-09-18 15:31:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0016", "$$Target$$": "SFDC"}'),
(3300340, 'mt_Product_Golden_To_ARIBA', 'MTT', '2026-09-18 15:31:00+00', '2026-09-18 15:35:00+00', 1, 1, 0, NULL, '{"$$ChangeRef$$": "PCN-26-0016", "$$Target$$": "ARIBA"}'),
(3300357, 'mt_Product_Golden_To_MANH_WMS', 'MTT', '2026-09-18 15:34:00+00', '2026-09-18 15:39:00+00', 3, 0, 1, 'HTTP 409 from WMS item API: item 61002 locked by open wave', '{"$$ChangeRef$$": "PCN-26-0016", "$$Target$$": "MANH_WMS"}')
ON CONFLICT DO NOTHING;

GRANT USAGE ON SCHEMA informatica_idmc TO egeria_user, airflow_user;
GRANT SELECT ON ALL TABLES IN SCHEMA informatica_idmc TO egeria_user, airflow_user;
