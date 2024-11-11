# fetch-exercise
This is the solution for Fetch's SRE take home exercise
# how to run
```shell
python healthCheck.py [-h] [-c FILE_PATH] [-s SECOND]
```
```
options:
  -h, --help    show this help message and exit
  -c FILE_PATH  Path to the YAML config file containing endpoint definitions
  -s SECOND     Health check test cycle length (default 15 seconds)
```
### OR
```shell
python healthCheck.py
```
then imput config file path:
```shell
Please input config file path:[path]
```