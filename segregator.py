from tkinter import *
import glob, os
import shutil
from tkinter import messagebox

root = Tk()
root.title('Ranas - Segregator')
root.geometry('300x150+500+200')
root.config(bg='#fafafa', padx=20, pady=20)
root.resizable(False, False)

def create_directory(parent_dir_path):
    dirNames = ['Audio', 'Pictures', 'Videos', 'Documents', 'Compressed', 'Programs']
  
    for item in dirNames:
        try: 
            os.mkdir(os.path.join(parent_dir_path, item)) 
        except OSError as error: 
            print(error)


def check_path(path):
    if os.path.exists(path):
        return True
    else:
        return False
        
def segregate():
    if appInput.get():
        if check_path(appInput.get()) == False:
            response = messagebox.showinfo("Information", "Please enter valid directory path")
            
        else:
            create_directory(appInput.get())

            for root, dirs, files in os.walk(appInput.get()):
                for file in files:
                    try:
                        if file.endswith(('.txt', '.doc', '.docx', '.html', '.htm', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods')):
                            shutil.move(appInput.get() + '\\' + file, appInput.get() + '/' + 'Documents' + '/' + file)
                
                        elif file.endswith(('.zip', '.7z', '.bz2', '.gz', '.rar', '.tar')):
                            shutil.move(appInput.get() + '/' + file, appInput.get() + '/' + 'Compressed' + '/' + file)
                
                        elif file.endswith(('.mp3', '.flac', '.aac', '.wav', '.wma')):
                            shutil.move(appInput.get() + '/' + file, appInput.get() + '/' + 'Audio' + '/' + file)
                
                        elif file.endswith(('.avi', '.mts', '.wmv', '.mkv', '.webm', '.flv', '.mp4', '.m4v')):
                            shutil.move(appInput.get() + '/' + file, appInput.get() + '/' + 'Videos' + '/' + file)
                
                        elif file.endswith(('.jpeg', '.png', '.rif', 'tiff', '.svg', '.jpg')):
                            shutil.move(appInput.get() + '/' + file, appInput.get() + '/' + 'Pictures' + '/' + file)
                
                        elif file.endswith(('.exe', '.apk')):
                            shutil.move(appInput.get() + '/' + file, appInput.get() + '/' + 'Programs' + '/' + file)
                    except OSError as error: 
                        print(error)

    else:
        response = messagebox.showinfo("Information", "Please input folder path")
    

appLabel = Label(root, text="Enter directory path", bg="#fafafa", font=("Poppins", 10))
appLabel.grid()

appInput = Entry(root, width=42)
appInput.grid(pady=10)
        
appButton = Button(root, text="Segregate", width=30, height=2, bg="teal", fg="white", padx=20, pady=2, command=segregate)
appButton.grid()

root.mainloop()




