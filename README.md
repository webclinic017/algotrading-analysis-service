
## Algo params
1. Name - S00-ORB-001
        base algo is : `S01-ORB`
        Version are last number, 
        RULE, algo = basealgo + `-` + versionNumber
        RULE, Version no 3 chars fixed.
        RULE, Base algo = algo minus last 4 characters
        


## Invoke trade signal
http://0.0.0.0:5000/tradesignals/?algo=algoid&symbol=symbolid&date=yyyy-mm-dd


docker run -d --name algotrading-analysis-service  -p 80:5000 paragba/algotrading-analysis-service:latest

docker rm --force algotrading-analysis-service


## Version : In-Development
* DB - table names updated

## Version : 0.1.7
* DB - compression policy updated

---
## Dev Environment 
---
###Virtual ENV
python3 -m venv env

**Activate venv**
VS Code - Ctrl+Shift+P -> Select python interpreter -> select venv
On Unix or MacOS, using the bash shell: `source /path/to/venv/bin/activate`
On Windows using the Command Prompt: `path\to\venv\Scripts\activate.bat`

`python3 -m pip install --upgrade pip`
`pip3 --version` - Check if refers the env path
`pip3 install --upgrade -r ./requirements.txt`



### Dependencies
pip3 install pipreqs
pipreqs --force
pip3 install --upgrade -r ./requirements.txt

Issue with code-server, version is removed from reqs for psycopg2-binary

### Build DOCKER Image
DOCKER_BUILDKIT=1 docker build -t paragba/algotrading-analysis-service:latest .

### ISSUES

#### QT5 issue
`'qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.'`
  `export QT_DEBUG_PLUGINS=1`  (to see the log for issues)

> It appears that as of PyQt5 5.15, the Qt plugin libqxcb.so is expecting to find the module libxcb-util.so.1 eg:
/lib/x86_64-linux-gnu/libxcb-util.so.1
However, Debian Buster (version 10.7) only has libxcb-util.so.0
This change was apparently made in PyQt 5.15.

**Possible Solution**

One possible solution might be to pin the max requirement for PyQt5 to 5.14.2 though I have not tested this (I opted to make a symbolic link called libxcb-util.so.1 in the same folder as libxcb-util.so.0 that pointed to libxcb-util.so.0, which seems to work), eg:

`sudo ln -s /usr/lib/x86_64-linux-gnu/libxcb-util.so.0 /usr/lib/x86_64-linux-gnu/libxcb-util.so.1`



