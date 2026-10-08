#!/usr/bin/env python3

import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


OUTPUT_FILE = "arsip.txt"
MAX_WORKERS = 100
TIMEOUT = 7
MIN_SIZE = 3000

USER_AGENT = (
    "Mozilla/5.0 (Linux; U; Android 4.2.2; en-ca; GT-P5113 Build/JDQ39) "
    "AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30"
)

HEADERS = {
    "User-Agent": USER_AGENT,
}

EXTENSIONS = [
    "zip",
    "rar",
    "7z",
    "tar",
    "tar.gz",
    "tgz",
    "tar.bz2",
    "tbz2",
    "tar.xz",
    "txz",
]

GLOBAL_ARCHIVE_NAMES = [
    "backup",
    "backups",
    "backup-old",
    "backup_old",
    "backup-site",
    "backup_site",
    "site-backup",
    "site_backup",
    "website-backup",
    "website_backup",
    "webbackup",
    "web-backup",
    "web_backup",
    "full-backup",
    "full_backup",
    "daily-backup",
    "daily_backup",
    "weekly-backup",
    "weekly_backup",
    "monthly-backup",
    "monthly_backup",
    "bak",
    "back",
    "old",
    "old-site",
    "old_site",
    "old-web",
    "old_web",
    "old-www",
    "old_www",
    "previous",
    "previous-site",
    "previous_site",
    "legacy",
    "legacy-site",
    "legacy_site",
    "archive",
    "archives",
    "archived",
    "Archive",
    "release",
    "releases",
    "production",
    "prod",
    "staging",
    "stage",
    "development",
    "dev",
    "testing",
    "test",
    "tes",
    "public_html",
    "public",
    "Public",
    "pub",
    "www",
    "wwwroot",
    "htdocs",
    "httpdocs",
    "html",
    "web",
    "website",
    "site",
    "wordpress",
    "wp",
    "wp-backup",
    "wp_backup",
    "joomla",
    "drupal",
    "magento",
    "prestashop",
    "opencart",
    "laravel",
    "codeigniter",
    "symfony",
    "yii",
    "django",
    "flask",
    "rails",
    "node",
    "nodejs",
    "express",
    "app",
    "App",
    "apps",
    "Apps",
    "application",
    "applications",
    "backend",
    "frontend",
    "api",
    "portal",
    "admin",
    "administrator",
    "webadmin",
    "database",
    "databases",
    "db",
    "sql",
    "mysql",
    "mariadb",
    "postgres",
    "postgresql",
    "data",
    "dump",
    "dumps",
    "config",
    "configuration",
    "configs",
    "server",
    "servers",
    "source",
    "sources",
    "src",
    "project",
    "projects",
    "migration",
    "migrate",
    "maintenance",
    "maintenance-backup",
    "pemeliharaan",
    "upgrade",
    "update",
    "updates",
    "install",
    "asset",
    "assets",
    "storage",
    "upload",
    "uploads",
    "files",
    "document",
    "documents",
    "documentation",
    "resources",
    "media",
    "repository",
    "repo",
    "git",
    "gitlab",
    "github",
    "deploy",
    "deployment",
    "cache",
    "system",
    "security",
    "plugins",
    "cgi-bin",
    "index",
    "new",
    "baru",
    "lama",
    "New_Folder",
    "__MACOSX",
    "smartcity",
    "smarttaxx",
    "setwan",
    "siakad",
    "siamik",
    "sia",
    "akademik",
    "mahasiswa",
    "mhs",
    "alumni",
    "registrasi",
    "learning",
    "elearning",
    "e-learning",
    "lms",
    "belajar",
    "cbt",
    "ujian",
    "jurnal",
    "jurnall",
    "journal",
    "journals",
    "ejournal",
    "ejournall",
    "ejournals",
    "e-journal",
    "e-journals",
    "ojs",
    "ojs1",
    "ojs2",
    "ojs3",
    "ojs4",
    "ojs-3.0.1",
    "ojs-3.0-13",
    "ojs-3.1.2-4",
    "ojs-3.3.0-15",
    "ojs3.3.0-13",
    "ojs-2.4.8-5",
    "backup-ojs",
    "backup_ojs",
    "backup-jurnal",
    "backup_jurnal",
    "jurnalbackup",
    "backup-ejournal",
    "backup_ejournal",
    "opac",
    "perpustakaan",
    "pmb",
    "ppdb",
    "spmi",
    "bem",
    "organisasi",
    "lppm",
    "lp3m",
    "lpm",
    "pasca",
    "pascasarjana",
    "humas",
    "ppid",
    "jdih",
    "layanan",
    "surat",
    "info",
    "bappeda",
    "diskominfo",
    "kominfo",
    "dinas",
    "kecamatan",
    "kelurahan",
    "kabupaten",
    "kota",
    "dpmptsp",
    "dpmptspd",
    "dpmp",
    "disdukcapil",
    "dukcapil",
    "dinsos",
    "sosial",
    "disnaker",
    "disnakertrans",
    "dishub",
    "dinkes",
    "rs",
    "rsud",
    "puskesmas",
    "stikes",
    "pkm",
    "gizi",
    "pupr",
    "dinaspupr",
    "dpupr2kp",
    "dpu",
    "putr",
    "pucktr",
    "binamarga",
    "dbmsda",
    "dpuair",
    "sdabk",
    "dsdabmbk",
    "dispuprkim",
    "disperkim",
    "disperkimtan",
    "disperkimta",
    "dinaspkp",
    "dpkp",
    "dprkp",
    "prkp",
    "satpolpp",
    "damkar",
    "disdamkar",
    "kebakaran",
    "pariwisata",
    "dispar",
    "disparekraf",
    "disparbudpar",
    "dinaspariwisata",
    "dp3a",
    "dp3ap2kb",
    "p3ap2kb",
    "dpapmk",
    "dpapmkb",
    "dpppappkb",
    "inspektorat",
    "korpri",
    "rapemda",
    "peraturan",
    "po",
    "po-admin",
    "v1",
    "v2",
    "v3",
    "openSID",
    "app_openSID",
    "cms",
    "cms-sekolahku-v2.4.13",
    "kcfinder",
    "adminer",
    "cpanel",
    "password",
    "username",
    "login",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
]

