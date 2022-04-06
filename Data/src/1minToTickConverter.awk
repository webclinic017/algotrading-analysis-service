BEGIN { FS = ","
# print "Symbol,timestamp,last_traded_price," }
print "time,symbol,last_traded_price,buy_demand,sell_demand,trades_till_now,open_interest"
}


{
    #print $0
    print substr($2, 1, 17)"01," $1 "," $3 ",0,0,0,0"
    print substr($2, 1, 17)"02," $1 "," $4 ",0,0,0,0"
    print substr($2, 1, 17)"03," $1 "," $5 ",0,0,0,0"
    print substr($2, 1, 17)"59," $1 "," $6 ",0,0,0,0"
    #print "\n\n"

}
# NIFTY-FUT,2010-02-24 15:20:00.000,
# 4858.8,4859.8,4858.0,4858.0
# Symbol,timestamp,open,high,low,close,volume,

END { }


# ❯ gawk -f ./1minToTickConverter.awk candles_1min_t_202201102340.csv > historic.csv
