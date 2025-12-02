import 'dotenv/config';
import { Agent, run } from '@openai/agents';

//* Create the agent
const helloAgent = new Agent({
  name: 'Hello Agent',
  instructions: function () {
    if (location == 'india') {
      return 'Always say namaste and then You are an agent that always says hello world';
    } else {
      return 'Just talk to the user';
    }
  },
});

//* Run the agent
run(helloAgent, 'Hey There, My name is Soumadip Majila').then(result => {
  console.log(result.finalOutput);
});
