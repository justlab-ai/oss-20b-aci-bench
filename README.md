# OpenAI OSS Model Evaluation on ACI-Bench

Evaluation of OpenAI's open-source models (gpt-oss-20b and gpt-oss-120b) on the ACI-Bench clinical note generation benchmark using AWS Bedrock.

## Overview

This repository contains evaluation results and analysis of OpenAI's open-source language models on the task of **Ambient Clinical Intelligence (ACI)** - automatically generating structured clinical notes from doctor-patient conversations.

## Repository Structure

```
├── README.md                 # This file
├── METHODOLOGY.md            # Detailed methodology and experimental setup
├── METRICS.md                # Explanation of evaluation metrics
├── FINDINGS.md               # Detailed findings and analysis
├── results/
│   ├── gpt-oss-20b_results.json
│   ├── gpt-oss-120b_results.json
│   └── comparison_results.json
└── scripts/
    └── evaluate_bedrock.py   # Evaluation script
```

## Quick Results

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L |
|-------|---------|---------|---------|
| gpt-oss-20b | 0.4503 | 0.1518 | 0.2133 |
| gpt-oss-120b | 0.4589 | 0.1515 | 0.1930 |

## Citation

If you use this work, please cite:

```bibtex
@misc{oss20b-aci-bench-2024,
  title={Evaluation of OpenAI OSS Models on ACI-Bench},
  author={JustLab},
  year={2024},
  url={https://github.com/justlab/oss-20b-aci-bench}
}
```

## References

- Yim, W., et al. (2023). ACI-BENCH: A Novel Ambient Clinical Intelligence Dataset for Benchmarking Automatic Visit Note Generation. *Scientific Data*, 10(1), 586.
- [ACI-Bench GitHub Repository](https://github.com/wyim/aci-bench)

## License

MIT License

## Date

December 3, 2024
