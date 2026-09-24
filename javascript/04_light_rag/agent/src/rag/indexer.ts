import { chunkText } from './chunker';
import { addDocumentsToVectorStore } from './vector-store';

export type IndexTextInput = {
  text: string;
  source?: string;
};

export type IndexTextResult = {
  documentCount: number;
  chunkCount: number;
  source: string;
};

/**
 * Splits text into chunks, generates embeddings for each chunk,
 * and stores the resulting vectors in the in-memory vector store.
 */

export async function indexText(input: IndexTextInput): Promise<IndexTextResult> {
  const text = (input.text ?? '').trim();

  if (!text) {
    throw new Error('Text to index cannot be empty.');
  }

  const source = input.source?.trim() || 'pasted-text';

  const documents = await chunkText(text, source);
  const chunkCount = await addDocumentsToVectorStore(documents);

  return {
    documentCount: 1,
    chunkCount,
    source,
  };
}
