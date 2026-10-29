-- DuckDB-compatible query. Run from the repository root.
CREATE OR REPLACE VIEW withdrawals AS
SELECT * FROM read_csv_auto('data/withdrawals.csv', header = true);

SELECT phase, COUNT(*) AS transactions, SUM(amount_usdt) AS usdt
FROM withdrawals
GROUP BY phase
ORDER BY phase;

SELECT id, date_utc, tx_hash, amount_usdt, verification
FROM withdrawals
ORDER BY date_utc;
