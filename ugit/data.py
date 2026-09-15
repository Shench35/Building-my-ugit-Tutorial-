import os
import hashlib

UGIT_DIR = ".ugit"

def init():
    os.mkdir(UGIT_DIR)
    os.makedirs(f'{UGIT_DIR}/objects')

def update_ref(ref, oid):
    ref_path = f"{UGIT_DIR}/{ref}"
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open (ref_path, 'w') as f:
        f.write (oid)

def get_ref(ref):
    ref_path = f"{UGIT_DIR}/{ref}"
    if os.path.isfile(ref_path):
        with open (ref_path) as f:
            return f.read ().strip ()

def iter_refs():
    refs = ["HEAD"]
    for root, _, filename in os.walk(f"{UGIT_DIR}/refs/"):
        root = os.path.relpath(root, UGIT_DIR)
        refs.extend(f"{root}/{name}" for name in filename)

    for refname in refs:
        yield refname, get_ref(refname)

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

