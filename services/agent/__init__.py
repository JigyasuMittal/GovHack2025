"""Agent package placeholder.

The agent orchestrates calls to the API tools based on natural language
input.  In this proof‑of‑concept implementation, the agent is very
simple: it calls the intent endpoint, then services, SEIFA, labour and
rulecards sequentially to build a plan.  In future iterations the
agent could leverage LangGraph or LLM function calling.
"""