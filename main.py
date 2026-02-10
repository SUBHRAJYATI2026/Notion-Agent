from fastapi import FastAPI
from src.routes.router import router
import uvicorn

app = FastAPI()


# @app.get("/{query}")
# def logic(query: str):
#     return {"query": query}


app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="localhost", port=8000)
