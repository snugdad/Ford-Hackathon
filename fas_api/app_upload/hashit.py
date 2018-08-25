import os
import hashlib

def md5OfFile(filepath):
    md = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10) # Magic number: one-megabyte blocks.
            if not block: break
            md.update(block)
        return md.hexdigest()

def hash_dir(dir_path):
    hashes = []
    for path, dirs, files in os.walk(dir_path):
        for file in sorted(files): # we sort to guarantee that files will always go in the same order
            hashes.append(md5OfFile(os.path.join(path, file)))
        for dir in sorted(dirs): # we sort to guarantee that dirs will always go in the same order
            hashes.append(hash_dir(os.path.join(path, dir)))
        break # we only need one iteration - to get files and dirs in current directory
    return str(hash(''.join(hashes)))
