from bvolt.api.v1.routers import health, battery, microgrid, inverter
from bvolt.infrastructure.lifecycle import ApplicationLifecycle

from fastapi import FastAPI

app = FastAPI()
app.include_router(health.router)
app.include_router(battery.router)
app.include_router(microgrid.router)

app.include_router(inverter.router)


def main() -> None:
    """
    Application entrypoint.
    """
    lifecycle = ApplicationLifecycle()
    lifecycle.start()
