-- Extract: OpenText ECM (Bucharest) -> Supplier Material Certificates / certificate_of_analysis
-- Source: bucharest_systems.opentext_ecm (SoftwareServer::SYS-024::OpenText ECM)
-- Target: coco_data_hub.supplier_material_certificates.certificate_of_analysis
-- Supplier certificate PDFs (category Certificat furnizor) pivoted from llattrdata; COC/COA to words; Conform DA/NU to
-- boolean.
WITH a AS (
  SELECT id,
         max(valstr) FILTER (WHERE attrid = 2) AS supplier, max(valstr) FILTER (WHERE attrid = 3) AS material,
         max(valstr) FILTER (WHERE attrid = 4) AS lot, max(valstr) FILTER (WHERE attrid = 5) AS cert_type,
         max(valdate) FILTER (WHERE attrid = 6) AS cert_date, max(valstr) FILTER (WHERE attrid = 7) AS conform,
         max(valstr) FILTER (WHERE attrid = 8) AS cert_no
  FROM opentext_ecm.llattrdata WHERE defid = 3002 GROUP BY id
)
SELECT
  a.cert_no::varchar(40) AS certificate_identifier,
  a.supplier::varchar(40) AS supplier_identifier,
  a.material::varchar(20) AS raw_material_code,
  a.lot::varchar(40) AS lot_identifier,
  (CASE a.cert_type WHEN 'COC' THEN 'certificate of conformity' ELSE 'certificate of analysis' END)::varchar(40) AS certificate_type,
  a.cert_date AS certificate_date,
  (a.conform = 'DA') AS certificate_conformity_flag
FROM a
JOIN opentext_ecm.dtree d ON d.dataid = a.id AND d.subtype = 144
