import os, hashlib

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            if not os.path.isfile(filepath):
                continue
            file_paths.append({'file_path':filepath,'size_in_bytes':os.stat(filepath).st_size})  # Add it to the list.

    return file_paths


def map_filepaths_by_size(files):
    mapped={}
    for file in files:
        if file['size_in_bytes'] in mapped.keys():
            mapped[file['size_in_bytes']].append(file)
        else:
            mapped[file['size_in_bytes']]=[file]
    return mapped


def filemd5(filename):
    try:
        with open(filename, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except:
        return "-1"

def hash_for_same_size(mapped):
    output_path=os.path.join(os.getcwd(),"duplicate_files_info.txt")
    if os.path.exists(output_path):
        os.remove(output_path)
    with open(output_path,"a") as my_output:
        for _, same_size_files in mapped.items():
            if len(same_size_files)==1:
                continue
            hash_mapped = {}
            for file in same_size_files:
                file_hash = filemd5(file['file_path'])
                if file_hash in hash_mapped.keys():
                    hash_mapped[file_hash].append(file)
                else:
                    hash_mapped[file_hash]=[file]

            output_line=""
            for key,value in hash_mapped.items():
                if len(value)<=1:
                    continue
                output_line+=f"hash:{key} size:{value[0]['size_in_bytes']}\n"
                for f in value:
                    output_line+=f['file_path']+"\n"
                output_line+="\n\n"
            my_output.write(output_line)


if __name__ == '__main__':
    files=get_filepaths(os.getcwd())
    mapped=map_filepaths_by_size(files)
    hash_for_same_size(mapped)