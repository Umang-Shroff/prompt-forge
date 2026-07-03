# PromptForge

PromptForge is a production-oriented prompt optimization pipeline that improves prompt quality, reduces unnecessary tokens, and preserves semantic intent before a prompt is sent to an LLM.

Unlike simple regex-based prompt cleaners, PromptForge combines prompt analysis, intent detection, semantic optimization, and adaptive compression using Microsoft's **LongLLMLingua**.

---

# Features

- Prompt normalization
- Prompt type detection
- Intent detection
- Quality analysis
- Adaptive optimization pipeline
- Semantic regex optimizations
- Smart prompt chunking
- Importance-based chunk scoring
- LongLLMLingua compression
- Token statistics
- Compression reports
- Diagnostics and optimization history

---

# Pipeline

```
Raw Prompt
      │
      ▼
Normalization
      │
      ▼
Analysis
      │
      ▼
Intent Detection
      │
      ▼
Quality Evaluation
      │
      ▼
Semantic Optimization
      │
      ▼
Adaptive Compression
      │
      ▼
Optimized Prompt
```

---

# Optimization Stages

## 1. Normalization

The normalization stage standardizes the prompt before any optimization occurs.

Examples:

- normalize whitespace
- normalize punctuation
- normalize markdown
- normalize line endings
- preserve code formatting
- preserve structured formats

This prevents later stages from operating on inconsistent input.

---

## 2. Prompt Analysis

The analyzer identifies important characteristics including:

- prompt type
- programming languages
- markdown
- JSON
- XML
- SQL
- logs
- code blocks
- mixed prompts

Every later stage relies on this analysis.

---

## 3. Intent Detection

Rather than treating every prompt equally, PromptForge detects user intent.

Examples include:

- Explain
- Debug
- Plan
- Role
- Generate
- Analyze

Intent influences:

- optimization rules
- compression strength
- chunk importance
- preservation strategy

---

## 4. Quality Analysis

Prompt quality is evaluated using multiple dimensions.

Examples:

- clarity
- structure
- completeness
- specificity
- conciseness

The resulting score is later used to adapt compression.

---

## 5. Semantic Optimization

Several independent optimizers execute sequentially.

Examples:

- filler removal
- sentence simplification
- role optimization
- instruction optimization
- duplicate word removal
- repeated line removal

Each optimizer:

- operates independently
- has a priority
- can be enabled or disabled
- records changes in the optimization report

This modular design makes new optimizers easy to add.

---

# Adaptive Compression

PromptForge does not compress every prompt equally.

A compression profile is created for every prompt.

The profile considers:

- optimization mode
- detected intent
- prompt quality
- prompt size
- code
- markdown
- JSON
- XML
- protected keywords

This profile determines:

- target compression ratio
- preservation strategy
- filtering behaviour
- LLMLingua configuration

---

# Smart Chunking

Large prompts are divided into semantic chunks before compression.

Chunk boundaries prioritize:

- paragraphs
- sections
- markdown blocks
- lists
- sentences

This allows compression decisions to be made at the semantic level instead of treating the prompt as one large block.

---

# Importance Scoring

Every chunk receives an importance score.

The score considers:

- prompt intent
- chunk position
- instructions
- role definitions
- reasoning
- output requirements
- requirements
- code
- structured formats
- markdown
- lists
- examples
- chunk length

Higher scoring chunks are preserved more aggressively during compression.

---

# LongLLMLingua Integration

Compression is performed using Microsoft's LongLLMLingua.

PromptForge dynamically configures:

- compression rate
- target tokens
- context filtering
- token filtering
- sentence filtering
- chunk importance
- compression permissions
- protected keywords

This produces significantly better results than fixed compression settings.

---

# Safety

PromptForge avoids destructive optimizations.

Special handling exists for:

- Python
- Java
- JavaScript
- JSON
- XML
- SQL
- Markdown
- Logs

Compression is automatically reduced when structural integrity is more important than token reduction.

---

# Architecture

The project is intentionally modular.

```
core/
    pipeline
    stages

engines/
    analysis
    compression
    optimization

models/
    shared data models

cli/
    terminal interface

service/
    optimization service
```

Every major component has a single responsibility.

---

# Emphasis given to

- Preserve semantics before reducing tokens
- Prefer adaptive behaviour over fixed rules
- Separate analysis from optimization
- Keep optimizers modular
- Protect structured formats
- Record every optimization step
- Fail safely when compression cannot be applied

---

# Technologies

- Python
- LongLLMLingua
- Hugging Face Transformers
- PyTorch
- Rich
- Dataclasses
