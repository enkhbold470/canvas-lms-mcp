# Use the llms.txt file
Source: https://docs.dedaluslabs.ai/ai-optimizations/llms-txt

Give your AI assistant instant access to Dedalus documentation.

Point your AI assistant to our `llms.txt` for instant access to all Dedalus documentation and examples.

## Access URL

For a directory of links to each part of the documentation:

```
https://docs.dedaluslabs.ai/llms.txt
```

or for the entire documentation in one file:

```
https://docs.dedaluslabs.ai/llms-full.txt
```

## Usage

Tell your AI assistant:

> "Use the documentation at [https://docs.dedaluslabs.ai/llms.txt](https://docs.dedaluslabs.ai/llms.txt) to help me with Dedalus"

Your AI will instantly understand:

* All API endpoints and parameters
* Complete code examples
* Best practices and patterns
* Troubleshooting guides


# Hello World
Source: https://docs.dedaluslabs.ai/examples/01-hello-world

Basic chat completion with Dedalus

This example demonstrates the most basic usage of the Dedalus SDK - making a simple chat completion call.

<CodeGroup>
  ```python Python theme={null}
  import asyncio
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_async

  load_dotenv()

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      response = await runner.run(
          input="What was the score of the 2025 Wimbledon final?",
          model="openai/gpt-5-mini",
          mcp_servers=["windsor/exa-search-mcp"]
      )

      print(response.final_output)

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>


# Basic Tools
Source: https://docs.dedaluslabs.ai/examples/02-basic-tools

Clean tool execution with the new Runner

This example demonstrates basic tool execution using the Dedalus Runner with simple mathematical tools.

<Tip>
  GPT 5 or 4.1 (`openai/gpt-5` or `openai/gpt-4.1`) are strong tool-calling models. In general, older models may struggle with tool calling.
</Tip>

<CodeGroup>
  ```python Python theme={null}
  import asyncio
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_async

  load_dotenv()

  def add(a: int, b: int) -> int:
      """Add two numbers."""
      return a + b

  def multiply(a: int, b: int) -> int:
      """Multiply two numbers."""
      return a * b

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = await runner.run(
          input="Calculate (15 + 27) * 2", 
          model="openai/gpt-5", 
          tools=[add, multiply]
      )

      print(f"Result: {result.final_output}")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>


# Streaming
Source: https://docs.dedaluslabs.ai/examples/03-streaming

Streaming responses with Agent system

This example demonstrates streaming agent output using the built-in streaming support with the Agent system.

<CodeGroup>
  ```python Async Streaming theme={null}
  import asyncio
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_async

  load_dotenv()

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = runner.run(
          input="What do you think of Mulligan?",
          model="openai/gpt-5-mini",
          stream=True
      )

      # use stream parameter and stream_async function to stream output
      await stream_async(result)

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```python Sync Streaming theme={null}
  from dedalus_labs import Dedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_sync

  load_dotenv()

  def main():
      client = Dedalus()
      runner = DedalusRunner(client)

      result = runner.run(
          input="What do you think of Mulligan?",
          model="openai/gpt-5-mini",
          stream=True
      )

      # use stream parameter and stream_sync function to stream output
      stream_sync(result)

  if __name__ == "__main__":
      main()
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>


# MCP Integration
Source: https://docs.dedaluslabs.ai/examples/04-mcp-integration

Basic remote MCP server usage with the Dedalus SDK

This example demonstrates basic remote MCP (Model Context Protocol) server usage with the Dedalus SDK for connecting to external tools and services.

<CodeGroup>
  ```python Python theme={null}
  import asyncio
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_async

  load_dotenv()

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = await runner.run(
          input="Who won Wimbledon 2025?",
          model="openai/gpt-5-mini",
          mcp_servers=["windsor/brave-search-mcp"],
          stream=False
      )

      print(result.final_output)

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>


# Structured Outputs
Source: https://docs.dedaluslabs.ai/examples/05-structured-outputs

Type-safe JSON responses with Pydantic models

Ensure model responses adhere to a schema you define. Dedalus provides OpenAI-compatible structured outputs with automatic Pydantic validation.

<Note>
  **API Compatibility**

  Dedalus supports structured outputs via the **Chat Completions API** (`/chat/completions`), which is the industry standard interface supported across providers.

  OpenAI's **Responses API** (`/responses`) uses different parameter names (`input`, `text_format`, `output_parsed`) and requires additional infrastructure. We do not support it yet. The Chat Completions API provides equivalent functionality with broader compatibility.

  All examples below use the Chat Completions API.
</Note>

<Tip>
  **Dedalus API**

  We are committed to full Chat Completions API support and will build Dedalus-native features on Chat Completions semantics. While we will maintain feature parity with the Responses API where applicable, its integration is a lower priority. Chat Completions has broader backward compatibility with existing codebases and tooling across the ecosystem.
</Tip>

## Client API

The client provides three methods for structured outputs:

* **`.parse()`** - Non-streaming with Pydantic models
* **`.stream()`** - Streaming with Pydantic models (context manager)
* **`.create()`** - Dict-based schemas only (rejects Pydantic)

### Basic Usage with .parse()

<CodeGroup>
  ```python Non-Streaming theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class PersonInfo(BaseModel):
      name: str
      age: int
      occupation: str
      skills: list[str]

  async def main():
      client = AsyncDedalus()

      completion = await client.chat.completions.parse(
          model="openai/gpt-4o-mini",
          messages=[
              {"role": "user", "content": "Profile for Alice, 28, software engineer"}
          ],
          response_format=PersonInfo,
      )

      # Access parsed Pydantic model
      person = completion.choices[0].message.parsed
      print(f"{person.name}, {person.age}")
      print(f"Skills: {', '.join(person.skills)}")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

### Streaming with .stream()

<CodeGroup>
  ```python Streaming Events theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class PersonInfo(BaseModel):
      name: str
      age: int
      occupation: str
      skills: list[str]

  async def main():
      client = AsyncDedalus()

      # Use context manager for streaming
      async with client.chat.completions.stream(
          model="openai/gpt-4o-mini",
          messages=[{"role": "user", "content": "Profile for Bob, 32, data scientist"}],
          response_format=PersonInfo,
      ) as stream:
          # Process events as they arrive
          async for event in stream:
              if event.type == "content.delta":
                  print(event.delta, end="", flush=True)
              elif event.type == "content.done":
                  # Snapshot available at content.done
                  print(f"\nSnapshot: {event.parsed.name}")

          # Get final parsed result
          final = await stream.get_final_completion()
          person = final.choices[0].message.parsed
          print(f"\nFinal: {person.name}, {person.age}")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

### Input + Instructions Pattern

Dedalus extends OpenAI's API to support both `messages` (Chat Completions) and `input`+`instructions` (Responses) patterns:

<CodeGroup>
  ```python Input Pattern theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class PersonInfo(BaseModel):
      name: str
      age: int

  async def main():
      client = AsyncDedalus()

      # Dedalus extension: input + instructions
      completion = await client.chat.completions.parse(
          input="Profile for Carol, 35, designer",
  				model="openai/gpt-4o-mini",
          instructions="Output only structured data.",
          response_format=PersonInfo,
      )

      person = completion.choices[0].message.parsed
      print(f"{person.name}, {person.age}")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

### Optional Fields

Use `Optional[T]` for nullable fields:

