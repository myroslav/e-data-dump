import datetime
import json
import sys

def log(s):
    sys.stderr.write(str(s))
    sys.stderr.flush()

def load(filename):
    with open(filename) as data_file:
        return json.load(data_file)

def write(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
            
def extract_transactions(data, ids):
    for transaction in data["response"]["transactions"]:
       tid = transaction["id"]
       if tid in ids:
          ids.remove(tid)
          yield transaction

def run(id_file, infile, outname, batch):
    ids = set(int(id.strip()) for id in id_file.readlines())

    result=[]
    for filename in infile.readlines():
        filename=filename.strip()
        for transaction in extract_transactions(load(filename), ids):
            result.append(transaction)
            if len(result) >= batch:
                filename = "{}-{}.json".format(outname, datetime.datetime.now().isoformat())
                write(filename, result)
                result =[]
                log(".")
    print ids




if __name__=="__main__":
    id_filename=sys.argv[1]
    run(open(id_filename), sys.stdin, "e-data-transactions-{}".format(datetime.datetime.now().isoformat()), 10000)
