# e-data-dump

* API: http://api.e-data.gov.ua:8080/api/rest/1.0/transactions
* Instructions:
* https://docs.google.com/document/d/1EjYNyXycEoTwjdIGrI_EV5R1_-kBt4fdCgTYSsBfvVs/edit
* Discussion:
* https://www.facebook.com/vladimir.tarnay/posts/1183590464985844

## Howto

1) Downloading

       python downloader.py transactions-seller


2) Generating list of Unique transaction IDs

       find . -type f -name transactions-\* | python unique-transactions.py
> ids.list

3) Deduplicating transactions:

       find . -type f -name transactions\* | python deduplicator.py ids.list

4) Generating CSV

       find . -type f -name e-data-transactions-\* | python csvficator.py >
e-data-transactions.csv

