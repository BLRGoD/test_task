INSERT INTO `SHOW CREATE TABLE ECB_table` (`statement`) VALUES
	 ('CREATE TABLE default.ECB_table
(
    `ID` LowCardinality(String),
    `NumCode` LowCardinality(String),
    `CharCode` LowCardinality(String),
    `Nominal` String,
    `Name` String,
    `Value` Float64,
    `X_to_USD` Float64,
    `USD_to_X` Float64,
    `X_to_EUR` Float64,
    `EUR_to_X` Float64,
    `ExecutionTime` DateTime
)
ENGINE = ReplacingMergeTree
ORDER BY (CharCode, ID)
SETTINGS index_granularity = 8192');
