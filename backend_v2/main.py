import sys

from fastapi.middleware.cors import CORSMiddleware
from fastapi_offline import FastAPIOffline

from api.root import root_router
from log import logger
from settings import PATH_VERSION_FILE

with open(PATH_VERSION_FILE, "r") as f:
    version = f.read()

ALLOW_ORIGINS = [
    "http://localhost:3000",
    "http://nanchuan.site:3000"
]

app = FastAPIOffline(title="皇家小虎数据中台API", version=version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    
)

app.include_router(root_router)

if __name__ == '__main__':
    import uvicorn
    
    if 'darwin' in sys.platform:
        logger.info("visit openapi docs at: http://127.0.0.1:8000/docs")
        uvicorn.run("main:app", reload=True)
    else:
        logger.info('visit openapi docs at: http://nanchuan.site:8000/docs')
        uvicorn.run("main:app", reload=False, host='0.0.0.0')
