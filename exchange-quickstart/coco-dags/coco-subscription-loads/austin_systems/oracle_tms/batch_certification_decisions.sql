-- Subscription: aus_oracle_tms__batch_certification_decisions - Oracle TMS (Austin) receives Batch Certification Decisions
-- Destination: austin_systems.oracle_tms (SoftwareServer::AUS-SYS-013::SN-TMS-AU-20211004)
-- Why it subscribes: Therapy Delivery Events depends on it (therapy released)
-- Keeps the release decisions on Austin batches in the NEW ie_batch_release interface table, so a shipment carrying
-- the batch can be tendered once it is certified for the destination market; the shipment and refnum tables, which
-- the extracts read, are not written. Other estates' batches are discarded.

UPDATE incoming_certification_decision i SET discard_reason = 'other estate: not an Austin batch'
 WHERE i.batch_identifier !~ '^A[0-9]{2}-';
INSERT INTO oracle_tms.ie_batch_release
       (batch_no, market_code, release_status, release_date, released_qty, record_complete, deviation_ref,
        storage_instructions)
SELECT i.batch_identifier, i.market_code, upper(i.batch_certification_status), i.batch_certification_date,
       i.batch_released_quantity, CASE WHEN i.batch_record_complete_flag THEN 'Y' ELSE 'N' END,
       i.deviation_identifier, i.shipment_storage_description
  FROM incoming_certification_decision i
 WHERE i.discard_reason IS NULL
ON CONFLICT (batch_no, market_code) DO UPDATE SET
       release_status = EXCLUDED.release_status, release_date = EXCLUDED.release_date,
       released_qty = EXCLUDED.released_qty, record_complete = EXCLUDED.record_complete,
       deviation_ref = EXCLUDED.deviation_ref, storage_instructions = EXCLUDED.storage_instructions;
