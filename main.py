import json
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.params import Path, Query, Body
from starlette.requests import Request
from starlette.responses import RedirectResponse

app = FastAPI(title="Stub")


@app.get('/', include_in_schema=False)
async def landing_page():
    return RedirectResponse(url='/docs')


@app.post('/')
async def good_request(request: Request, data: dict = Body(...)):
    store(request, data)
    return {
        'detail': 'OK'
    }


@app.post('/status/{status_code}')
async def specific_request(status_code: int = Path(...),
                           msg: Optional[str] = Query(...)):
    raise HTTPException(status_code=status_code, detail=msg or 'Testing error response')


def store(request: Request, data: dict):
    filename = 'log/{timestamp}'.format(timestamp=datetime.now().timestamp())

    with open("%s.content.json" % filename, 'w+') as fh:
        fh.write(json.dumps(data, indent=4))

    with open("%s.header.json" % filename, 'w+') as fh:
        fh.write(json.dumps(dict(request.headers.items()), indent=4))

    with open("%s.query.json" % filename, 'w+') as fh:
        fh.write(json.dumps(dict(request.query_params.items()), indent=4))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
