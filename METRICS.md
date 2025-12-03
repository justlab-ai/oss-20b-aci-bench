# Evaluation Metrics

This document provides detailed explanations of the evaluation metrics used in this study for assessing clinical note generation quality.

## Table of Contents

1. [ROUGE Metrics](#rouge-metrics)
2. [Why ROUGE for Clinical Notes](#why-rouge-for-clinical-notes)
3. [Metric Interpretation](#metric-interpretation)
4. [Limitations](#limitations)
5. [Additional Metrics in Literature](#additional-metrics-in-literature)

---

## ROUGE Metrics

**ROUGE** (Recall-Oriented Understudy for Gisting Evaluation) is a family of metrics originally developed by Chin-Yew Lin (2004) for evaluating automatic summarization and machine translation. It measures the overlap between a system-generated text and reference text(s).

### ROUGE-1 (Unigram Overlap)

**Definition**: Measures the overlap of unigrams (single words) between the generated text and reference text.

**Formula**:
```
ROUGE-1 = (Number of overlapping unigrams) / (Total unigrams in reference)
```

**What it measures**:
- Content coverage at the word level
- Whether the generated note contains the same vocabulary as the reference
- High ROUGE-1 indicates the model captured similar content/topics

**Example**:
```
Reference: "Patient presents with chest pain and shortness of breath"
Generated: "Patient reports chest pain with difficulty breathing"

Overlapping unigrams: {Patient, chest, pain, with}
ROUGE-1 Recall = 4/9 = 0.44
```

### ROUGE-2 (Bigram Overlap)

**Definition**: Measures the overlap of bigrams (consecutive word pairs) between generated and reference texts.

**Formula**:
```
ROUGE-2 = (Number of overlapping bigrams) / (Total bigrams in reference)
```

**What it measures**:
- Fluency and phrase-level accuracy
- Whether word ordering and phrasing matches the reference
- More sensitive to grammatical structure than ROUGE-1

**Example**:
```
Reference: "chest pain and shortness of breath"
Generated: "chest pain with difficulty breathing"

Overlapping bigrams: {chest pain}
Reference bigrams: {chest pain, pain and, and shortness, shortness of, of breath}
ROUGE-2 Recall = 1/5 = 0.20
```

### ROUGE-L (Longest Common Subsequence)

**Definition**: Based on the Longest Common Subsequence (LCS) between the generated and reference texts. Unlike ROUGE-1/2, it does not require consecutive matches.

**Formula**:
```
ROUGE-L = LCS(generated, reference) / Length(reference)
```

**What it measures**:
- Sentence-level structural similarity
- Captures long-range word order without requiring contiguous matches
- More flexible than n-gram metrics

**Example**:
```
Reference: "The patient was prescribed medication for hypertension"
Generated: "The patient received medication to treat hypertension"

LCS: "The patient medication hypertension" (length 4)
ROUGE-L = 4/7 = 0.57
```

### F1 Score (Our Reported Metric)

We report **F1 scores** which balance precision and recall:

```
Precision = Overlap / Length(generated)
Recall = Overlap / Length(reference)
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

F1 is preferred because:
- Pure recall rewards overly verbose outputs
- Pure precision rewards overly terse outputs
- F1 balances both, rewarding appropriate length and content

---

## Why ROUGE for Clinical Notes

### Advantages

1. **Interpretability**: Easy to understand and explain to clinicians
2. **Reproducibility**: Deterministic computation, no model dependencies
3. **Speed**: Fast to compute, enabling large-scale evaluation
4. **Standard**: Widely used in NLP, enabling cross-study comparison

### Clinical Relevance

| ROUGE Variant | Clinical Interpretation |
|---------------|------------------------|
| ROUGE-1 | Does the note mention the right medical concepts? |
| ROUGE-2 | Are clinical phrases correctly formed? (e.g., "blood pressure", "chest pain") |
| ROUGE-L | Is the overall narrative structure preserved? |

---

## Metric Interpretation

### Score Ranges

| Score Range | Interpretation |
|-------------|----------------|
| 0.0 - 0.2 | Poor: Little overlap, likely missing key information |
| 0.2 - 0.4 | Fair: Some content captured, significant gaps |
| 0.4 - 0.6 | Good: Majority of content captured |
| 0.6 - 0.8 | Very Good: Strong alignment with reference |
| 0.8 - 1.0 | Excellent: Near-perfect match |

### Our Results in Context

| Metric | Our Score | Interpretation |
|--------|-----------|----------------|
| ROUGE-1: 0.45 | Good | ~45% of medical concepts captured |
| ROUGE-2: 0.15 | Fair | Phrase-level accuracy needs improvement |
| ROUGE-L: 0.21 | Fair | Structural similarity is moderate |

### Benchmark Context

Top-performing models on ACI-Bench achieve:
- ROUGE-1: ~0.53 (BART + FTSAMSum Division)
- ROUGE-2: ~0.25
- ROUGE-L: ~0.49

Our models perform competitively but have room for improvement, particularly in ROUGE-L (structural similarity).

---

## Limitations

### ROUGE Limitations

1. **Semantic Blindness**: ROUGE only measures lexical overlap
   - "The patient has hypertension" vs "The patient has high blood pressure"
   - These are semantically identical but have low ROUGE overlap

2. **No Factual Accuracy**: ROUGE cannot detect hallucinations
   - A note could have high ROUGE but contain fabricated information

3. **Reference Dependency**: Assumes reference is the gold standard
   - Multiple valid ways to write clinical notes
   - Penalizes equally valid alternative phrasings

4. **Length Sensitivity**: Very sensitive to verbosity differences

### Clinical-Specific Limitations

1. **Medical Terminology Variations**: Same concept, different terms
2. **Section Ordering**: ROUGE-L penalizes different but valid orderings
3. **Abbreviation Handling**: "HTN" vs "hypertension" treated as different

---

## Additional Metrics in Literature

The ACI-Bench paper and clinical NLP literature use additional metrics:

### BERTScore

**What it is**: Uses BERT embeddings to compute semantic similarity

**Advantage**: Captures semantic equivalence ("hypertension" ≈ "high blood pressure")

**Typical scores**: 0.70-0.85 for clinical note generation

### BLEURT

**What it is**: Learned evaluation metric trained on human judgments

**Advantage**: Better correlation with human quality assessments

**Typical scores**: 0.40-0.60 for clinical note generation

### MedCon (Medical Concept F1)

**What it is**: Extracts medical entities using UMLS and computes F1

**Advantage**: Directly measures clinical content accuracy

**Used in**: ACI-Bench evaluation

### Human Evaluation

**Gold standard** but expensive:
- Factual accuracy
- Completeness
- Clinical utility
- Readability

---

## References

1. Lin, C. Y. (2004). ROUGE: A package for automatic evaluation of summaries. *Text Summarization Branches Out*.

2. Zhang, T., et al. (2020). BERTScore: Evaluating text generation with BERT. *ICLR 2020*.

3. Sellam, T., et al. (2020). BLEURT: Learning robust metrics for text generation. *ACL 2020*.

4. Yim, W., et al. (2023). ACI-BENCH: A Novel Ambient Clinical Intelligence Dataset. *Scientific Data*.
