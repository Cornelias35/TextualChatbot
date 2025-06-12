from typing import Literal
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from LLM_models import State, Request

class Chatbot:
    def __init__(self, llm_with_tools, tools, llm, sys_message, request):
        self.llm_with_tools = llm_with_tools
        self.tools = tools
        self.llm = llm
        self.sys_message = sys_message
        self.request = request
        self.graph = None

    def assistant(self, state : State):
        sys_message = state["sys_message"]
        return {"messages": [self.llm_with_tools.invoke(sys_message + state["messages"])]}

    def route_tools(self, state : State) -> Literal["tools", "summary_node"]:
        if isinstance(state, list):
            ai_message = state[-1]
        elif messages := state.get("messages", []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"
        return "summary_node"

    def summarize_conversation(self, state : State):
        if state["summary_prev"]:
            summary_prev = state["summary_prev"]
            summary_message = (
                f"Summary of previous conversation: {summary_prev}\n\n"
                "Update this summary with the new messages above. Focus on key information and conciseness, maintaining the overall context."
            )
        else:
            summary_message = "Create a summary of the conversation above:"
        messages = state["messages"] + [HumanMessage(content=summary_message)]
        response = self.llm.invoke(messages)
        return {"current_summary": response.content, "messages": state["messages"]}

    def build_graph(self):
        builder = StateGraph(State)
        builder.add_node("assistant", self.assistant)
        builder.add_node("tools", ToolNode(self.tools))
        builder.add_node("summary_node", self.summarize_conversation)

        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant", self.route_tools)
        builder.add_edge("tools", "assistant")
        builder.add_edge("summary_node", END)

        self.graph = builder.compile()

    def run(self, request : Request):
        initial_state = {
            "messages": [HumanMessage(content=request.prompt)],
            "sys_message": [self.sys_message],
            "summary_prev": request.summary_prev,
        }
        self.build_graph()
        return self.graph.invoke(initial_state)