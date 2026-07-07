import asyncio
import sys

sys.stderr = sys.stdout
import logging
from fasthtml.common import *
from uvicorn.config import LOGGING_CONFIG

from config import settings
from scheduler import scheduler
from storage import proxy_data


logger = logging.getLogger(__name__)


app, rt = fast_app()


def render_proxy_table():
    if not proxy_data:
        return P("Waiting for the first proxy check... Please wait.", style="color: gray;")

    headers = Tr(Th("Proxy IP:Port"), Th("Status"), Th("Latency"), Th("Last Updated"))

    rows = []
    for proxy, info in proxy_data.items():
        status = info["status"]

        if status == "Fast":
            status_style = "color: #2ecc71; font-weight: bold;"
        elif status == "Slow":
            status_style = "color: #f1c40f; font-weight: bold;"
        else:
            status_style = "color: #e74c3c; font-weight: bold;"

        row = Tr(
            Td(proxy),
            Td(status, style=status_style),
            Td(info["latency"]),
            Td(info["updated_at"])
        )
        rows.append(row)

    return Table(headers, *rows)


@rt("/")
def get():
    refresh_seconds = settings.UI_REFRESH_INTERVAL_SECONDS

    return Titled("Proxy Live Monitor",
                  Main(
                      H2("Real-time Proxy Status Dashboard"),
                      P(f"This dashboard updates automatically every {refresh_seconds} seconds "
                        f"without reloading the page.",
                        style="font-size: 0.9rem; color: gray;"),
                      Hr(),

                      Div(render_proxy_table(),
                          id="proxy-table-container",
                          hx_get="/update-table",
                          hx_trigger=f"every {refresh_seconds}s"),

                      cls="container"
                  )
                  )


@rt("/update-table")
def get_table():
    return render_proxy_table()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting background scheduler...")
    scheduler.start()
    from scheduler import monitor_worker
    asyncio.create_task(monitor_worker())


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down background scheduler...")
    scheduler.shutdown()


if __name__ == "__main__":
    LOGGING_CONFIG["handlers"]["default"]["stream"] = "ext://sys.stdout"
    LOGGING_CONFIG["handlers"]["access"]["stream"] = "ext://sys.stdout"
    serve(log_config=LOGGING_CONFIG)
