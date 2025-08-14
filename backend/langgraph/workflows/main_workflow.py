from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage
import asyncio

# State definition for the workflow
class AgentState(TypedDict):
    user_message: str
    route_to: List[str]
    routing_reason: str
    finance_response: str
    technical_response: str
    general_response: str
    final_response: str
    messages: Annotated[List[HumanMessage | AIMessage], add_messages]

def create_workflow():
    """Create the main workflow graph"""
    
    # Import nodes
    from ..nodes.router import RouterNode
    from ..nodes.experts import FinanceExpert, TechnicalExpert, GeneralExpert
    from ..nodes.aggregator import AggregatorNode
    
    # Initialize nodes
    router = RouterNode()
    finance_expert = FinanceExpert()
    technical_expert = TechnicalExpert()
    general_expert = GeneralExpert()
    aggregator = AggregatorNode()
    
    # Create workflow
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", router.route_query)
    workflow.add_node("finance_expert", finance_expert.process)
    workflow.add_node("technical_expert", technical_expert.process)
    workflow.add_node("general_expert", general_expert.process)
    workflow.add_node("aggregator", aggregator.synthesize)
    
    # Define conditional edges based on routing
    def route_to_experts(state):
        """Route to appropriate experts based on routing decision"""
        route_to = state.get("route_to", [])
        # Return the first expert for now (we'll handle multiple experts in the aggregator)
        if route_to:
            return route_to[0]
        return "general_expert"
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "router",
        route_to_experts,
        {
            "finance_expert": "finance_expert",
            "technical_expert": "technical_expert", 
            "general_expert": "general_expert"
        }
    )
    
    # Add edges from experts to aggregator
    workflow.add_edge("finance_expert", "aggregator")
    workflow.add_edge("technical_expert", "aggregator")
    workflow.add_edge("general_expert", "aggregator")
    
    # Add edge from aggregator to end
    workflow.add_edge("aggregator", END)
    
    # Compile workflow
    return workflow.compile()

# Create the workflow instance
workflow = create_workflow()

async def run_workflow_async(initial_state: dict):
    """Run the workflow asynchronously"""
    try:
        result = await workflow.ainvoke(initial_state)
        return result
    except Exception as e:
        print(f"Workflow execution error: {e}")
        # Return fallback response
        return {
            "final_response": f"I apologize, but there was an error processing your request: {str(e)}. Please try again or contact support if the issue persists."
        } 