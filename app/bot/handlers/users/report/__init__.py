from aiogram import Router

from .fio import report_fio_router
from .floor import report_floor_router
from .cabinet import report_cabinet_router
from .reason import report_reason_router
from .description import report_description_router


report_router = Router()

report_router.include_routers(
    report_fio_router,
    report_floor_router,
    report_cabinet_router,
    report_reason_router,
    report_description_router,
)

__all__ = ["report_router"]
