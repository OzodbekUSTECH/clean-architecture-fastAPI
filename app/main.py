from fastapi import FastAPI
from app.di import init_dependencies
from app.api import all_routers
from app.config import settings

app = FastAPI(
    title="CLEAN ARCHITECTURE"
)

for router in all_routers:
    app.include_router(router, prefix=settings.api_prefix)

# init_dependencies(app)
from app.di.dep_collector import collector


collector.init_dependencies(app)