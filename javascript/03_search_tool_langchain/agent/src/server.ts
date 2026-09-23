import express, { type Request, type Response } from 'express';
import helmet from 'helmet';

import { env } from './config/env.config.ts';
import { configCors } from './config/cors.config.ts';
import { searchRouter } from './routes/search_lcel.ts';

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

  app.use('/search', searchRouter);

  const PORT = env.PORT || 8080;

  app.listen(PORT, () => {
    console.log(`Server listening at http://localhost:${PORT} 🌐`);
  });
}

bootstrap().catch(error => {
  console.error('Failed to start the server ❌', error);
  process.exit(1);
});