<CodeGroup>
  ```python Optional Fields theme={null}
  import asyncio

  from typing import Optional

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class PartialInfo(BaseModel):
      name: str
      # You can also use `<type> | None = None` notation (Python 3.10+)
      age: Optional[int] = None
      occupation: Optional[str] = None

  async def main():
      client = AsyncDedalus()

      completion = await client.chat.completions.parse(
          model="openai/gpt-4o-mini",
          messages=[{"role": "user", "content": "Just name: Dave"}],
          response_format=PartialInfo,
      )

      person = completion.choices[0].message.parsed
      print(f"Name: {person.name}")
      print(f"Age: {person.age or 'unknown'}")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

## Streaming Helpers

Dedalus provides unified `stream_async()` and `stream_sync()` helpers that work with **both** streaming APIs:

<CodeGroup>
  ```python Unified Helper theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus
  from dedalus_labs.utils.stream import stream_async
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class PersonInfo(BaseModel):
      name: str
      age: int


  async def main():
      client = AsyncDedalus()

      # Works with .stream() (Pydantic models)
      stream = client.chat.completions.stream(
          model="openai/gpt-4o-mini",
          messages=[{"role": "user", "content": "Profile for Alice, 28"}],
          response_format=PersonInfo,
      )
      await stream_async(stream)  # Auto-detects context manager

      # Also works with .create(stream=True) (dict-based)
      stream = await client.chat.completions.create(
          model="openai/gpt-4o-mini",
          messages=[{"role": "user", "content": "Count to 10"}],
          stream=True,
      )
      await stream_async(stream)  # Auto-detects raw chunks

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

**Helper Auto-Detection:**

* Detects `ChatCompletionStreamManager` (from `.stream()`) → uses event API
* Detects raw `StreamChunk` iterator (from `.create(stream=True)`) → uses chunk API
* Single unified interface - no need to choose which helper to use

## DedalusRunner API

The Runner supports `response_format` with automatic Pydantic conversion:

<CodeGroup>
  ```python Runner with Structured Outputs theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class WeatherResponse(BaseModel):
      location: str
      temperature: int
      summary: str


  async def get_weather(location: str) -> str:
      """Get weather for a location."""
      return f"Sunny, 72°F in {location}"


  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = await runner.run(
          input="What's the weather in Paris?",
          model="openai/gpt-4o-mini",
          tools=[get_weather],
          response_format=WeatherResponse,  # Pydantic model
          max_steps=5,
      )

      print(result.final_output)

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

<Note>
  The Runner auto-converts Pydantic models to dict schemas. For tool-only workflows without structured final output, omit `response_format`.
</Note>

### Tools + Structured Outputs with Client API

For more control, use the client's `.parse()` method with `tools` parameter.

<Note>
  Tools must have `"strict": true` and `"additionalProperties": false` when used with `.parse()`. This ensures both the response and tool calls are validated.
</Note>

<CodeGroup>
  ```python Tools + Structured Outputs theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class WeatherInfo(BaseModel):
      location: str
      temperature: int
      conditions: str


  async def main():
      client = AsyncDedalus()

      # Define strict tool schemas (required for .parse())
      tools = [
          {
              "type": "function",
              "function": {
                  "name": "get_weather",
                  "description": "Get weather for a location",
                  "parameters": {
                      "type": "object",
                      "properties": {
                          "location": {"type": "string"}
                      },
                      "required": ["location"],
                      "additionalProperties": False,
                  },
                  "strict": True,
              }
          }
      ]

      completion = await client.chat.completions.parse(
          model="openai/gpt-4o-mini",
          messages=[{"role": "user", "content": "What's the weather in Paris?"}],
          tools=tools,
          response_format=WeatherInfo,
      )

      # Check if tool was called or structured response returned
      message = completion.choices[0].message
      if message.tool_calls:
          print(f"Tool called: {message.tool_calls[0].function.name}")
      elif message.parsed:
          print(f"Weather: {message.parsed.location}, {message.parsed.temperature}°C")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

## .create() vs .parse() vs .stream()

| Method      | Pydantic Support | Streaming | Use Case                |
| ----------- | ---------------- | --------- | ----------------------- |
| `.create()` | ❌ Dict only      | ✓         | Manual JSON schemas     |
| `.parse()`  | ✓ Direct         | ❌         | Type-safe non-streaming |
| `.stream()` | ✓ Direct         | ✓         | Type-safe streaming     |

<Note>
  `.create()` will throw a `TypeError` if you pass a Pydantic model:

  ```
  TypeError: You tried to pass a `BaseModel` class to `chat.completions.create()`;
  You must use `chat.completions.parse()` instead
  ```
</Note>

## Advanced: Nested Models

<CodeGroup>
  ```python Nested Structures theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class Skill(BaseModel):
      name: str
      years_experience: int


  class DetailedProfile(BaseModel):
      name: str
      age: int
      skills: list[Skill]


  async def main():
      client = AsyncDedalus()

      completion = await client.chat.completions.parse(
          model="openai/gpt-4o-mini",
          messages=[{
              "role": "user",
              "content": "Profile for expert developer Alice, 28, with 5 years Python and 3 years Rust"
          }],
          response_format=DetailedProfile,
      )

      profile = completion.choices[0].message.parsed
      print(f"{profile.name}: {len(profile.skills)} skills")
      for skill in profile.skills:
          print(f"  - {skill.name}: {skill.years_experience}y")
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

## Error Handling

<CodeGroup>
  ```python Refusals theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class PersonInfo(BaseModel):
      name: str
      age: int


  async def main():
      client = AsyncDedalus()

      completion = await client.chat.completions.parse(
          model="openai/gpt-4o-mini",
          messages=[{"role": "user", "content": "Generate harmful content"}],
          response_format=PersonInfo,
      )

      message = completion.choices[0].message
      if message.refusal:
          print(f"Model refused: {message.refusal}")
      elif message.parsed:
          print(f"Parsed: {message.parsed.name}")
      else:
          print("No response or parsing failed")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

## Advanced Patterns

### Messages + Instructions Override

<CodeGroup>
  ```python Override System Message theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class PersonInfo(BaseModel):
      name: str
      age: int


  async def main():
      client = AsyncDedalus()

      # Instructions override system message in messages list
      completion = await client.chat.completions.parse(
          model="openai/gpt-4o-mini",
          messages=[
              {"role": "system", "content": "This gets replaced"},
              {"role": "user", "content": "Profile for Eve, 29"}
          ],
          instructions="Be concise.",  # Overrides system message
          response_format=PersonInfo,
      )

      person = completion.choices[0].message.parsed
      print(f"{person.name}, {person.age}")
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

### Using Dict Response Format

For cases where you can't use Pydantic models, use dict-based schemas:

<CodeGroup>
  ```python Dict Schema theme={null}
  import asyncio
  import json

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv

  load_dotenv()


  async def main():
      client = AsyncDedalus()

      # Manual JSON schema
      response_format = {
          "type": "json_schema",
          "json_schema": {
              "name": "person",
              "strict": True,
              "schema": {
                  "type": "object",
                  "properties": {
                      "name": {"type": "string"},
                      "age": {"type": "integer"}
                  },
                  "required": ["name", "age"],
                  "additionalProperties": False
              }
          }
      }

      # Works with .create() and streaming
      completion = await client.chat.completions.create(
          model="openai/gpt-4o-mini",
          messages=[{"role": "user", "content": "Profile for Frank, 31"}],
          response_format=response_format,
      )

      data = json.loads(completion.choices[0].message.content)
      print(f"{data['name']}, {data['age']}")
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

### MCP Servers Flexibility

The `mcp_servers` parameter accepts both single strings and lists:

