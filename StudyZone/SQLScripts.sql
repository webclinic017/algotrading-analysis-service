SELECT * FROM public.zerodha_ticks
ORDER by "time" desc limit 100;

SELECT * FROM public.candles_1min 
where symbol like '%BANKNIFTY%'
ORDER by "bucket" desc limit 10;