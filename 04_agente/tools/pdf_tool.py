import os
import shutil
import subprocess
from pathlib import Path


class HTMLToPDFExporter:
    """
    Herramienta / Skill 2:
    Conversor de reportes HTML analíticos a documentos PDF ejecutivos
    utilizando el motor Chromium Headless del sistema (Microsoft Edge / Google Chrome).
    Garantiza el renderizado exacto de scripts interactivos (Chart.js),
    estilos CSS (Tailwind) y paginación ejecutiva sin requerir servidores externos.
    """

    CANDIDATE_PATHS = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge SxS\Application\msedge.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]

    def __init__(self, browser_path=None):
        self.browser_path = browser_path or self._locate_browser()

    def _locate_browser(self):
        """Localiza un ejecutable de navegador Chromium disponible en el sistema."""
        for path in self.CANDIDATE_PATHS:
            if os.path.isfile(path):
                return path

        # Si no está en las rutas fijas, buscar en el PATH del sistema
        edge_which = shutil.which("msedge")
        if edge_which:
            return edge_which

        chrome_which = shutil.which("chrome")
        if chrome_which:
            return chrome_which

        raise FileNotFoundError(
            "No se encontró Microsoft Edge ni Google Chrome para la exportación a PDF."
        )

    def convert(self, html_path, output_pdf_path=None):
        """
        Convierte el archivo HTML a PDF y lo guarda en el disco.
        """
        html_file = Path(html_path).resolve()
        if not html_file.exists():
            raise FileNotFoundError(f"Archivo HTML de entrada no encontrado: {html_file}")

        if output_pdf_path is None:
            output_pdf = html_file.with_suffix(".pdf")
        else:
            output_pdf = Path(output_pdf_path).resolve()

        output_pdf.parent.mkdir(parents=True, exist_ok=True)

        # Formato de URL de archivo local
        file_url = html_file.as_uri()

        # Flags para impresión headless de alta calidad
        cmd = [
            self.browser_path,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={str(output_pdf)}",
            file_url
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if not output_pdf.exists() or output_pdf.stat().st_size == 0:
                raise RuntimeError(
                    f"Fallo en la generación del PDF. Código de salida: {result.returncode}. "
                    f"Stderr: {result.stderr}"
                )

            size_mb = output_pdf.stat().st_size / (1024 * 1024)
            return {
                "success": True,
                "pdf_path": str(output_pdf),
                "size_mb": round(size_mb, 2),
                "browser_used": self.browser_path
            }

        except subprocess.TimeoutExpired:
            raise TimeoutError("Tiempo de espera agotado al renderizar el documento PDF.")
        except Exception as e:
            raise RuntimeError(f"Error durante la impresión a PDF: {e}")


if __name__ == "__main__":
    exporter = HTMLToPDFExporter()
    print("Navegador localizado:", exporter.browser_path)

