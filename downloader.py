import datetime
import json
import sys

import requests

API_ENDPOINT='http://api.e-data.gov.ua:8080/api/rest/1.0/transactions'

class ChunkificationNecessary(Exception):pass
class DownloadError(ChunkificationNecessary):pass
class LimitReached(ChunkificationNecessary):
    def __init__(self, data):
        self.data = data

def log(s):
    sys.stderr.write(str(s))
    sys.stderr.flush()

def download(criteria, lst, start, end):
    if start and end:
       log("[{} {}]".format(start, end))
    else:
       log(len(lst))
    parameters={criteria: lst}
    if start: parameters["startdate"]=start
    if end: parameters["enddate"]=end
    r = requests.post(API_ENDPOINT, json=parameters)
    if r.status_code == 200:
       return r.json()
    else:
       log("E({})".format(r.status_code))
       raise DownloadError


def chunkify(lst, n):
   return [ lst[i::n] for i in xrange(n) ]

DATE_FORMAT="%d-%m-%Y"

def go(criteria, lst, outname, n=10, start=None, end=None):
    log("(")
    for chunk in chunkify(lst, n):
        try:
            result = download(criteria, chunk, start, end)
            if len(result["response"]["transactions"])>=10000:
                raise LimitReached(result)
            fname = "{}-{}.json".format(outname, datetime.datetime.now().isoformat())
            write(fname, result)
            log(".")
        except DownloadError:
            go(criteria, chunk, outname, n=2)        
        except LimitReached, e:
            if len(chunk)>1:
                go(criteria, chunk, outname, n=2)
            else:
                startdate = datetime.datetime.strptime(e.data["response"]["request"]["startdate"], DATE_FORMAT)
                enddate = datetime.datetime.strptime(e.data["response"]["request"]["enddate"], DATE_FORMAT)
                midday = startdate + (enddate - startdate)/2
                go(criteria, chunk, outname, n=1, start=startdate.strftime(DATE_FORMAT), end=midday.strftime(DATE_FORMAT))
                go(criteria, chunk, outname, n=1, start=midday.strftime(DATE_FORMAT), end=enddate.strftime(DATE_FORMAT))
    log(")")

def run(criteria, lst, outname, splitter):
    log("{}({}/{}): ".format(outname, criteria, splitter))
    runtime=datetime.datetime.now().isoformat()
    outname="{}-{}-{}".format(outname, runtime, splitter)
    go(criteria, lst, outname, n=splitter)
    log("\n")

def write(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
        
        
def load(filename):
    with open(filename) as data_file:    
        return json.load(data_file)
        
VARIANTS={
      "transactions-buyer": ("payers_edrpous", 'buyer-edrpou.json', 500),
      "transactions-buyer-rev": ("recipt_edrpous", 'buyer-edrpou.json', 500),
      "transactions-seller": ("recipt_edrpous", 'seller-edrpou.json', 1000),
      "transactions-seller-rev": ("payers_edrpous", 'seller-edrpou.json', 20),
    }

def help():
    print VARIANTS.keys()
        
if __name__=='__main__':
    try:
        variant=sys.argv[1]
        (criteria, source, splitter) = VARIANTS[variant]
    except:
        help()
        sys.exit(1)
    run(criteria, load(source), variant, splitter)

