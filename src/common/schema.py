from dataclasses import dataclass
from typing import List


@dataclass
class SensorEvent:
    timestamp: str
    location: str
    event: str


@dataclass
class SensorWindow:
    date: str
    num_events: int
    event_level_text: str
    minute_level_text: str
    hourly_text: str


@dataclass
class Annotation:
    date: str
    summary_gold: str
    qa_pairs: List[dict]


@dataclass
class EvaluationResult:
    run_id: str
    date: str
    representation: str
    prompt_type: str
    clarity: str
    faithfulness: str
    behavior_inference: str
    hallucination_risk: str