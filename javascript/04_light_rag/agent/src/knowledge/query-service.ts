// Ask the knowledge base -> retrieve relevant chunks -> generate answer

import { HumanMessage, SystemMessage } from '@langchain/core/messages';
import { ContextualCompressionRetriever } from '@langchain/classic/retrievers/contextual_compression';
import { LLMChainExtractor } from '@langchain/classic/retrievers/document_compressors/chain_extract';
import { ChatGoogle } from '@langchain/google';

import { env } from '../config/env.config';
import { getVectorStore, RETRIEVER_TOP_K } from './vector-store';

export type KnowledgeBaseSource = {
  source: string;
  chunkId: number;
};

type RetrievedChunk = {
  text: string;
  metadata: Record<string, unknown>;
};

export type KnowledgeBaseQueryResult = {
  answer: string;
  sources: KnowledgeBaseSource[];
};

const llm = new ChatGoogle({
  model: env.LLM_MODEL_NAME,
  apiKey: env.GEMINI_API_KEY,
  temperature: 0.2,
});

/**
 * Builds the context passed to the answer-generation LLM
 * from the chunks retrieved from the knowledge base.
 */
function buildRetrievalContext(chunks: RetrievedChunk[]): string {
  return chunks
    .map(({ text, metadata }, index) => {
      const source = String(metadata.source ?? 'unknown');
      const chunkId = String(metadata.chunkId ?? 'unknown');

      return [`[#${index + 1}] ${source} #${chunkId}`, text || 'Empty text'].join('\n');
    })
    .join('\n\n---\n\n');
}

/**
 * Generates an answer using only the retrieved knowledge-base context.
 */
async function generateAnswer(query: string, context: string): Promise<string> {
  const response = await llm.invoke([
    new SystemMessage(
      [
        'You are a helpful assistant that answers only using the provided context.',
        'If the answer is not found in the provided context, say so briefly.',
        'Be concise (4-5 sentences), neutral, and avoid marketing information.',
        'Do not fabricate sources or cite information that is not present in the context.',
      ].join('\n')
    ),
    new HumanMessage(
      [`Question:\n${query}`, '', 'Context:', context || 'No relevant context was found.'].join(
        '\n'
      )
    ),
  ]);

  const answer = typeof response.content === 'string' ? response.content : String(response.content);

  return answer.trim().slice(0, 1500);
}

/**
 * Queries the knowledge base by retrieving relevant chunks,
 * compressing the retrieved content, and generating an answer.
 */
export async function queryKnowledgeBase(
  query: string,
  topK = RETRIEVER_TOP_K
): Promise<KnowledgeBaseQueryResult> {
  const normalizedQuery = query.trim();

  if (!normalizedQuery) {
    throw new Error('Query cannot be empty.');
  }

  if (topK <= 0) {
    throw new Error('topK must be greater than 0.');
  }

  const vectorStore = getVectorStore();

  const baseRetriever = vectorStore.asRetriever({
    k: topK,
  });

  const compressor = LLMChainExtractor.fromLLM(llm);

  const compressionRetriever = new ContextualCompressionRetriever({
    baseRetriever,
    baseCompressor: compressor,
  });

  const documents = await compressionRetriever.invoke(normalizedQuery);

  const chunks: RetrievedChunk[] = documents.map(document => ({
    text: document.pageContent,
    metadata: document.metadata ?? {},
  }));

  const context = buildRetrievalContext(chunks);
  const answer = await generateAnswer(normalizedQuery, context);

  const sources: KnowledgeBaseSource[] = chunks
    .map(({ metadata }) => ({
      source: String(metadata.source ?? 'unknown'),
      chunkId: Number(metadata.chunkId ?? -1),
    }))
    .filter(({ chunkId }) => Number.isFinite(chunkId) && chunkId >= 0);

  return {
    answer,
    sources,
  };
}
