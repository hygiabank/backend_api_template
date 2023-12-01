from fastapi import FastAPI
from .database import init_db
from .security import init_security
from .exceptions import init_error_handling
from .routes import init_routes
from .middlewares import init_middlewares

def create_app() -> FastAPI:
    app = FastAPI(title="Backend", description="Backend for some App", version="0.0.1")

    init_db(app)
    init_error_handling(app)
    init_routes(app)
    init_security(app)
    init_middlewares(app)

    return app
