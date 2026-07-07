import asyncio
import time
import logging
from aiohttp import ClientSession, ClientTimeout
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import settings
from storage import proxy_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


async def check_single_proxy(session: ClientSession, proxy_ip_port: str):
    proxy_url = f"{settings.PROXY_BASE_DOMAIN}{proxy_ip_port}"
    timeout = ClientTimeout(total=settings.TIMEOUT_SECONDS)

    start_time = time.time()
    try:
        async with session.get(settings.TEST_URL, proxy=proxy_url, timeout=timeout) as response:
            if response.status == 200:
                latency_ms = int((time.time() - start_time) * 1000)
                return latency_ms
    except Exception as e:
        logger.debug(f"Proxy {proxy_ip_port} failed. Error: {e}")
        return None
    return None


async def monitor_worker():
    logger.info("Starting automatic proxy check...")
    proxies = settings.PROXY_LIST

    async with ClientSession() as session:
        tasks = [check_single_proxy(session, proxy) for proxy in proxies]
        results = await asyncio.gather(*tasks)

        current_time = time.strftime("%H:%M:%S")

        for proxy, latency in zip(proxies, results):
            if latency is not None:
                status = "Fast" if latency <= settings.FAST_THRESHOLD_MS else "Slow"
                proxy_data[proxy] = {
                    "status": status,
                    "latency": f"{latency} ms",
                    "updated_at": current_time
                }
            else:
                proxy_data[proxy] = {
                    "status": "Dead",
                    "latency": "N/A",
                    "updated_at": current_time
                }

    logger.info(f"Proxy check completed. Total proxies updated in memory: {len(proxy_data)}")


scheduler = AsyncIOScheduler()

scheduler.add_job(monitor_worker, 'interval', seconds=settings.MONITOR_INTERVAL_SECONDS)