<CodeGroup>
  ```python Flexible MCP Servers theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class Info(BaseModel):
      result: str


  async def main():
      client = AsyncDedalus()

      # Single string
      completion = await client.chat.completions.parse(
          model="openai/gpt-4o-mini",
          messages=[{"role": "user", "content": "What time is it?"}],
          mcp_servers="time",  # Single server
          response_format=Info,
      )

      # List of servers
      completion = await client.chat.completions.parse(
          model="openai/gpt-4o-mini",
          messages=[{"role": "user", "content": "Check my notes"}],
          mcp_servers=["time", "memory"],  # Multiple servers
          response_format=Info,
      )
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

## Supported Models

The SDK's `.parse()` and `.stream()` methods work across all providers. Schema enforcement varies by provider:

**Strict Enforcement** (CFG-based, schema guarantees):

* ✓ `openai/*` - Context-free grammar compilation
* ✓ `xai/*` - Native schema validation
* ✓ `fireworks_ai/*` - Native schema validation (select models)
* ✓ `deepseek/*` - Native schema validation (select models)

**Best-Effort** (schema sent for guidance, no guarantees):

* 🟡 `google/*` - Schema forwarded to `generationConfig.responseSchema`. Typically conforms but not guaranteed.
* 🟡 `anthropic/*` - Prompt-based JSON generation. \~85-90% success rate.

<Warning>
  For `google/*` and `anthropic/*` models, always validate parsed output and implement retry logic. The SDK uses schemas for validation but cannot enforce adherence.
</Warning>

<Note>
  **HTTP API Limitation:** The `response_format` parameter in raw HTTP requests only works with OpenAI/xAI/Fireworks/DeepSeek. Use the SDK's `.parse()` method for cross-provider support.
</Note>

## Quick Reference

### All Streaming Methods Compared

| Method                 | Syntax                                                      | Pydantic    | Events          | Use When           |
| ---------------------- | ----------------------------------------------------------- | ----------- | --------------- | ------------------ |
| `.create(stream=True)` | `await client.chat.completions.create(stream=True, ...)`    | ❌ Dict only | Raw chunks      | Legacy/simple      |
| `.stream()`            | `async with client.chat.completions.stream(...) as stream:` | ✓           | Granular events | Pydantic models    |
| `stream_async()`       | `await stream_async(stream)`                                | ✓ Both      | Auto-detect     | Convenience helper |

### Helper Functions

```python  theme={null}
from dedalus_labs.lib.utils.stream import stream_async, stream_sync

# Async
await stream_async(stream)  # Works with .stream() or .create(stream=True)

# Sync
stream_sync(stream)  # Works with .stream() or .create(stream=True)
```

The helpers auto-detect the stream type and use the appropriate API.

## OpenAI Responses API Translation

OpenAI's documentation primarily shows the Responses API. Here's how to translate those examples to our Chat Completions API:

| OpenAI Responses API       | Dedalus Chat Completions API            | Notes                   |
| -------------------------- | --------------------------------------- | ----------------------- |
| `client.responses.parse()` | `client.chat.completions.parse()`       | Different resource path |
| `input=[...]`              | `messages=[...]`                        | Parameter name differs  |
| `text_format=Model`        | `response_format=Model`                 | Parameter name differs  |
| `response.output_parsed`   | `completion.choices[0].message.parsed`  | Different access path   |
| `response.output_text`     | `completion.choices[0].message.content` | Different access path   |
| `response.status`          | `completion.choices[0].finish_reason`   | Different field         |

### Example Translation

<CodeGroup>
  ```python OpenAI Responses API (not supported) theme={null}
  from openai import OpenAI
  from pydantic import BaseModel

  client = OpenAI()

  class CalendarEvent(BaseModel):
      name: str
      date: str
      participants: list[str]

  # This will NOT work with Dedalus
  response = client.responses.parse(
      model="gpt-4o-2024-08-06",
      input=[
          {"role": "system", "content": "Extract the event information."},
          {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
      ],
      text_format=CalendarEvent,
  )

  event = response.output_parsed
  ```

  ```python Dedalus Chat Completions API (supported) theme={null}
  import asyncio

  from dedalus_labs import AsyncDedalus
  from dotenv import load_dotenv
  from pydantic import BaseModel

  load_dotenv()


  class CalendarEvent(BaseModel):
      name: str
      date: str
      participants: list[str]


  async def main():
      client = AsyncDedalus()

      # Use this instead
      completion = await client.chat.completions.parse(
          model="openai/gpt-4o-mini",
          messages=[
              {"role": "system", "content": "Extract the event information."},
              {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
          ],
          response_format=CalendarEvent,
      )

      event = completion.choices[0].message.parsed
      print(f"Event: {event.name} on {event.date}")
      print(f"Participants: {', '.join(event.participants)}")


  if __name__ == "__main__":
      asyncio.run(main())
  ```
</CodeGroup>

<Info>
  The Responses API requires additional infrastructure beyond what Chat Completions provides. Chat Completions has broader ecosystem support and backward compatibility with existing codebases.
</Info>


# Model Handoffs
Source: https://docs.dedaluslabs.ai/examples/06-handoffs

Multi-model routing where the agent intelligently selects the best model based on task complexity

This example demonstrates multi-model routing where the agent intelligently selects the best model based on task complexity, with model attributes for optimization.

<Tip>
  Claude (`anthropic/claude-sonnet-4-20250514`) is great at writing and creative tasks. Experiment with different models for different use-cases!
</Tip>

<CodeGroup>
  ```python Python theme={null}
  import os
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_async
  import asyncio

  load_dotenv()

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = await runner.run(
          input="Find the year GPT-5 released, and handoff to Claude to write a haiku about Elon Musk. Output this haiku. Use your tools.",
          model=["openai/gpt-5", "claude-sonnet-4-20250514"],
          mcp_servers=["windsor/brave-search-mcp"],
          stream=False
      )

      print(result.final_output)

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>


# Tool Chaining
Source: https://docs.dedaluslabs.ai/examples/07-tool-chaining

Advanced tool chaining workflow with async execution

This example demonstrates advanced tool chaining where multiple tools are executed in sequence, with the Runner handling complex multi-step workflows automatically.

<Tip>
  GPT 5 or 4.1 (`openai/gpt-5` or `openai/gpt-4.1`) are strong tool-calling models. In general, older models may struggle with tool calling.
</Tip>

<CodeGroup>
  ```python Python theme={null}
  import asyncio
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_async

  load_dotenv()

  def celsius_to_fahrenheit(celsius: float) -> float:
      """Convert temperature from Celsius to Fahrenheit."""
      return (celsius * 9/5) + 32

  def get_clothing_recommendation(temp_f: float) -> str:
      """Recommend clothing based on temperature in Fahrenheit."""
      if temp_f < 32:
          return "Heavy winter coat, gloves, hat, and warm boots"
      elif temp_f < 50:
          return "Warm jacket or coat, long pants, closed shoes"
      elif temp_f < 65:
          return "Light jacket or sweater, long pants"
      elif temp_f < 80:
          return "T-shirt or light shirt, comfortable pants or shorts"
      else:
          return "Lightweight clothing, shorts, sandals, and sun protection"

  def plan_activity(temp_f: float, clothing: str) -> str:
      """Suggest outdoor activities based on temperature and clothing."""
      if temp_f < 32:
          return f"Great weather for skiing, ice skating, or cozy indoor activities. Dress in: {clothing}"
      elif temp_f < 50:
          return f"Perfect for hiking, jogging, or outdoor photography. Dress in: {clothing}"
      elif temp_f < 80:
          return f"Ideal for picnics, outdoor sports, or walking in the park. Dress in: {clothing}"
      else:
          return f"Excellent for swimming, beach activities, or water sports. Dress in: {clothing}"

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = await runner.run(
          input="It's 22 degrees Celsius today in Paris. Convert this to Fahrenheit, recommend what I should wear, suggest outdoor activities, and search for current weather conditions in Paris to confirm.",
          model=["openai/gpt-5"],
          tools=[celsius_to_fahrenheit, get_clothing_recommendation, plan_activity],
          mcp_servers=["joerup/open-meteo-mcp", "windsor/brave-search-mcp"],
          stream=False
      )

      print(result.final_output)

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>


# Concert Planner
Source: https://docs.dedaluslabs.ai/examples/use-case/concert-planner

Create a concert planner agent using the Ticketmaster MCP to search for concerts and venue information.

<CodeGroup>
  ```python Python theme={null}
  import asyncio
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_async

  load_dotenv()

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = await runner.run(
          input="""I want to see Taylor Swift perform in New York City. 
          Can you help me find upcoming concerts, get details about the venue, 
          and provide information about ticket prices? I'm particularly interested 
          in accessibility information and seating options.""",
          model="openai/gpt-4.1",
          mcp_servers=["windsor/ticketmaster-mcp"]
      )

      print(f"Concert Planning Results:\n{result.final_output}")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

<Tip>
  This example uses the Ticketmaster MCP (`windsor/ticketmaster-mcp`).

  Try it out in your projects!
</Tip>


# Data Analyst
Source: https://docs.dedaluslabs.ai/examples/use-case/data-analyst

Create a data analyst agent that can search for real-time data, write and execute Python code to analyze it, and generate insights.

<CodeGroup>
  ```python Python theme={null}
  import asyncio
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dedalus_labs.utils.stream import stream_async
  from dotenv import load_dotenv

  load_dotenv()

  def execute_python_code(code: str) -> str:
      """
      Execute Python code and return the result.
      Safely executes code in a controlled namespace.
      """
      try:
          namespace = {}
          exec(code, {"__builtins__": __builtins__}, namespace)

          if 'result' in namespace:
              return str(namespace['result'])

          results = {k: v for k, v in namespace.items() if not k.startswith('_')}
          return str(results) if results else "Code executed successfully"
      except Exception as e:
          return f"Error executing code: {str(e)}"

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = runner.run(
          input="""Research the current stock price of Tesla (TSLA) and Apple (AAPL).
          Then write and execute Python code to:
          1. Compare their current prices
          2. Calculate the percentage difference
          3. Determine which stock has grown more in the past year based on the data you find
          4. Provide investment insights based on your analysis

          Use web search to get the latest stock information.""",
          model="openai/gpt-5",
          tools=[execute_python_code],
          mcp_servers=["windsor/brave-search-mcp"],
          stream=True
      )

      await stream_async(result)

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

<Tip>
  This data analyst example combines real-time web search with code execution capabilities:

  * **Brave Search MCP** (`windsor/brave-search-mcp`): Fetches real-time data from the web
  * **execute\_python\_code** tool: Allows the agent to write and run Python code for analysis

  The agent can search for current information, extract relevant data, then dynamically write code to analyze it and generate insights.

  **Note**: In production environments, consider using sandboxed code execution for security.
</Tip>


# Travel Agent
Source: https://docs.dedaluslabs.ai/examples/use-case/travel-agent

Creating a travel planning agent that can search for flights, hotels, and provide travel recommendations.

<CodeGroup>
  ```python Python theme={null}
  import asyncio
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_async

  load_dotenv()

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = await runner.run(
          input="""I'm planning a trip to Paris, France from New York City 
          for 5 days in October. Can you help me find:
          1. Flight options and prices
          2. Hotel recommendations in central Paris
          3. Weather forecast for my travel dates
          4. Popular attractions and restaurants
          5. Currency exchange rates and travel tips
          
          My budget is around $3000 total and I prefer mid-range accommodations.""",
          model="openai/gpt-4.1",
          mcp_servers=[
              "joerup/exa-mcp",        # For semantic travel research
              "windsor/brave-search-mcp", # For travel information search
              "joerup/open-meteo-mcp"   # For weather at destination
          ]
      )

      print(f"Travel Planning Results:\n{result.final_output}")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

<Tip>
  This travel agent example uses multiple MCP servers:

  * **Exa MCP** (`joerup/exa-mcp`): For semantic search of travel content and recommendations
  * **Brave Search MCP** (`windsor/brave-search-mcp`): For finding current travel information, reviews, and booking options
  * **Open Meteo MCP** (`joerup/open-meteo-mcp`): For weather forecasts at your destination

  Try these servers out in your projects!
</Tip>


# Weather Forecaster
Source: https://docs.dedaluslabs.ai/examples/use-case/weather-forecaster

Create a weather forecasting agent using the Open Meteo MCP to provide detailed weather information and forecasts.

<CodeGroup>
  ```python Python theme={null}
  import asyncio
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_async

  load_dotenv()

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = await runner.run(
          input="""I'm planning a outdoor wedding in San Francisco next weekend. 
          Can you provide:
          1. Current weather conditions
          2. 7-day forecast with hourly details
          3. Probability of precipitation
          4. Temperature highs and lows
          5. Wind conditions and UV index
          6. Recommendations for outdoor event planning based on the forecast""",
          model="openai/gpt-4.1",
          mcp_servers=["joerup/open-meteo-mcp"]
      )

      print(f"Weather Forecast Results:\n{result.final_output}")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

<Tip>
  This example uses the Open Meteo MCP (`joerup/open-meteo-mcp`) which provides:

  * Current weather conditions
  * Multi-day weather forecasts
  * Hourly weather data
  * Historical weather information
  * Weather alerts and warnings

  Try it out in your projects!
</Tip>


# Web Search Agent
Source: https://docs.dedaluslabs.ai/examples/use-case/web-search-agent

Create a web search agent using multiple search MCPs to find and analyze information from the web.

<CodeGroup>
  ```python Python theme={null}
  import asyncio
  from dedalus_labs import AsyncDedalus, DedalusRunner
  from dotenv import load_dotenv
  from dedalus_labs.utils.stream import stream_async

  load_dotenv()

  async def main():
      client = AsyncDedalus()
      runner = DedalusRunner(client)

      result = await runner.run(
          input="""I need to research the latest developments in AI agents for 2024. 
          Please help me:
          1. Find recent news articles about AI agent breakthroughs
          2. Search for academic papers on multi-agent systems
          3. Look up startup companies working on AI agents
          4. Find GitHub repositories with popular agent frameworks
          5. Summarize the key trends and provide relevant links
          
          Focus on developments from the past 6 months.""",
          model="openai/gpt-4.1",
          mcp_servers=[
              "joerup/exa-mcp",        # Semantic search engine
              "windsor/brave-search-mcp"  # Privacy-focused web search
          ]
      )

      print(f"Web Search Results:\n{result.final_output}")

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ```typescript TypeScript theme={null}
  Coming soon.
  ```
</CodeGroup>

<Tip>
  This example uses multiple search MCP servers:

  * **Exa MCP** (`joerup/exa-mcp`)
  * **Brave Search MCP** (`windsor/brave-search-mcp`)

  Try these servers out in your projects!
</Tip>


# FAQ
Source: https://docs.dedaluslabs.ai/faq

Frequently Asked Questions

<AccordionGroup>
  <Accordion icon="question" title="Why use Dedalus?" defaultOpen>
    * We make it easy to build complex AI agents with just 5 (or so) lines of code.
    * Agents built with our SDK can connect to any MCP server on our marketplace, switch between any model provider, and even execute locally-defined tools.
    * Don’t yet see an MCP you want to use on our marketplace? Upload any MCP server and we’ll host it for free.
  </Accordion>

  <Accordion icon="key" title="How do I get an API key?" defaultOpen>
    Log into your [dashboard](https://dedaluslabs.ai) and navigate to the "API Keys" section.
  </Accordion>

  <Accordion icon="key" title="Can I bring my own API key?" defaultOpen>
    Yes! However, you don't need to. With a `DEDALUS_API_KEY` in your environment, we take care of routing to any provider or model for you, including handoffs between models from different providers. For an example, see our [handoffs](https://docs.dedaluslabs.ai/examples/06-handoffs) page.
  </Accordion>

  <Accordion icon="code" title="What languages do you support?" defaultOpen>
    Our SDK is currently available for Python and TypeScript (beta), with plans for Go in the near future. We accept MCP servers written Python and TypeScript. For best practices in writing MCP servers see our [server guidelines](https://docs.dedaluslabs.ai/server-guidelines).
  </Accordion>

  <Accordion icon="lock" title="Is authentication supported?" defaultOpen>
    Not yet, but it's coming soon! Until authentication is supported, please ensure your servers are stateless and do not require auth.
  </Accordion>

  <Accordion icon="envelope" title="How do I send feedback?" defaultOpen>
    Send us an email at [support@dedaluslabs.ai](mailto:support@dedaluslabs.ai) or send a message in our [Discord](https://discord.gg/K3SjuFXZJw).
  </Accordion>
</AccordionGroup>


# Quickstart
Source: https://docs.dedaluslabs.ai/index

Get started with the Dedalus SDK.

# Setup and Integration

<AccordionGroup defaultOpen>
  <Accordion icon="key" title="Get Your API Key" defaultOpen>
    To use Dedalus Labs, you'll need an API key. To get one:

    1. Create an account at [dedaluslabs.ai](https://dedaluslabs.ai).
    2. Navigate to your dashboard.
    3. Generate a new API key in the settings section.
    4. Add your API key to your environment as `DEDALUS_API_KEY`. Keep your API key secure and never share it publicly.
  </Accordion>

  <Accordion icon="code" title="Install Our SDK" defaultOpen>
    We provide SDKs for multiple programming languages to make integration seamless:

    <CodeGroup>
      ```bash Python theme={null}
      pip install dedalus-labs
      ```

      ```bash TypeScript theme={null}
      npm install dedalus-labs
      ```
    </CodeGroup>
  </Accordion>

  <Accordion icon="hand-wave" title="Hello World" defaultOpen>
    This example demonstrates the most basic usage of the Dedalus SDK - making a simple chat completion call.

    <CodeGroup>
      ```python Python theme={null}
      import asyncio
      from dedalus_labs import AsyncDedalus, DedalusRunner
      from dotenv import load_dotenv
      from dedalus_labs.utils.stream import stream_async

      load_dotenv()

      async def main():
          client = AsyncDedalus()
          runner = DedalusRunner(client)

          response = await runner.run(
              input="What was the score of the 2025 Wimbledon final?",
              model="openai/gpt-5-mini",
              mcp_servers=["windsor/exa-search-mcp"]
          )

          print(response.final_output)

      if __name__ == "__main__":
          asyncio.run(main())
      ```

      ```typescript TypeScript theme={null}
      Coming soon.
      ```
    </CodeGroup>
  </Accordion>

  <Accordion icon="hammer" title="Basic Tools" defaultOpen>
    This example demonstrates basic tool execution using the Dedalus Runner with simple mathematical tools.

    <Tip>
      GPT 5 or 4.1 (`openai/gpt-5` or `openai/gpt-4.1`) are strong tool-calling models. In general, older models may struggle with tool calling.
    </Tip>

    <CodeGroup>
      ```python Python theme={null}
      import asyncio
      from dedalus_labs import AsyncDedalus, DedalusRunner
      from dotenv import load_dotenv
      from dedalus_labs.utils.stream import stream_async

      load_dotenv()

      def add(a: int, b: int) -> int:
          """Add two numbers."""
          return a + b

      def multiply(a: int, b: int) -> int:
          """Multiply two numbers."""
          return a * b

      async def main():
          client = AsyncDedalus()
          runner = DedalusRunner(client)

          result = await runner.run(
              input="Calculate (15 + 27) * 2",
              model="openai/gpt-5",
              tools=[add, multiply]
          )

          print(f"Result: {result.final_output}")

      if __name__ == "__main__":
          asyncio.run(main())
      ```

      ```typescript TypeScript theme={null}
      Coming soon.
      ```
    </CodeGroup>
  </Accordion>
</AccordionGroup>

<CardGroup cols={4}>
  <Card title="Streaming" icon="water" href="examples/03-streaming" />

  <Card title="MCP Integration" icon="plug" href="examples/04-mcp-integration" />

  <Card title="Model Handoffs" icon="arrows-rotate" href="examples/06-handoffs" />

  <Card title="Tool Chaining" icon="link" href="examples/07-tool-chaining" />
</CardGroup>

# Next Steps

<Card title="View the Examples" icon="book-open" href="examples/use-case/travel-agent">
  See detailed examples for your use-case
</Card>

<Card title="Join Our Community" icon="discord" href="https://discord.com/invite/RuDhZKnq5R">
  Get help, suggest improvements, and connect with other developers.
</Card>


# Introduction
Source: https://docs.dedaluslabs.ai/introduction

Dedalus Labs is building the MCP gateway for next-gen AI applications by unifying the fragmented AI-agent ecosystem with a **single drop-in API endpoint**. 

<CardGroup cols={2}>
  <Card title="Quickstart" img="https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-1.png?fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=030d4cfe0974199ec62070046fa7c587" href="/index" data-og-width="2408" width="2408" data-og-height="2512" height="2512" data-path="images/card-design-1.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-1.png?w=280&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=2601424e7cd8e9a13a02a6362b61895b 280w, https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-1.png?w=560&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=918e1ab518e882df96a534dd206067ce 560w, https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-1.png?w=840&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=65fd6654e049ec9668f46952d457607e 840w, https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-1.png?w=1100&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=52ad009f3a1d2b0f6835fd2539deddfc 1100w, https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-1.png?w=1650&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=6cc6c7d03147c8f79a98c9a0367d24f2 1650w, https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-1.png?w=2500&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=ebed645f11a8ef0a63eb0ff295a51daf 2500w">
    Jump right in and start building agents with our SDK.
  </Card>

  <Card title="Examples" img="https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-wing.png?fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=0b96280d21a77d0078fb4df9666fb912" href="/examples/use-case/travel-agent" data-og-width="2408" width="2408" data-og-height="2512" height="2512" data-path="images/card-design-wing.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-wing.png?w=280&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=821dfbbc850b54fc4b7b0b29d6823f15 280w, https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-wing.png?w=560&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=c1d1b9669ddf8d171384a9dfa6e74d2f 560w, https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-wing.png?w=840&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=01ab66a6c5bc4bc0fea07f211181e957 840w, https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-wing.png?w=1100&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=e822e6d58ef78a51c476d4f0f4a439e0 1100w, https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-wing.png?w=1650&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=73a9ecf07c53242542d0c5a12175f6a0 1650w, https://mintcdn.com/dedaluslabs/h04RAzy7Uc9PSpSd/images/card-design-wing.png?w=2500&fit=max&auto=format&n=h04RAzy7Uc9PSpSd&q=85&s=a816fd81baa63f08d03935cf65870819 2500w">
    Explore real-world examples and use cases to inspire your projects.
  </Card>
</CardGroup>

## Give Your Agents Wings with Dedalus

* We host and manage your MCP servers
* Users can select models from any vendor and combine various tools from our MCP marketplace
* Teams can transition from concept to functioning agents with tools in minutes


# Model Providers
Source: https://docs.dedaluslabs.ai/providers

Mix and match models from supported providers.

<CardGroup cols={3}>
  <Card title="OpenAI" icon="robot">
    `OPENAI_API_KEY`
  </Card>

  <Card title="Anthropic" icon="brain">
    `ANTHROPIC_API_KEY`
  </Card>

  <Card title="Google Gemini" icon="google">
    `GOOGLE_API_KEY`
  </Card>

  <Card title="Fireworks AI" icon="fire">
    `FIREWORKS_API_KEY`
  </Card>

  <Card title="xAI" icon="x">
    `XAI_API_KEY`
  </Card>

  <Card title="Perplexity" icon="circle-question">
    `PERPLEXITY_API_KEY`
  </Card>

  <Card title="DeepSeek" icon="magnifying-glass">
    `DEEPSEEK_API_KEY`
  </Card>

  <Card title="Groq" icon="bolt">
    `GROQ_API_KEY`
  </Card>

  <Card title="Cohere" icon="comments">
    `COHERE_API_KEY`
  </Card>

  <Card title="Together AI" icon="users">
    `TOGETHERAPI_KEY`
  </Card>

  <Card title="Cerebras" icon="microchip">
    `CEREBRAS_API_KEY`
  </Card>

  <Card title="Mistral" icon="wind">
    `MISTRAL_API_KEY`
  </Card>
</CardGroup>

## Supported Models

### OpenAI

#### Chat Models

* `openai/gpt-5`
* `openai/gpt-5-mini`
* `openai/gpt-5-nano`
* `openai/gpt-5-chat-latest`
* `openai/gpt-5-codex`
* `openai/gpt-5-pro`
* `openai/gpt-4.1`
* `openai/gpt-4.1-mini`
* `openai/gpt-4.1-nano`
* `openai/gpt-4o`
* `openai/gpt-4o-2024-05-13`
* `openai/gpt-4o-mini`
* `openai/gpt-4o-search-preview`
* `openai/gpt-4o-mini-search-preview`
* `openai/chatgpt-4o-latest`
* `openai/gpt-4-turbo`
* `openai/gpt-4-turbo-2024-04-09`
* `openai/gpt-4`
* `openai/gpt-4-0125-preview`
* `openai/gpt-4-1106-preview`
* `openai/gpt-4-1106-vision-preview`
* `openai/gpt-4-0613`
* `openai/gpt-4-0314`
* `openai/gpt-4-32k`
* `openai/gpt-3.5-turbo`
* `openai/gpt-3.5-turbo-0125`
* `openai/gpt-3.5-turbo-1106`
* `openai/gpt-3.5-turbo-0613`
* `openai/gpt-3.5-0301`
* `openai/gpt-3.5-turbo-instruct`
* `openai/gpt-3.5-turbo-16k-0613`

#### Reasoning Models

* `openai/o1`
* `openai/o1-pro`
* `openai/o1-mini`
* `openai/o1-preview`
* `openai/o3`
* `openai/o3-pro`
* `openai/o3-mini`
* `openai/o3-deep-research`
* `openai/o4-mini`
* `openai/o4-mini-deep-research`

#### Image Generation

* `openai/dall-e-3`

#### Audio Transcription

* `openai/whisper-1`

### Anthropic (Claude)

#### Claude 4.5 Series

* `anthropic/claude-haiku-4-5-20251001`
* `anthropic/claude-sonnet-4-5-20250929`

#### Claude 4 Series

* `anthropic/claude-opus-4-1-20250805`
* `anthropic/claude-opus-4-20250514`
* `anthropic/claude-sonnet-4-20250514`

#### Claude 3.7 Series

* `anthropic/claude-3-7-sonnet-20250219`

#### Claude 3.5 Series

* `anthropic/claude-3-5-sonnet-20241022`
* `anthropic/claude-3-5-haiku-20241022`

#### Claude 3 Series

* `anthropic/claude-3-opus-20240229`
* `anthropic/claude-3-sonnet-20240229`
* `anthropic/claude-3-haiku-20240307`

### Google (Gemini)

#### Gemini 2.5 Series

* `google/gemini-2.5-pro`
* `google/gemini-2.5-flash`
* `google/gemini-2.5-flash-lite`

#### Gemini 2.0 Series

* `google/gemini-2.0-flash`
* `google/gemini-2.0-flash-exp`
* `google/gemini-2.0-flash-001`
* `google/gemini-2.0-flash-lite`

#### Gemini 1.5 Series

* `google/gemini-1.5-pro`
* `google/gemini-1.5-flash`

#### Image Generation Models

* `google/gemini-2.5-flash-image`
* `google/gemini-2.5-flash-image-preview`
* `google/gemini-2.0-flash-exp-image-generation`
* `google/gemini-2.0-flash-preview-image-generation`

### xAI (Grok)

#### Grok 4 Series

* `xai/grok-4-fast-reasoning`
* `xai/grok-4-fast-non-reasoning`
* `xai/grok-code-fast-1`
* `xai/grok-4-0709`

#### Grok 3 Series

* `xai/grok-3`
* `xai/grok-3-mini`

#### Grok 2 Series

* `xai/grok-2`
* `xai/grok-2-1212`
* `xai/grok-2-vision-1212`

#### Legacy

* `xai/grok-beta`

### DeepSeek

* `deepseek/deepseek-chat`
* `deepseek/deepseek-reasoner`
* `deepseek/deepseek-coder`

### Fireworks AI

#### GLM Models

* `fireworks/glm-4p5`
* `fireworks/glm-4p6`
* `fireworks/glm-4p5-air`

#### Meta Llama Models

* `fireworks/llama-v3p1-405b-instruct`
* `fireworks/llama-v3p1-70b-instruct`
* `fireworks/llama-v3p1-8b-instruct`
* `fireworks/llama-v3p2-1b-instruct`
* `fireworks/llama-v3p2-3b-instruct`
* `fireworks/llama-v3p3-70b-instruct`

#### Qwen Models

* `fireworks/accounts/fireworks/models/qwen2p5-72b-instruct`
* `fireworks/accounts/fireworks/models/qwen-v2p5-7b`
* `fireworks/qwen2p5-72b-instruct`
* `fireworks/qwen-v2p5-7b`

#### Mixtral Models

* `fireworks/accounts/fireworks/models/mixtral-8x7b-instruct`
* `fireworks/accounts/fireworks/models/mixtral-8x22b-instruct`
* `fireworks/mixtral-8x7b-instruct`
* `fireworks/mixtral-8x22b-instruct`

#### FireFunction

* `fireworks/accounts/fireworks/models/firefunction-v2`
* `fireworks/firefunction-v2`

#### DBRX

* `fireworks/dbrx-instruct`


# MCP Server Guidelines
Source: https://docs.dedaluslabs.ai/server-guidelines

Ensure your server works with the Dedalus platform.

<Warning>
  We're open-sourcing an MCP framework to help users easily build and deploy their MCP servers in October 2025.
  Until then, users are encouraged to structure their MCP servers according to the [templates](#key-details) below.
</Warning>

# Key Details

* **We support both TypeScript and Python servers:**
  * **TypeScript servers:** We look for an `index.ts` in `src/`. The simplest server is a repo with a `src/` folder with `index.ts` in it that starts the server. Use this [template](https://github.com/windsornguyen/brave-search-mcp) ([copy as markdown](https://gitingest.com/dedalus-labs/brave-search-mcp)).
  * **Python servers:** We look for a `main.py` in `src/`. The simplest server is a repo with a `src/` folder with `main.py` in it that starts the server. Use this [template](https://github.com/dedalus-labs/framework-mcp) ([copy as markdown](https://gitingest.com/dedalus-labs/framework-mcp)). Dedalus has open-sourced the MCP framework—install the required `openmcp` package with:

    ```
    git clone https://github.com/dedalus-labs/openmcp-python

    cd openmcp-python    # Keep here so Claude/Codex can inspect

    uv pip install -e .  # Install as an editable

    uv pip show openmcp  # Should display a version

    #Don't forget to active your virtual environment
    ```
* Since servers will be remotely deployed, they must use the streamable HTTP transport method.

<Warning>
  Authentication is under rapid development but is not currently supported. Accordingly, your servers should be stateless and not require auth.
</Warning>

# Full MCP Server Architecture Guide

<Tip>
  Pro tip: Click the "Copy page" button to paste this page as context to your coding assistant to refactor your existing server to follow our recommended specification.
</Tip>

## Overview

This guide defines the standard architecture and conventions for Model Context Protocol (MCP) servers with streamable HTTP transport. This structure ensures consistency, maintainability, and production readiness across all MCP server implementations.

## Core Principles

1. **Modular Architecture** - Clear separation of concerns with dedicated modules
2. **Streamable HTTP First** - Modern HTTP transport as the primary interface
3. **Type Safety** - Full TypeScript coverage with proper interfaces
4. **Production Ready** - Built-in error handling, logging, and configuration management
5. **Testable** - Dependency injection and isolated components

## Directory Structure

```
project-root/
├── src/
│   ├── index.ts            # Main entry point
│   ├── cli.ts              # Command-line argument parsing
│   ├── config.ts           # Configuration management
│   ├── server.ts           # Server instance creation
│   ├── client.ts           # External API client
│   ├── types.ts            # TypeScript type definitions
│   ├── tools/
│   │   ├── index.ts        # Tool exports
│   │   └── [service].ts    # Tool definitions and handlers
│   └── transport/
│       ├── index.ts        # Transport exports
│       ├── http.ts         # HTTP transport (primary)
│       └── stdio.ts        # STDIO transport (development)
├── package.json
├── tsconfig.json
└── .gitignore
```

## Implementation Guide

### 1. Main Entry Point (`src/index.ts`)

The main entry point should handle transport selection and error management:

```typescript  theme={null}
#!/usr/bin/env node

import { config as loadEnv } from 'dotenv';
loadEnv();

import { loadConfig } from './config.js';
import { parseArgs } from './cli.js';
import { [Service]Server } from './server.js';
import { runStdioTransport, startHttpTransport } from './transport/index.js';

/**
 * Transport selection logic:
 * 1. --stdio flag forces STDIO transport
 * 2. Default: HTTP transport for production compatibility
 */
