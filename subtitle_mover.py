import os
import re 

def regex_searcher(dirs_found):
    # original expression used: re.search(r"\([0-9]+\)") 
    for root, dirs, files in os.walk(".", topdown = True): # Traverse the current working directory 
        for curr_dir in dirs: # Look at all directories in current directory  
            if re.search(r"\(\d{4}\)", curr_dir): # Search for (xxxx) format in the directory's name (x = number)
                dirs_found.append(curr_dir) # Create a list of all matching directory names

      
def sub_mover(dirs_found):
    cwd = "D:\\Downloads\\"

    for sub_folder in range(len(dirs_found)):
        dest_path = cwd + dirs_found[sub_folder] 
        source_path = cwd + dirs_found[sub_folder] + "\\Subs\\"
        
        if os.path.exists(source_path): # Only execute if the Subs folder exists 
            os.chdir(source_path)
            
            for filename in os.listdir():
                if filename.lower().endswith(".srt"):
                    print(f"Subtitle file found: {filename}")
                    os.rename(source_path + filename, "..\\" + filename) # Move file to parent directory
                    # os.rename() does not natively support moving files from one disk to another. To 
                    # do so easily, shutil can be imported, and shutil.move() can be used instead, 
                    # which invokes os.rename(), but handles the copying and deleting of the original
                    # file for you 
                    os.chdir("..") # Must leave folder before deleting or else an in-use error will occur 
                    os.rmdir(source_path) # Delete the now empty Subs folder 
                    # To avoid deleting something that may be required, the Send2Trash module can
                    # be used instead. The os.rmdir() will delete the folder permanently; whereas 
                    # the Send2Trash module will move it to the systems recycle bin or trash can.
                    # Send2Trash must be installed. The link and instructions for it can be found here:
                        # https://github.com/arsenetar/send2trash 
                elif filename.lower().endswith(".idx") or filename.lower().endswith(".sub"):
                    print("IDX and SUB files found")
                    idx_and_sub = os.listdir(source_path) # Create list of all files in directory 
                    
                    for file in idx_and_sub: # Iterate over list and move files individually 
                        os.rename(source_path + filename, "..\\" + filename)
                        idx_and_sub.remove(file) # Remove moved files from list 
                    
                    if len(idx_and_sub) == 0: # If Subs folder is empty 
                        os.chdir("..")
                        os.rmdir(source_path)
                else:
                    print("Unable to locate subtitle file(s)")
        else:
            print(f"Subs folder does not exist for:\n\t {dirs_found[sub_folder]}")
    

if __name__ == '__main__':
    dirs_found = []

    regex_searcher(dirs_found)
    
    if len(dirs_found) == 0:
        exit()
    else: 
        sub_mover(dirs_found)
        print("\nAll subtitle files successfully moved.") 
