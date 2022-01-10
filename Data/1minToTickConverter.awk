BEGIN { FS = ","
print "Symbol,timestamp,last_traded_price," }

{
    #print $0
    print $1 "," substr($2, 1, 17)"01," $3
    print $1 "," substr($2, 1, 17)"02," $4
    print $1 "," substr($2, 1, 17)"03," $5
    print $1 "," substr($2, 1, 17)"59," $6
    #print "\n\n"

}
# NIFTY-FUT,2010-02-24 15:20:00.000,
# 4858.8,4859.8,4858.0,4858.0
# Symbol,timestamp,open,high,low,close,volume,

END { }
