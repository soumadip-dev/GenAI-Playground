import { selectAndHello } from './provider';

async function main() {
  try {
    const result = await selectAndHello();

    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(message);
    process.exit(1);
  }
}

main();
