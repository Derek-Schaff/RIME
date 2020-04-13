import hashlib

def generate_chk_sum(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as h_file:
        buf = h_file.read()
        hasher.update(buf)

        return hasher.hexdigest()

