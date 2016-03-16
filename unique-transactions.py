import json
import sys

def log(s):
    sys.stderr.write(str(s))
    sys.stderr.flush()

def load(filename):
    with open(filename) as data_file:
        return json.load(data_file)

def transaction_ids(data):
    return [transaction["id"] for transaction in data["response"]["transactions"]]
    

def run(infile):
    result=set()
    for filename in infile.readlines():
        filename=filename.strip()
        result = result.union(set(transaction_ids(load(filename))))
        log(".")
    log("\n")
    for tid in result:
        print tid


if __name__=="__main__":
    run(sys.stdin)