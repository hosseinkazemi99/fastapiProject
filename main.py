import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    uvicorn.run('config:app', host=os.environ.get('UVICORN_HOST'), port=int(os.environ.get('UVICORN_PORT')),
                reload=bool(os.environ.get('UVICORN_RELOAD')))
