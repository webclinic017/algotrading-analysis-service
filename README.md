
## Algo params
1. Name - S00-ORB-001
        base algo is : `S01-ORB`
        Version are last number, 
        RULE, algo = basealgo + `-` + versionNumber
        RULE, Version no 3 chars fixed.
        RULE, Base algo = algo minus last 4 characters
        

# Historic Data in Ticker
1. Export data from DB
2. Run the script, to convert data as ticker. Req to generate Con Agg views
❯ gawk -f 1minToTickConverter.awk candles_1min_t_202201102340.csv > historicTicks.csv
3. Import data back in DB.


# Create Table in Timescale db
`CREATE TABLE 
ticker_t ( 									timestamp TIMESTAMP NOT NULL,
		symbol VARCHAR(30) NOT NULL,
		last_traded_price double precision NOT NULL,
		buy_demand bigint NOT NULL,
		sell_demand bigint NOT NULL,
        	trades_till_now bigint NOT NULL,
		open_interest bigint NOT NULL
		);
SELECT create_hypertable('ticker_t', 'timestamp');
SELECT set_chunk_time_interval('ticker_t', INTERVAL '24 hours');`