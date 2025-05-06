import asyncio
import httpx
from pathlib import Path
from typing import List, Set
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.config.settings import settings
from app.utils.helpers import (
    setup_logger,
    async_retry,
    timing_decorator,
    clean_html_content,
)

logger = setup_logger(__name__)

class CrawlerService:
    def __init__(self):
        self.results_dir = Path(settings.RESULTS_DIR)
        self.results_dir.mkdir(exist_ok=True)

    def extract_domain(self, url: str) -> str:
        """Извлечение домена из URL"""
        from tldextract import extract
        extracted = extract(url)
        return f"{extracted.domain}.{extracted.suffix}"

    @async_retry(max_retries=settings.MAX_RETRIES, delay=settings.RETRY_DELAY)
    async def check_subdomain(self, session: httpx.AsyncClient, domain: str, subdomain: str) -> str:
        """Проверка доступности поддомена"""
        url = f"https://{subdomain}.{domain}"
        try:
            response = await session.head(url, follow_redirects=True, timeout=settings.REQUEST_TIMEOUT)
            if response.status_code < 400:
                return str(response.url)
        except Exception as e:
            logger.warning(f"Failed to check subdomain {url}: {e}")
        return ""

    @timing_decorator
    async def scan_subdomains(self, domain: str) -> List[str]:
        """Сканирование поддоменов"""
        subdomains = Path(settings.SUBDOMAINS_FILE).read_text().splitlines()
        async with httpx.AsyncClient(verify=False) as client:
            tasks = [self.check_subdomain(client, domain, sd) for sd in subdomains]
            results = await asyncio.gather(*tasks)
        return list(filter(None, results))

    @async_retry(max_retries=settings.MAX_RETRIES, delay=settings.RETRY_DELAY)
    async def fetch_content(self, url: str, max_redirects: int = 5, visited: set = None) -> str:
        """Получение контента с улучшенной обработкой редиректов"""
        if visited is None:
            visited = set()
        
        if url in visited:
            logger.warning(f"Cyclic redirect detected: {url}")
            return ""
        
        if len(visited) >= max_redirects:
            logger.warning(f"Max redirects reached: {url}")
            return ""
        
        try:
            async with httpx.AsyncClient(follow_redirects=False) as client:
                response = await client.get(
                    url,
                    timeout=settings.REQUEST_TIMEOUT,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                )
                
                if response.status_code in (301, 302, 303, 307, 308):
                    redirect_url = response.headers.get("Location")
                    if not redirect_url:
                        logger.warning(f"No Location header: {url}")
                        return ""
                    
                    if not redirect_url.startswith(("http://", "https://")):
                        from urllib.parse import urljoin
                        redirect_url = urljoin(url, redirect_url)
                    
                    logger.info(f"Redirect: {url} -> {redirect_url}")
                    return await self.fetch_content(redirect_url, max_redirects, visited | {url})
                
                response.raise_for_status()
                return response.text
                
        except httpx.HTTPStatusError as e:
            logger.warning(f"HTTP Error: {str(e)}")
            return await self._dynamic_fetch(url)
        except Exception as e:
            logger.error(f"Fetch failed: {str(e)}")
            return ""

    async def _dynamic_fetch(self, url: str) -> str:
        """Асинхронный запуск Selenium"""
        loop = asyncio.get_event_loop()
        try:
            return await loop.run_in_executor(None, self._sync_selenium_fetch, url)
        except Exception as e:
            logger.error(f"Selenium error: {str(e)}")
            return ""

    def _sync_selenium_fetch(self, url: str) -> str:
        """Синхронный код Selenium"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            return driver.page_source
        finally:
            driver.quit()

    @timing_decorator
    async def crawl_pages(self, base_url: str, domain: str) -> Set[str]:
        """Поиск всех страниц на сайте"""
        initial_content = await self.fetch_content(base_url)
        soup = BeautifulSoup(initial_content, "html.parser")
        urls = {base_url}

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/"):
                href = f"{base_url}{href}"
            if domain in href and href not in urls:
                urls.add(href)
        return urls

    async def save_content(self, pages: Set[str], output_path: Path) -> None:
        """Сохранение контента с проверкой валидности"""
        lines_count = 0
        with output_path.open("w", encoding="utf-8") as f:
            for page in pages:
                content = await self.fetch_content(page)
                if not content:
                    logger.warning(f"Skipping empty content for {page}")
                    continue
                
                try:
                    cleaned = clean_html_content(content)
                except Exception as e:
                    logger.error(f"Failed to clean HTML for {page}: {str(e)}")
                    continue
                
                if lines_count >= settings.MAX_CONTENT_LINES:
                    break
                
                f.write(f"=== {page} ===\n{cleaned}\n\n")
                lines_count += cleaned.count("\n") + 1

    @timing_decorator
    async def process_site(self, url: str) -> dict:
        """Основной метод обработки сайта"""
        domain = self.extract_domain(url)
        logger.info(f"Начато сканирование домена: {domain}")
    
        subdomains = await self.scan_subdomains(domain)
        logger.info(f"Найдено поддоменов: {len(subdomains)}")
    
        pages = await self.crawl_pages(f"https://{domain}", domain)
        logger.info(f"Найдено страниц: {len(pages)}")
    
        content_file = self.results_dir / f"{domain}.txt"
        await self.save_content(pages, content_file)
        logger.info(f"Контент сохранен в файл: {content_file}")
    
        return {
            "domain": domain,
            "subdomains": subdomains,
            "pages_found": len(pages),
            "content_file": str(content_file)
        }