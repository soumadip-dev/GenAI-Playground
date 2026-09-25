<div align="center">

# GenAI-Playground ✨

<p>
A comprehensive, hands-on repository of <b>AI agents</b>, <b>RAG pipelines</b>, <b>LangChain/LCEL abstractions</b>, <b>prompt engineering strategies</b>, and <b>full-stack Generative AI applications</b>.
</p>

<img src="./notes/images/banner.jpg" alt="GenAI Playground Banner" width="900">

</div>

---

## 🔋 Contents

This repository serves as an active playground for exploring and implementing modern Generative AI engineering concepts across both **Python** and **JavaScript/TypeScript** ecosystems.

- 🤖 **AI Agents & Workflows**: Standard LLM calls, function/tool calling, ReAct loop, Planner-Executor pattern, Research agent, and Reflection agent loops.
- 🔍 **Retrieval-Augmented Generation (RAG)**: Ingestion pipelines, text splitters (length, structured, code-aware), vector stores (Chroma, FAISS, in-memory), and advanced retrievers (MMR, Multi-Query, Contextual Compression, Wikipedia).
- 🦜 **LangChain & LCEL**: Building blocks including LLMs, ChatModels, Embeddings, PromptTemplates, Output Parsers, Chains, and LCEL Runnables (`RunnableSequence`, `RunnableParallel`, `RunnablePassthrough`, `RunnableLambda`, `RunnableBranch`).
- 📄 **Structured Outputs**: Schema-enforced JSON extraction using Pydantic, TypedDict, Zod schemas, and LangChain structured outputs.
- 🎯 **Prompt Engineering**: Zero-shot, Few-shot, Persona, and Chain-of-Thought (CoT) techniques.
- 🚀 **Full-Stack Applications**: Modern web apps built with Express/TypeScript backends and Next.js UI clients for structured outputs, search agents, and Light RAG indexing.
- 📚 **In-Depth Notes**: Conceptual documentation and architecture diagrams covering core LLM theory, prompt design, agent patterns, LangChain mechanics, and RAG pipelines.

---

## 🐍 Python Development Guide

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install project dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the development server of the FastAPI application

```bash
uvicorn main:app --reload
```

### 5. Update dependencies (when required)

```bash
pip freeze > requirements.txt
```

---

<div align="center">

> **Learning by building, experimenting, and iterating. 🌱**

</div>
