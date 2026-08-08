# Prompt Engineering Notes

---

# RTCFO Framework

RTCFO is a simple framework for writing better AI prompts.

| Letter | Meaning       | Description                                          |
| ------ | ------------- | ---------------------------------------------------- |
| **R**  | **Role**      | Tell the AI who it should act as.                    |
| **T**  | **Task**      | Tell the AI exactly what it should do.               |
| **C**  | **Context**   | Provide background information or necessary details. |
| **F**  | **Format**    | Specify how the output should be presented.          |
| **O**  | **Objective** | Explain the final goal or why you're asking.         |

## Example

```text
Role:
You are a senior software engineer.

Task:
Explain JWT authentication.

Context:
I know basic Express.js but I'm new to authentication.

Format:
Markdown with examples.

Objective:
Help me prepare for backend interviews.
```

---

# Prompting Techniques

## 1. Zero-Shot Prompting

The model is given a direct instruction or task without any prior examples.

### Example

```text
Translate this sentence into French.

Hello, how are you?
```

**Best for:**

- Simple tasks
- Well-known problems
- Modern LLMs (GPT, Claude, Gemini)

---

## 2. One-Shot Prompting

One-shot prompting provides **exactly one example** before asking the model to perform the actual task. The example teaches the model the expected pattern, format, or behavior.

### Example

```text
Determine whether each customer review has a positive or negative sentiment.

Example

Input:
The phone has an amazing camera and battery life.

Output:
Positive

Now classify the following review.

The app crashes every time I open it.
```

---

## 3. Few-Shot Prompting

Few-shot prompting provides **multiple examples** before asking the model to solve a similar task. The additional examples help the model learn patterns, formatting, and expected behavior.

### Example

```text
Determine whether each customer review has a positive or negative sentiment.

Example 1

Input:
The laptop is fast and lightweight.

Output:
Positive

Example 2

Input:
The battery drains within an hour.

Output:
Negative

Example 3

Input:
The display is bright and the speakers sound great.

Output:
Positive

Now classify the following review.

The keyboard feels cheap and several keys stopped working after a week.
```

### Best for

- Classification
- Information extraction
- Custom formatting
- Maintaining consistent responses
- Domain-specific tasks

---

## 4. Persona Prompting (Role Prompting)

Persona prompting assigns the model a specific role, expertise, or communication style. This helps guide the tone, depth, and perspective of the response.

### Example

```text
You are a technical interviewer.

Ask me five backend interview questions, one at a time, and provide feedback after each answer.
```

Common personas:

- Software Engineer
- Teacher
- Interviewer
- Doctor
- Lawyer
- Data Analyst
- Product Manager

---

## 5. Chain of Thought (CoT)

Chain-of-Thought (CoT) prompting encourages the model to solve a problem step by step before arriving at the final answer. It is particularly useful for problems requiring multiple reasoning steps.

### Example

```text
You are a mathematical reasoning assistant.

When solving numerical or logical problems:
1. Understand the problem.
2. Break it into smaller steps.
3. Perform the necessary calculations.
4. Verify the result.
5. Present the final answer clearly.

Problem:
A shop gives a 20% discount on a ₹2,500 item and then applies 18% GST. Calculate the final price.
```

Example output:

```text
Step 1...
Step 2...
Final Answer...
```

**Best for:**

- Mathematics
- Logic
- Coding
- Complex reasoning

> **Note:** Some modern reasoning models perform internal reasoning automatically, so explicitly requesting Chain-of-Thought is not always necessary.

---

# Prompt Styles

Different AI models are trained using different prompt formats.

---

# 1. Alpaca Prompt Format

**Mainly used by:**

- Alpaca
- OpenLLaMA
- Many open-source instruction models

### Structure

```text
### Instruction:
<SYSTEM_PROMPT>

### Input:
<USER_QUERY>

### Response:
```

### Example

```text
### Instruction:
You are a mathematics teacher.

### Input:
Expand (a+b)^2.

### Response:
(a+b)^2 = a² + 2ab + b²
```

---

# 2. ChatML Prompt Format

**Mainly used by:**

- ChatGPT
- OpenAI
- Groq
- Mistral
- Most modern chat models

### Structure

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

### Roles

| Role      | Purpose                |
| --------- | ---------------------- |
| system    | Sets the AI's behavior |
| user      | User's message         |
| assistant | Model's response       |

### Example

```json
[
  {
    "role": "system",
    "content": "You are a math teacher."
  },
  {
    "role": "user",
    "content": "Expand (a+b)^2."
  },
  {
    "role": "assistant",
    "content": "(a+b)^2 = a² + 2ab + b²"
  }
]
```

---

# 3. INST Prompt Format

**Mainly used by:**

- Llama 2
- Llama 3
- Meta models

### Structure

```text
[INST]
<SYSTEM_PROMPT>

<USER_QUERY>
[/INST]
```

### Example

```text
[INST]
You are a mathematics teacher.

Expand (a+b)^2.
[/INST]

(a+b)^2 = a² + 2ab + b²
```

### Multi-turn Example

```text
[INST]
You are a mathematics teacher.

What is (a+b)^2?
[/INST]

(a+b)^2 = a² + 2ab + b²

[INST]
Can you explain why?
[/INST]

It comes from the distributive property...
```

---

# Which Prompt Style Should We Use?

| Model     | Prompt Style  |
| --------- | ------------- |
| ChatGPT   | ChatML        |
| GPT-4o    | ChatML        |
| GPT-5     | ChatML        |
| Claude    | ChatML-like   |
| Gemini    | ChatML-like   |
| Groq      | ChatML        |
| Mistral   | ChatML        |
| Llama 2   | INST          |
| Llama 3   | INST          |
| Alpaca    | Alpaca Format |
| OpenLLaMA | Alpaca Format |

---
