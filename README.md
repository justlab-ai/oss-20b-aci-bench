<div align="center">

<!-- Technology Banners -->
<a href="https://openai.com">
  <img src="https://img.shields.io/badge/OpenAI-000000?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" height="35"/>
</a>
&nbsp;&nbsp;
<a href="https://aws.amazon.com/bedrock/">
  <img src="https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-web-services&logoColor=white" alt="AWS" height="35"/>
</a>
&nbsp;&nbsp;
<a href="https://aws.amazon.com/bedrock/">
  <img src="https://img.shields.io/badge/AWS_Bedrock-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="Bedrock" height="35"/>
</a>

<br/><br/>

# Evaluation of OpenAI OSS Models on ACI-Bench

**Benchmarking Clinical Note Generation with Large Language Models**

<br/>

[![OpenAI Models](https://img.shields.io/badge/Models-gpt--oss--20b_|_gpt--oss--120b-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![AWS Bedrock](https://img.shields.io/badge/Infrastructure-AWS_Bedrock-FF9900?style=flat-square&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/bedrock/)
[![Dataset](https://img.shields.io/badge/Dataset-ACI--Bench-blue?style=flat-square)](https://github.com/wyim/aci-bench)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## Abstract

This repository presents an evaluation of OpenAI's open-source language models (`gpt-oss-20b` and `gpt-oss-120b`) on the ACI-Bench benchmark for automated clinical note generation. Using AWS Bedrock for inference, we assess model performance on converting doctor-patient conversations into structured clinical documentation. Our results demonstrate competitive zero-shot performance, achieving ROUGE-1 scores of 45.0-45.9%, comparable to ChatGPT while outperforming baseline BART models.

---

## Results

### Performance Summary

| Model | Parameters | ROUGE-1 | ROUGE-2 | ROUGE-L | Inference Time |
|:------|:----------:|:-------:|:-------:|:-------:|:--------------:|
| gpt-oss-20b | 20B | 45.03 | 15.18 | 21.33 | ~50s/sample |
| gpt-oss-120b | 120B | 45.89 | 15.15 | 19.30 | ~12s/sample |

> *Evaluation conducted on ACI-Bench validation set (n=20). Scores reported as F1 percentages.*

### Baseline Comparison

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L | Source |
|:------|:-------:|:-------:|:-------:|:------:|
| BART + FTSAMSum (Division) | **53.46** | **25.08** | **48.62** | Yim et al. 2023 |
| GPT-4 | 51.76 | 22.58 | 45.97 | Yim et al. 2023 |
| ChatGPT | 47.44 | 19.01 | 42.47 | Yim et al. 2023 |
| **gpt-oss-120b** | 45.89 | 15.15 | 19.30 | This work |
| **gpt-oss-20b** | 45.03 | 15.18 | 21.33 | This work |
| BART (base) | 41.76 | 19.20 | 34.70 | Yim et al. 2023 |
| LED | 28.37 | 5.52 | 22.78 | Yim et al. 2023 |

---

## Key Findings

### Model Performance

1. **Competitive Zero-Shot Results**: Both models achieve ROUGE-1 scores within 2 percentage points of ChatGPT without task-specific fine-tuning.

2. **Limited Scaling Benefit**: The 120B model provides only marginal improvement (+1.9% ROUGE-1) over the 20B variant, suggesting diminishing returns from increased model capacity for this task.

3. **Structural Differences**: Lower ROUGE-L scores indicate generated notes differ structurally from reference notes, likely due to the full-note generation approach versus division-based methods.

4. **Inference Efficiency**: Counterintuitively, the 120B model demonstrated faster inference times (~12s vs ~50s per sample), potentially due to infrastructure optimizations.

### Recommendations

| Objective | Approach | Expected Impact |
|:----------|:---------|:---------------:|
| Improved accuracy | Division-based prompting | +5-10 ROUGE-1 |
| Better phrasing alignment | Few-shot learning | +2-5 ROUGE-1 |
| Production deployment | Domain-specific fine-tuning | +5-8 ROUGE-1 |
| Cost optimization | Use 20B model | 6x parameter reduction |

---

## Methodology

### Task Definition

**Ambient Clinical Intelligence (ACI)**: Automated generation of structured clinical notes from doctor-patient conversation transcripts.

**Input**: Natural language dialogue transcript
**Output**: Structured clinical note (SOAP format)

### Experimental Setup

| Component | Specification |
|:----------|:--------------|
| Models | OpenAI gpt-oss-20b, gpt-oss-120b |
| Infrastructure | AWS Bedrock (us-east-1) |
| Dataset | ACI-Bench validation split (n=20) |
| Evaluation | ROUGE-1, ROUGE-2, ROUGE-L (F1) |
| Generation | Zero-shot, full-note approach |
| Temperature | 0.3 |
| Max Tokens | 1024 |

### Dataset

The [ACI-Bench](https://github.com/wyim/aci-bench) corpus (Yim et al., 2023) is the largest publicly available dataset for clinical note generation from medical conversations, containing doctor-patient dialogues paired with reference clinical notes.

---

## Usage

### Prerequisites

```bash
pip install boto3 rouge-score tqdm
aws configure  # Set up AWS credentials
```

### Running Evaluation

```bash
git clone https://github.com/justlab-ai/oss-20b-aci-bench.git
cd oss-20b-aci-bench

python scripts/evaluate_bedrock.py --model both --data-split valid
```

### Output

Results are saved to `results/` directory:
- `gpt-oss-20b_results.json` — Per-sample predictions and scores
- `gpt-oss-120b_results.json` — Per-sample predictions and scores
- `comparison_results.json` — Aggregate metrics comparison

---

## Documentation

| Document | Description |
|:---------|:------------|
| [METHODOLOGY.md](METHODOLOGY.md) | Detailed experimental procedures and setup |
| [METRICS.md](METRICS.md) | ROUGE metric definitions and interpretation |
| [FINDINGS.md](FINDINGS.md) | Extended analysis and discussion |

---

## Citation

```bibtex
@misc{justlab2024ossacibench,
  title     = {Evaluation of OpenAI OSS Models on ACI-Bench},
  author    = {JustLab AI},
  year      = {2024},
  publisher = {GitHub},
  url       = {https://github.com/justlab-ai/oss-20b-aci-bench}
}
```

---

## References

1. Yim, W., Fu, Y., Ben Abacha, A., Snider, N., Lin, T., & Yetisgen, M. (2023). ACI-BENCH: A Novel Ambient Clinical Intelligence Dataset for Benchmarking Automatic Visit Note Generation. *Scientific Data*, 10(1), 586. [https://doi.org/10.1038/s41597-023-02487-3](https://www.nature.com/articles/s41597-023-02487-3)

2. Lin, C. Y. (2004). ROUGE: A Package for Automatic Evaluation of Summaries. *Text Summarization Branches Out*.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

**JustLab AI** · [GitHub](https://github.com/justlab-ai)

</div>
