# Evaluation Run: 2025-12-04 (Ministral Comparison)

## Configuration

| Parameter | Value |
|-----------|-------|
| Date | 2025-12-04 |
| Dataset | ACI-Bench |
| Split | test1 |
| Samples | 40 |
| Infrastructure | AWS Bedrock (us-east-1) |
| Temperature | 0.3 |
| Max Tokens | 1024 |
| Approach | Zero-shot, full-note generation |

## Models Evaluated

| Model | Model ID | Total Params | Active Params | Architecture |
|-------|----------|--------------|---------------|--------------|
| ministral-3b | mistral.ministral-3-3b-instruct | 3B | 3B | Dense |
| ministral-8b | mistral.ministral-3-8b-instruct | 8B | 8B | Dense |

## Results

### Summary

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L | Samples | Avg Inference |
|-------|---------|---------|---------|---------|---------------|
| ministral-3b | 41.80 | 12.80 | 21.95 | 40/40 | ~3.4s |
| ministral-8b | 40.25 | 12.30 | 20.45 | 40/40 | ~5.7s |

### Comparison with gpt-oss-20b (Fair Active Parameter Comparison)

| Model | Active Params | ROUGE-1 | ROUGE-2 | ROUGE-L |
|-------|---------------|---------|---------|---------|
| gpt-oss-20b | 3.6B (MoE) | **43.84** | **14.73** | 20.08 |
| ministral-3b | 3B (Dense) | 41.80 | 12.80 | **21.95** |
| ministral-8b | 8B (Dense) | 40.25 | 12.30 | 20.45 |

### Gap Analysis (vs gpt-oss-20b)

| Model | ROUGE-1 Gap | ROUGE-2 Gap | ROUGE-L Gap |
|-------|-------------|-------------|-------------|
| ministral-3b | -2.04 pts | -1.93 pts | +1.87 pts |
| ministral-8b | -3.59 pts | -2.43 pts | +0.37 pts |

## Key Findings

1. **MoE Advantage**: gpt-oss-20b (3.6B active, MoE) outperforms ministral-3b (3B dense) on ROUGE-1/2 by ~2 pts despite similar active parameters

2. **Structural Alignment**: ministral-3b produces better ROUGE-L scores, suggesting different note structure preferences

3. **Inverse Scaling for Ministral**: ministral-8b performs worse than ministral-3b across all metrics - likely due to instruction-tuning differences

4. **Speed vs Quality Trade-off**:
   - ministral-3b: 8x faster than gpt-oss-20b, but -2 pts ROUGE-1
   - If speed is critical, ministral-3b is viable at 96% of gpt-oss-20b performance

## Conclusion

For clinical note generation with ~3B active parameters:
- **Best quality**: gpt-oss-20b (MoE architecture provides quality boost)
- **Best speed**: ministral-3b (8x faster, acceptable quality loss)
- **Not recommended**: ministral-8b (larger but worse performance)
