from abc import ABC, abstractmethod
from data_storage.models import Job
from typing import Optional, Any

class Processor(ABC):
    def setup(self):
        """Called only once before processing any job to initialize the pipeline"""
        pass

    @abstractmethod
    def process(self, job: Job) -> Optional[Any]:
        """Process a job item"""
        pass
