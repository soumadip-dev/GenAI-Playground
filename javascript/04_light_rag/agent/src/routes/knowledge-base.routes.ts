import { Router, type Request, type Response } from 'express';
import { z } from 'zod';

import { indexText } from '../knowledge/indexer';
import { queryKnowledgeBase } from '../knowledge/query-service';
import { resetVectorStore } from '../knowledge/vector-store';

export const knowledgeBaseRouter = Router();

const IndexTextRequestSchema = z.object({
  text: z.string().trim().min(1, 'Text is required.'),
  source: z.string().trim().optional(),
});

const QueryKnowledgeBaseRequestSchema = z.object({
  query: z.string().trim().min(3, 'Query must be at least 3 characters long.'),
});

/**
 * Indexes text into the knowledge base.
 *
 * POST /ingest
 */
knowledgeBaseRouter.post('/ingest', async (req: Request, res: Response): Promise<void> => {
  try {
    const input = IndexTextRequestSchema.parse(req.body);

    const result = await indexText({
      text: input.text,
      source: input.source || 'pasted-text',
    });

    res.status(200).json({
      success: true,
      data: result,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({
        success: false,
        error: 'Validation failed.',
        details: error.issues,
      });
      return;
    }

    const message = error instanceof Error ? error.message : 'An unexpected error occurred.';

    console.error('Knowledge base ingestion failed:', error);

    res.status(500).json({
      success: false,
      error: message,
    });
  }
});

/**
 * Queries the knowledge base and generates an answer.
 *
 * POST /query
 */
knowledgeBaseRouter.post('/query', async (req: Request, res: Response): Promise<void> => {
  try {
    const { query } = QueryKnowledgeBaseRequestSchema.parse(req.body);

    const result = await queryKnowledgeBase(query);

    res.status(200).json({
      success: true,
      data: result,
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({
        success: false,
        error: 'Validation failed.',
        details: error.issues,
      });
      return;
    }

    const message = error instanceof Error ? error.message : 'An unexpected error occurred.';

    console.error('Knowledge base query failed:', error);

    res.status(500).json({
      success: false,
      error: message,
    });
  }
});

/**
 * Clears all documents from the in-memory vector store.
 *
 * POST /reset
 */
knowledgeBaseRouter.post('/reset', (_req: Request, res: Response): void => {
  try {
    resetVectorStore();

    res.status(200).json({
      success: true,
      message: 'Knowledge base reset successfully.',
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'An unexpected error occurred.';

    console.error('Knowledge base reset failed:', error);

    res.status(500).json({
      success: false,
      error: message,
    });
  }
});
