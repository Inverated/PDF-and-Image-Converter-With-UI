from pathlib import Path
from ui.display.preview_content.preview_item import PreviewItem
from fitz import open as open_new_document, Document, Matrix, Page
from PySide6.QtCore import QObject, Signal


class Downloader(QObject):
    progress = Signal(int, int)
    finished = Signal()

    def __init__(self, quality: int = 0, chosen_image_format: str = "png"):
        super().__init__()
        self.quality = quality
        self.chosen_image_format = chosen_image_format
        self.output = open_new_document()

    def update(self, quality: int, chosen_image_format: str):
        if quality is not None:
            self.quality = quality
        if chosen_image_format is not None:
            self.chosen_image_format = chosen_image_format
        
    # no need to add signal for download progress, very fast
    def downloadFile(self, fileList: list[PreviewItem], save_location: str, scaled: bool = False):
        # returns (successful, message)
        opened_files: dict[str, Document] = dict()

        for each in fileList:
            if each.full_path in opened_files:
                continue
            doc = self.open_file(each.full_path)

            if doc is None:
                return (False, f"File not found at {each.full_path}")
            opened_files[each.full_path] = doc

        self.output = open_new_document()
        page_no = 0
        for each in fileList:
            file = opened_files[each.full_path]
            docRange = each.document_page_range

            if scaled:
                if each.extension == '.pdf':
                    for i in range(docRange[0] - 1, docRange[1]):
                        new_page: Page = self.output.new_page(
                            page_no, each.image.normWidth, each.image.normHeight)
                        new_page.show_pdf_page(
                            new_page.rect,
                            file,
                            i
                        )
                        page_no += 1
                else:
                    new_page: Page = self.output.new_page(
                        page_no, each.image.normWidth, each.image.normHeight)
                    new_page.insert_image(
                        new_page.rect,
                        filename=each.full_path
                    )
                    page_no += 1
            else:
                self.output.insert_file(
                    file, from_page=docRange[0] - 1, to_page=docRange[1] - 1)

        try:
            if not save_location.endswith("pdf"):
                count = self.output.page_count
                for i in range(count):
                    page = self.output.load_page(i)
                    mtx = Matrix(1, 1)
                    if fileList[i].extension == '.pdf':
                        # pdf very blurry otherwise
                        zoom = 4 - self.quality
                        mtx = Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=mtx)

                    path = Path(save_location)
                    if path.exists() and path.is_dir():
                        pix.save(save_location +
                                 f"/page_{i+1}.{self.chosen_image_format}")
                    else:
                        pix.save(save_location)
                        
                    self.progress.emit(i + 1, count)
            else:
                self.output.save(save_location)
                self.finished.emit()
            return (True, f"File saved at {save_location}")

        except Exception as e:
            return (False, f"Unable to save at {save_location}: {e}")
        finally:
            self.close_all_files(opened_files)
            self.finished.emit()

    def open_file(self, path):
        try:
            return open_new_document(path)
        except Exception as _:
            return None

    def close_all_files(self, doc_list: dict[str, Document]):
        self.output.close()
        for each in doc_list.values():
            each.close()
