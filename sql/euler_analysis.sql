-- DuckDB-compatible analysis after loading data/cases.csv as evidence.
-- Keep missing values NULL; do not infer them from secondary reports.
CREATE OR REPLACE VIEW evidence AS
SELECT * FROM read_csv_auto('data/cases.csv', header = true, nullstr = '');

SELECT id, date_utc, tx_hash, from_address, to_address, amount, verification
FROM evidence
ORDER BY date_utc NULLS LAST, id;

SELECT to_address, kind, count(*) AS tx_count,
       sum(CASE WHEN verification = 'explorer_index' THEN amount ELSE 0 END) AS checked_eth
FROM evidence
GROUP BY to_address, kind
ORDER BY checked_eth DESC;
