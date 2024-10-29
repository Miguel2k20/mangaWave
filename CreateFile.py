import os

class CreateFile: 
        
    def pasteCreate(mangaObject):
        
        repositoryManga = mangaObject

        if not os.path.exists(repositoryManga):
            os.makedirs(repositoryManga)
            response = "Directory created"
        else:
            response = "Oops! This manga already exists"

        return response
        