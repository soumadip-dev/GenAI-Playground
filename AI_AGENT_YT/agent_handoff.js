import 'dotenv/config';
import { Agent, tool, run } from '@openai/agents';
import { z } from 'zod';
import fs from 'node:fs/promises';
import { RECOMMENDED_PROMPT_PREFIX } from '@openai/agents-core/extensions';

//* Tool to fetch available plans
const fetchAvailablePlans = tool({
  name: 'fetch_available_plans',
  description: 'Fetches the available plans for the user',
  parameters: z.object({}),
  execute: async () => {
    return [
      { plan_id: '1', price_inr: 399, speed: '30MB/s' },
      { plan_id: '2', price_inr: 599, speed: '50MB/s' },
      { plan_id: '3', price_inr: 999, speed: '100MB/s' },
      { plan_id: '4', price_inr: 1499, speed: '150MB/s' },
    ];
  },
});

//* Tool to process refund
const processRefund = tool({
  name: 'process_refund',
  description: 'Processes a refund for the customer',
  parameters: z.object({
    customer_id: z.string().describe('The ID of the customer'),
    plan_id: z.string().describe('The ID of the plan'),
    reason: z.string().describe('The reason for the refund'),
  }),
  execute: async ({ customer_id, plan_id, reason }) => {
    await fs.appendFile(
      './refund_log.txt',
      `Refund request for customer ${customer_id} for plan ${plan_id} due to: ${reason}\n`,
      'utf-8'
    );
    return { refundIssued: true };
  },
});

//* Agent to process refunds
const refundAgent = new Agent({
  name: 'refund_agent',
  instruction: `You are an expert refund agent for an internet broadband company.
You are only allowed to refund plans for customers who have already purchased them.`,
  tools: [processRefund],
});

//* Agent to handle sales
const salesAgent = new Agent({
  name: 'sales_agent',
  instruction: `You are an expert sales agent for an internet broadband company.
Talk to the user and help them with what they need.`,
  tools: [fetchAvailablePlans],
});

//* Agent to handle reception
const receptionAgent = new Agent({
  name: 'reception_agent',
  instruction: `${RECOMMENDED_PROMPT_PREFIX}
  You are a receptionist for an internet broadband company.
  Talk to the user about what they need and then route or handoff them to the appropriate agent.`,
  handoffDescription: `You have two agents available to assist the user:
  1. sales_agent: Handles sales-related queries; ideal for new customers.
  2. refund_agent: Handles refund-related queries for existing customers.
  Use sales_agent for new customers and refund_agent for existing customers.`,
  handoffs: [salesAgent, refundAgent],
});

//* Function to run the agent
async function runAgent(query = '') {
  const result = await run(receptionAgent, query);
  console.log('Result:', result.finalOutput);
  console.log('History:', result.history);
}

runAgent('I want to know about the available plans because I am shifting to a new place');
// runAgent('I want to refund my plan because I am shifting to a new place');
