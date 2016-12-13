import sys, os, shutil, hashlib

nombre = os.environ.get( "USERNAME" )
print (nombre)

#file on nas ex. "smb://a-nas/a-dir/a-file.txt"
original_las = sys.argv[1]
#local dir ex. "/home/user/temp"
local_wkdir = sys.argv[2]

#create wkspace on nas
nas_dir_un = sys.argv[3] + "/" + str(nombre)
nas_dir_un_las = nas_dir_un + str(nombre) + "/" + sys.argv[4] # name of a file

#local las file
orig_local_las = sys.argv[5] # ex "C:/Local/ORIG/a-file.txt"
mover_local_las = sys.argv[6] #ex "C:/Local/MOVER/a-file.txt"
mover_local = sys.argv[7] #ex "C:/Local/Mover/a-file.txt"

if not os.path.exists(local_wkdir):
    os.makedirs(local_wkdir)

if not os.path.exists(nas_dir_un):
    os.makedirs(nas_dir_un)

if not os.path.exists(mover_local):
    os.makedirs(mover_local)


#copies from nas to local dir
shutil.copy(original_las, orig_local_las)

#copies from local dir to mover dir
shutil.copy(orig_local_las, mover_local_las)

#copies from mover dir to workspace on isilon
shutil.copy(mover_local_las, nas_dir_un)

print(nombre, original_las)
print(orig_local_las, mover_local_las)
print(nas_dir_un, nas_dir_un_las)



orig_hash = hashlib.md5(open(orig_local_las,'rb').read()).hexdigest()
new_hash = hashlib.md5(open(nas_dir_un_las,'rb').read()).hexdigest()

x = 0

while orig_hash == new_hash:
    print("they are the same")
    shutil.copy(nas_dir_un_las, mover_local_las)
    shutil.copy(mover_local_las,nas_dir_un_las)
    new_hash = hashlib.md5(open(nas_dir_un_las, 'rb').read()).hexdigest()
    x = x + 1
    print(orig_hash, new_hash, x)


else:
    print(x, "they are different")


print("all done")