
#########################################################################
#                    Encode exit critirea for Strategy
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Arg: Exit list
# Ret: Encoded values.
# Noote: Both are kept in same file to avoid en/dec errors by subscribers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def encodeExitCriteria (sl, sldeep, sldelay, stalld, tt, pr):
    
    #print('encode:', sl, sldeep, sldelay, stalld, tt, pr)
    return 'STPL='+sl+\
            '|SLDP='+sldeep+\
            '|SLDL='+sldelay+\
            '|STLD='+stalld+\
            '|TTRL='+tt+\
            '|POSR='+pr

#########################################################################
#                    Read exit critirea from Strategy
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Arg: Exit list
# Ret: Decoded values. Values are position dependent
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def readExitCriteria (val):

    #print(val)
    # Read exit criterias
    ec = val.split('|')

    v = ec[0].split('=')
    sl = v[1]
    
    v = ec[1].split('=')
    sldeep = float(v[1])
    
    v = ec[2].split('=')
    sldelay = v[1]
    
    v = ec[3].split('=')
    stalld = v[1]
    
    v = ec[4].split('=')
    tt = v[1]
    
    v = ec[5].split('=')
    pr = v[1]


#     print('Exit Criterias (lib_* module)',' pSl:', sl, \
#           ' pSlDeep:', sldeep, ' pSlDelay:', sldelay, \
#           ' pStallDetect:', stalld, ' pTargetTrail:', tt,\
#           ' pPositionReversal:', pr)


    return sl, sldeep, sldelay, stalld, tt, pr
