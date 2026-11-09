import asyncio
import json
import asyncio
import json
import sys

from provider import select_and_hello


async def main():

    try:
        result = await select_and_hello()

        print(json.dumps(result, indent=2))

    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
