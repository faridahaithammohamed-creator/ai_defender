# In-Line White-Box Neuro-Probing for Real-Time AI Agent Security

**Author:** Farida Haitham Mohamed Amin  
**Date:** November 2026  

## Abstract
Autonomous AI Agents powered by Large Language Models (LLMs) face critical security vulnerabilities, including Direct Prompt Injection, Indirect Prompt Injection via external tools, and Unauthorized Tool Execution. Traditional black-box text classifiers introduce high latency and fail against obfuscated adversarial prompts. In this paper, we present `ai_defender`, a lightweight white-box neuro-probing framework that attaches non-intrusive forward hooks to intermediate transformer layers to monitor internal neural activations in real time. Evaluated on the unseen test split of the `deepset/prompt-injections` benchmark using `Qwen2.5-0.5B-Instruct`, our linear probe achieves **97.41% accuracy** (0.98 precision, 0.97 recall) with near-zero inference overhead.

## 1. Methodology
Instead of analyzing surface-level input tokens, `ai_defender` intercepts the residual stream hidden states $h_l \in \mathbb{R}^d$ at layer $l = -2$ during the standard forward pass. A trained lightweight linear classifier $f(h_l) = \sigma(W h_l + b)$ evaluates the threat probability prior to autoregressive token generation or external tool invocation.

## 2. Experimental Results
- **Dataset:** `deepset/prompt-injections` (546 training samples, 116 unseen test samples).
- **Target Model:** `Qwen/Qwen2.5-0.5B-Instruct`.
- **Performance:** 97.41% Test Accuracy, 0.97 Macro F1-Score.

## 3. Conclusion
White-box neuro-probing provides a fast, model-native defense layer capable of securing autonomous agentic workflows against prompt hijacking.