_write_lock = threading.Lock()
_seen_lock = threading.Lock()
_found_urls = set()


class ProgressDisplay:
    SPINNER = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")

    def __init__(self, total: int) -> None:
        self.total = total
        self.completed = 0
        self.current_domain = "-"
        self.current_status = "READY"

        self._spinner_index = 0
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            target=self._animate,
            daemon=True,
        )

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        self._thread.join(timeout=1)
        self._render(final=True)
        sys.stdout.write("\n")
        sys.stdout.flush()

    def scanning(self, domain: str) -> None:
        with self._lock:
            self.current_domain = domain
            self.current_status = "SCANNING"

    def finished(self, domain: str, found: bool) -> None:
        with self._lock:
            self.completed += 1
            self.current_domain = domain
            self.current_status = "OK Archive" if found else "NO Archive"

    def error(self, domain: str) -> None:
        with self._lock:
            self.completed += 1
            self.current_domain = domain
            self.current_status = "ERROR"

    def _animate(self) -> None:
        while not self._stop_event.is_set():
            self._render()
            self._spinner_index = (self._spinner_index + 1) % len(self.SPINNER)
            time.sleep(0.08)

    def _render(self, final: bool = False) -> None:
        with self._lock:
            spinner = "✓" if final else self.SPINNER[self._spinner_index]
            width = max(1, len(str(self.total)))

            line = (
                f"\r{spinner} "
                f"[{self.completed:>{width}}/{self.total}] "
                f"{self.current_domain} | {self.current_status}"
            )

        terminal_width = 120

        try:
            terminal_width = os.get_terminal_size().columns
        except OSError:
            pass

        if len(line) >= terminal_width:
            line = line[: max(1, terminal_width - 1)]

        sys.stdout.write(line.ljust(max(1, terminal_width - 1)))
        sys.stdout.flush()


def normalize_site(site: str) -> str:
    site = site.strip()

    if not site:
        return ""

    if "://" not in site:
        site = f"http://{site}"

    try:
        parsed = urlparse(site)
        host = parsed.hostname or ""
    except Exception:
        return ""

    host = host.strip().lower().rstrip(".")

    if host.startswith("www."):
        host = host[4:]

    return host


def archive_candidates(site: str) -> list[str]:
    parts = [part for part in site.split(".") if part]
    names = set(GLOBAL_ARCHIVE_NAMES)

    names.update(
        {
            site,
            site.replace(".", "-"),
            site.replace(".", "_"),
            site.replace(".", ""),
        }
    )

    for part in parts:
        if len(part) < 2:
            continue

        names.update(
            {
                part,
                part.lower(),
                part.upper(),
            }
        )

    if parts:
        first = parts[0]

        names.update(
            {
                first,
                f"{first}-backup",
                f"{first}_backup",
                f"{first}backup",
                f"backup-{first}",
                f"backup_{first}",
                f"backup{first}",
                f"{first}-old",
                f"{first}_old",
                f"{first}old",
                f"old-{first}",
                f"old_{first}",
                f"old{first}",
                f"{first}-site",
                f"{first}_site",
                f"{first}site",
                f"{first}-web",
                f"{first}_web",
                f"{first}web",
                f"{first}-www",
                f"{first}_www",
                f"{first}www",
                f"{first}-prod",
                f"{first}_prod",
                f"{first}-production",
                f"{first}_production",
                f"{first}-archive",
                f"{first}_archive",
                f"{first}-database",
                f"{first}_database",
                f"{first}-db",
                f"{first}_db",
                f"{first}-source",
                f"{first}_source",
            }
        )

    if len(parts) >= 2:
        first, second = parts[0], parts[1]

        base_variants = {
            f"{first}.{second}",
            f"{first}-{second}",
            f"{first}_{second}",
            f"{first}{second}",
        }

        names.update(base_variants)

        for base in base_variants:
            names.update(
                {
                    f"{base}-backup",
                    f"{base}_backup",
                    f"backup-{base}",
                    f"backup_{base}",
                    f"{base}-old",
                    f"{base}_old",
                    f"old-{base}",
                    f"old_{base}",
                }
            )

    for year in range(2010, 2027):
        names.update(
            {
                str(year),
                f"backup-{year}",
                f"backup_{year}",
                f"backup{year}",
                f"archive-{year}",
                f"archive_{year}",
                f"archive{year}",
                f"site-{year}",
                f"site_{year}",
                f"site{year}",
                f"website-{year}",
                f"website_{year}",
                f"www-{year}",
                f"www_{year}",
            }
        )

        if parts:
            first = parts[0]

            names.update(
                {
                    f"{first}-{year}",
                    f"{first}_{year}",
                    f"{first}{year}",
                    f"{first}-backup-{year}",
                    f"{first}_backup_{year}",
                    f"{first}-backup_{year}",
                    f"{first}_backup-{year}",
                    f"backup-{first}-{year}",
                    f"backup_{first}_{year}",
                    f"{first}-archive-{year}",
                    f"{first}_archive_{year}",
                }
            )

    return sorted(
        name
        for name in names
        if name and "/" not in name and "\\" not in name
    )


