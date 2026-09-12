import os
import hashlib

UGIT_DIR = ".ugit"

def init():
    os.mkdir(UGIT_DIR)
    os.makedirs(f'{UGIT_DIR}/objects')

def set_HEAD(oid):
    with open (f'{UGIT_DIR}/HEAD', 'w') as f:
        f.write (oid)

def get_HEAD():
    if os.path.isfile (f'{UGIT_DIR}/HEAD'):
        with open (f'{UGIT_DIR}/HEAD') as f:
            return f.read ().strip ()


def hash_object(data, type_= "blob"):
    obj = type_.encode() + b"\x00" + data
    oid = hashlib.sha1(obj).hexdigest() # oid - Object ID
    with open(f'{UGIT_DIR}/objects/{oid}', 'wb') as out:
        out.write(obj)
    return oid

def get_object(oid, expected="blob"):
    with open(f"{UGIT_DIR}/objects/{oid}", "rb") as f:
        obj = f.read()

    type_, _, content = obj.partition(b"\x00") # b"\x00" means a null byte represented by binary/bytes literal
    type_ = type_.decode()

    if expected is not None:
        assert type_ == expected, f"Expected {expected}, got {type_}"
    return content

