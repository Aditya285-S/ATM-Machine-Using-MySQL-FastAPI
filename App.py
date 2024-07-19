from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from Atm import Atm
from DB import connect_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.head("/")
async def read_root_head():
    return JSONResponse(content={})

@app.get('/')
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.head("/user")
async def user_head():
    return JSONResponse(content={})

@app.get('/user')
def get_create_user(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@app.post('/user')
async def create_user(card_no: int, name: str):
    conn = connect_db()
    try:
        obj = Atm(conn)
        result = obj.new_user(card_no, name)
        if result['status']:
            return JSONResponse(content={'message': result['value']})
        else:
            raise HTTPException(status_code=400, detail=result['value']})
    finally:
        conn.close()

@app.head("/createpin")
async def create_pin_head():
    return JSONResponse(content={})

@app.get('/createpin')
def get_create_pin(request: Request):
    return templates.TemplateResponse('add_pin.html', {'request': request})

@app.put('/createpin')
async def create_pin(card_no: int, pin: int):
    conn = connect_db()
    try:
        obj = Atm(conn)
        result = obj.create_pin(card_no, pin)
        if result['status']:
            return JSONResponse(content={'message': result['value']})
        else:
            raise HTTPException(status_code=400, detail=result['value']})
    finally:
        conn.close()

@app.head("/updatepin")
async def update_pin_head():
    return JSONResponse(content={})

@app.get('/updatepin')
def get_update_pin(request: Request):
    return templates.TemplateResponse("update_pin.html", {'request': request})

@app.put('/updatepin')
async def update_pin(card_no: int, pin: int):
    conn = connect_db()
    try:
        obj = Atm(conn)
        result = obj.update_pin(card_no, pin)
        if result['status']:
            return JSONResponse(content={'message': result['value']})
        else:
            raise HTTPException(status_code=400, detail=result['value']})
    finally:
        conn.close()

@app.head("/balance")
async def balance_head():
    return JSONResponse(content={})

@app.get('/balance')
def get_check_balance(request: Request):
    return templates.TemplateResponse('check_balance.html', {'request': request})

@app.post('/balance')
async def check_balance(card_no: int, pin: int):
    conn = connect_db()
    try:
        obj = Atm(conn)
        result = obj.check_balance(card_no, pin)
        if result['status']:
            return JSONResponse(content={'message': result['value']})
        else:
            raise HTTPException(status_code=400, detail=result['value']})
    finally:
        conn.close()

@app.head("/checkdetails_add")
async def check_details_add_head():
    return JSONResponse(content={})

@app.get('/checkdetails_add')
def get_details(request: Request):
    return templates.TemplateResponse('check_details_add.html', {'request': request})

@app.post('/checkdetails_add')
async def check_details(card_no: int, pin: int):
    conn = connect_db()
    try:
        obj = Atm(conn)
        result = obj.check_details(card_no, pin)
        if result['status']:
            return JSONResponse(content = {'message': result['value']})
        else:
            raise HTTPException(status_code=400, detail=result['value']})
    finally:
        conn.close()

@app.head("/checkdetails_add/addmoney")
async def check_details_add_money_head():
    return JSONResponse(content={})

@app.get('/checkdetails_add/addmoney')
def get_details(request: Request):
    return templates.TemplateResponse('add_money.html', {'request': request})

@app.put('/checkdetails_add/addmoney')
async def add_money(card_no: int, pin: int, amount: float):
    conn = connect_db()
    try:
        obj = Atm(conn)
        result = obj.add_money(card_no, pin, amount)
        if result['status']:
            return JSONResponse(content={'message': result['value']})
        else:
            raise HTTPException(status_code=400, detail=result['value']})
    finally:
        conn.close()

@app.head("/checkdetails_withdraw")
async def check_details_withdraw_head():
    return JSONResponse(content={})

@app.get('/checkdetails_withdraw')
def get_details(request: Request):
    return templates.TemplateResponse('check_details_withdraw.html', {'request': request})

@app.post('/checkdetails_withdraw')
async def check_details(card_no: int, pin: int):
    conn = connect_db()
    try:
        obj = Atm(conn)
        result = obj.check_details(card_no, pin)
        if result['status']:
            return JSONResponse(content = {'message': result['value']})
        else:
            raise HTTPException(status_code=400, detail=result['value']})
    finally:
        conn.close()

@app.head("/checkdetails_withdraw/withdraw")
async def withdraw_head():
    return JSONResponse(content={})

@app.get('/checkdetails_withdraw/withdraw')
def get_details(request: Request):
    return templates.TemplateResponse('withdraw.html', {'request': request})

@app.put('/checkdetails_withdraw/withdraw')
async def withdraw(card_no: int, pin: int, amount: float):
    conn = connect_db()
    try:
        obj = Atm(conn)
        result = obj.withdraw(card_no, pin, amount)
        if result['status']:
            return JSONResponse(content={'message': result['value']})
        else:
            raise HTTPException(status_code=400, detail=result['value']})
    finally:
        conn.close()

@app.head("/card_details")
async def card_details_head():
    return JSONResponse(content={})

@app.get('/card_details')
def user_details(request: Request):
    return templates.TemplateResponse('user_details.html', {'request': request})

@app.post('/card_details')
async def get_card_details(card_no: int):
    conn = connect_db()
    try:
        obj = Atm(conn)
        result = obj.card_details(card_no)
        if result['status']:
            return JSONResponse(content={'message': result['value']})
        else:
            raise HTTPException(status_code=400, detail=result['value']})
    finally:
        conn.close()
