# Prompt Style Guide

## 1. Alpaca Prompt Format

**Mainly used by:** Alpaca, OpenLLaMA, and various open-source models

### Structure:

```
### Instruction:
<SYSTEM_PROMPT>

### Input:
<USER_QUERY>

### Response:
```

### Example:

```
### Instruction:
You are an expert in mathematics. Answer only questions related to mathematics.

### Input:
Hey, can you help me solve (a + b)²?

### Response:
(a + b)² = a² + 2ab + b²

This is the algebraic expansion of a binomial squared, where:
- a² is the first term squared
- 2ab is twice the product of both terms
- b² is the second term squared
```

---

## 2. ChatML Prompt Format

**Mainly used by:** ChatGPT, OpenAI, Groq, Mistral, and most modern chat-based models

### Structure:

```json
[
  {
    "role": "system",
    "content": "<SYSTEM_PROMPT>"
  },
  {
    "role": "user",
    "content": "<USER_QUERY>"
  },
  {
    "role": "assistant",
    "content": "<MODEL_RESPONSE>"
  }
]
```

### Example:

```json
[
  {
    "role": "system",
    "content": "You are an expert in mathematics. Answer only questions related to mathematics."
  },
  {
    "role": "user",
    "content": "Hey, can you help me solve (a + b)²?"
  },
  {
    "role": "assistant",
    "content": "(a + b)² = a² + 2ab + b²\n\nThis is the algebraic expansion of a binomial squared."
  }
]
```

---

## 3. INST Prompting Format

**Mainly used by:** Llama 2, Llama 3, and Meta's language models

### Structure:

```
[INST] <SYSTEM_PROMPT>

<USER_QUERY> [/INST]
```

### Example:

```
[INST] You are an expert in mathematics. Answer only questions related to mathematics.

Hey, can you help me solve (a + b)²? [/INST]

(a + b)² = a² + 2ab + b²

This is the algebraic expansion of a binomial squared, where:
- a² is the first term squared
- 2ab is twice the product of both terms
- b² is the second term squared
```

### Multi-turn Example:

```
[INST] You are an expert in mathematics. Answer only questions related to mathematics.

What is (a + b)²? [/INST]

(a + b)² = a² + 2ab + b²

[INST] Can you explain why? [/INST]

This comes from the distributive property: (a + b)² = (a + b)(a + b) = a·a + a·b + b·a + b·b = a² + 2ab + b²
```

Choose the format based on which model you're using to ensure optimal performance and compatibility.
