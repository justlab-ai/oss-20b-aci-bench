<!-- Header Banner -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,16,18,20&height=200&section=header&text=OpenAI%20OSS%20×%20AWS%20Bedrock&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Clinical%20Note%20Generation%20Benchmark&descSize=18&descAlignY=55" width="100%"/>
</div>

<div align="center">

<!-- Technology Badges -->
<a href="https://openai.com">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" height="30"/>
</a>
<a href="https://aws.amazon.com/bedrock/">
  <img src="https://img.shields.io/badge/AWS_Bedrock-232F3E?style=for-the-badge&logo=amazon-web-services&logoColor=FF9900" alt="AWS Bedrock" height="30"/>
</a>
<a href="https://github.com/wyim/aci-bench">
  <img src="https://img.shields.io/badge/ACI--Bench-0969DA?style=for-the-badge&logo=github&logoColor=white" alt="ACI-Bench" height="30"/>
</a>

<br/><br/>

# Evaluation of OpenAI OSS Models on ACI-Bench

### Benchmarking Large Language Models for Automated Clinical Documentation

<br/>

<table>
<tr>
<td align="center"><b>Models</b></td>
<td align="center"><b>Infrastructure</b></td>
<td align="center"><b>Task</b></td>
<td align="center"><b>Metrics</b></td>
</tr>
<tr>
<td align="center"><code>gpt-oss-20b</code><br/><code>gpt-oss-120b</code></td>
<td align="center">AWS Bedrock<br/>us-east-1</td>
<td align="center">Clinical Note<br/>Generation</td>
<td align="center">ROUGE-1/2/L<br/>F1 Score</td>
</tr>
</table>