def load_existing_results() -> None:
    if not os.path.exists(OUTPUT_FILE):
        return

    try:
        with open(
            OUTPUT_FILE,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as handle:
            for line in handle:
                url = line.strip()

                if url:
                    _found_urls.add(url)

    except OSError:
        pass


def save_result(url: str) -> None:
    with _seen_lock:
        if url in _found_urls:
            return

        _found_urls.add(url)

    with _write_lock:
        with open(
            OUTPUT_FILE,
            "a",
            encoding="utf-8",
        ) as handle:
            handle.write(f"{url}\n")
            handle.flush()
            os.fsync(handle.fileno())



def looks_like_archive(response: requests.Response) -> bool:
    if response.status_code != 200:
        return False

    content_type = response.headers.get("Content-Type", "").lower()
    server = response.headers.get("Server", "").lower()
    content_length = response.headers.get("Content-Length")
    etag = response.headers.get("ETag")

    if "imunify360" in server:
        return False

    if etag:
        return False

    if not content_length:
        return False

    try:
        size = int(content_length)
    except (TypeError, ValueError):
        return False

    if size <= MIN_SIZE:
        return False

    valid_types = (
        "application/",
        "binary/",
        "octet-stream",
        "zip",
        "rar",
        "compressed",
        "gzip",
        "x-gzip",
        "x-rar",
        "x-7z",
        "x-tar",
    )

    return any(item in content_type for item in valid_types)


def check_url(session: requests.Session, url: str) -> bool:
    try:
        response = session.get(
            url,
            headers=HEADERS,
            stream=True,
            timeout=TIMEOUT,
            verify=False,
            allow_redirects=True,
        )

        try:
            if looks_like_archive(response):
                save_result(url)
                return True

        finally:
            response.close()

    except requests.RequestException:
        pass

    return False


def scan_site(site: str, progress: ProgressDisplay) -> bool:
    site = normalize_site(site)

    if not site:
        return False

    progress.scanning(site)

    session = requests.Session()
    session.headers.update(HEADERS)

    archive_names = archive_candidates(site)
    schemes = ("https", "http")
    found_archive = False

    try:
        for archive_name in archive_names:
            for extension in EXTENSIONS:
                for scheme in schemes:
                    url = f"{scheme}://{site}/{archive_name}.{extension}"

                    if check_url(session, url):
                        found_archive = True
                        break

    finally:
        session.close()

    return found_archive


def load_targets(path: str) -> list[str]:
    with open(
        path,
        "r",
        encoding="utf-8",
        errors="ignore",
    ) as handle:
        return [
            line.strip()
            for line in handle
            if line.strip() and not line.strip().startswith("#")
        ]


def run() -> None:
    print("Massive Archive Backup Scanner | @github: wongalus7")
    input_file = input("List : ").strip()

    if not input_file:
        print("File list kosong.")
        return

    if not os.path.exists(input_file):
        print(f"File tidak ditemukan: {input_file}")
        return

    targets = load_targets(input_file)

    if not targets:
        print("Tidak ada target.")
        return

    load_existing_results()

    print(f"Target       : {len(targets)}")
    print(f"Workers      : {MAX_WORKERS}")
    print(f"Output       : {OUTPUT_FILE}")
    print(f"Extensions   : {len(EXTENSIONS)}")
    print(f"Archive word : {len(GLOBAL_ARCHIVE_NAMES)}+ dynamic")
    print("-" * 60)

    progress = ProgressDisplay(len(targets))
    progress.start()

    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(scan_site, target, progress): target
                for target in targets
            }

            for future in as_completed(futures):
                target = futures[future]
                normalized = normalize_site(target) or target

                try:
                    found = future.result()
                    progress.finished(normalized, found)

                except KeyboardInterrupt:
                    raise

                except Exception:
                    progress.error(normalized)

    finally:
        progress.stop()


if __name__ == "__main__":
    try:
        run()

    except KeyboardInterrupt:
        print("\nDihentikan user.")
