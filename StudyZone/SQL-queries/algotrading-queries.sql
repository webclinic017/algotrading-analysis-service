-- ##################################################################  instruments
-- load futures tokens based on intruments and user_symbols
SELECT i.instrument_token, ts.mysymbol, i.exchange, ts.mysymbol, i.tradingsymbol 
    FROM user_symbols ts, instruments i
    WHERE 
    		ts.symbol = i.name
		and 
			ts.segment = i.instrument_type 
		and 
			ts.exchange = i.exchange
    	and 
    		EXTRACT(MONTH FROM TO_DATE(i.expiry,'YYYY-MM-DD')) = EXTRACT(MONTH FROM current_date);
-- select * from user_symbols where mysymbol = 'NIFTY-FUT';

-- fetch Option instruments
SELECT tradingsymbol, lot_size
    FROM user_symbols ts, instruments i
    WHERE 
    		ts.symbol = i.name 
    	and 
    		mysymbol= 'BANKNIFTY-FUT' 
    	and 
    		strike >= (35120  + 5*ts.strikestep)
		and 
    		strike < (35120 + ts.strikestep + 5*ts.strikestep)     		
    	and 
    		tradingsymbol like '%PE' 
    	and 
    		expiry > '2022-03-23'
    	and 
    		expiry < '2022-03-30'
	ORDER BY 
		expiry asc
	LIMIT 10;

-- fetch FUT instruments

 -- fetch EQ instruments
SELECT tradingsymbol, lot_size
    FROM user_symbols ts, instruments i
    WHERE 
    		ts.symbol = i.name 
    	and 
    		ts.mysymbol = 'ASHOK LEYLAND' 
    	and
    		i.segment = 'NSE'
       	and 
    		instrument_type = 'EQ'  
	LIMIT 100;

-- ##################################################################  delete view
DROP MATERIALIZED VIEW candles_15min

-- ##################################################################  view symbol within specific time frame
select * from ticks_data 
 WHERE (time between '2022-01-25 09:00:00' and '2022-01-25 09:40:00')
 and symbol like '%BANKNIFTY%'
ORDER by time asc;
 
-- ##################################################################  view tick count for each day
SELECT 
    DATE_TRUNC('day', "time") AS "day", 
	COUNT("time") AS "total ticks"
FROM public.ticks_data
GROUP BY DATE_TRUNC('day', "time")
order by day DESC;

-- ################################################################## Hypertable size
SELECT 	
		-- hypertable_schema, 
		hypertable_name as "Hypertable", 
		chunk_name as "Chunk",
		--chunk_id,
		--(total_bytes) as "Size", 
		pg_size_pretty(total_bytes + compressed_total_size) as "Size", 
		pg_size_pretty(compressed_total_size) as "Compressed Size"
		--pg_size_pretty(compressed_total_size) as "Compressed Size"
		--100 - ((compressed_total_size*100 / total_bytes)) as Percentage
FROM _timescaledb_internal.hypertable_chunk_local_size
WHERE NOT(hypertable_name like '_compressed%')
ORDER BY total_bytes desc

-- ################################################################## Copy specific date

SELECT * FROM ticks_nsefut WHERE CAST(time AS date) = '2022-05-30 00:00:00';

-- ################################################################## Compression

-- remove hypertable compression 
ALTER TABLE ticks_data set (timescaledb.compress ='false');
-- remove hypertable compression policy
SELECT remove_compression_policy('ticks_data');

SELECT * FROM hypertable_compression_stats('ticks_data');
SELECT * FROM chunk_compression_stats('ticks_data');

-- enable compression
ALTER TABLE ticks_data SET (timescaledb.compress, timescaledb.compress_segmentby = 'symbol');
-- add compression policy
SELECT add_compression_policy('ticks_data ', INTERVAL '30 days');


-- ################################################################## Delete date based
DELETE FROM ticks_data WHERE time < '2011-03-01 01:01:01';


select * from public.information_schema.tables;

select table_name from information_schema.tables WHERE table_name = 'zerodha_ticks';
