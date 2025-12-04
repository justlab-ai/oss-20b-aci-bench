#!/usr/bin/env python3
"""
Evaluate OpenAI OSS models on ACI-Bench using AWS Bedrock.

Usage:
    python evaluation/evaluate_bedrock.py --model both --data-split valid
    python evaluation/evaluate_bedrock.py --model gpt-oss-20b --data-split valid
    python evaluation/evaluate_bedrock.py --model gpt-oss-120b --data-split test1
"""

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm

# Try to import rouge_score, provide helpful message if not installed
try:
    from rouge_score import rouge_scorer
except ImportError:
    print("Please install rouge-score: pip install rouge-score")
    exit(1)


# Model configurations
MODELS = {
    "gpt-oss-20b": "openai.gpt-oss-20b-1:0",
    "gpt-oss-120b": "openai.gpt-oss-120b-1:0",
    "ministral-3b": "mistral.ministral-3-3b-instruct",
    "ministral-8b": "mistral.ministral-3-8b-instruct",
}

# Data split configurations
DATA_SPLITS = {
    "train": "train.json",
    "valid": "valid.json",
    "test1": "clinicalnlp_taskB_test1.json",
    "test2": "clinicalnlp_taskC_test2.json",
    "test3": "clef_taskC_test3.json",
}

# System prompt for clinical note generation
SYSTEM_PROMPT = """You are a medical scribe assistant. Your task is to convert a doctor-patient conversation into a structured clinical note.

The clinical note should include:
- CHIEF COMPLAINT: The main reason for the visit
- HISTORY OF PRESENT ILLNESS: Detailed description of the current problem
- REVIEW OF SYSTEMS: Relevant symptoms mentioned
- PHYSICAL EXAMINATION: Any examination findings discussed
- ASSESSMENT AND PLAN: Diagnosis and treatment plan

Generate a professional clinical note based on the conversation provided. Be concise but thorough."""


def load_aci_bench_data(data_dir: str, split: str) -> List[Dict]:
    """Load ACI-Bench data from JSON file."""
    data_path = Path(data_dir) / "challenge_data_json" / DATA_SPLITS[split]

    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    with open(data_path, 'r') as f:
        data = json.load(f)

    return data['data']


def call_bedrock_model(
    client,
    model_id: str,
    dialogue: str,
    max_retries: int = 3,
    retry_delay: float = 2.0
) -> Optional[str]:
    """Call Bedrock model to generate clinical note from dialogue."""

    prompt = f"{SYSTEM_PROMPT}\n\nDoctor-Patient Conversation:\n{dialogue}\n\nClinical Note:"

    # Build request body based on model provider
    if model_id.startswith("mistral."):
        # Mistral models use a different format
        request_body = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1024,
            "temperature": 0.3,
        }
    else:
        # OpenAI models on Bedrock
        request_body = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1024,
            "temperature": 0.3,
        }

    for attempt in range(max_retries):
        try:
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body),
                contentType="application/json",
                accept="application/json"
            )

            response_body = json.loads(response['body'].read())

            # Extract generated text from response based on provider
            if 'choices' in response_body:
                # OpenAI and Mistral format
                return response_body['choices'][0]['message']['content']
            elif 'content' in response_body:
                # Anthropic format
                return response_body['content'][0]['text']
            elif 'outputs' in response_body:
                # Some Mistral models
                return response_body['outputs'][0]['text']
            else:
                print(f"Unexpected response format: {response_body.keys()}")
                return str(response_body)

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ThrottlingException':
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    print(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"Max retries exceeded for throttling")
                    return None
            else:
                print(f"Bedrock error: {e}")
                return None
        except Exception as e:
            print(f"Error calling model: {e}")
            return None

    return None


def calculate_rouge_scores(predictions: List[str], references: List[str]) -> Dict:
    """Calculate ROUGE scores between predictions and references."""
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    scores = {
        'rouge1': [],
        'rouge2': [],
        'rougeL': []
    }

    for pred, ref in zip(predictions, references):
        if pred and ref:
            result = scorer.score(ref, pred)
            scores['rouge1'].append(result['rouge1'].fmeasure)
            scores['rouge2'].append(result['rouge2'].fmeasure)
            scores['rougeL'].append(result['rougeL'].fmeasure)

    # Calculate averages
    avg_scores = {
        'rouge1': sum(scores['rouge1']) / len(scores['rouge1']) if scores['rouge1'] else 0,
        'rouge2': sum(scores['rouge2']) / len(scores['rouge2']) if scores['rouge2'] else 0,
        'rougeL': sum(scores['rougeL']) / len(scores['rougeL']) if scores['rougeL'] else 0,
    }

    return avg_scores, scores


