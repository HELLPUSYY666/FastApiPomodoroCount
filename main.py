from fastapi import FastAPI
from handlers import routers
app = FastAPI()

for router in routers:
    app.include_router(router)


@app.get("/")
async def root(name: str):
    return {"Hello": "World"}
