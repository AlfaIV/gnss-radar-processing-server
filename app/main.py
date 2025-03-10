# from fastapi import FastAPI
# from starlette.middleware.cors import CORSMiddleware

# from app.core.container import Container
# from app.interfaces.http import router

# container = Container()
# container.config.from_yaml('config.yml')
# container.wire(modules=[__name__, 'app'])

# app = container.fastapi_app()

# app.include_router(router)

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='0.0.0.0', port=8000)

# from fastapi import FastAPI

# app = FastAPI()


from fastapi import FastAPI

from app.api.v1.routes import routers as v1_routers
from app.core.config import configs

class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI(
            title=configs.PROJECT_NAME,
            openapi_url=f"{configs.API}/openapi.json",
            version="0.0.1",
        )

        # set routes
        @self.app.get("/")
        async def root():
            return f"{configs.PROJECT_NAME} service is working"

        self.app.include_router(v1_routers, prefix=configs.API_V1_STR)

app_creator = AppCreator()
app = app_creator.app
