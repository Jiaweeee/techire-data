import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.spider import iter_spider_classes
import importlib
import pkgutil

def load_spiders(package_name='data_scrape.spiders'):
    """自动加载指定包下的所有爬虫类"""
    spiders = []
    package = importlib.import_module(package_name)
    
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f'{package_name}.{name}')
        for spider_class in iter_spider_classes(module):
            spiders.append(spider_class)
    return spiders

def main(spider_name=None):
    process = CrawlerProcess(settings=get_project_settings())
    # 自动加载并运行所有爬虫
    spiders = load_spiders()
    if spider_name:
        # 只运行指定的爬虫
        spiders = [spider for spider in spiders if spider.name == spider_name]
    
    for spider in spiders:
        process.crawl(spider)
    process.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Scrapy spiders.')
    parser.add_argument('--spider', type=str, help='The name of the spider to run')
    args = parser.parse_args()
    
    main(spider_name=args.spider)