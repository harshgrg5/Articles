from typing import List, Optional
from fastapi import FastAPI, Path, Query, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from models import ApiResponse, Article, ArticleCreate, ErrorDetail
from database import db_repo

app = FastAPI(
    title="Articles REST API",
    description="A simple, fast, and structured REST API for managing articles.",
    version="1.0.0"
)


# --- Custom Exception Handlers ---

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    error_code = "NOT_FOUND" if exc.status_code == status.HTTP_404_NOT_FOUND else "HTTP_ERROR"
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiResponse(
            success=False,
            error=ErrorDetail(
                code=error_code,
                message=str(exc.detail)
            )
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = " -> ".join([str(loc) for loc in err.get("loc", [])])
        errors.append({"field": field, "msg": err.get("msg")})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY if hasattr(status, "HTTP_422_UNPROCESSABLE_ENTITY") else 422,
        content=ApiResponse(
            success=False,
            error=ErrorDetail(
                code="INVALID_INPUT",
                message="Request validation failed. Please check input parameters.",
                details={"errors": errors}
            )
        ).model_dump()
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ApiResponse(
            success=False,
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected server error occurred."
            )
        ).model_dump()
    )


# --- API Routes ---

@app.get("/", response_model=ApiResponse[dict], summary="API Root")
def get_root():
    """Returns basic API info and endpoints summary."""
    return ApiResponse(
        success=True,
        data={
            "name": "Articles REST API",
            "version": "1.0.0",
            "docs_url": "/docs",
            "endpoints": {
                "structured_articles_list": "GET /articles",
                "structured_article_detail": "GET /articles/{id}",
                "raw_myapp_list": "GET /myapp/list/",
                "raw_myapp_detail": "GET /myapp/list/{id}",
                "create_article": "POST /articles",
                "health": "GET /health"
            }
        }
    )


@app.get("/health", response_model=ApiResponse[dict], summary="Health Check")
def health_check():
    """Health check status endpoint."""
    return ApiResponse(
        success=True,
        data={"status": "healthy"}
    )


# Standard Structured GET /articles
@app.get(
    "/articles",
    response_model=ApiResponse[List[Article]],
    summary="Get Structured List of Articles",
    response_description="Returns a clean, structured JSON envelope with data array and pagination metadata."
)
def get_articles(
    prompt: Optional[str] = Query(None, description="Filter articles by prompt category (e.g. 'Virtual Realms')"),
    search: Optional[str] = Query(None, description="Search query matching title, short description, or content"),
    limit: int = Query(10, ge=1, le=100, description="Page size limit (1-100)"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """
    Retrieve articles in standard ApiResponse JSON wrapper with metadata.
    """
    articles, total = db_repo.get_all(
        prompt=prompt,
        search=search,
        limit=limit,
        offset=offset
    )

    return ApiResponse(
        success=True,
        data=articles,
        meta={
            "total": total,
            "count": len(articles),
            "limit": limit,
            "offset": offset,
            "has_more": (offset + len(articles)) < total
        }
    )


# Standard Structured GET /articles/{id}
@app.get(
    "/articles/{id}",
    response_model=ApiResponse[Article],
    summary="Get Article by ID",
    response_description="Returns structured single article object or 404 error response."
)
def get_article_by_id(
    id: int = Path(..., gt=0, description="Positive integer ID of article")
):
    """
    Retrieve a single article by ID.
    
    Validates that `id` is a positive integer.
    """
    article = db_repo.get_by_id(id)
    if not article:
        raise StarletteHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with ID {id} was not found."
        )

    return ApiResponse(
        success=True,
        data=article
    )


# Direct Raw Array GET /myapp/list/ (Matching sample output format)
@app.get(
    "/myapp/list/",
    response_model=List[Article],
    summary="Get Raw List of Articles",
    response_description="Direct JSON list of articles matching standard REST listing format."
)
def get_myapp_list(
    prompt: Optional[str] = Query(None, description="Filter articles by prompt category"),
    search: Optional[str] = Query(None, description="Search keyword"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Direct array endpoint returning `[ { "id": 4, "title": "...", ... }, ... ]`.
    """
    articles, _ = db_repo.get_all(prompt=prompt, search=search, limit=limit, offset=offset)
    return articles


# Direct Raw Object GET /myapp/list/{id}
@app.get(
    "/myapp/list/{id}",
    response_model=Article,
    summary="Get Raw Single Article",
    response_description="Direct JSON object of single article."
)
def get_myapp_detail(
    id: int = Path(..., gt=0, description="Positive integer ID")
):
    """
    Direct single object endpoint returning article directly or 404 error.
    """
    article = db_repo.get_by_id(id)
    if not article:
        raise StarletteHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with ID {id} was not found."
        )
    return article


# POST /articles
@app.post(
    "/articles",
    response_model=ApiResponse[Article],
    status_code=status.HTTP_201_CREATED,
    summary="Create Article"
)
def create_article(article_in: ArticleCreate):
    """
    Create a new article entry.
    """
    new_article = db_repo.create(article_in)
    return ApiResponse(
        success=True,
        data=new_article
    )
