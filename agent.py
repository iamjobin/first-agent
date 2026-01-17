import asyncio


async def calculator(expression: str) -> str:
    await asyncio.sleep(1)
    return str(eval(expression))


async def llm_reasoning(prompt: str) -> dict:
    if 'add' in prompt:
        return {
            "action": "tool",
            "tool_name": "calculator",
            "tool_input": "2 + 3"
        }
    else:
        return {
            "action": "answer",
            "final_answer": "I can answer directly"
        }


async def run_agent(user_input: str):
    memory = []

    print("Agent is started\n")

    while True:

        decision = await llm_reasoning(user_input)

        if decision['action'] == 'answer':
            print("\nFinal answer: ", decision['final_answer'])
            break

        if decision['action'] == 'tool':
            print("\nCalling tool: ", decision['tool_name'])
            result = await calculator(decision['tool_input'])

            memory.append({
                "tool": decision['tool_name'],
                "input": decision['tool_input'],
                "result": result
            })

            print("\nFinal Result: ", result)
            break


async def async_input(prompt: str = "") -> str:
    return await asyncio.to_thread(input, prompt)


async def main():
    user_input = await async_input("Enter your query: ")
    await run_agent(user_input)


asyncio.run(main())