async function main() {
    try {
        const config = loadConfig();
        const cliOptions = parseArgs();
        
        if (cliOptions.stdio) {
            // STDIO transport for local development
            const server = new [Service]Server(config.apiKey);
            await runStdioTransport(server.getServer());
        } else {
            // HTTP transport for production/cloud deployment
            const port = cliOptions.port || config.port;
            startHttpTransport({ ...config, port });
        }
    } catch (error) {
        console.error("Fatal error running [Service] server:", error);
        process.exit(1);
    }
}

main();
```

### 2. Configuration Management (`src/config.ts`)

Centralized configuration with environment variable validation:

```typescript  theme={null}
import dotenv from 'dotenv';
dotenv.config();

export interface Config {
    apiKey: string;
    port: number;
    isProduction: boolean;
}

export function loadConfig(): Config {
    const apiKey = process.env['[SERVICE]_API_KEY'];
    if (!apiKey) {
        throw new Error('[SERVICE]_API_KEY environment variable is required');
    }

    const port = parseInt(process.env.PORT || '8080', 10);
    const isProduction = process.env.NODE_ENV === 'production';

    return { apiKey, port, isProduction };
}
```

### 3. Command Line Interface (`src/cli.ts`)

Standardized CLI with help documentation:

```typescript  theme={null}
export interface CliOptions {
    port?: number;
    stdio?: boolean;
}

