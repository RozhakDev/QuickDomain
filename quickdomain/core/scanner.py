import asyncio
import logging
import aiohttp

log = logging.getLogger(__name__)

class DomainScanner:
    """
    Kelas untuk memindai daftar domain dan memeriksa status HTTP/HTTPS mereka.
    """
    def __init__(self, domains: set, protocols: list, concurrency: int = 100, timeout: int = 10):
        """
        Inisialisasi pemindai.

        :param domains: Set domain yang akan dipindai.
        :param protocols: List protokol untuk diperiksa (misal: ['http', 'https']).
        :param concurrency: Jumlah maksimum permintaan simultan.
        :param timeout: Waktu tunggu untuk setiap permintaan.
        """
        self.domains = domains
        self.protocols = protocols
        self.concurrency = concurrency
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.results = []

    async def _check_domain(self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, url: str):
        """
        Fungsi worker untuk memeriksa satu URL. Dijalankan secara konkurens.

        :param session: Objek aiohttp.ClientSession yang dibagikan.
        :param semaphore: Objek asyncio.Semaphore untuk mengontrol konkurensi.
        :param url: URL lengkap yang akan diperiksa (misal: https://example.com).
        """
        async with semaphore:
            try:
                headers = {'User-Agent': 'QuickDomainPro/1.0'}
                async with session.head(url, allow_redirects=False, headers=headers) as response:
                    log.debug(f"Respons diterima dari {url} dengan status {response.status}")
                    return (url, response.status, response.reason)
            except asyncio.TimeoutError:
                log.warning(f"Timeout saat memeriksa {url}")
                return (url, 408, "Request Timeout")
            except aiohttp.ClientConnectorError as e:
                log.warning(f"Gagal koneksi ke {url}: {e.os_error}")
                return (url, 503, "Connection Error")
            except aiohttp.ClientError as e:
                log.warning(f"Error klien saat memeriksa {url}: {type(e).__name__}")
                return (url, 500, f"Client Error: {type(e).__name__}")
            except Exception as e:
                log.error(f"Error tidak terduga saat memeriksa {url}: {e}", exc_info=False)
                return (url, 500, "Unexpected Error")
            
    async def scan(self) -> list:
        """
        Menjalankan proses pemindaian untuk semua domain dan protokol.

        :return: List berisi tuple hasil pemindaian (url, status, reason).
        """
        semaphore = asyncio.Semaphore(self.concurrency)
        tasks = []

        connector = aiohttp.TCPConnector(ssl=False, limit_per_host=20)

        async with aiohttp.ClientSession(connector=connector, timeout=self.timeout) as session:
            for domain in self.domains:
                for protocol in self.protocols:
                    url = f"{protocol}://{domain}"
                    task = self._check_domain(session, semaphore, url)
                    tasks.append(task)

            log.info(f"Memulai {len(tasks)} tugas pemindaian dengan konkurensi {self.concurrency}...")
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return [r for r in results if not isinstance(r, Exception)]