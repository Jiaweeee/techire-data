# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from .storage import JobInfoStoragePipeline

__all__ = [
    'JobInfoStoragePipeline'
]
