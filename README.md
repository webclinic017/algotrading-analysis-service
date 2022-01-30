
## Algo params
1. Name - S00-ORB-001
        base algo is : `S01-ORB`
        Version are last number, 
        RULE, algo = basealgo + `-` + versionNumber
        RULE, Version no 3 chars fixed.
        RULE, Base algo = algo minus last 4 characters
        


## Invoke trade signal
http://0.0.0.0:5000/tradesignals/?algo=S001-ORB-001&symbol=BANKNIFTY&date=2022-01-25        


## Dependencies
pipreqs

## Build DOCKER Image
DOCKER_BUILDKIT=1 docker build -t paragba/algotrading-analysis-service:latest .

docker run -d --name algotrading-analysis-service  -p 80:5000 paragba/algotrading-analysis-service:latest

docker rm --force algotrading-analysis-service