# Sensor2LLM

## Overview
Sensor2LLM is a project that explores the ability of Large Language Models (LLMs) to interpret IoT sensor data from smart home environments.

The goal is to transform raw sensor logs into natural language and evaluate whether an LLM can:
- understand human behavior
- identify patterns
- detect anomalies
- generate summaries

---

## Research Question
Can an LLM infer complex behavioral patterns from raw sensor data without rule-based logic?

---

## Approach

The project follows these steps:

1. Data preprocessing  
   - Raw sensor logs (Milan dataset)  
   - Cleaning and sorting  

2. Text transformation  
   - Event-level representation  
   - Minute-level aggregation  
   - Hourly aggregation  

3. Prompt generation  
   - Different prompt strategies  

4. LLM evaluation  
   - Behavioral summaries  
   - Pattern recognition  

---

## Project Structure

Sensor2LLM/

├── data/  
│   ├── raw/  
│   └── processed/  

├── src/  
│   ├── preprocessing/  
│   ├── llm/  
│   ├── eval/  
│   └── common/  

├── scripts/  
│   ├── build_dataset.py  
│   ├── create_annotated_windows.py  
│   ├── generate_prompts.py  
│   └── evaluate_results.py  

├── prompts/  
├── outputs/  
├── results/  
│   ├── predictions/  
│   └── metrics/  

└── README.md  

---

## How to Run

### Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Build dataset
```bash
python3 scripts/build_dataset.py
```

### Create annotated dataset
```bash
python3 scripts/create_annotated_windows.py
```

### Generate prompts
```bash
python3 scripts/generate_prompts.py
```

### Generate prompts
```bash
python3 scripts/evaluate_results.py
```

### Generate prompts
The results will be saved in:
- results/metrics/run_results.csv
- results/metrics/summary.csv