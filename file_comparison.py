import os
import concurrent.futures

path1=r"//n1/mnt/share1/test"
path2=r"//n2/mnt/share1/test"
files_paths=[path1,path2]

"""
First function to get file objects and some metadata converting to a key value pair where
 the key is the file name and value is a list of meta values
"""


def get_sorted_files(paths):
    try:

        files = os.listdir(paths)
        files_s = sorted(files)
        files_array = []
        # using conditional to handle event where no file objects are found in directory
        if len(files_s) > 0:
            for file in files_s:
                file_dict = {}
                """
                 adding key of file name and value of list of file size,last accessed time,metadatachange time,userid 
                of owner,group id of owner and file mode
                """
                file_dict[file] = [os.stat(paths + "/" + file).st_size, os.stat(paths + "/" + file).st_atime,
                                   os.stat(paths + "/" + file).st_ctime, os.stat(paths + "/" + file).st_uid,
                                   os.stat(paths + "/" + file).st_gid, os.stat(paths + "/" + file).st_mtime,
                                   os.stat(paths + "/" + file).st_mode]
                # adding keyvalue pairs to empty list
                files_array.append(file_dict)
            return files_array
        else:
            return files_s
    except:
        return "cannot find path"


def comparison_of_list(file_paths):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        #using executor to call get_sorted_files function while iterating through arguments and executing in parallel
        results = executor.map(get_sorted_files, [file_path for file_path in file_paths])
    results_list=[]
    for result in results:
        if result !="cannot find path" :
            results_list.append(result)
        else:
            return "invalid path"
    # comparing the 2 lists to see if they are equal
    if (results_list[0]) == results_list[1]:
        return "success"
    else:
        return "error"


print(comparison_of_list(files_paths))

