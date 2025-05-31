# backend.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from typing import TypedDict, Annotated, List

load_dotenv()

# Gemini LLM + Tools
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
search_tool = TavilySearchResults(k=5)
tools = [search_tool]
tools_dict = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

# System Prompt
MEDICAL_SYSTEM_PROMPT = """
You are an experienced and knowledgeable medical AI assistant acting as a licensed doctor.

Given the patient's symptoms, perform the following steps carefully:

1. Identify the most likely medical condition(s).
2. Provide a clear diagnosis.
3. Recommend specific medicines:
   - Name, strength, dosage, frequency, and duration
4. Include precautions and side effects
5. Suggest when to see a doctor
6. Provide self-care advice

Format:

**Condition:** [Name]

**Medicines:**
- [Medicine]: [Dosage] - [Frequency] - [Duration]

**Precautions:** [Details]
"""

# Agent Setup
class AgentState(TypedDict):
    messages: Annotated[List, add_messages]
    symptoms: str
    diagnosis_complete: bool

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    return "tools" if hasattr(last_message, 'tool_calls') and last_message.tool_calls else "end"

def call_model(state: AgentState):
    messages = state["messages"]
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=MEDICAL_SYSTEM_PROMPT)] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def call_tools(state: AgentState):
    last_message = state["messages"][-1]
    tool_messages = []
    if hasattr(last_message, 'tool_calls'):
        for tool_call in last_message.tool_calls:
            try:
                result = tools_dict[tool_call["name"]].run(tool_call["args"])
                tool_messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
            except Exception as e:
                tool_messages.append(ToolMessage(content=f"Error: {str(e)}", tool_call_id=tool_call["id"]))
    return {"messages": tool_messages}

def create_medical_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", call_tools)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", "end": END})
    workflow.add_edge("tools", "agent")
    return workflow.compile()

medical_agent = create_medical_agent()

def diagnose_symptoms(symptoms: str) -> str:
    user_prompt = f"Patient symptoms: {symptoms}"
    initial_state = {
        "messages": [HumanMessage(content=user_prompt)],
        "symptoms": symptoms,
        "diagnosis_complete": False
    }
    try:
        result = medical_agent.invoke(initial_state)
        return result["messages"][-1].content
    except Exception as e:
        return f"Error: {str(e)}"

# FastAPI Setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- In production, replace "*" with your frontend URL(s)
    allow_methods=["*"],  # Allow all HTTP methods including OPTIONS and POST
    allow_headers=["*"],  # Allow all headers
)

class SymptomRequest(BaseModel):
    symptoms: str

@app.post("/diagnose")
async def diagnose(request: SymptomRequest):
    result = diagnose_symptoms(request.symptoms)
    return {"response": result}
