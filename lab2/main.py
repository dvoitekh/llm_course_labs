# https://app.tavily.com/playground
# https://cloud.langfuse.com/project/cm4lw9qew000z61xwe6mikdgl

import os
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.callback import CallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from requests.exceptions import RequestException

load_dotenv(override=True)

def main():
    # Initialize LangFuse for analytics
    langfuse = Langfuse()
    langfuse_handler = CallbackHandler()

    # Verify Langfuse is set up correctly
    assert langfuse.auth_check()
    assert langfuse_handler.auth_check()

    # Initialize memory
    memory = MemorySaver()

    # Initialize the model
    client = ChatOpenAI(model="gpt-4o", temperature=0.7)

    # Set up the search tool (Replace with a working tool if necessary)
    from langchain_community.tools.tavily_search import TavilySearchResults
    search_tool = TavilySearchResults(max_results=2)
    tools = [search_tool]

    # Create the agent
    agent_executor = create_react_agent(client, tools, checkpointer=memory)

    # Config for memory threading
    config = {
        "configurable": {"thread_id": "example_thread_id"},
        "callbacks": [langfuse_handler]
    }

    # Interact with the agent
    print("Starting interaction with the agent.")

    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="hi im bob! and i live in sf")]}, config
    ):
        print(chunk)
        print("----")

    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="what is the name of their mayor?")]}, config
    ):
        print(chunk)
        print("----")

if __name__ == "__main__":
    main()
