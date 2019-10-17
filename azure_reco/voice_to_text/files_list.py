import os

i = 0
fl = []
dirname = "C:\\Users\\JBKD37\\PycharmProjects\\voice_to_text"
list = os.listdir(dirname)
for l in list:
    z = l.find(".wav")
    if z != -1:
        fl.append(l)
    else:
        pass

for f in fl:
    (shortname, extension) = os.path.splitext(f)
    print(shortname)
