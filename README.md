<div align="center">

# 🏥 OpenAI OSS Models on ACI-Bench

### Clinical Note Generation Evaluation

[![OpenAI](https://img.shields.io/badge/OpenAI-OSS_Models-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/bedrock/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*Evaluating OpenAI's open-source language models on automated clinical documentation*

[📊 Results](#-results) • [📖 Methodology](METHODOLOGY.md) • [📐 Metrics](METRICS.md) • [🔬 Findings](FINDINGS.md)

</div>

---

## 🎯 Overview

This repository evaluates **OpenAI's open-source models** (`gpt-oss-20b` and `gpt-oss-120b`) on the **ACI-Bench** benchmark for **Ambient Clinical Intelligence** — the task of automatically generating structured clinical notes from doctor-patient conversations.

<div align="center">

```
┌─────────────────────────┐         ┌─────────────────────────┐
│   Doctor-Patient        │         │   Structured Clinical   │
│   Conversation          │  ───►   │   Note (SOAP format)    │
│   (Audio/Transcript)    │   AI    │   - Chief Complaint     │
│                         │         │   - History             │
│                         │         │   - Assessment & Plan   │
└─────────────────────────┘         └─────────────────────────┘
```

</div>

---

## 📊 Results

### Model Performance

<div align="center">

| Model | Parameters | ROUGE-1 | ROUGE-2 | ROUGE-L | Speed |
|:-----:|:----------:|:-------:|:-------:|:-------:|:-----:|
| **gpt-oss-20b** | 20B | `45.03` | `15.18` | `21.33` | ~50s/sample |
| **gpt-oss-120b** | 120B | `45.89` | `15.15` | `19.30` | ~12s/sample |

</div>

### Comparison with State-of-the-Art

<div align="center">

```
ROUGE-1 Score Comparison (%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BART+FTSAMSum(Div) ████████████████████████████████████  53.5
GPT-4              ██████████████████████████████████    51.8
ChatGPT            ███████████████████████████████       47.4
gpt-oss-120b       ██████████████████████████████        45.9  ◄ Ours
gpt-oss-20b        █████████████████████████████         45.0  ◄ Ours
BART (base)        ███████████████████████████           41.8
LED                █████████████████                     28.4
```

</div>

---

## 🔑 Key Findings

<table>
<tr>
<td width="50%">

### ✅ Strengths

- **Competitive zero-shot performance** — within 2 points of ChatGPT
- **Outperforms base BART** by +4 ROUGE-1 points
- **No fine-tuning required** — works out-of-the-box
- **Enterprise-ready** via AWS Bedrock

</td>
<td width="50%">

### ⚠️ Observations

- **Minimal scaling benefit** — 120B only +1.9% over 20B
- **ROUGE-L gap** — structural differences in note format
- **Room for improvement** — 8 points below best baseline
- **120B faster** — counterintuitive speed advantage

</td>
</tr>
</table>

### 💡 Recommendations

| Goal | Recommendation | Expected Gain |
|------|----------------|---------------|
| Higher accuracy | Use division-based prompting | +5-10 ROUGE-1 |
| Better phrasing | Add few-shot examples | +2-5 ROUGE-1 |
| Production use | Fine-tune on domain data | +5-8 ROUGE-1 |
| Cost efficiency | Use 20B model (similar quality) | 6x smaller |

---

## 🛠️ Tech Stack

<div align="center">

| Component | Technology |
|:---------:|:----------:|
| **Models** | ![OpenAI](https://img.shields.io/badge/OpenAI-gpt--oss--20b/120b-412991?logo=openai) |
| **Infrastructure** | ![AWS](https://img.shields.io/badge/AWS-Bedrock-FF9900?logo=amazon-aws) |
| **Dataset** | ![Dataset](https://img.shields.io/badge/ACI--Bench-Clinical_NLP-blue) |
| **Metrics** | ![Metrics](https://img.shields.io/badge/ROUGE-1/2/L-orange) |
| **Language** | ![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white) |

</div>

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/justlab-ai/oss-20b-aci-bench.git
cd oss-20b-aci-bench

# Install dependencies
pip install boto3 rouge-score tqdm

# Configure AWS credentials
aws configure

# Run evaluation
python scripts/evaluate_bedrock.py --model both --data-split valid
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [📖 METHODOLOGY.md](METHODOLOGY.md) | Task definition, dataset details, experimental setup |
| [📐 METRICS.md](METRICS.md) | ROUGE-1/2/L explained with formulas and examples |
| [🔬 FINDINGS.md](FINDINGS.md) | Detailed results, analysis, and recommendations |

---

## 📖 Citation

```bibtex
@misc{oss20b-aci-bench-2024,
  title   = {Evaluation of OpenAI OSS Models on ACI-Bench},
  author  = {JustLab AI},
  year    = {2024},
  url     = {https://github.com/justlab-ai/oss-20b-aci-bench}
}
```

---

## 🔗 References

- **ACI-Bench Paper**: Yim et al. (2023). [ACI-BENCH: A Novel Ambient Clinical Intelligence Dataset](https://www.nature.com/articles/s41597-023-02487-3). *Scientific Data*
- **Dataset**: [github.com/wyim/aci-bench](https://github.com/wyim/aci-bench)
- **AWS Bedrock**: [aws.amazon.com/bedrock](https://aws.amazon.com/bedrock/)

---

<div align="center">

**Made with ❤️ by [JustLab AI](https://github.com/justlab-ai)**

[![GitHub stars](https://img.shields.io/github/stars/justlab-ai/oss-20b-aci-bench?style=social)](https://github.com/justlab-ai/oss-20b-aci-bench)

</div>
