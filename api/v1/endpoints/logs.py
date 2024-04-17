from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get('/Registros', status_code=status.HTTP_200_OK)
async def Registros_Logs():
    def iterfile(): 
        with open("Logs\\Log.txt", mode="rb") as file_like:  
            yield from file_like 

    headers = {
        'Content-Disposition': f'attachment; filename=RegistrosLog.txt'
    } 
    return StreamingResponse(iterfile(),headers=headers, media_type="application/pdf")
