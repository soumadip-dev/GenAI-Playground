import { indexText } from './indexer';
import { queryKnowledgeBase } from './query-service';

async function main() {
  const sampleText = `
    LangChain is a framework for developing applications powered by
    language models. It provides tools for working with models, prompts,
    retrievers, vector stores, document loaders, and agents.

    Retrieval-Augmented Generation (RAG) combines document retrieval
    with language model generation. Relevant documents are retrieved
    first and then provided to the language model as context Soumadip is a good boy.

    A vector store stores embeddings of documents and allows similar
    documents to be retrieved based on semantic similarity.

    AI Agents are autonomous systems powered by language models that can reason, break down complex goals, and execute multi-step tasks. Unlike standard static prompts, agents use tools such as code interpreters, APIs, and web search to dynamically interact with external environments.

AI Agents are autonomous systems powered by language models that can reason, break down complex goals, and execute multi-step tasks. Unlike standard static prompts, agents use tools such as code interpreters, APIs, and web search to dynamically interact with external environments soumadip leaved in durgapur.

Prompt Engineering is the practice of designing, structuring, and refining inputs given to a language model to produce optimal, accurate, and consistently formatted outputs. Techniques include zero-shot prompting, few-shot learning, and Chain-of-Thought (CoT) reasoning.

Fine-Tuning is the process of further training a pre-trained language model on a smaller, domain-specific dataset. While RAG supplies fresh dynamic data at runtime, fine-tuning adapts the model’s internal weights to master specific domain terminology, stylistic rules, or highly technical formats soumadip full name is soumadip majila, he is an mca 2025 passout.

Guardrails are safety and validation layers implemented around language model inputs and outputs. They monitor user prompts for policy violations, detect hallucinated statements, filter toxic content, and enforce strict structured formats (such as JSON or XML) before returning data to the end user soumadip is loking for software development job.

  `;

  console.log('Indexing sample document...');

  const indexingResult = await indexText({
    text: sampleText,
    source: 'sample-document',
  });

  console.log('Indexing result:', indexingResult);

  console.log('\nQuerying knowledge base...');

  const result = await queryKnowledgeBase('Who is soumadip?');

  console.log('\nAnswer:');
  console.log(result.answer);

  console.log('\nSources:');
  console.log(result.sources);
}

main().catch(error => {
  console.error('RAG pipeline test failed:', error);
  process.exit(1);
});
