from ui.display.preview_item import PreviewItem

from fitz import open as open_doc, Document, Matrix, Rect, Page
import fitz

class Downloader:
    #no need to add signal for download progress, very fast
    def downloadFile(self, fileList:list[PreviewItem], save_location:str, scaled:bool = False):
        # returns (successful, message)
        opened_files:dict[str, Document | None] = dict()
        
        for each in fileList:
            if each.full_path in opened_files:
                continue
            doc = self.open_file(each.full_path) if not (scaled and not each.extension == 'pdf') else None
            #No need to open image if scaled, will open later 
            if doc == None:
                return (False, "File not found at {}".format(each.full_path))
            opened_files[each.full_path] = doc

        self.output = open_doc()
        for i, each in enumerate(fileList):
            file = opened_files[each.full_path]
            range = each.document_page_range
            
            if scaled:
                new_page:Page = self.output.new_page(i, each.image.normWidth, each.image.normHeight)
                if each.extension == 'pdf':
                    new_page.show_pdf_page(
                        new_page.rect,
                        file, 
                        range[0]-1   
                    )
                else:
                    new_page.insert_image(
                        new_page.rect,
                        filename=each.full_path
                    )
            else:
                self.output.insert_file(file, from_page=range[0] - 1, to_page=range[1] - 1)
                
        try:
            if save_location.endswith("pdf"):
                page = self.output.load_page(0)
                mtx = Matrix(1, 1)
                if fileList[0].extension == 'pdf':
                    #pdf very blurry otherwise
                    mtx = Matrix(2, 2)
                pix = page.get_pixmap(matrix=mtx)
                pix.save(save_location)
            else:
                self.output.save(save_location)
            
        except Exception as e:
            print(e)
            return (False, "Unable to save at {}".format(save_location))   
        finally:
            self.close_all_files(opened_files) 
            return (True, "File saved at {}".format(save_location))
        
    def open_file(self, path):
        try:
            return open_doc(path) 
        except:
            return None
    
    def close_all_files(self, doc_list:dict[str, Document]):
        self.output.close()
        for each in doc_list.values():
            each.close()