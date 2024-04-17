from fastapi import APIRouter
from fastapi import APIRouter, Depends
from helpers.__Session__ import Token_Verifier_Login

from api.v1.endpoints import Adiciona,Auth, Atualiza, Consulta , Deleta, logs


api_router = APIRouter()
api_router.include_router(Consulta.router, prefix='/Consulta', tags=["Consulta"])
api_router.include_router(Adiciona.router, prefix='/Adiciona', tags=["Adiciona"],dependencies=[Depends(Token_Verifier_Login)])
api_router.include_router(Atualiza.router, prefix='/Atualiza', tags=["Atualiza"],dependencies=[Depends(Token_Verifier_Login)])
api_router.include_router(Deleta.router, prefix='/Deleta', tags=["Deleta"],dependencies=[Depends(Token_Verifier_Login)])
api_router.include_router(Auth.router, prefix='/Auth', tags=["Auth"])
api_router.include_router(logs.router, prefix='/logs', tags=["Logs"])



