## Connect to MySQL local server
```
mysql -h 0.0.0.0 -u root -p
```

## Add new companies to scrape

1. Add new company info to `data_storage/data/companies.json`
2. Run `python data_storage/scripts/ingest.py` to insert company info into database
3. Add new spider file to `data_scrape/spiders`, e.g. `microsoft.py`

## Run spiders
There are two ways to run the spiders:

1. Run all spiders at once:
```
python run_spiders.py
```

2. Run a specific spider:
```
scrapy crawl <spider_name>
```

## Migrate the database
// TODO

## Troubleshooting
Cannot find module named `data_storage`
```
Traceback (most recent call last):
  File "/Users/jiawei.an/code/TechHire/data_scrape/data_storage/scripts/ingest.py", line 6, in <module>
    from data_storage.models import Base
ModuleNotFoundError: No module named 'data_storage'
```

Solution:
```
pip install -e .
```