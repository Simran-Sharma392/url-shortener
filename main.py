from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import  Session
import secrets
import string

from app.database import engine, get_db, Base
from app.models import URL, Click
from app.schemas import CreateURLRequest, URLResponse, UpdateURLRequest, URLStatsResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app=FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

def generate_short_code(length=6)->str:
    """Create a short code."""
    characters=string.ascii_letters+string.digits
    return "".join(secrets.choice(characters) for _ in range(length))

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/shorten", response_model=URLResponse, status_code=201, responses = {400: {"description":"Slug already exists."}})
def shorten(request: CreateURLRequest, db: Session=Depends(get_db)):
    """Create a new shortened URL."""
    if request.slug :
        short_code = request.slug
        existing=db.query(URL).filter(URL.slug==short_code).first()
        if request.slug and existing:
            raise HTTPException(
            status_code=400,
            detail="Slug already exists."
        )
    else:
        short_code=generate_short_code()
        existing=db.query(URL).filter(URL.slug==short_code).first()
        while existing:
            short_code = generate_short_code()
            existing = db.query(URL).filter(URL.slug == short_code).first()
    db_url=URL(original_url=str(request.url), slug=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return {
        "id": db_url.id,
        "url": db_url.original_url,
        "shortCode": db_url.slug,
        "createdAt": db_url.created_at,
        "updatedAt": db_url.updated_at
    }

@app.get("/shorten/{short_code}", response_model=URLResponse, status_code=200, responses={404:{"description":"Short URL not found."}})
def retrieve_long_url(short_code:str, db:Session=Depends(get_db)):
    """Retrieve the original long URL from a short URL."""
    db_url= db.query(URL).filter(URL.slug==short_code).first()
    if not db_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found."
        )
   
    return{
        "id": db_url.id,
        "url": db_url.original_url,
        "shortCode": db_url.slug,
        "createdAt": db_url.created_at,
        "updatedAt": db_url.updated_at
        }
    
@app.put("/shorten/{short_code}", response_model=URLResponse, status_code=200, responses={404:{"description":"Short URL not found."}})
def update_short_url(request:UpdateURLRequest, short_code:str, db:Session=Depends(get_db)):
    """Update the URL the short URL redirects to."""
    db_url=db.query(URL).filter(URL.slug == short_code).first()
    if not db_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found."
        )
    
    db_url.original_url=str(request.url)
    db.commit()
    db.refresh(db_url)
    return{
        "id": db_url.id,
        "url": db_url.original_url,
        "shortCode": db_url.slug,
        "createdAt": db_url.created_at,
        "updatedAt": db_url.updated_at
        }
    
@app.delete("/shorten/{short_code}", status_code=204, responses={404:{"description":"Short URL not found."}})
def delete_url(short_code: str, db:Session=Depends(get_db)):
    """Delete a short URL."""
    db_url=db.query(URL).filter(URL.slug == short_code).first()
    if not db_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )
    
    db.delete(db_url)
    db.commit()

@app.get("/shorten/{short_code}/stats", response_model=URLStatsResponse, status_code=200, responses={404:{"description":"Short URL not found."}})
def url_stats(short_code:str, db:Session=Depends(get_db)):
    """View the statistics of a short URL."""
    db_url=db.query(URL).filter(URL.slug == short_code).first()
    if not db_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found."
        )
    
    return{
        "id": db_url.id,
        "url": db_url.original_url,
        "shortCode": db_url.slug,
        "createdAt": db_url.created_at,
        "updatedAt": db_url.updated_at,
        "accessCount": db_url.access_count,
        "clicks": db_url.clicks
        }

@app.get("/{short_code}", responses={404:{"description":"Short URL not found."}})
def redirect(short_code: str, request: Request, db: Session=Depends(get_db)):
    """Redirect the short URL to the original destination."""
    db_url=db.query(URL).filter(URL.slug==short_code).first()
    if not db_url:
        raise HTTPException(
             status_code=404,
             detail="Short URL not found."
             )
    db_url.access_count += 1
    click = Click( url_id=db_url.id, user_agent=request.headers.get("User-Agent"))
    db.add(click)
    db.commit()
    db.refresh(db_url)
    return RedirectResponse(
        url=db_url.original_url,
        status_code=307
    )