from ui.display.preview_item import PreviewItem

from fitz import open as open_pdf, Document, Matrix

class Downloader:
    #no need to add signal for download progress, very fast
    def downloadFile(self, fileList:list[PreviewItem], save_location):
        # returns (successful, message)
        
        opened_files:dict[str, Document] = dict()
        
        for each in fileList:
            if each.full_path in opened_files:
                continue
            doc = self.open_file(each.full_path)
            if doc == None:
                return (False, "File not found at {}".format(each.full_path))
            opened_files[each.full_path] = doc

        self.output = open_pdf()
        for each in fileList:
            file = opened_files[each.full_path]
            range = each.document_page_range
            self.output.insert_file(file, from_page=range[0] - 1, to_page=range[1] - 1)
        
        try:
            if save_location[-3:] != "pdf":
                page = self.output.load_page(0)
                pix = page.get_pixmap(matrix=Matrix(2,2))
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
            return open_pdf(path) 
        except:
            return None
    
    def close_all_files(self, doc_list:dict[str, Document]):
        self.output.close()
        for each in doc_list.values():
            each.close()