

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


