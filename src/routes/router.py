from fastapi import APIRouter
from src.graph import ai_graph
from test import notion_page

graph = ai_graph()

router = APIRouter()


@router.get("/notionai/{query}")
def logic(query: str):
    result = graph.invoke({"message": query})
    response = result["message"]
    notion_page(markdown=response)
    return {
        "query": query,
        "response": result["message"]
    }
    