export function parseArgs(): CliOptions {
    const args = process.argv.slice(2);
    const options: CliOptions = {};
    
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--port':
                if (i + 1 < args.length) {
                    options.port = parseInt(args[i + 1], 10);
                    i++;
                } else {
                    throw new Error('--port flag requires a value');
                }
                break;
            case '--stdio':
                options.stdio = true;
                break;
            case '--help':
                printHelp();
                process.exit(0);
                break;
        }
    }
    return options;
}

function printHelp(): void {
    console.log(`
[Service] MCP Server

USAGE:
    [service] [OPTIONS]

OPTIONS:
    --port <PORT>    Run HTTP server on specified port (default: 8080)
    --stdio          Use STDIO transport instead of HTTP
    --help           Print this help message

ENVIRONMENT VARIABLES:
    [SERVICE]_API_KEY    Required: Your [Service] API key
    PORT                 HTTP server port (default: 8080)
    NODE_ENV            Set to 'production' for production mode
`);
}
```

### 4. Type Definitions (`src/types.ts`)

All TypeScript interfaces and types:

```typescript  theme={null}
/**
 * Arguments for [tool_name] tool
 */
export interface [Tool]Args {
    // Define tool-specific arguments
    query: string;
    options?: Record<string, unknown>;
}

/**
 * External API response structure
 */
