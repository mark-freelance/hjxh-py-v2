from fastapi.middleware.cors import CORSMiddleware
from fastapi_offline import FastAPIOffline

from api.routers.root import api_root
from settings import PATH_VERSION_FILE

with open(PATH_VERSION_FILE, "r") as f:
    version = f.read()

app = FastAPIOffline(title="皇家小虎数据中台API", version=version)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
                   allow_credentials=True)
app.include_router(api_root)

if __name__ == '__main__':
    import uvicorn
    
    print("visit openapi docs at: http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", reload=True)
