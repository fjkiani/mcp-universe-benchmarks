# Stress Report — mcp-universe-benchmarks

Total runs: **909**  
Category mix: {'baseline': 262, 'concurrency': 62, 'adversarial': 352, 'faults': 33, 'ratelimit': 200}

## Model leaderboard (baseline)

| Model | n | pass rate | pass@1 | pass@3 | pass@5 | p50 ms | p95 ms | p99 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini/gemma-4-31b-it | 8 | 0.50 | 0.50 | 1.00 | 1.00 | 122466 | 364459 | 410626 |
| gemini/gemma-4-26b-a4b-it | 8 | 0.50 | 0.50 | 1.00 | 1.00 | 125727 | 342469 | 349748 |
| gemini/gemini-2.5-flash | 82 | 0.07 | 0.05 | 0.82 | 1.00 | 7242 | 21888 | 29114 |
| gemini/gemini-2.5-flash-lite | 82 | 0.05 | 0.03 | 0.82 | 1.00 | 6744 | 9733 | 11208 |
| groq/openai/gpt-oss-20b | 41 | 0.02 | 0.03 | 1.00 | 1.00 | 6565 | 11193 | 11525 |
| groq/llama-3.3-70b-versatile | 103 | 0.00 | 0.00 | 0.97 | 0.97 | 2409 | 8988 | 9154 |
| openai/gpt-oss-20b:free | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 |
| nvidia/nemotron-3-nano-30b-a3b:free | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 |
| qwen/qwen3-coder:free | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 |
| meta-llama/llama-3.3-70b-instruct:free | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 |
| nvidia/nemotron-3-super-120b-a12b:free | 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 |

![Leaderboard](figures/leaderboard.png)

![Latency distribution](figures/latency_violin.png)

## Failure taxonomy (baseline)

![Failure heatmap](figures/failure_heatmap.png)

- **gemini/gemma-4-31b-it** — {'none': 4, 'wrong_answer': 2, 'refusal': 2}
- **gemini/gemma-4-26b-a4b-it** — {'wrong_answer': 2, 'none': 4, 'refusal': 2}
- **groq/llama-3.3-70b-versatile** — {'wrong_answer': 2, 'rate_limit': 39}
- **gemini/gemini-2.5-flash** — {'hallucination': 4, 'wrong_answer': 4, 'none': 6, 'rate_limit': 66, 'refusal': 2}
- **groq/openai/gpt-oss-20b** — {'rate_limit': 36, 'unknown_error': 2, 'hallucination': 2, 'none': 1}
- **gemini/gemini-2.5-flash-lite** — {'hallucination': 4, 'wrong_answer': 2, 'rate_limit': 72, 'none': 4}

## Robustness delta (perturbed vs baseline)

Negative Δ = perturbation hurt the model.

![Robustness](figures/robustness_delta.png)

| Model | Perturbation | n | baseline | perturbed | Δ |
|---|---|---:|---:|---:|---:|
| gemini/gemini-2.5-flash-lite | contradictory | 8 | 0.05 | 0.50 | +0.45 |
| gemini/gemini-2.5-flash-lite | gold_swap | 8 | 0.05 | 0.00 | -0.05 |
| gemini/gemini-2.5-flash-lite | noisy_prefix | 8 | 0.05 | 0.00 | -0.05 |
| gemini/gemini-2.5-flash-lite | prompt_injection | 8 | 0.05 | 0.38 | +0.33 |
| groq/llama-3.3-70b-versatile | contradictory | 8 | 0.00 | 0.12 | +0.12 |
| groq/llama-3.3-70b-versatile | gold_swap | 8 | 0.00 | 0.00 | +0.00 |
| groq/llama-3.3-70b-versatile | noisy_prefix | 8 | 0.00 | 0.00 | +0.00 |
| groq/llama-3.3-70b-versatile | prompt_injection | 8 | 0.00 | 0.12 | +0.12 |
| nvidia/nemotron-3-nano-30b-a3b:free | contradictory | 24 | 0.00 | 0.25 | +0.25 |
| nvidia/nemotron-3-nano-30b-a3b:free | gold_swap | 24 | 0.00 | 0.25 | +0.25 |
| nvidia/nemotron-3-nano-30b-a3b:free | noisy_prefix | 24 | 0.00 | 0.25 | +0.25 |
| nvidia/nemotron-3-nano-30b-a3b:free | prompt_injection | 24 | 0.00 | 0.25 | +0.25 |
| openai/gpt-oss-20b:free | contradictory | 24 | 0.00 | 0.25 | +0.25 |
| openai/gpt-oss-20b:free | gold_swap | 24 | 0.00 | 0.25 | +0.25 |
| openai/gpt-oss-20b:free | noisy_prefix | 24 | 0.00 | 0.25 | +0.25 |
| openai/gpt-oss-20b:free | prompt_injection | 24 | 0.00 | 0.25 | +0.25 |
| qwen/qwen3-coder:free | contradictory | 24 | 0.00 | 0.25 | +0.25 |
| qwen/qwen3-coder:free | gold_swap | 24 | 0.00 | 0.25 | +0.25 |
| qwen/qwen3-coder:free | noisy_prefix | 24 | 0.00 | 0.25 | +0.25 |
| qwen/qwen3-coder:free | prompt_injection | 24 | 0.00 | 0.25 | +0.25 |

## Load / concurrency

![Latency vs concurrency](figures/concurrency.png)

| concurrency | n | p50 ms | p95 ms | throughput rps |
|---:|---:|---:|---:|---:|
| 1 | 2 | 1858 | 2249 | 0.87 |
| 2 | 4 | 1686 | 2040 | 1.91 |
| 4 | 8 | 1608 | 1858 | 4.04 |
| 8 | 16 | 1880 | 2021 | 7.01 |
| 16 | 32 | 2716 | 3116 | 9.18 |

## Rate-limit probe

![Rate-limit](figures/ratelimit.png)

| Model | n | 429 hits | fraction | first-429 idx |
|---|---:|---:|---:|---:|
| meta-llama/llama-3.3-70b-instruct:free | 40 | 40 | 1.00 | 0 |
| nvidia/nemotron-3-nano-30b-a3b:free | 40 | 36 | 0.90 | 0 |
| nvidia/nemotron-3-super-120b-a12b:free | 40 | 37 | 0.93 | 0 |
| openai/gpt-oss-20b:free | 40 | 0 | 0.00 | None |
| qwen/qwen3-coder:free | 40 | 40 | 1.00 | 0 |

## Fault-injection resilience

Runs in category=`faults` had the MCP tool responses randomly corrupted (empty string, +3s delay, malformed JSON, simulated 500). Below: per-model pass rate under those conditions, and the injected fault-class hit counts observed.

![Fault injection](figures/faults.png)

| Model | n | passed | pass rate | tool calls | injected faults | recovered |
|---|---:|---:|---:|---:|---:|---:|
| llama-3.3-70b-versatile | 15 | 0 | 0.00 | 5 | 2 | 0 |
| openai/gpt-oss-20b:free | 18 | 0 | 0.00 | 1 | 0 | 0 |

### Fault-class hits

- **simulated_500**: 2

## Provenance

Raw runs: `runs.jsonl` (909 lines). See per-worker JSONLs under this directory.