export interface [Service]Response {
    // Define API response structure
    data: unknown;
    metadata?: Record<string, unknown>;
}
```

### 5. External API Client (`src/client.ts`)

Dedicated client for external API interactions:

```typescript  theme={null}
import { [Service]Response } from './types.js';

export class [Service]Client {
    private apiKey: string;
    private baseUrl: string = 'https://api.[service].com';

    constructor(apiKey: string) {
        this.apiKey = apiKey;
    }

    /**
     * Performs API request with proper error handling
     */
    async performRequest(params: unknown): Promise<string> {
        const response = await fetch(`${this.baseUrl}/endpoint`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`,
            },
            body: JSON.stringify(params),
        });

        if (!response.ok) {
            let errorText: string;
            try {
                errorText = await response.text();
            } catch {
                errorText = "Unable to parse error response";
            }
            throw new Error(
                `[Service] API error: ${response.status} ${response.statusText}\n${errorText}`
            );
        }

        const data: [Service]Response = await response.json();
        return this.formatResponse(data);
    }

    private formatResponse(data: [Service]Response): string {
        // Format response according to service requirements
        return JSON.stringify(data, null, 2);
    }
}
```

### 6. Tool Definitions (`src/tools/[service].ts`)

Tool definitions with handlers following the established pattern:

```typescript  theme={null}
import { Tool, CallToolResult } from '@modelcontextprotocol/sdk/types.js';
import { [Service]Client } from '../client.js';
import { [Tool]Args } from '../types.js';

/**
 * Tool definition for [tool_name]
 */
export const [tool]ToolDefinition: Tool = {
    name: "[service]_[action]",
    description: "Description of what this tool does and when to use it.",
    inputSchema: {
        type: "object",
        properties: {
            // Define input schema
        },
        required: ["required_field"],
    },
};

/**
 * Type guard for [tool] arguments
 */
function is[Tool]Args(args: unknown): args is [Tool]Args {
    return (
        typeof args === "object" &&
        args !== null &&
        "required_field" in args &&
        typeof (args as { required_field: unknown }).required_field === "string"
    );
}

/**
 * Handles [tool] tool calls
 */
export async function handle[Tool]Tool(
    client: [Service]Client, 
    args: unknown
): Promise<CallToolResult> {
    try {
        if (!args) {
            throw new Error("No arguments provided");
        }

        if (!is[Tool]Args(args)) {
            throw new Error("Invalid arguments for [service]_[action]");
        }

        const result = await client.performRequest(args);
        
        return {
            content: [{ type: "text", text: result }],
            isError: false,
        };
    } catch (error) {
        return {
            content: [
                {
                    type: "text",
                    text: `Error: ${error instanceof Error ? error.message : String(error)}`,
                },
            ],
            isError: true,
        };
    }
}
```

### 7. Tool Exports (`src/tools/index.ts`)

Centralized tool exports:

```typescript  theme={null}
export {
    [tool]ToolDefinition,
    handle[Tool]Tool,
    // Export all tool definitions and handlers
} from './[service].js';
```

### 8. Server Instance (`src/server.ts`)

Server configuration with tool registration:

```typescript  theme={null}
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
    InitializedNotificationSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { [Service]Client } from './client.js';
import {
    [tool]ToolDefinition,
    handle[Tool]Tool,
} from './tools/index.js';

export function createStandaloneServer(apiKey: string): Server {
    const serverInstance = new Server(
        {
            name: "org/[service]",
            version: "0.2.0",
        },
        {
            capabilities: {
                tools: {},
            },
        }
    );

    const [service]Client = new [Service]Client(apiKey);

    serverInstance.setNotificationHandler(InitializedNotificationSchema, async () => {
        console.log('[Service] MCP client initialized');
    });

    serverInstance.setRequestHandler(ListToolsRequestSchema, async () => ({
        tools: [[tool]ToolDefinition],
    }));

    serverInstance.setRequestHandler(CallToolRequestSchema, async (request) => {
        const { name, arguments: args } = request.params;
        
        switch (name) {
            case "[service]_[action]":
                return await handle[Tool]Tool([service]Client, args);
            default:
                return {
                    content: [{ type: "text", text: `Unknown tool: ${name}` }],
                    isError: true,
                };
        }
    });

    return serverInstance;
}

export class [Service]Server {
    private apiKey: string;

    constructor(apiKey: string) {
        this.apiKey = apiKey;
    }

    getServer(): Server {
        return createStandaloneServer(this.apiKey);
    }
}
```

### 9. HTTP Transport (`src/transport/http.ts`)

Streamable HTTP transport with session management:

```typescript  theme={null}
import { createServer, IncomingMessage, ServerResponse } from 'http';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { randomUUID } from 'crypto';
import { createStandaloneServer } from '../server.js';
import { Config } from '../config.js';

const sessions = new Map<string, { transport: StreamableHTTPServerTransport; server: any }>();

export function startHttpTransport(config: Config): void {
    const httpServer = createServer();

    httpServer.on('request', async (req, res) => {
        const url = new URL(req.url!, `http://${req.headers.host}`);

        switch (url.pathname) {
            case '/mcp':
                await handleMcpRequest(req, res, config);
                break;
            case '/sse':
                await handleSSERequest(req, res, config);
                break;
            case '/health':
                handleHealthCheck(res);
                break;
            default:
                handleNotFound(res);
        }
    });

