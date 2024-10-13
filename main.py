import argparse
import asyncio
import time
import logging
from datetime import datetime

from quickdomain.core.extractor import DomainExtractor
from quickdomain.core.scanner import DomainScanner
from quickdomain.utils.logger import setup_logging

log = logging.getLogger(__name__)

async def main():
    """Fungsi utama untuk menjalankan alur kerja aplikasi."""
    parser = argparse.ArgumentParser(
        description="QuickDomain Pro: Pemindai Status Domain Massal yang Cepat dan Profesional.",
        epilog="Contoh: python main.py -f domains.txt -c 200 -p https"
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Path wajib ke file input yang berisi daftar domain (txt, json, dll)."
    )
    parser.add_argument(
        "-o", "--output",
        default=f"results/scan_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        help="Nama file untuk menyimpan log hasil pemindaian."
    )
    parser.add_argument(
        "-c", "--concurrency",
        type=int,
        default=100,
        help="Jumlah permintaan asinkron yang berjalan bersamaan (default: 100)."
    )
    parser.add_argument(
        "-p", "--protocols",
        nargs='+',
        default=['http', 'https'],
        choices=['http', 'https'],
        help="Protokol yang akan diperiksa (default: http https)."
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=10,
        help="Waktu tunggu (detik) untuk setiap permintaan (default: 10)."
    )

    args = parser.parse_args()

    setup_logging(args.output)

    start_time = time.time()
    log.info("=================================================")
    log.info("🔥 QuickDomain Pro Dimulai")
    log.info(f"File Input: {args.file}")
    log.info(f"Konkurensi: {args.concurrency}, Timeout: {args.timeout} detik")
    log.info(f"Protokol: {', '.join(args.protocols)}")
    log.info("=================================================")

    try:
        log.info("Mulai tahap ekstraksi domain dari file...")
        extractor = DomainExtractor(args.file)
        unique_domains = await extractor.extract_domains()

        if not unique_domains:
            log.warning("Tidak ada domain valid yang ditemukan di file input. Proses dihentikan.")
            return

        log.info(f"Ekstraksi selesai. Ditemukan {len(unique_domains)} domain unik.")

        log.info("Mulai tahap pemindaian domain...")
        scanner = DomainScanner(unique_domains, args.protocols, args.concurrency, args.timeout)
        results = await scanner.scan()

        log.info("Pemindaian selesai. Mengolah hasil...")
        
        successful_results = [res for res in results if res and 200 <= res[1] < 300]
        redirect_results = [res for res in results if res and 300 <= res[1] < 400]
        failed_results = [res for res in results if not res or res[1] >= 400]

        log.info("--- HASIL PEMINDAIAN ---")
        log.info(f"✅ Total Sukses (2xx): {len(successful_results)}")
        log.info(f"🔄 Total Redirect (3xx): {len(redirect_results)}")
        log.info(f"❌ Total Gagal/Error (4xx, 5xx, Lainnya): {len(failed_results)}")
        log.info("------------------------")

        if successful_results:
            log.info("\n--- Domain yang Merespons dengan Status 2xx ---")
            for url, status, reason in sorted(successful_results):
                log.info(f"  [+] {url} -> Status: {status} ({reason})")
        
        if redirect_results:
            log.info("\n--- Domain yang Merespons dengan Status 3xx (Redirect) ---")
            for url, status, reason in sorted(redirect_results):
                log.warning(f"  [!] {url} -> Status: {status} ({reason})")
    except FileNotFoundError:
        log.error(f"File tidak ditemukan: {args.file}")
    except Exception as e:
        log.error(f"Terjadi kesalahan yang tidak terduga: {e}", exc_info=True)
    finally:
        end_time = time.time()
        log.info("=================================================")
        log.info(f"🌟 QuickDomain Pro Selesai dalam {end_time - start_time:.2f} detik.")
        log.info(f"Hasil log lengkap tersimpan di: {args.output}")
        log.info("=================================================")

if __name__ == "__main__":
    asyncio.run(main())