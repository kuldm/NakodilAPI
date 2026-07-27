from fastapi import APIRouter

from api.routes.reports import router as reports_router
from api.routes.routes_other import router as routes_router
from api.routes.events import router as router_events
from api.routes.system import router_ping
from api.routes.seats import router as router_seats
from api.routes.seats import router_events_seats
from api.routes.organizers import router as router_organizer

__all__ = ("main_router",)


main_router = APIRouter()


main_router.include_router(reports_router)
main_router.include_router(routes_router)
main_router.include_router(router_events)
main_router.include_router(router_ping)
main_router.include_router(router_seats)
main_router.include_router(router_events_seats)
main_router.include_router(router_organizer)
