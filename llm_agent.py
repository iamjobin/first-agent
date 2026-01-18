import asyncio
import json
from ollama import AsyncClient

client = AsyncClient()

SYSTEM_PROMPT = """
You are an AI agent.
Decide the next action.

Available tool:
- calculator: evaluates math expressions

Rules:
- Respond ONLY in JSON
- Possible actions:
  1) tool
  2) answer

JSON formats:

Tool call:
{
  "action": "tool",
  "tool_name": "calculator",
  "tool_input": "2 + 3"
}

Final answer:
{
  "action": "answer",
  "final_answer": "result"
}
"""

async def calculator(expression: str) -> str:
    await asyncio.sleep(1)
    return str(eval(expression))


async def llm_reasoning(prompt: str, memory: list) -> dict:
    '''
    Decide what to do next based on memory
    '''
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"User request: {prompt}"},
        {"role": "user", "content": f"Memory: {json.dumps(memory)}"},
    ]

    response = await client.chat(
        model="llama3.2",
        messages=messages
    )

    print(f"LLM Response: {response}\n")

    content = response.message.content
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Fallback in case the LLM returns bad JSON
        print("Error: LLM did not return valid JSON. Content was:", content)
        return {"action": "answer", "final_answer": "I encountered an internal error parsing my own thoughts."}


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