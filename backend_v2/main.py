import sys

from fastapi.middleware.cors import CORSMiddleware
from fastapi_offline import FastAPIOffline

from api.root import api_root
from log import logger
from settings import PATH_VERSION_FILE

with open(PATH_VERSION_FILE, "r") as f:
    version = f.read()

app = FastAPIOffline(title="皇家小虎数据中台API", version=version)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
                   allow_credentials=True)

app.include_router(api_root)

if __name__ == '__main__':
    import uvicorn
    
    if 'darwin' in sys.platform:
        logger.info("visit openapi docs at: http://127.0.0.1:8000/docs")
        uvicorn.run("main:app", reload=True)
    else:
        logger.info('visit openapi docs at: http://nanchuan.site:8000/docs')
        uvicorn.run("main:app", reload=True, host='0.0.0.0')
