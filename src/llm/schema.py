from dataclasses import dataclass
from typing import Optional


@dataclass
class GeneratedPrompt:
    run_id: str
    date: str
    representation: str
    prompt_type: str
    prompt: str


@dataclass
class LLMOutput:
    run_id: str
    date: str
    representation: str
    prompt_type: str
    model: str
    output: str


@dataclass
class PromptEvaluation:
    run_id: str
    date: str
    representation: str
    prompt_type: str
    prompt_chars: int
    prompt_lines: int
    clarity: str
    faithfulness: str
    behavior_inference: str
    hallucination_risk: str
    notes: Optional[str] = None