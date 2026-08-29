# LangChain

LangChain is an open-source framework for developing applications powered by large language models (LLMs).

## LangChain Components

```mermaid
graph TD

    %% Central Node
    LC(("LangChain"))

    %% Outer Nodes
    N1["1. Models"]
    N2["2. Prompts"]
    N3["3. Chains"]
    N4["4. Memory"]
    N5["5. Indexes"]
    N6["6. Agents"]

    %% Connections
    LC --> N1
    LC --> N2
    LC --> N3
    LC --> N4
    LC --> N5
    LC --> N6
```

### 1. Models

In LangChain, models are the core components through which we interact with AI models. LangChain is designed to facilitate interaction with different types of models, including **language models** for text-based applications and **embedding models** that convert text into numerical representations for applications such as **semantic search** and **RAG (Retrieval-Augmented Generation)**.

```mermaid
graph TD

    %% Nodes
    M["Models"]

    LM["Language<br/>Models"]
    EM["Embedding<br/>Models"]

    LLM["LLMs"]
    CM["Chat Models"]

    %% Connections
    M --> LM
    M --> EM

    LM --> LLM
    LM --> CM
```

#### Language Models

Language models are AI systems designed to process, understand, and generate natural language text.

**i. LLMs:**
LLMs are general-purpose language models that typically accept a text prompt as input and generate text as output. They are useful for tasks such as text generation, summarization, and question answering.

> 📁 **Reference File:** [`LLM`](../python/03_langchain/01_models/01_llm.py)

**ii. Chat Models:**
Chat models are language models designed to work with conversational messages. They typically accept a sequence of messages, such as system, user, and assistant messages, as input and return a message as output. Modern LLM applications commonly use chat models because they provide a structured interface for conversational interactions.

> 📁 **Reference File:** [`Chat Model`](../python/03_langchain/01_models/02_chat_model.py)

#### Embedding Models

Embedding models convert text or other data into numerical vectors called **embeddings**. These vectors capture the semantic meaning of the input and are commonly used for:

* Semantic search
* Similarity search
* Retrieval-Augmented Generation (RAG)
* Recommendation systems
* Document clustering

### 2. Prompts

Prompts are how we provide instructions and input to models. They guide the model on what to do, what information to consider, and how to structure its response.

### 3. Chains

Chains allow us to combine models, prompts, and other components to create a sequence of operations. They act as pipelines where the output of one component can be passed as the input to another component.

### 4. Memory

LLM API calls are generally stateless. Therefore, applications need a mechanism to maintain relevant information from previous interactions when building conversational systems. This is where memory comes in.

Common memory approaches include:

* **ConversationBufferMemory:** Stores the complete conversation history. It is useful for short conversations but can grow large quickly and increase token usage.
* **ConversationBufferWindowMemory:** Keeps only the most recent N interactions to limit the amount of conversation history sent to the model.
* **Custom Memory:** For advanced use cases, custom memory can be implemented to store specialized state, such as user preferences, important facts, or application-specific information.

### 5. Indexes

Indexes connect your application to external knowledge sources, such as PDFs, websites, or databases. They help transform and organize external data so that relevant information can be retrieved when needed.

A typical indexing and retrieval pipeline consists of four components:

* **Document Loader** — Loads data from sources such as PDFs, websites, or databases.
* **Text Splitter** — Splits documents into smaller chunks that can be processed and retrieved efficiently.
* **Vector Store** — Stores vector embeddings and enables similarity-based searches.
* **Retriever** — Retrieves the most relevant documents or chunks based on a query.

### 6. Agents

Agents use a language model to decide which actions or tools to use to accomplish a given task. Unlike fixed chains, agents can dynamically determine the next step based on the current task, available tools, and previous results.
