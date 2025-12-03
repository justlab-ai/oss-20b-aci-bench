# Findings and Analysis

This document presents detailed findings from our evaluation of OpenAI OSS models on the ACI-Bench clinical note generation benchmark.

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Quantitative Results](#quantitative-results)
3. [Comparison with Baselines](#comparison-with-baselines)
4. [Analysis](#analysis)
5. [Discussion](#discussion)
6. [Recommendations](#recommendations)

---

## Executive Summary

### Key Findings

1. **Competitive Performance**: Both OpenAI OSS models achieve ROUGE-1 scores around 0.45, competitive with base BART models but below state-of-the-art division-based approaches.

2. **Minimal Scaling Benefit**: The 120B model shows only marginal improvement (+0.86% ROUGE-1) over the 20B model despite 6x more parameters.

3. **Speed-Size Tradeoff**: Counterintuitively, the 120B model was 4x faster than the 20B model in our tests.

4. **ROUGE-L Gap**: Both models show notably lower ROUGE-L scores compared to baselines, suggesting structural differences in generated notes.

---

## Quantitative Results

### Primary Results

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L | Samples | Failures |
|-------|---------|---------|---------|---------|----------|
| gpt-oss-20b | 0.4503 | 0.1518 | 0.2133 | 20 | 1 |
| gpt-oss-120b | 0.4589 | 0.1515 | 0.1930 | 20 | 0 |

### Per-Metric Analysis

#### ROUGE-1 (Content Coverage)
- **20B**: 0.4503 (45.03% unigram overlap)
- **120B**: 0.4589 (45.89% unigram overlap)
- **Difference**: +0.0086 (+1.9% relative improvement)

**Interpretation**: Both models capture approximately 45% of the medical vocabulary from reference notes. This suggests reasonable content extraction from dialogues.

#### ROUGE-2 (Phrase Accuracy)
- **20B**: 0.1518 (15.18% bigram overlap)
- **120B**: 0.1515 (15.15% bigram overlap)
- **Difference**: -0.0003 (negligible)

**Interpretation**: Low bigram overlap indicates the models use different phrasing than the reference notes. This is expected for zero-shot generation without exposure to the specific writing style.

#### ROUGE-L (Structural Similarity)
- **20B**: 0.2133 (21.33% LCS-based similarity)
- **120B**: 0.1930 (19.30% LCS-based similarity)
- **Difference**: -0.0203 (-9.5% relative)

**Interpretation**: The 20B model actually outperforms 120B on structural similarity. The 120B model may generate longer or differently structured notes.

---

## Comparison with Baselines

### Full Comparison Table

| Rank | Model | ROUGE-1 | ROUGE-2 | ROUGE-L | Notes |
|------|-------|---------|---------|---------|-------|
| 1 | BART + FTSAMSum (Division) | **53.46** | **25.08** | **48.62** | Fine-tuned, division-based |
| 2 | GPT-4 | 51.76 | 22.58 | 45.97 | Proprietary |
| 3 | BART (Division) | 51.56 | 24.06 | 45.92 | Division-based |
| 4 | BioBART (Division) | 49.53 | 22.47 | 44.92 | Domain-specific |
| 5 | ChatGPT | 47.44 | 19.01 | 42.47 | Proprietary |
| 6 | Text-Davinci-003 | 47.07 | 22.08 | 43.11 | Proprietary |
| 7 | **gpt-oss-120b (Ours)** | 45.89 | 15.15 | 19.30 | Zero-shot, full-note |
| 8 | **gpt-oss-20b (Ours)** | 45.03 | 15.18 | 21.33 | Zero-shot, full-note |
| 9 | BART | 41.76 | 19.20 | 34.70 | Full-note |
| 10 | Text-Davinci-002 | 41.08 | 17.27 | 37.46 | Proprietary |
| 11 | LED (Division) | 34.15 | 8.01 | 29.80 | Long-context |
| 12 | LED | 28.37 | 5.52 | 22.78 | Long-context |

### Visual Comparison

```
ROUGE-1 Scores (Higher is Better)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BART+FTSAMSum(Div) ████████████████████████████████████████ 53.46
GPT-4              ███████████████████████████████████████  51.76
ChatGPT            ███████████████████████████████████      47.44
gpt-oss-120b       ██████████████████████████████████       45.89
gpt-oss-20b        █████████████████████████████████        45.03
BART               ██████████████████████████████           41.76
LED                ████████████████████                     28.37
```

### Gap Analysis

| Comparison | ROUGE-1 Gap | Explanation |
|------------|-------------|-------------|
| vs GPT-4 | -5.87 | Proprietary model advantage |
| vs BART+FTSAMSum(Div) | -7.57 | Fine-tuning + division approach |
| vs ChatGPT | -1.55 | Comparable with prompt optimization |
| vs BART (base) | +4.13 | OSS models outperform base BART |

---

## Analysis

### Why Is ROUGE-L So Low?

Our models show disproportionately low ROUGE-L scores (0.19-0.21) compared to baselines (0.43-0.49). Possible explanations:

1. **Different Note Structure**: Generated notes may organize information differently than references
2. **Verbosity**: More verbose outputs dilute LCS scores
3. **Section Ordering**: Different ordering of clinical sections
4. **Full-Note Approach**: Division-based approaches naturally align section-by-section

### Model Size vs Performance

| Metric | 20B | 120B | 120B Advantage |
|--------|-----|------|----------------|
| ROUGE-1 | 0.4503 | 0.4589 | +1.9% |
| ROUGE-2 | 0.1518 | 0.1515 | -0.2% |
| ROUGE-L | 0.2133 | 0.1930 | -9.5% |
| Speed | ~50s/sample | ~12s/sample | **4x faster** |

**Finding**: The 6x parameter increase provides minimal quality benefit. The 20B model is actually preferable considering:
- Better ROUGE-L score
- Comparable ROUGE-1/2
- Lower cost (smaller model)

### Error Analysis

One sample (5%) failed for gpt-oss-20b due to timeout. This suggests:
- 20B model has higher latency variance
- Longer dialogues may cause timeouts
- Production systems need robust retry logic

---

## Discussion

### Strengths of OpenAI OSS Models

1. **Out-of-box Capability**: Reasonable performance without fine-tuning
2. **Medical Knowledge**: Captures clinical concepts despite no medical fine-tuning
3. **Structured Output**: Generates properly formatted clinical notes
4. **Enterprise Ready**: Available via AWS Bedrock for healthcare compliance

### Limitations Observed

1. **Phrasing Differences**: Low ROUGE-2 indicates different writing style
2. **Structural Variations**: Low ROUGE-L suggests different note organization
3. **No Medical Validation**: ROUGE doesn't verify clinical accuracy
4. **Zero-shot Ceiling**: Performance limited without task-specific tuning

### Comparison with Prior Work

| Study | Best Model | ROUGE-1 | Our Gap |
|-------|------------|---------|---------|
| ACI-Bench (Yim 2023) | BART+FTSAMSum(Div) | 53.46 | -7.57 |
| Same study | GPT-4 | 51.76 | -5.87 |
| Same study | ChatGPT | 47.44 | -1.55 |

Our zero-shot OSS models are within 2 ROUGE-1 points of ChatGPT, suggesting strong baseline capability.

---

## Recommendations

### For Practitioners

1. **Use gpt-oss-20b** for cost-effective deployment
2. **Implement division-based generation** for higher quality
3. **Add few-shot examples** from training set to improve phrasing
4. **Validate outputs clinically** before production use

### For Researchers

1. **Fine-tune on ACI-Bench training set** to close the gap with BART+FTSAMSum
2. **Evaluate with BERTScore/BLEURT** for semantic similarity
3. **Conduct human evaluation** for clinical accuracy
4. **Test division-based prompting** for structural improvement

### Suggested Improvements

| Improvement | Expected Impact | Effort |
|-------------|-----------------|--------|
| Division-based prompting | +5-10 ROUGE-1 | Low |
| Few-shot examples | +2-5 ROUGE-1 | Low |
| Fine-tuning | +5-8 ROUGE-1 | High |
| Ensemble methods | +1-3 ROUGE-1 | Medium |

---

## Conclusion

OpenAI's OSS models demonstrate competitive zero-shot performance on clinical note generation, achieving ROUGE-1 scores within 2 points of ChatGPT and outperforming base BART models. However, significant gaps remain compared to fine-tuned and division-based approaches.

The minimal benefit of scaling from 20B to 120B parameters suggests that task-specific adaptations (fine-tuning, prompting strategies) are more impactful than raw model size for this domain.

**Bottom Line**: OpenAI OSS models are viable for clinical note generation with appropriate post-processing and validation, but should not replace fine-tuned domain-specific models in production healthcare settings without further evaluation.

---

## Appendix: Raw Results

### gpt-oss-20b Detailed Metrics

```json
{
  "model": "openai.gpt-oss-20b-1:0",
  "num_samples": 20,
  "num_successful": 19,
  "metrics": {
    "rouge1": 0.4503,
    "rouge2": 0.1518,
    "rougeL": 0.2133
  }
}
```

### gpt-oss-120b Detailed Metrics

```json
{
  "model": "openai.gpt-oss-120b-1:0",
  "num_samples": 20,
  "num_successful": 20,
  "metrics": {
    "rouge1": 0.4589,
    "rouge2": 0.1515,
    "rougeL": 0.1930
  }
}
```
