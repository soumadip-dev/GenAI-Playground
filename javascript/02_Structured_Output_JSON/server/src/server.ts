import express, { type Request, type Response } from 'express';
import helmet from 'helmet';

import { env } from './config/env.config.ts';
import { configCors } from './config/cors.config.ts';
import { getStructuredAnswer } from './ask-core.ts';

async function bootstrap() {
  const app = express();

  app.use(configCors());
  app.use(helmet());

  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  app.get('/health', (_req: Request, res: Response) => {
    return res.status(200).json({
      status: 'ok',
      message: 'Server is healthy and running 💚',
    });
  });

  app.get('/', (_req: Request, res: Response) => {
    return res.status(200).json({
      status: 'ok',
      message: 'Welcome to the GenAI Playground!',
    });
  });

  app.post('/ask', async (req: Request, res: Response) => {
    try {
      const { query } = req.body ?? {};

      if (!query) {
        return res.status(400).json({
          status: 'error',
          error: 'Missing query parameter ❌',
        });
      }

      const result = await getStructuredAnswer(query);

      return res.status(200).json({
        status: 'success',
        message: 'Successfully generated the answer 🎉',
        data: result,
      });
    } catch (error) {
      return res.status(500).json({
        status: 'error',
        error: error instanceof Error ? error.message : 'Internal server error',
      });
    }
  });

  const PORT = env.PORT || 8080;

  app.listen(PORT, () => {
    console.log(`Server listening at http://localhost:${PORT} 🌐`);
  });
}

bootstrap().catch(error => {
  console.error('Failed to start the server ❌', error);
  process.exit(1);
});
