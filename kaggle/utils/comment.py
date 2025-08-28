from dataclasses import dataclass
from typing import Optional, List

import pandas as pd


@dataclass
class Comment:
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
    def load(file_path: str) -> List['Comment']:
        df = pd.read_csv(file_path)
        dicts = df.to_dict(orient='records')
        return [Comment(**d) for d in dicts]

    @staticmethod
    def save(file_path: str, data: List['Comment']) -> None:
        df = pd.DataFrame([{'row_id': comment.row_id, 'rule_violation': comment.rule_violation}
                          for comment in sorted(data, key=lambda x:x.row_id)])
        df.to_csv(file_path, index=False)

