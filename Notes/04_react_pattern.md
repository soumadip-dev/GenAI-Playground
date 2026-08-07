# ReAct Agent: Reason + Act

The **ReAct (Reason + Act)** pattern allows an LLM (like Gemini) to solve complex problems by combining step-by-step reasoning with external tool execution in an iterative loop.

$$\text{Think} \longrightarrow \text{Action} \longrightarrow \text{Observation} \longrightarrow \text{Repeat} \longrightarrow \text{Final Answer}$$

---

## What is a ReAct Agent?

Instead of generating a response instantly, a ReAct agent operates in a continuous feedback loop:

1. **Reason (Think):** The model analyzes the goal and previous steps to decide what information it still needs.
2. **Act:** The model selects and calls an external tool or function (e.g., API, search, custom code).
3. **Observe:** The agent receives the tool's result, appends it to its memory, and repeats the cycle until it has enough context.

---

## Agent Lifecycle: `CareerCoachAgent` Example

Here is how a practical implementation works step by step:

```
                  ┌─────────────────────────────┐
                  │   User inputs career goal   │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │ Initialize CareerCoachAgent │
                  │  (self.observations = [])   │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
┌─────────────────────────> run() Loop <────────────────────────┐
│                                │                              │
│                                ▼                              │
│                         1. think()                            │
│                 Send history + goal to Gemini                 │
│                Asks: "Which tool to run next?"                │
│                                │                              │
│         ┌──────────────────────┴──────────────────────┐       │
│         ▼                                             ▼       │
│  Returns Tool Name                            Returns "FINISH"│
│ (e.g., SKILL_TOOL)                                    │       │
│         │                                             │       │
│         ▼                                             │       │
│ 2. execute_action()                                   │       │
│ Calls Python function                                 │       │
│         │                                             │       │
│         ▼                                             │       │
│ 3. Observation                                        │       │
│ Append output to self.observations                    │       │
└─────────┴─────────────────────────────────────────────┘       │
                                                                ▼
                                                ┌──────────────────────────────────┐
                                                │    generate_final_plan()         │
                                                │ Send all gathered observation    │
                                                │ data to Gemini for final response│
                                                └──────────────────────────────────┘

```

---

## Simplified 3-Step Summary

- **1. Think:** Gemini decides the next step based on the goal and history.
- **2. Act & Observe:** The agent executes a Python tool, records the output, and feeds it back into Gemini.
- **3. Finish:** Once sufficient context is gathered, Gemini exits the loop and synthesizes the final answer.

> 📁 **Reference File:** [`07_react_pattern_career_agent.py`](https://www.google.com/search?q=../python/02_Ai_Api_Clients/07_react_pattern_career_agent.py)
