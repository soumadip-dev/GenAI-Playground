import express, { type Request, type Response } from 'express';
import helmet from 'helmet';

import { configCors } from './config/cors.config.ts';
import { env } from './config/env.config.ts';
import { knowledgeBaseRouter } from './routes/knowledge-base.routes.ts';

async function bootstrap(): Promise<void> {
  const app = express();

  // Security and request configuration
  app.use(helmet());
  app.use(configCors());
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  // Health check
  app.get('/health', (_req: Request, res: Response) => {
    res.status(200).json({
      status: 'ok',
      message: 'Server is healthy and running.',
    });
  });

  // API routes
  app.use('/api/knowledge-base', knowledgeBaseRouter);

  const port = env.PORT || 8080;

  app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
  });
}

bootstrap().catch((error: unknown) => {
  console.error('Failed to start the server:', error);
  process.exit(1);
});
