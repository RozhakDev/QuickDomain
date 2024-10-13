import re
import json
import logging
from pathlib import Path
import aiofiles

log = logging.getLogger(__name__)

class DomainExtractor:
    """
    Kelas untuk mengekstrak domain dari file.
    Mendukung file teks biasa dan JSON, serta mampu membersihkan
    dan memvalidasi domain dari data yang tidak terstruktur.
    """
    DOMAIN_REGEX = re.compile(
        r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}'
    )

    def __init__(self, file_path: str):
        """
        Inisialisasi dengan path ke file input.
        
        :param file_path: String path ke file.
        """
        self.file_path = Path(file_path)

    async def extract_domains(self) -> set:
        """
        Membaca file input secara asinkron dan mengekstrak domain unik.
        Secara otomatis memilih metode ekstraksi berdasarkan ekstensi file.

        :return: Sebuah set berisi domain-domain unik yang ditemukan.
        """
        if not self.file_path.is_file():
            log.error(f"Path yang diberikan bukan file yang valid: {self.file_path}")
            raise FileNotFoundError(f"File tidak ditemukan di {self.file_path}")

        file_content = ""
        try:
            async with aiofiles.open(self.file_path, mode='r', encoding='utf-8', errors='ignore') as f:
                file_content = await f.read()
        except Exception as e:
            log.error(f"Gagal membaca file {self.file_path}: {e}")
            return set()
    
        if self.file_path.suffix == '.json':
            return self._extract_from_json(file_content)
        else:
            return self._extract_from_text(file_content)

    def _extract_from_text(self, content: str) -> set:
        """
        Mengekstrak domain dari konten teks biasa menggunakan regex.

        :param content: Konten file sebagai string.
        :return: Set domain unik.
        """
        log.debug("Mengekstrak domain menggunakan metode teks.")
        domains = self.DOMAIN_REGEX.findall(content)
        cleaned_domains = {d.strip('.').lower() for d in domains}
        return cleaned_domains
    
    def _extract_from_json(self, content: str) -> set:
        """
        Mengekstrak domain dari konten string berformat JSON.
        Secara rekursif mencari semua nilai string dalam struktur JSON.

        :param content: Konten file JSON sebagai string.
        :return: Set domain unik.
        """
        log.debug("Mengekstrak domain menggunakan metode JSON.")
        all_domains = set()
        try:
            data = json.loads(content)
            strings_found = self._find_strings_in_json(data)
            for item in strings_found:
                domains_in_string = self.DOMAIN_REGEX.findall(item)
                all_domains.update(d.strip('.').lower() for d in domains_in_string)
        except json.JSONDecodeError:
            log.warning("Gagal mendekode JSON. Mencoba ekstraksi sebagai teks biasa.")
            return self._extract_from_text(content)
        return all_domains
    
    def _find_strings_in_json(self, data) -> list:
        """
        Fungsi rekursif untuk menemukan semua nilai string dalam objek Python
        (hasil dari parsing JSON).

        :param data: Objek Python (dict, list, str, dll).
        :return: List berisi semua nilai string yang ditemukan.
        """
        strings = []
        if isinstance(data, dict):
            for key, value in data.items():
                strings.extend(self._find_strings_in_json(value))
        elif isinstance(data, list):
            for item in data:
                strings.extend(self._find_strings_in_json(item))
        elif isinstance(data, str):
            strings.append(data)
        return strings