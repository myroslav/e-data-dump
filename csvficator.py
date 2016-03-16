import csv
import json
import sys

def log(s):
    sys.stderr.write(str(s))
    sys.stderr.flush()

def load(filename):
    with open(filename) as data_file:
        return json.load(data_file)

FIELDS=(
    "id",
    "trans_date",
    "region_id",
    "amount",
    "payer_edrpou",
    "payer_name",
    "payer_mfo",
    "payer_bank",
    "recipt_edrpou",
    "recipt_name",
    "recipt_mfo",
    "recipt_bank",
    "payment_details",
    )

def run(infile, outfile):
    #w = csv.writer
    outfile.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    w = csv.DictWriter(outfile, FIELDS)
    w.writeheader()
    for filename in infile.readlines():
        filename=filename.strip()
        for transaction in load(filename):
            w.writerow({k:unicode(v).encode('utf8') for k,v in transaction.items()})
        log(".")  
    log("\n")


if __name__=="__main__":
    run(sys.stdin, sys.stdout)
