
## Algo params
1. Name - S00-ORB-001
        base algo is : `S01-ORB`
        Version are last number, 
        RULE, algo = basealgo + `-` + versionNumber
        RULE, Version no 3 chars fixed.
        RULE, Base algo = algo minus last 4 characters
        


## Invoke trade signal
http://0.0.0.0:5000/tradesignals/?algo=algoid&symbol=symbolid&date=yyyy-mm-dd


## Dependencies
pipreqs --force
pip3 install --upgrade -r ./requirements.txt

Issue with code-server, version is removed from reqs for psycopg2-binary

## Build DOCKER Image
DOCKER_BUILDKIT=1 docker build -t paragba/algotrading-analysis-service:latest .

docker run -d --name algotrading-analysis-service  -p 80:5000 paragba/algotrading-analysis-service:latest

docker rm --force algotrading-analysis-service


## Version : In-Development
* DB - table names updated

## Version : 0.1.7
* DB - compression policy updated


## Dev Env - Issues

### QT5 issue
'qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.'
use the debug - current file, start debug, then switch back to FastAPI/Reseach. it works!

### Virtual ENV
python3 -m venv env
python3 -m pip install --upgrade pip
pip3 --version - Check if refers the env path
pip3 install --upgrade -r ./requirements.txt

### using env
command line -> source env/bin/activate                      
VS COde - Ctrl+Shift+P -> Select python interpreter -> select venv

