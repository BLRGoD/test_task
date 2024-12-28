WITH raw_data AS (
    SELECT
        toStartOfMonth(ExecutionTime) AS month,
        AVG(EUR_to_X / USD_to_X) as rate
    FROM default.ECB_table
    GROUP BY month
    HAVING from_currency = 'EUR' and to_currency = 'USD'
)

SELECT
    month,
    'EUR' as from_currency,
    'USD' as to_currency,
    AVG(rate)
FROM raw_data
GROUP BY month