    const host = config.isProduction ? '0.0.0.0' : 'localhost';
    
    httpServer.listen(config.port, host, () => {
        logServerStart(config);
    });
}

async function handleMcpRequest(
    req: IncomingMessage,
    res: ServerResponse,
    config: Config
): Promise<void> {
    const sessionId = req.headers['mcp-session-id'] as string | undefined;

    if (sessionId) {
        const session = sessions.get(sessionId);
        if (!session) {
            res.statusCode = 404;
            res.end('Session not found');
            return;
        }
        return await session.transport.handleRequest(req, res);
    }

    if (req.method === 'POST') {
        await createNewSession(req, res, config);
        return;
    }

    res.statusCode = 400;
    res.end('Invalid request');
}

async function handleSSERequest(
    req: IncomingMessage,
    res: ServerResponse,
    config: Config
): Promise<void> {
    const serverInstance = createStandaloneServer(config.apiKey);
    const transport = new SSEServerTransport('/sse', res);
    
    try {
        await serverInstance.connect(transport);
        console.log('SSE connection established');
    } catch (error) {
        console.error('SSE connection error:', error);
        res.statusCode = 500;
        res.end('SSE connection failed');
    }
}

async function createNewSession(
    req: IncomingMessage,
    res: ServerResponse,
    config: Config
): Promise<void> {
    const serverInstance = createStandaloneServer(config.apiKey);
    const transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: () => randomUUID(),
        onsessioninitialized: (sessionId) => {
            sessions.set(sessionId, { transport, server: serverInstance });
            console.log('New [Service] session created:', sessionId);
        }
    });

    transport.onclose = () => {
        if (transport.sessionId) {
            sessions.delete(transport.sessionId);
            console.log('[Service] session closed:', transport.sessionId);
        }
    };

    try {
        await serverInstance.connect(transport);
        await transport.handleRequest(req, res);
    } catch (error) {
        console.error('Streamable HTTP connection error:', error);
        res.statusCode = 500;
        res.end('Internal server error');
    }
}

