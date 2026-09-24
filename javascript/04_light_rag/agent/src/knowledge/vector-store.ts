import { GoogleGenerativeAIEmbeddings } from '@langchain/google-genai';
import { MemoryVectorStore } from '@langchain/classic/vectorstores/memory';
import type { Document } from '@langchain/core/documents';

import { env } from '../config/env.config';

export const RETRIEVER_TOP_K = 2;

function createEmbeddings(): GoogleGenerativeAIEmbeddings {
  const apiKey = env.GEMINI_API_KEY;

  if (!apiKey) {
    throw new Error('GEMINI_API_KEY environment variable is not configured.');
  }

  return new GoogleGenerativeAIEmbeddings({
    apiKey,
    model: env.EMBEDDING_MODEL_NAME,
  });
}

let vectorStore: MemoryVectorStore | null = null;

export function getVectorStore(): MemoryVectorStore {
  if (!vectorStore) {
    vectorStore = new MemoryVectorStore(createEmbeddings());
  }

  return vectorStore;
}

// input -> docs
/*
our document structure
pageContent,
        metadata: {
          source,
          chunkId,
          totalChunks,
        },
*/
export async function addDocumentsToVectorStore(documents: Document[]): Promise<number> {
  if (documents.length === 0) {
    return 0;
  }

  const store = getVectorStore();

  await store.addDocuments(documents);

  return documents.length;
}

export function resetVectorStore(): void {
  vectorStore = null;
}
