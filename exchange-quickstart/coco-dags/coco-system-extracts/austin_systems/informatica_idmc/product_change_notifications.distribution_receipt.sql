-- Extract: Informatica IDMC (Austin) -> Product Change Notifications / distribution_receipt
-- Source: austin_systems.informatica_idmc (SoftwareServer::AUS-SYS-042::SN-ETL-AU-20200901)
-- Target: coco_data_hub.product_change_notifications.distribution_receipt
-- activity_log runs of the product propagation tasks grouped per change and target: first attempt sent, applied when
-- any run succeeded, applied time = end of the successful run; target code mapped to the system qualified name.
SELECT
  (a.runtime_params ->> '$$ChangeRef$$')::varchar(40) AS product_change_identifier,
  (CASE a.runtime_params ->> '$$Target$$' WHEN 'SAP_S4' THEN 'SoftwareServer::AUS-SYS-009::SN-SAP-AU-20180923' WHEN 'SFDC' THEN 'SoftwareServer::AUS-SYS-016::SN-CRM-AU-20200901' WHEN 'ARIBA' THEN 'SoftwareServer::AUS-SYS-014::SN-SRM-AU-20190617' WHEN 'MANH_WMS' THEN 'SoftwareServer::AUS-SYS-012::SN-WMS-AU-20200315' END)::varchar(60) AS system_identifier,
  bool_or(a.state = 1) AS product_change_applied_flag,
  max(a.end_time) FILTER (WHERE a.state = 1) AS product_change_applied_timestamp
FROM informatica_idmc.activity_log a
WHERE a.object_name LIKE 'mt_Product_Golden_To_%'
GROUP BY a.runtime_params ->> '$$ChangeRef$$', a.runtime_params ->> '$$Target$$'
