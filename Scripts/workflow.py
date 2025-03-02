from typing import TypedDict, List
from langgraph.graph import StateGraph
from Scripts.agents.ask_ai import AskAIAgent
from Scripts.agents.evaluation import EvaluationAgent

class WorkflowState(TypedDict):
    """Type definition for the workflow state."""
    query: str
    answer: str | None
    category: str | None
    video_links: List[str] | None

__all__ = ['handle_query']

def create_workflow():
    # Initialize agents
    ask_ai_agent = AskAIAgent()
    eval_agent = EvaluationAgent()

    # Initialize the graph with state schema
    graph = StateGraph(WorkflowState)

    # Add nodes to the graph by passing the functions directly
    graph.add_node("ask_ai", ask_ai_agent.ask_ai)
    graph.add_node("evaluate", eval_agent.evaluate)

    # Define the workflow (ask_ai -> evaluate)
    graph.add_edge("ask_ai", "evaluate")
    graph.set_entry_point("ask_ai")

    # Compile the graph into an executable workflow
    return graph.compile()

def handle_query(query):
    """Process a user query through the AI workflow."""
    # Create the workflow by initializing our agents and linking them
    executor = create_workflow()

    # Execute the workflow with the provided query as input
    result = executor.invoke({"query": query})
    return result

if __name__ == "__main__":
    # Example usage
    query = "How does photosynthesis work?"
    result = handle_query(query)

    # Display results with fallback handling if keys are missing
    print("\nAI Answer:", result.get("answer", "No answer provided"))
    print("\nQuery Category:", result.get("category", "No category provided"))
    print("\nRelevant YouTube Videos:")
    for link in result.get("video_links", []):
        print(f"- {link}")
