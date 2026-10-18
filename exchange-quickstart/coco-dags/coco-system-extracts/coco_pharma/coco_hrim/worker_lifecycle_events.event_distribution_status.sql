-- Extract: Human Resources Information Manager (HRIM) (Coco core) -> Worker Lifecycle Events / event_distribution_status
-- Source: coco_pharma.coco_hrim (System::coco-hrim)
-- Target: coco_data_hub.worker_lifecycle_events.event_distribution_status
-- hr_event_dist; Y/N acknowledgement to boolean.
SELECT
  d.event_id::varchar(40)          AS worker_event_identifier,
  d.target_sys::varchar(60)        AS system_identifier,
  d.sent_at                        AS worker_event_sent_timestamp,
  (d.ack_yn = 'Y')                 AS worker_event_applied_flag,
  d.ack_at                         AS worker_event_applied_timestamp
FROM coco_hrim.hr_event_dist d
