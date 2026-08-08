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

> 📁 **Reference File:** [`React Pattern`](../python/01_llm_api_and_agents/09_react_agent.py)

---

# Planner Agent: Plan → Execute → Final Answer

## What is a Planner Agent?

A **Planner Agent** first analyzes the user's goal and creates an execution plan before calling any tools.

Unlike ReAct, where the agent repeatedly decides what to do next during execution, a Planner Agent makes the tool-selection decision **up front**, then executes the selected tools in sequence.

$$\text{Goal} \longrightarrow \text{Plan} \longrightarrow \text{Execute Tools} \longrightarrow \text{Observations} \longrightarrow \text{Final Answer}$$

---

## How does a Planner Agent work?

The Planner Agent follows three main stages:

1. **Plan:** Gemini analyzes the user's goal and determines which tools are actually necessary.
2. **Execute:** The agent executes the selected tools sequentially and collects their outputs.
3. **Final Answer:** Gemini receives the collected information and generates the final response.

The important difference is that the agent does **not** continuously decide the next tool during execution. The complete tool sequence is created before execution begins.

---

## Agent Lifecycle: `CareerCoachAgent` Example

```text
                  ┌─────────────────────────────┐
                  │   User inputs career goal   │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │ Initialize CareerCoachAgent │
                  │   self.plan = []            │
                  │   self.observation = []     │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │       1. create_plan()      │
                  │                             │
                  │ Send goal + available tools │
                  │        to Gemini            │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │      Generated Plan         │
                  │                             │
                  │ SKILL_TOOL                  │
                  │ PROJECT_TOOL                │
                  │ SALARY_TOOL                 │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │       2. execute_plan()     │
                  │                             │
                  │ Execute each selected tool  │
                  │ sequentially                │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │       Observations          │
                  │                             │
                  │ Store each tool's output    │
                  │ in self.observation         │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │  3. generate_final_plan()   │
                  │                             │
                  │ Send goal + collected data  │
                  │        to Gemini            │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │        Final Answer         │
                  └─────────────────────────────┘
```

---

## Simplified 3-Step Summary

- **1. Plan:** Gemini determines the minimum set of tools required for the user's goal.
- **2. Execute:** The agent runs the selected tools in the predetermined order and collects their outputs.
- **3. Final Answer:** Gemini uses the collected information to generate the final response.

### Key Difference from ReAct

**ReAct:** Decide → Execute → Observe → Decide again → Execute...

**Planner:** Decide the complete plan → Execute all selected tools → Generate answer.

> 📁 **Reference File:** [`Planner Agent`](../python/01_llm_api_and_agents/10_planner_agent.py)

---

# Research Agent: Plan → Gather → Analyze → Recommend

## What is a Research Agent?

A **Research Agent** extends the Planner pattern by adding an explicit **analysis stage**.

Instead of directly converting tool outputs into a final answer, the agent first gathers evidence, analyzes that evidence, and then generates recommendations.

$$\text{Goal} \longrightarrow \text{Research Plan} \longrightarrow \text{Gather Evidence} \longrightarrow \text{Analyze} \longrightarrow \text{Recommend}$$

---

## How does a Research Agent work?

The Research Agent follows four main stages:

1. **Plan:** Gemini creates a minimal research plan by selecting the tools required for the goal.
2. **Gather Evidence:** The selected tools are executed and their outputs are stored as evidence.
3. **Analyze Evidence:** Gemini analyzes the gathered evidence to identify key findings, opportunities, and challenges.
4. **Generate Recommendations:** Gemini uses the goal and analysis to produce the final recommendations.

---

## Agent Lifecycle: `ResearchAgent` Example

```text
                  ┌─────────────────────────────┐
                  │   User inputs career goal   │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │     Initialize Agent        │
                  │                             │
                  │ self.plan = []              │
                  │ self.evidence = []          │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │   1. create_research_plan() │
                  │                             │
                  │ Goal + available tools      │
                  │          ↓                  │
                  │         Gemini              │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │       Research Plan         │
                  │                             │
                  │ SKILL_TOOL                  │
                  │ CERTIFICATION_TOOL          │
                  │ PROJECT_TOOL                │
                  │ SALARY_TOOL                 │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │    2. gather_evidence()     │
                  │                             │
                  │ Execute planned tools       │
                  │        ↓                    │
                  │ Store results in evidence   │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │    3. analyze_evidence()    │
                  │                             │
                  │ Evidence + Goal             │
                  │        ↓                    │
                  │       Gemini                │
                  │        ↓                    │
                  │ Key Findings                │
                  │ Opportunities               │
                  │ Challenges                  │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │ 4. generate_recommendations │
                  │                             │
                  │ Goal + Analysis             │
                  │        ↓                    │
                  │       Gemini                │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌─────────────────────────────┐
                  │   Final Recommendations     │
                  └─────────────────────────────┘
```

---

## Simplified 4-Step Summary

- **1. Plan:** Gemini decides which tools are necessary.
- **2. Gather:** Execute those tools and collect their outputs as evidence.
- **3. Analyze:** Gemini interprets the collected evidence and extracts findings, opportunities, and challenges.
- **4. Recommend:** Gemini converts the analysis into practical recommendations, learning paths, and a final verdict.

> 📁 **Reference File:** [`Research Agent`](../python/01_llm_api_and_agents/11_research_agent.py)

---

## Planner vs Research Agent

| Agent              | Flow                                | Main Purpose                                       |
| ------------------ | ----------------------------------- | -------------------------------------------------- |
| **ReAct Agent**    | Think → Act → Observe → Repeat      | Iterative decision-making                          |
| **Planner Agent**  | Plan → Execute → Final Answer       | Plan tool execution before running                 |
| **Research Agent** | Plan → Gather → Analyze → Recommend | Gather evidence and analyze it before recommending |

### Core Concept

The three patterns progressively add structure:

```text
ReAct
  ↓
Think → Act → Observe → Repeat

Planner
  ↓
Plan → Execute → Final Answer

Research
  ↓
Plan → Gather Evidence → Analyze → Recommend
```

The **Planner Agent** is useful when the required tools can be determined beforehand. The **Research Agent** goes one step further by introducing an explicit evidence-analysis phase before producing recommendations.
