from dataclasses import dataclass
from typing import Optional, List

import pandas as pd


@dataclass
class Data:
    row_id: int
    body: str
    rule: str
    subreddit: str
    positive_example_1: str
    positive_example_2: str
    negative_example_1: str
    negative_example_2: str
    rule_violation: Optional[float] = None

    @staticmethod
    def load(file_path: str) -> List['Data']:
        df = pd.read_csv(file_path)
        dicts = df.to_dict(orient='records')
        return [Data(**d) for d in dicts]
