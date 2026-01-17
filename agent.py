import asyncio


async def calculator(expression: str) -> str:
    await asyncio.sleep(1)
    return str(eval(expression))


async def llm_reasoning(prompt: str, memory: list) -> dict:
    '''
    Decide what to do next based on memory
    '''
    if not memory:
        return {
            "action": "tool",
            "tool_name": "calculator",
            "tool_input": "2 + 3"
        }
    if len(memory) == 1:
        return {
            "action": "tool",
            "tool_name": "calculator",
            "tool_input": "5 * 10"
        }
    else:
        return {
            "action": "answer",
            "final_answer": f"Final answer is {memory[-1]['result']}"
        }


async def run_agent(user_input: str, max_steps: int = 5):
    memory = []

    print("Agent is started\n")

    for step in range(max_steps):

        print(f"\n___Step {step + 1}___")
        print("Mempry:", memory)

        decision = await llm_reasoning(user_input, memory)

        if decision['action'] == 'answer':
            print("\nAgent Finished.")
            print("\nFinal answer: ", decision['final_answer'])
            return

        if decision['action'] == 'tool':
            print("\nCalling tool: ", decision['tool_name'])
            result = await calculator(decision['tool_input'])

            memory.append({
                "tool": decision['tool_name'],
                "input": decision['tool_input'],
                "result": result
            })

            print("\nFinal Result: ", result)

    print("\nAgent stopped: max steps reached")


async def async_input(prompt: str = "") -> str:
    return await asyncio.to_thread(input, prompt)


async def main():
    user_input = await async_input("Enter your query: ")
    await run_agent(user_input, 5)


asyncio.run(main())