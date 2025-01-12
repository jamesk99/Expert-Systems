from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from decision_tree import Node, root  # Import your existing decision tree

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NodeResponse(BaseModel):
    question: Optional[str]
    options: List[str]
    result: Optional[str]

class Decision(BaseModel):
    choice: str

@app.get("/")
async def read_root():
    return {"status": "active"}

@app.get("/node/{node_id}", response_model=NodeResponse)
async def get_node(node_id: str = "root"):
    # Convert path to node
    if node_id == "root":
        current_node = root
    else:
        # Parse path and traverse tree
        try:
            current_node = root
            choices = node_id.split('.')
            for choice in choices:
                current_node = current_node.children[choice]
        except (KeyError, AttributeError):
            raise HTTPException(status_code=404, detail="Node not found")
    
    return NodeResponse(
        question=current_node.question,
        options=current_node.options,
        result=current_node.result
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)