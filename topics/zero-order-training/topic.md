---
schema_version: 1
id: zero-order-training
type: topic
title: Zero-order training and pretraining
name: Zero-order training and pretraining
summary: Gradient-free and backpropagation-free training of neural networks and foundation models.
status: active
permalink: /topics/zero-order-training/
---

# Zero-order training and pretraining

## Objective

Track credible research on training neural networks and foundation models without standard backpropagated weight gradients, with particular attention to whether methods can scale to meaningful pretraining workloads.

## Core research question

Which gradient-free, forward-only, or perturbation-based training methods deliver useful quality, compute efficiency, memory efficiency, or scaling behavior relative to strong gradient-based baselines?

## Include

- New methods, theory, experiments, negative results, replications, and substantive revisions about zero-order or backpropagation-free **training** of neural networks.
- Pretraining and fine-tuning of language models or other foundation models using these methods.
- Activation, parameter, or directional perturbation methods; SPSA, MeZO, and related estimators when they train model parameters.
- Efficiency analyses with clear accounting for forward passes, memory, wall time, hardware, and model scale.
- Code and project releases that materially change reproducibility or understanding of an included method.

## Exclude

- Black-box optimization unrelated to neural-network training, unless it establishes a directly transferable result.
- Inference-only, prompting-only, or architecture-only work with no relevant training method.
- Purely gradient-based optimization papers without a meaningful comparison or connection.
- Duplicated versions without a substantive change; record an update to the existing finding instead.
- Promotional claims lacking enough method or result detail to assess. A substantive first-party technical report can qualify even without peer review.

## Search vocabulary

Core terms: zeroth-order optimization, zero-order optimization, ZO training, ZO fine-tuning, gradient-free training, derivative-free training, backpropagation-free training, forward-only learning, forward gradient, activation perturbation, parameter perturbation, simultaneous perturbation stochastic approximation, SPSA, MeZO, memory-efficient ZO, parameter-efficient ZO.

Synonyms and variants: no-backprop training, training without backpropagation, perturbation-based learning, evolution strategies for neural network training, black-box gradient estimation. Combine broad terms with `neural network`, `transformer`, `language model`, `pretraining`, or `fine-tuning` to control noise.

These terms are starting points, not an exhaustive query list. Follow citations, new terminology, and relevant work found outside `web/_data/sources.yml`; apply the inclusion and relevance rules above to every candidate.

Adjacent topics: local learning rules, feedback alignment, synthetic gradients, evolution strategies, low-memory training, forward-mode automatic differentiation, hardware-constrained training, and biologically motivated learning. Include adjacent work only when it informs the core research question.

## Relevance levels

- **High:** Directly tests or advances zero-order/backpropagation-free training or pretraining of neural networks; central to the topic.
- **Medium:** Closely adjacent method or analysis with a plausible, explicit implication for zero-order training.
- **Low:** Peripheral context worth retaining for later comparison, but no immediate methodological contribution to the core question.

## Eligible release types

arXiv preprints, OpenReview submissions, accepted conference papers, journal papers, technical reports, lab and institutional research pages, and substantial code or project releases. Publication type and evidence maturity must be stated separately.