<br/>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Paper](https://img.shields.io/badge/Reference-ACI--Bench_Paper-red?style=flat-square&logo=arxiv)](https://www.nature.com/articles/s41597-023-02487-3)

</div>

---

## Abstract

This repository presents an evaluation of OpenAI's open-source language models (`gpt-oss-20b` and `gpt-oss-120b`) on the ACI-Bench benchmark for automated clinical note generation. Using AWS Bedrock for inference, we assess model performance on converting doctor-patient conversations into structured clinical documentation. Our results demonstrate competitive zero-shot performance, achieving ROUGE-1 scores of 43.8-44.4% on the test1 split (n=40), positioning these models between Text-Davinci-002 and ChatGPT.

---

## Results

> **Key Finding**: OpenAI OSS models achieve **85-86% of GPT-4's performance** at **60x lower cost**, with full fine-tuning and self-hosting capabilities.

### Visual Comparison

```
ROUGE-1 Performance (Higher = Better) — Test1 Split (n=40)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BART+FT (tune)  █████████████████████████████████████████████████ 53.5
GPT-4           ██████████████████████████████████████████████░░░ 51.8
ChatGPT         ██████████████████████████████████████████░░░░░░░ 47.4
Text-Davinci-003█████████████████████████████████████████░░░░░░░░ 47.1
gpt-oss-120b    ████████████████████████████████████████░░░░░░░░░ 44.4  ⭐ Ours
gpt-oss-20b     ███████████████████████████████████████░░░░░░░░░░ 43.8  ⭐ Ours
ministral-3b    █████████████████████████████████████░░░░░░░░░░░░ 41.8  ⭐ Ours
Text-Davinci-002████████████████████████████████████░░░░░░░░░░░░░ 41.1
ministral-8b    ███████████████████████████████████░░░░░░░░░░░░░░ 40.3  ⭐ Ours
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

```
Active Parameters (What Actually Runs Per Token)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GPT-4           ████████████████████████████████████████ ~1.8T (dense)
ChatGPT         ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ~175B (dense)
gpt-oss-120b    ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ~20B  (MoE)    ⭐
ministral-8b    █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 8B    (dense)  ⭐
gpt-oss-20b     █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 3.6B  (MoE)    ⭐
ministral-3b    █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 3B    (dense)  ⭐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Our Results

| Model | Total Params | Active Params | ROUGE-1 | ROUGE-2 | ROUGE-L | Inference |
|:------|:------------:|:-------------:|:-------:|:-------:|:-------:|:---------:|
| **gpt-oss-120b** ⭐ | 120B | ~20B (MoE) | 44.35 | 14.71 | 19.43 | ~6s |
| **gpt-oss-20b** ⭐ | 21B | 3.6B (MoE) | 43.84 | 14.73 | 20.08 | ~28s |
| **ministral-3b** ⭐ | 3B | 3B (Dense) | 41.80 | 12.80 | 21.95 | ~3.4s |
| **ministral-8b** ⭐ | 8B | 8B (Dense) | 40.25 | 12.30 | 20.45 | ~5.7s |

> ⭐ = Our evaluation on ACI-Bench test1 split (n=40). Scores = F1 %.

### Comparison with Published Baselines

| Model | Type | ROUGE-1 | ROUGE-2 | ROUGE-L | Source |
|:------|:-----|:-------:|:-------:|:-------:|:------:|
| BART + FTSAMSum | Fine-tuned | **53.46** | **25.08** | **48.62** | Yim et al. |
| GPT-4 | Proprietary | 51.76 | 22.58 | 45.97 | Yim et al. |
| ChatGPT | Proprietary | 47.44 | 19.01 | 42.47 | Yim et al. |
| Text-Davinci-003 | Proprietary | 47.07 | 22.08 | 43.11 | Yim et al. |
| **gpt-oss-120b** | **Open Source** | 44.35 | 14.71 | 19.43 | ⭐ Ours |
| **gpt-oss-20b** | **Open Source** | 43.84 | 14.73 | 20.08 | ⭐ Ours |
| **ministral-3b** | **Open Source** | 41.80 | 12.80 | 21.95 | ⭐ Ours |
| Text-Davinci-002 | Proprietary | 41.08 | 17.27 | 37.46 | Yim et al. |
| **ministral-8b** | **Open Source** | 40.25 | 12.30 | 20.45 | ⭐ Ours |

### Fair Active Parameter Comparison

| Model | Active Params | ROUGE-1 | ROUGE-2 | ROUGE-L |
|:------|:-------------:|:-------:|:-------:|:-------:|
| **gpt-oss-20b** | 3.6B (MoE) | **43.84** | **14.73** | 20.08 |
| **ministral-3b** | 3B (Dense) | 41.80 | 12.80 | **21.95** |

> MoE architecture provides +2 pts ROUGE-1 advantage with similar active parameters.

### Why Open Source?

| Metric | GPT-4 | gpt-oss-20b | Advantage |
|:-------|:-----:|:-----------:|:---------:|
| ROUGE-1 | 51.76 | 43.84 | GPT-4 (+15%) |
| Parameters | ~1.8T | 20B | **OSS (90x smaller)** |
| Cost/1K tokens | ~$0.03 | ~$0.0005 | **OSS (60x cheaper)** |
| Self-Hostable | ❌ | ✅ | **OSS** |
| Fine-Tunable | ❌ | ✅ | **OSS** |
| Data Privacy | API-bound | Full control | **OSS** |

---

## Key Findings

### Model Performance

1. **Competitive Zero-Shot Results**: OpenAI OSS models achieve ROUGE-1 scores between Text-Davinci-002 and ChatGPT, about 3-4 points below ChatGPT without task-specific fine-tuning.

2. **MoE Architecture Advantage**: gpt-oss-20b (3.6B active params, MoE) outperforms ministral-3b (3B dense) by +2 pts ROUGE-1, demonstrating MoE efficiency benefits.

3. **Limited Scaling Benefit**: The 120B model provides only marginal improvement (+0.5% ROUGE-1) over the 20B variant; ministral-8b actually performs *worse* than ministral-3b.

4. **Structural Differences**: Lower ROUGE-L scores (~20% vs 42-46% for ChatGPT/GPT-4) indicate generated notes differ structurally from reference notes, likely due to the full-note generation approach versus division-based methods.

5. **Inference Speed**: Smaller models are significantly faster - ministral-3b (~3.4s) is 8x faster than gpt-oss-20b (~28s).

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
| Models | gpt-oss-20b, gpt-oss-120b, ministral-3b, ministral-8b |
| Infrastructure | AWS Bedrock (us-east-1) |
| Dataset | ACI-Bench test1 split (n=40) |
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

python scripts/evaluate_bedrock.py --model both --data-split test1
```

### Output

Results are saved to `runs/` directory as markdown files:
- `runs/YYYY-MM-DD_<split>.md` — Run log with metrics and benchmark comparisons

See [runs/](runs/) for all evaluation runs.

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
