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

## Database Migrations

After modifying database models in `data_storage/models.py`:

1. Create and apply new migration:
```
python -m data_storage.scripts.migrate "描述你的改动"
```

2. If you just want to run existing migrations (e.g., when deploying to a new environment):
```
python -m data_storage.scripts.migrate
```

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