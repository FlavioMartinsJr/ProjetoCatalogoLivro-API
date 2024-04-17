import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Logger import logger
from api.v1.router import api_router
from Configs import settings

log_Level = logging
app = FastAPI(title='API_V1 - PROJETO LIVRO')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1)

if __name__ == "__main__":
    logger.GravarLog("__main__","Iniciando Programa","Sitema",log_Level.WARNING)
    config = uvicorn.Config("main:app", port=7777,log_level='info', reload=True)
    server = uvicorn.Server(config)
    server.run()