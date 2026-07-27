# Assistant vs Agent

## What is an Assistant?

An **Assistant** is an AI system that responds to user queries and performs tasks **only when instructed**. It typically follows a **request → response** pattern and does not independently decide what actions to take.

### Workflow

```text
User Request
      │
      ▼
 Assistant
      │
      ▼
  Response
```

### Examples

An assistant can perform tasks such as:

- **Answering questions**
- **Writing emails**
- **Summarizing documents**
- **Explaining concepts**
- **Translating text**

---

## What is an Agent?

An **Agent** is an AI system that is designed to achieve a specific goal. Instead of simply responding to a prompt, it can **reason**, **create a plan**, **use tools**, and **execute multiple steps** to complete a task.

An agent typically follows this workflow:

```text
Goal
  │
  ▼
Reason
  │
  ▼
 Plan
  │
  ▼
Execute
  │
  ▼
Result
```

### Agent Workflow

1. **Goal**
   - Understands what the user wants to achieve.

2. **Reasoning**
   - Breaks down the problem.
   - Determines what information or skills are needed.

3. **Planning**
   - Creates a sequence of steps to accomplish the goal.

4. **Execution**
   - Performs the planned actions.
   - May call external tools, APIs, databases, or other services.

### Example

**User Goal**

```text
I want to become a Backend Developer.
```

The agent may:

1. **Identify** the required skills.
2. **Arrange** them in the correct learning order.
3. **Generate** a 90-day roadmap.
4. **Recommend** learning resources.

---

# Tool Calling

**Tool Calling** is the general concept of allowing an **LLM (Large Language Model)** to use external tools to perform tasks beyond its built-in knowledge.

A tool can be:

- **Python function**
- **Database**
- **API**
- **Calculator**
- **Web Search**
- **File Reader**
- **Code Interpreter**
- **Image Generator**
- **Any external system**

Tool calling can be implemented in two ways:

- **Manual Tool Calling**
- **Automatic Tool Calling (Function Calling)**

---

# 1. Manual Tool Calling

In **Manual Tool Calling**, **you are responsible for selecting and executing the tool**.

The LLM only tells you **which tool should be used**. Your application then calls that tool manually.

### Workflow

```text
 User
   │
   ▼
  LLM
   │
   ▼
Returns Tool Name
   │
   ▼
Your Code Executes the Tool
   │
   ▼
 Tool Result
```

### Example

**User:**

```text
What time is it?
```

**LLM returns:**

```text
TIME_TOOL
```

**Your code executes:**

```python
get_current_time()
```

---

# 2. Automatic Tool Calling (Function Calling)

In **Automatic Tool Calling (Function Calling)**, **you provide all available functions to the LLM**.

The model automatically:

1. **Chooses** the correct function.
2. **Generates** the required arguments.
3. **Calls** the function (through the SDK/framework).
4. **Uses** the returned result to generate the final response.

### Workflow

```text
 User
   │
   ▼
  LLM
   │
   ▼
Selects Function
   │
   ▼
Function Executes
   │
   ▼
 Tool Result
   │
   ▼
  LLM
   │
   ▼
Final Answer
```

### Example

**Available functions:**

```python
tools = [
    get_skills,
    get_salary,
    get_certificate,
]
```

**User:**

```text
What is the salary of a Backend Developer?
```

**Gemini automatically calls:**

```python
get_salary("Backend Developer")
```

The result is sent back to the model, which generates the final answer.

---

# Difference

| **Manual Tool Calling**                      | **Automatic Tool Calling (Function Calling)**         |
| -------------------------------------------- | ----------------------------------------------------- |
| You ask the LLM which tool to use.           | You provide the available functions to the LLM.       |
| The LLM returns the tool name.               | The LLM selects the function automatically.           |
| You manually execute the tool.               | The SDK/framework handles the function call workflow. |
| You write the routing logic.                 | The model performs the routing.                       |
| Requires an extra prompt for tool selection. | No separate routing prompt is needed.                 |

---
