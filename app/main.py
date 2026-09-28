from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middlewares.exception_handler import register_exception_handlers
from app.routers import auth, crm, admin

def create_application() -> FastAPI:
    """Khởi tạo và cấu hình ứng dụng FastAPI"""
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # Cấu hình CORS cho phép Frontend truy cập
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Đăng ký Global Exception Handlers (Trọng tâm SCRUM-38)
    register_exception_handlers(application)

    # Đăng ký các router nghiệp vụ
    application.include_router(auth.router, prefix=settings.API_V1_STR)
    application.include_router(crm.router, prefix=settings.API_V1_STR)
    application.include_router(admin.router, prefix=settings.API_V1_STR)

    @application.get("/", tags=["Health Check"])
    def root():
        return {
            "success": True,
            "message": "CRM Backend API đang hoạt động bình thường",
            "version": settings.VERSION,
            "docs": "/docs"
        }

    @application.get("/health", tags=["Health Check"])
    def health_check():
        return {"status": "healthy"}

    return application

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
