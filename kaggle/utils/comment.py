from dataclasses import dataclass
from typing import Optional, List

import pandas as pd


@dataclass
class Task:
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
    def load(file_path: str) -> List['Task']:
        df = pd.read_csv(file_path)
        dicts = df.to_dict(orient='records')
        return [Task(**d) for d in dicts]

    @staticmethod
    def save(file_path: str, data: List['Task']) -> None:
        df = pd.DataFrame([{'row_id': comment.row_id, 'rule_violation': comment.rule_violation}
                           for comment in sorted(data, key=lambda x: x.row_id)])
        df.to_csv(file_path, index=False)


@dataclass
class Comment:
    """
    These are samples from train and test data of single violation samples.
    """
    body: str
    rule: str
    subreddit: str
    rule_violation: bool

    @staticmethod
    def extract_single(task: 'Task') -> List['Comment']:
        names = ['positive_example_1', 'positive_example_2', 'negative_example_1', 'negative_example_2']
        violations = [True, True, False, False]
        ans = [Comment(body=getattr(task, name), rule=task.rule, subreddit=task.subreddit, rule_violation=violation)
               for name, violation in zip(names, violations)]
        if task.rule_violation is not None and task.rule_violation in [0, 1]:
            violation = task.rule_violation == 1
            ans.append(Comment(body=task.body, rule=task.rule, subreddit=task.subreddit, rule_violation=violation))
        return ans

    @staticmethod
    def extract(file_path:str) -> List['Comment']:
        tasks = Task.load(file_path)
        ans = []
        for task in tasks:
            ans.extend(Comment.extract_single(task))
        return ans
