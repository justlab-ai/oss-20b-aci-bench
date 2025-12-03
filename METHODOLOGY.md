# Methodology

This document describes the experimental setup, data, and procedures used to evaluate OpenAI OSS models on the ACI-Bench clinical note generation task.

## Table of Contents

1. [Task Definition](#task-definition)
2. [Dataset](#dataset)
3. [Models](#models)
4. [Experimental Setup](#experimental-setup)
5. [Evaluation Procedure](#evaluation-procedure)
6. [Reproducibility](#reproducibility)

---

## Task Definition

### Ambient Clinical Intelligence (ACI)

**Ambient Clinical Intelligence** refers to AI systems that passively listen to doctor-patient conversations and automatically generate structured clinical documentation. This technology aims to:

- Reduce physician documentation burden
- Decrease time spent on Electronic Health Records (EHR)
- Improve accuracy of clinical notes
- Allow physicians to focus on patient care

### Clinical Note Generation Task

**Input**: A transcript of a doctor-patient conversation (dialogue)

**Output**: A structured clinical note containing:

| Section | Description |
|---------|-------------|
| **Chief Complaint (CC)** | The primary reason for the patient's visit |
| **History of Present Illness (HPI)** | Detailed narrative of the current problem |
| **Review of Systems (ROS)** | Systematic inquiry about body systems |
| **Physical Examination (PE)** | Findings from the physical exam |
| **Assessment & Plan (A&P)** | Diagnosis and treatment plan |

### Example

**Input (Dialogue excerpt)**:
```
Doctor: What brings you in today?
Patient: I've been having this pain in my chest for about three days now.
Doctor: Can you describe the pain? Is it sharp or dull?
Patient: It's more of a pressure feeling, especially when I climb stairs.
...
```

**Output (Clinical Note)**:
```
CHIEF COMPLAINT: Chest pain x 3 days

HISTORY OF PRESENT ILLNESS:
Patient is a [age] year old [gender] presenting with chest pain
for the past three days. Pain is described as pressure-like,
exacerbated by exertion such as climbing stairs...

ASSESSMENT AND PLAN:
1. Chest pain - concerning for possible angina
   - Order EKG, troponins, chest X-ray
   - Consider stress test if initial workup negative
...
```

---

## Dataset

### ACI-Bench

We use the **ACI-Bench** dataset (Yim et al., 2023), the largest publicly available corpus for clinical note generation from conversations.

#### Dataset Statistics

| Split | Samples | Purpose |
|-------|---------|---------|
| Train | 67 | Model training/fine-tuning |
| Validation | 20 | Hyperparameter tuning |
| Test 1 | 40 | ClinicalNLP 2023 Task B |
| Test 2 | 40 | ClinicalNLP 2023 Task C |
| Test 3 | 40 | CLEF 2023 Task C |

#### Data Sources

The dataset combines two sources:
1. **ACI corpus**: Real transcribed medical conversations
2. **VirtScribe**: Scripted medical conversations

#### Data Format

Each sample contains:
- `src`: Doctor-patient dialogue transcript
- `tgt`: Reference clinical note (ground truth)
- `file`: Unique identifier

### Our Evaluation Split

We evaluate on the **validation set (n=20)** because:
1. Test sets were used for shared task competitions
2. Validation set provides unbiased evaluation
3. Small size enables rapid iteration

---

## Models

### OpenAI OSS Models on AWS Bedrock

We evaluate two models from OpenAI's open-source release, accessed via AWS Bedrock:

| Model | Parameters | Bedrock Model ID |
|-------|------------|------------------|
| gpt-oss-20b | 20 billion | `openai.gpt-oss-20b-1:0` |
| gpt-oss-120b | 120 billion | `openai.gpt-oss-120b-1:0` |

### Model Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Temperature | 0.3 | Lower temperature for more deterministic, factual output |
| Max Tokens | 1024 | Sufficient for comprehensive clinical notes |
| Top-p | (default) | Not modified |

### Why These Models?

1. **Open Source**: Enables reproducibility and transparency
2. **AWS Bedrock**: Enterprise-ready, secure healthcare deployment
3. **Scale Comparison**: 20B vs 120B tests parameter scaling effects
4. **Zero-shot**: No fine-tuning required, tests out-of-box capability

---

## Experimental Setup

### Infrastructure

| Component | Specification |
|-----------|--------------|
| Cloud Provider | AWS |
| Service | Bedrock Runtime |
| Region | us-east-1 |
| API | invoke_model |

### Prompt Design

We use a **zero-shot prompt** with structured instructions:

```
You are a medical scribe assistant. Your task is to convert a
doctor-patient conversation into a structured clinical note.

The clinical note should include:
- CHIEF COMPLAINT: The main reason for the visit
- HISTORY OF PRESENT ILLNESS: Detailed description of current problem
- REVIEW OF SYSTEMS: Relevant symptoms mentioned
- PHYSICAL EXAMINATION: Any examination findings discussed
- ASSESSMENT AND PLAN: Diagnosis and treatment plan

Generate a professional clinical note based on the conversation provided.
Be concise but thorough.

Doctor-Patient Conversation:
{dialogue}

Clinical Note:
```

### Generation Approach

We use **full-note generation**:
- Single prompt generates the entire clinical note
- All sections produced in one inference call
- No section-by-section (division) approach

**Note**: The ACI-Bench paper shows that division-based approaches (generating each section separately) achieve higher ROUGE scores. Our full-note approach is simpler but potentially less accurate.

---

## Evaluation Procedure

### Pipeline

```
┌─────────────────┐
│  Load ACI-Bench │
│  Validation Set │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ For each sample │◄──────────────┐
└────────┬────────┘               │
         │                        │
         ▼                        │
┌─────────────────┐               │
│ Call Bedrock API│               │
│ Generate Note   │               │
└────────┬────────┘               │
         │                        │
         ▼                        │
┌─────────────────┐               │
│ Store Prediction│───────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Calculate ROUGE │
│ Scores          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Save Results    │
└─────────────────┘
```

### ROUGE Calculation

We use the `rouge-score` Python package:

```python
from rouge_score import rouge_scorer

scorer = rouge_scorer.RougeScorer(
    ['rouge1', 'rouge2', 'rougeL'],
    use_stemmer=True
)
```

- **Stemming**: Enabled to normalize word forms
- **Metric**: F1 score (harmonic mean of precision and recall)
- **Tokenization**: Default whitespace tokenization

### Error Handling

- **Timeout**: 120s per request, 3 retries with exponential backoff
- **Rate Limiting**: 0.5s delay between requests
- **Failed Samples**: Marked as "[FAILED]", excluded from ROUGE calculation

---

## Reproducibility

### Dependencies

```
boto3>=1.28.0
rouge-score>=0.1.2
tqdm>=4.65.0
```

### Code Availability

The evaluation script is provided in `scripts/evaluate_bedrock.py`.

### Running the Evaluation

```bash
# Install dependencies
pip install boto3 rouge-score tqdm

# Configure AWS credentials
aws configure

# Run evaluation
python scripts/evaluate_bedrock.py \
    --model both \
    --data-split valid \
    --output-dir results/
```

### Random Seed

No random seed is needed as:
- Temperature 0.3 provides near-deterministic outputs
- ROUGE calculation is deterministic
- No sampling or shuffling in evaluation

### Expected Runtime

| Model | Time per Sample | Total (20 samples) |
|-------|-----------------|-------------------|
| gpt-oss-20b | ~50 seconds | ~17 minutes |
| gpt-oss-120b | ~12 seconds | ~4 minutes |

---

## Limitations

1. **Small Sample Size**: Only 20 validation samples
2. **Zero-shot Only**: No fine-tuning or few-shot prompting
3. **Full-note Generation**: Division-based approach not tested
4. **Single Run**: No statistical significance testing
5. **ROUGE Only**: No BERTScore, BLEURT, or human evaluation

---

## References

1. Yim, W., Fu, Y., Ben Abacha, A., Snider, N., Lin, T., & Yetisgen, M. (2023). ACI-BENCH: A Novel Ambient Clinical Intelligence Dataset for Benchmarking Automatic Visit Note Generation. *Scientific Data*, 10(1), 586.

2. Lin, C. Y. (2004). ROUGE: A Package for Automatic Evaluation of Summaries. *Text Summarization Branches Out*.