function handleHealthCheck(res: ServerResponse): void {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        service: '[service]-mcp',
        version: '0.2.0'
    }));
}

function handleNotFound(res: ServerResponse): void {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
}

function logServerStart(config: Config): void {
    const displayUrl = config.isProduction 
        ? `Port ${config.port}` 
        : `http://localhost:${config.port}`;
    
    console.log(`[Service] MCP Server listening on ${displayUrl}`);

    if (!config.isProduction) {
        console.log('Put this in your client config:');
        console.log(JSON.stringify({
            "mcpServers": {
                "[service]": {
                    "url": `http://localhost:${config.port}/mcp`
                }
            }
        }, null, 2));
        console.log('For backward compatibility, you can also use the /sse endpoint.');
    }
}
```

### 10. STDIO Transport (`src/transport/stdio.ts`)

Simple STDIO transport for development:

```typescript  theme={null}
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

export async function runStdioTransport(server: Server): Promise<void> {
    const transport = new StdioServerTransport();
    
    try {
        await server.connect(transport);
        console.error("[Service] MCP Server running on stdio");
    } catch (error) {
        console.error("Failed to start STDIO transport:", error);
        throw error;
    }
}
```

### 11. Transport Exports (`src/transport/index.ts`)

```typescript  theme={null}
export { startHttpTransport } from './http.js';
export { runStdioTransport } from './stdio.js';
```

## Configuration Files

### package.json Configuration

```json  theme={null}
{
  "name": "[service]-mcp-server",
  "version": "0.2.0",
  "type": "module",
  "main": "dist/index.js",
  "bin": {
    "[service]-mcp": "dist/index.js"
  },
  "files": [
    "dist"
  ],
  "scripts": {
    "build": "tsc && shx chmod +x dist/*.js",
    "prepare": "npm run build",
    "watch": "tsc --watch",
    "start": "node dist/index.js",
    "start:stdio": "node dist/index.js --stdio",
    "dev": "tsc && node dist/index.js",
    "dev:stdio": "tsc && node dist/index.js --stdio"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.17.3"
  }
}
```

**Key Configuration Points:**

* `"main": "dist/index.js"` - Points to compiled entry point
* `"bin"` - Makes the server executable as a CLI tool
* `"files": ["dist"]` - Only includes compiled code in npm package
* `"type": "module"` - Enables ES modules
* `"@modelcontextprotocol/sdk": "^1.17.3"` - **Required**: Version 1.16.0+ needed for StreamableHTTPServerTransport

### TypeScript Configuration

```json  theme={null}
{
  "compilerOptions": {
    "target": "ES2015",
    "module": "ESNext",
    "outDir": "./dist",
    "rootDir": ".",
    "strict": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "moduleResolution": "node"
  },
  "include": [
    "src/**/*.ts"
  ],
  "exclude": [
    "node_modules",
    "dist"
  ]
}
```

**Build Process:**

1. TypeScript compiles `src/index.ts` → `dist/index.js`
2. Package.json points to compiled version
3. Build script makes output executable
4. No root-level index.ts needed

### .gitignore

```gitignore  theme={null}
# Build artifacts
node_modules/
dist/
npm-debug.log
yarn-error.log

# Environment files
.env
*.env

# IDE files
.vscode/
.idea/
*.swp
*.swo

# System files
.DS_Store
Thumbs.db
```

## Best Practices

### 1. Error Handling

* Always wrap API calls in try-catch blocks
* Provide meaningful error messages
* Log errors for debugging while sanitizing sensitive data

### 2. Type Safety

* Define interfaces for all data structures
* Use type guards for runtime validation
* Enable strict TypeScript checking

### 3. Session Management

* Implement proper session cleanup
* Handle connection timeouts
* Monitor memory usage for session storage

### 4. Production Readiness

* Use environment variables for configuration
* Implement health checks
* Add structured logging
* Consider rate limiting for external APIs

### 5. Testing

* Keep components isolated for easy unit testing
* Mock external API clients in tests
* Test both transport methods

## Migration Checklist

When refactoring an existing MCP server to this architecture:

* [ ] Create modular directory structure with `src/` folder
* [ ] Move main entry point to `src/index.ts` (single entry point)
* [ ] Extract configuration management (`src/config.ts`)
* [ ] Separate CLI argument parsing (`src/cli.ts`)
* [ ] Create dedicated API client class (`src/client.ts`)
* [ ] Define TypeScript interfaces (`src/types.ts`)
* [ ] Create server instance factory (`src/server.ts`)
* [ ] Move tool definitions to separate files (`src/tools/[service].ts`)
* [ ] Implement modular transport system (`src/transport/`)
* [ ] Add streamable HTTP transport as primary
* [ ] Configure package.json to point to `dist/index.js`
* [ ] Set up proper TypeScript compilation (`src/` → `dist/`)
* [ ] Add health check endpoint
* [ ] Update build scripts and .gitignore
* [ ] Add proper error handling throughout
* [ ] Test both HTTP and STDIO transport methods

This architecture ensures consistency, maintainability, and production readiness across all MCP server implementations while prioritizing the modern streamable HTTP transport.


