from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
    ingested_train_dir: Path
    ingested_test_dir: Path


@dataclass(frozen=True)
class DataValidationConfig:
    """Data Validation Config"""
    training_dataset: Path 
    test_dataset: Path
    schema_path: Path
        




