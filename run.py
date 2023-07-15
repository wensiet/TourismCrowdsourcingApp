import uvicorn
from API import app
from fastapi.middleware.cors import CORSMiddleware
if __name__ == "__main__":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app)
