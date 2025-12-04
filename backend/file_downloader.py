from ui.display.preview_content.preview_item import PreviewItem

from fitz import open as open_new_document, Document, Matrix, Page

class Downloader:
    quality: int = 0
    output = open_new_document()
    
    def __init__(self, quality: int = 0):
        self.quality = quality
        
    #no need to add signal for download progress, very fast
    def downloadFile(self, fileList:list[PreviewItem], save_location:str, scaled:bool = False):
        # returns (successful, message)
        opened_files:dict[str, Document] = dict()
        
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
                    for i in range(docRange[0]-1, docRange[1]):
                        new_page:Page = self.output.new_page(page_no, each.image.normWidth, each.image.normHeight)
                        new_page.show_pdf_page(
                            new_page.rect,
                            file, 
                            i  
                        )
                        page_no += 1
                else:
                    new_page:Page = self.output.new_page(page_no, each.image.normWidth, each.image.normHeight)
                    new_page.insert_image(
                        new_page.rect,
                        filename=each.full_path
                    )
                    page_no += 1
            else:
                self.output.insert_file(file, from_page=docRange[0] - 1, to_page=docRange[1] - 1)
                
        try:
            if not save_location.endswith("pdf"):
                page = self.output.load_page(0)
                mtx = Matrix(1, 1)
                if fileList[0].extension == '.pdf':
                    #pdf very blurry otherwise
                    zoom = 4 - self.quality
                    mtx = Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mtx)
                pix.save(save_location)
            else:
                self.output.save(save_location)
            return (True, "File saved at {}".format(save_location))      
              
        except Exception as _:
            return (False, "Unable to save at {}".format(save_location))   
        finally:
            self.close_all_files(opened_files) 

    def open_file(self, path):
        try:
            return open_new_document(path) 
        except Exception as _:
            return None

    def close_all_files(self, doc_list:dict[str, Document]):
        self.output.close()
        for each in doc_list.values():
            each.close()