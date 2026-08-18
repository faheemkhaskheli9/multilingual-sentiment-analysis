# Architecture Notes: Multilingual Sentiment Analysis

## Pipeline

```text
Multilingual Text -> Preprocessing -> Classical Baseline vs Transformer Model -> Sentiment Label -> Comparison Report
```

## Components

- English sentiment analysis
- Spanish sentiment analysis
- Additional language support
- Classical NLP baseline
- Transformer-based comparison

## Design Notes

- Keep provider/model choices swappable behind interfaces (see `multi-llm-router`
  and similar projects in this portfolio for the general pattern).
- Prefer configuration-driven pipelines (YAML/JSON in `configs/`) over hardcoded
  parameters so experiments are reproducible.
