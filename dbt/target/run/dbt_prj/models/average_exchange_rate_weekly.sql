

  create view `default`.`average_exchange_rate_weekly__dbt_tmp` 
  
    
    
  as (
    WITH raw_data AS (
    SELECT
        toStartOfWeek(ExecutionTime, 1) AS start_of_week,    
        CharCode AS from_currency,                       
        'USD' AS to_currency,                            
        AVG(Value) AS average_rate                       
    FROM default.ECB_table 
    GROUP BY start_of_week, from_currency, to_currency
)

SELECT
    start_of_week,
    from_currency,
    to_currency,
    average_rate AS rate
FROM raw_data
    
  )
      
      
                    -- end_of_sql
                    
                    