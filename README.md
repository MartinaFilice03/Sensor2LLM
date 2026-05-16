# Sensor2LLM

Sensor2LLM is an NLP-oriented project that converts smart home sensor events into natural language representations for Large Language Model (LLM) analysis.

The project explores how different temporal representations of sensor data influence readability, behavioral interpretation, and information preservation.

---

# Project Goal

The main objective is to transform raw smart-home activity logs into textual prompts suitable for LLM reasoning and behavioral analysis.

The project compares multiple representations:

- Event-level representation
- Minute-level aggregation
- Hourly-level aggregation

The generated prompts are evaluated through custom NLP-inspired metrics.

---

# Project Structure

```text
Sensor2LLM/
├── configs/
│   └── experiments.yml
├── data/
│   └── processed/
│       └── annotated_milan_windows.json
├── outputs/
│   └── generated_prompts.json
├── prompts/
│   ├── aggregated_prompt.txt
│   ├── analysis_prompt.txt
│   ├── hourly_prompt.txt
│   └── summary_prompt.txt
├── results/
│   ├── metrics/
│   │   ├── event_level.csv
│   │   ├── minute_level.csv
│   │   ├── hourly_level.csv
│   │   └── summary.csv
│   └── predictions/
├── scripts/
│   ├── build_dataset.py
│   ├── create_annotated_windows.py
│   ├── evaluate_results.py
│   ├── export_outputs.py
│   ├── generate_prompts.py
│   └── run_experiments.py
├── src/
│   ├── common/
│   │   ├── io.py
│   │   └── schema.py
│   ├── eval/
│   │   └── metrics.py
│   └── llm/
│       ├── prompt.py
│       ├── runner.py
│       └── schema.py
├── README.md
└── requirements.txt
```

# Dataset
The project uses smart-home sensor activity data collected from indoor environments.
Sensor events are transformed into:
- natural language event streams
- aggregated temporal summaries
- behavioral descriptions

# Representations
Event-level
Each sensor activation is converted into a detailed natural language event.

Example:
- At 01:29, movement detected in the kitchen.
- At 01:30, movement detected in the living room.

# Minute-level
Events are aggregated by minute.
Example:
- At 01:29, activity occurred in multiple areas: kitchen, living room.

# Minute-level
Events are aggregated by minute.
Example:
- At 01:29, activity occurred in multiple areas: kitchen, living room.

# Evaluation Metrics
The project includes qualitative and structural evaluation metrics inspired by NLP analysis.
Metrics include:
- clarity
- faithfulness
- behavior inference
- hallucination risk
- sentence length
- active rooms count
- temporal coverage
- movement density

# Experimental Pipeline
The complete pipeline is executed through:
- python3 -m scripts.run_experiments

This automatically:
- Generates prompts
- Evaluates representations
- Produces CSV reports

# Results
Evaluation reports are saved inside:
- results/metrics/
Generated files:
- event_level.csv
- minute_level.csv
- hourly_level.csv
- summary.csv

# Results
Evaluation reports are saved inside:
- results/metrics/
Generated files:
- event_level.csv
- minute_level.csv
- hourly_level.csv
- summary.csv
