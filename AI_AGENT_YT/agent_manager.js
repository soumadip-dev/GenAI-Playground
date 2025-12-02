import 'dotenv/config';
import { Agent, tool } from '@openai/agents';
import { z } from 'zod';
import fs from 'node:fs/promises';

const fetchAvailablePlans = tool({
  name: 'fetch_available_plans',
  description: 'Fetches the available plans for the user',
  parameters: z.object(),
  execute: async () => {
    return [
      { plan_id: '1', price_inr: 399, speed: '30MB/s' },
      { plan_id: '2', price_inr: 599, speed: '50MB/s' },
      { plan_id: '3', price_inr: 999, speed: '100MB/s' },
      { plan_id: '4', price_inr: 1499, speed: '150MB/s' },
    ];
  },
});

const processRefund = tool({
  name: 'process_refund',
  description: 'Processes the refund for the customer',
  parameters: z.object({
    customer_id: z.string().describe('The ID of the customer'),
    plan_id: z.string().describe('The ID of the plan'),
    reason: z.string().describe('The reason for the refund'),
  }),
  execute: async ({ customer_id, plan_id, reason }) => {
    fs.appendFile(
      '/refund_log.txt',
      `Refund request for customer ${customer_id} for plan ${plan_id} due to ${reason}`,
      'utf-8'
    );
    return { refundIssued: true };
  },
});

const refundAgent = new Agent({
  name: 'refund_agent',
  instruction: `You are an expert refund agent for an internet broadband company.
  You are only allowed to refund the plans for customers who have already purchased the plan.
  `,
  tools: [processRefund],
});

const salesAgent = new Agent({
  name: 'sales_agent',
  instruction: `You are an expert sales agent for an internet broadband company.
  Talk to the user and help them with what they need.
  `,
  tools: [
    fetchAvailablePlans,
    refundAgent.asTool({
      toolName: 'refund_agent',
      toolDescription: 'Handle refund questions and requests',
    }),
  ],
});

async function runAgent(query = '') {
  const result = await run(salesAgent, query);
  console.log(result.finalOutput);
}

runAgent('I want to know about the available plans because I am shifting to a new place');
