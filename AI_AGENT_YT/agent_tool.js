import { Agent, run, tool } from '@openai/agents';
import { z } from 'zod';
import axios from 'axios';

const GetWeatherResultSchema = z.object({
  city: z.string().describe('Name of the city'),
  degree_c: z.number().describe('The degree celcious of the temp'),
  condition: z.string().optional().describe('Condition of the weather'),
});

const getWeatherTool = tool({
  name: 'get_weather',
  description: 'Returs the current weather information for the given city',
  parameters: z.object({
    city: z.string().describe('name fo the city'),
  }),
  execute: async function ({ city }) {
    const url = `https://wttr.in/${city.toLowerCase()}?format=%C+%t`;
    axios.get(url, { responseType: 'text' });
    return `The weather of the ${city} is ${response.data}`;
  },
});

const agent = new Agent({
  name: 'Weather agent',
  instruction: `
  You are an expert weather agent that helps user to tell weather report
  `,
  tools: [getWeatherTool],
  outputType: GetWeatherResultSchema,
});

async function main(query = '') {
  const result = run(agent, query);
  console.log('Result', result.finalOutput);
}

main('What is the weather of durgapur');
