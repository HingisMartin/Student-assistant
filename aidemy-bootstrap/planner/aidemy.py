import os
import random
import requests
import vertexai
import json
from typing import TypedDict, Literal
from vertexai.preview import reasoning_engines
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from curriculums import get_curriculum 
from search import search_latest_resource 
from book import recommend_book 
from onramp_workaround import get_next_region

from google.cloud import pubsub_v1


PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")  # Get project ID from env


tools = [get_curriculum, search_latest_resource, recommend_book]
# from toolbox_core import ToolboxSyncClient

# toolbox = ToolboxSyncClient("http://127.0.0.1:5000")  # or your deployed URL

# tools = toolbox.get_tools()

def determine_tool(state: MessagesState):
    llm = ChatVertexAI(model_name="gemini-2.5-flash", location=get_next_region())
    sys_msg = SystemMessage(
                    content=(
                        f"""You are a helpful teaching assistant that helps gather all needed information. 
                            Your ultimate goal is to create a detailed 3-week teaching plan. 
                            You have access to tools that help you gather information.  
                            Based on the user request, decide which tool(s) are needed. 

                        """
                    )
                )

    llm_with_tools = llm.bind_tools(tools)
    return {"messages": llm_with_tools.invoke([sys_msg] + state["messages"])}


def prep_class(prep_needs):
   
    builder = StateGraph(MessagesState)
    builder.add_node("determine_tool", determine_tool)
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_edge(START, "determine_tool")
    builder.add_conditional_edges("determine_tool",tools_condition)
    builder.add_edge("tools", "determine_tool")

    
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": "1"}}
    messages = graph.invoke({"messages": prep_needs},config)
    print(messages)
    for m in messages['messages']:
        m.pretty_print()
    teaching_plan_result = messages["messages"][-1].content  


    return teaching_plan_result

if __name__ == "__main__":
  prep_class("I'm doing a course for  year 5 on subject Mathematics in Geometry, , get school curriculum, and come up with few books recommendation plus  search latest resources on the internet base on the curriculum outcome. And come up with a 3 week teaching plan")
