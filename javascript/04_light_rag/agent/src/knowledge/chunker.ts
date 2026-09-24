import { Document } from '@langchain/core/documents';
import { RecursiveCharacterTextSplitter } from '@langchain/textsplitters';

export const CHUNK_SIZE = 1000;
export const CHUNK_OVERLAP = 200;

/**
 * Splits text into overlapping chunks and converts each chunk
 * into a LangChain Document with source metadata.
 *
 * Example:
 * chunkSize = 10
 * chunkOverlap = 3
 * text = ABCDEFGHIJKLM
 *
 * Chunk 0: ABCDEFGHIJ
 * Chunk 1: HIJKLM
 */
export async function chunkText(text: string, source: string): Promise<Document[]> {
  const normalizedText = (text ?? '').replace(/\r\n/g, '\n');

  if (!normalizedText.trim()) {
    return [];
  }

  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: CHUNK_SIZE,
    chunkOverlap: CHUNK_OVERLAP,
  });

  const chunks = await splitter.splitText(normalizedText);

  return chunks.map(
    (chunk, index) =>
      new Document({
        pageContent: chunk,
        metadata: {
          source,
          chunkId: index,
          totalChunks: chunks.length,
        },
      })
  );
}
