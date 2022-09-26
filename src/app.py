import hashlib
import os
import sys


BKP_PATH = "Z:\\Setembro\\"
BUF_SIZE = 8388608
def write_digest(digest, alg, img_name, path = BKP_PATH):
        h = open(path + img_name + "." + alg, 'w', encoding = "utf-8")
        h.write(digest + " *" + img_name)
        h.close()  

def list_path(path):
    file_list = os.listdir(path)
    if 'backup_running' in file_list: # checks if backup folder is locked, quits if True
        raise Exception("A backup is running right now. Can't proceed with the verification")
    else:
        file_list.sort()
        return file_list
    
def create_hasher(alg):
    alg = alg.lower()
    if alg == "sha1":
        hasher = hashlib.sha1()
    elif alg == "sha256":
        hasher = hashlib.sha256()
    elif alg == "md5":
        hasher = hashlib.md5()
    return hasher


def hash_all(alg, path = BKP_PATH):
    file_list = list_path(path)

    unhashed_imgs = []
    for i in file_list:
        if i.endswith(".mrimg"):
            if i + "." + alg not in file_list:
                unhashed_imgs.append(i)

    print("You have " + str(len(unhashed_imgs)) + " unverified backups")
    for i in unhashed_imgs:
            print("          " + i)
    if len(unhashed_imgs) > 1:
        print("Starting verification now...")

    for i in unhashed_imgs:
        digest = hash_img(alg, i, path)
        write_digest(digest, alg, i)

def hash_img(alg, img, path = BKP_PATH):
    file_list = list_path(path)
    print("Hashing "+ path + img, ". Please wait...")
    with open(path + img, 'rb') as f:     
        hasher = create_hasher(alg)
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hasher.update(data)
        print("Hash generation succeeded.")
        return hasher.hexdigest()

def hash_last(alg, path = BKP_PATH):
    file_list = list_path(path)

    for i in reversed(range(len(file_list))):
        if file_list[i].endswith('.mrimg'):
            last_file = file_list[i]
            break
        if file_list[i].endswith('.mrimg.' + alg) :
            raise Exception("Last backup is already hashed using " + alg) 
        elif '.mrimg.sha' in file_list[i]:
            if alg.lower() == "sha1":
                a = "sha256"
            else:
                a = "sha1"
            print("File hashed with " + a + ". Hashing again using " + alg)
            continue
        else:
            print("File hashed with md5. Hashing again using " + alg)
            continue
    digest = hash_img(alg, last_file, path)
    write_digest(digest, alg, last_file)

       
hash_all("sha1")
#hash_last("sha1")
'''
Just checked and there's more than one unverified backup.
I should:
1. organize this code into functions and;
2. Make it create a list of all unverified backups at launch
Something like this should do:
    for i in file_list:
        if i + ".sha1" not in file_list:
            (...) 
'''