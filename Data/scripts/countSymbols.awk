BEGIN { FS = ","
    cnt = 0
    cntFUT = 0
    cntIDX = 0
}


{
    if (gsub("-FUT","",$0)) {
        ++cntFUT
    }
    if (gsub("-IDX","",$0)) {
        ++cntIDX
    }
    ++cnt

}

END {print FILENAME, "\tFUT = ", cntFUT ",\tIDX = ", cntIDX, ",\tTOTAL = ", cnt}


# ❯ gawk -f ./countSymbols.awk aa.csv

# For just the current directory:
# ---------------------------------------
# for file in *
# do awk ... "$file"
# done > result.txt

# If you need to recurse into subdirectories:
# ---------------------------------------

# find . -type f -exec awk ... {} ; > result.txt


# ---------------------------------------
# for file in *
# do  gawk -f ./countSymbols.awk  "$file"
# done > result.txt