def evaluate_model(
    client,
    model_name: str,
    model_id: str,
    data: List[Dict],
    output_dir: Path
) -> Dict:
    """Evaluate a single model on the dataset."""

    print(f"\n{'='*60}")
    print(f"Evaluating: {model_name} ({model_id})")
    print(f"{'='*60}")

    predictions = []
    references = []
    results_detail = []

    for i, sample in enumerate(tqdm(data, desc=f"Processing {model_name}")):
        dialogue = sample['src']
        reference = sample['tgt']
        file_id = sample.get('file', f'sample_{i}')

        # Generate prediction
        prediction = call_bedrock_model(client, model_id, dialogue)

        if prediction:
            predictions.append(prediction)
            references.append(reference)
            results_detail.append({
                'file': file_id,
                'dialogue': dialogue[:500] + '...' if len(dialogue) > 500 else dialogue,
                'reference': reference,
                'prediction': prediction
            })
        else:
            print(f"Failed to generate for sample {i}")
            predictions.append("")
            references.append(reference)
            results_detail.append({
                'file': file_id,
                'dialogue': dialogue[:500] + '...' if len(dialogue) > 500 else dialogue,
                'reference': reference,
                'prediction': "[FAILED]"
            })

        # Small delay to avoid rate limiting
        time.sleep(0.5)

    # Calculate ROUGE scores
    avg_scores, all_scores = calculate_rouge_scores(predictions, references)

    # Prepare results
    results = {
        'model': model_id,
        'model_name': model_name,
        'num_samples': len(data),
        'num_successful': len([p for p in predictions if p]),
        'timestamp': datetime.now().isoformat(),
        'metrics': avg_scores,
        'per_sample_scores': {
            'rouge1': all_scores['rouge1'],
            'rouge2': all_scores['rouge2'],
            'rougeL': all_scores['rougeL']
        },
        'predictions': results_detail
    }

    # Save results
    output_file = output_dir / f"{model_name}_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults for {model_name}:")
    print(f"  ROUGE-1: {avg_scores['rouge1']:.4f}")
    print(f"  ROUGE-2: {avg_scores['rouge2']:.4f}")
    print(f"  ROUGE-L: {avg_scores['rougeL']:.4f}")
    print(f"  Saved to: {output_file}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Evaluate OpenAI OSS models on ACI-Bench")
    parser.add_argument(
        "--model",
        type=str,
        default="both",
        choices=["gpt-oss-20b", "gpt-oss-120b", "ministral-3b", "ministral-8b", "both", "ministral"],
        help="Which model to evaluate"
    )
    parser.add_argument(
        "--data-split",
        type=str,
        default="valid",
        choices=["train", "valid", "test1", "test2", "test3"],
        help="Which data split to use"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="raw_data/aci_bench/data",
        help="Path to ACI-Bench data directory"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="evaluation/results",
        help="Output directory for results"
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Maximum number of samples to evaluate (for testing)"
    )

    args = parser.parse_args()

    # Setup paths
    script_dir = Path(__file__).parent.parent
    data_dir = script_dir / args.data_dir
    output_dir = script_dir / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    print(f"Loading ACI-Bench {args.data_split} split...")
    data = load_aci_bench_data(data_dir, args.data_split)

    if args.max_samples:
        data = data[:args.max_samples]

    print(f"Loaded {len(data)} samples")

    # Initialize Bedrock client
    print("Initializing Bedrock client...")
    client = boto3.client('bedrock-runtime', region_name='us-east-1')

    # Determine which models to evaluate
    models_to_eval = []
    if args.model == "both":
        models_to_eval = [(k, v) for k, v in MODELS.items() if k.startswith("gpt-oss")]
    elif args.model == "ministral":
        models_to_eval = [(k, v) for k, v in MODELS.items() if k.startswith("ministral")]
    else:
        models_to_eval = [(args.model, MODELS[args.model])]

    # Run evaluations
    all_results = []
    for model_name, model_id in models_to_eval:
        results = evaluate_model(client, model_name, model_id, data, output_dir)
        all_results.append(results)

    # Save comparison results
    if len(all_results) > 1:
        comparison = {
            'data_split': args.data_split,
            'num_samples': len(data),
            'timestamp': datetime.now().isoformat(),
            'models': {}
        }

        for result in all_results:
            comparison['models'][result['model_name']] = result['metrics']

        comparison_file = output_dir / "comparison_results.json"
        with open(comparison_file, 'w') as f:
            json.dump(comparison, f, indent=2)

        print(f"\n{'='*60}")
        print("COMPARISON SUMMARY")
        print(f"{'='*60}")
        print(f"{'Model':<20} {'ROUGE-1':<10} {'ROUGE-2':<10} {'ROUGE-L':<10}")
        print("-" * 50)
        for result in all_results:
            m = result['metrics']
            print(f"{result['model_name']:<20} {m['rouge1']:<10.4f} {m['rouge2']:<10.4f} {m['rougeL']:<10.4f}")
        print(f"\nComparison saved to: {comparison_file}")


if __name__ == "__main__":
    main()
