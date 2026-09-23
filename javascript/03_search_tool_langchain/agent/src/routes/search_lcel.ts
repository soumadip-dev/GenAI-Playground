import { Router, type Request, type Response } from 'express';
import { ZodError } from 'zod';
import { searchInputSchema } from '../schemas';
import { runSearch } from '../search_tool/searchChain';

export const searchRouter = Router();

searchRouter.post('/', async (req: Request, res: Response): Promise<void> => {
  try {
    const validatedInput = searchInputSchema.parse(req.body);
    const searchResult = await runSearch(req.body);

    res.status(200).json(searchResult);
  } catch (error) {
    // Handle request payload schema validation failures
    if (error instanceof ZodError) {
      res.status(400).json({
        error: 'Validation Failed',
        details: error.issues,
      });
      return;
    }

    // Handle internal server or systemic runtime failures
    const errorMessage = error instanceof Error ? error.message : 'An unexpected error occurred';
    res.status(500).json({ error: errorMessage });
  }
});
