from ui.display.preview_item import PreviewItem

from fitz import open as open_pdf, Document

class Downloader:
    #add signal for download progress
    def downloadFile(self, fileList:list[PreviewItem], save_location:str):
        #destroy when finish download
        # returns (successful, message)
        opened_files:dict[str, Document] = dict()
        
        for each in fileList:
            if each.full_path in opened_files:
                continue
            doc = self.open_file(each.full_path)
            if doc == None:
                return (False, "File not found", each.full_path)
            opened_files[each.full_path] = doc

        self.output = open_pdf()
        for each in fileList:
            file = opened_files[each.full_path]
            range = each.document_page_range
            self.output.insert_file(file, from_page=range[0] - 1, to_page=range[1] - 1)
        
        try:
            self.output.save(save_location[0] + ".pdf")
        except:
            return (False, "Unable to save at location", save_location)   
        finally:
            self.close_all_files(opened_files) 
            return (True, "Successful", save_location)
        
    def open_file(self, path):
        try:
            return open_pdf(path) 
        except:
            return None
    
    def close_all_files(self, doc_list:dict[str, Document]):
        self.output.close()
        for each in doc_list.values():
            each.close()