from pathlib import Path

import pymupdf
import pytesseract

from PIL import Image


class Extractor:

    def extract(
        self,
        file_path: str,
    ) -> list[dict]:

        extension = Path(
            file_path
        ).suffix.lower()

        if extension == ".pdf":
            return self.extract_pdf(
                file_path
            )

        if extension in [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        ]:
            return self.extract_image(
                file_path
            )

        raise Exception(
            f"Unsupported file {extension}"
        )

    def extract_pdf(
        self,
        file_path: str,
    ) -> list[dict]:

        document = pymupdf.open(
            file_path
        )

        results = []

        for page_number, page in enumerate(
            document,
            start=1,
        ):

            text = page.get_text()

            if not text.strip():

                pixmap = page.get_pixmap()

                image = Image.frombytes(
                    "RGB",
                    (
                        pixmap.width,
                        pixmap.height,
                    ),
                    pixmap.samples,
                )

                text = pytesseract.image_to_string(
                    image,
                    lang="eng",
                )

            results.append(
                {
                    "page_number": page_number,
                    "text": text.strip(),
                }
            )

        document.close()

        return results

    def extract_image(
        self,
        file_path: str,
    ) -> list[dict]:

        image = Image.open(
            file_path
        )

        text = pytesseract.image_to_string(
            image,
            lang="eng",
        )

        return [
            {
                "page_number": 1,
                "text": text.strip(),
            }
        ]

