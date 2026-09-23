import { RunnableBranch, RunnableSequence } from '@langchain/core/runnables';

import { directPipeline } from './directPipeline';
import { validateFinalOutputStep } from './finalValidate';
import { routerStep } from './routeStrategy';
import { webPipeline } from './webPipeline';
import type { SearchInput } from '../schemas';

const searchPipeline = RunnableBranch.from<{ query: string; mode: 'web' | 'direct' }, any>([
  [input => input.mode === 'web', webPipeline],
  directPipeline,
]);

export const searchChain = RunnableSequence.from([
  routerStep,
  searchPipeline,
  validateFinalOutputStep,
]);

export async function runSearch(query: SearchInput) {
  return await searchChain.invoke(query);
}
