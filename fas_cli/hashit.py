import os
import hmac

def hmac_for_file(filename, block_size=2**20):
    hmc = hmac.new(bytes('the shared secret key here', 'utf-8'))
    with open(filename, "rb") as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            hmc.update(data)
    return hmc.hexdigest()

def hmacOfFile(filepath):
    md = hashlib.hmac()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10) # Magic number: one-megabyte blocks.
            if not block: break
            md.update(block)
        return md.hexdigest()

import hashlib

def hash_file(filename, block_size=65536):
   sha256 = hashlib.sha256()
   with open(filename, 'rb') as f:
       for block in iter(lambda: f.read(block_size), b''):
           sha256.update(block)
   return sha256.hexdigest()

def hash_dir(dir_path):
    hashes = []
    for path, dirs, files in os.walk(dir_path):
        for file in sorted(files): # we sort to guarantee that files will always go in the same order
            hashes.append(hmac_for_file(os.path.join(path, file)))
        for dir in sorted(dirs): # we sort to guarantee that dirs will always go in the same order
            hashes.append(hash_dir(os.path.join(path, dir)))
        break # we only need one iteration - to get files and dirs in current directory
    return str(hash(''.join(hashes)))

