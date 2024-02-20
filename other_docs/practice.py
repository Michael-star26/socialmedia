import os
import shutil

# with open('Hello.txt','r')as f:
#     for line in f:
#         print(line)
#
# with open('Hello.txt','w') as h:
#     h.write('filedata')
#
# with open('Hello.txt','a') as wr:
#     wr.write("\n Writing a new line")
#
# with open("Hello.txt",'r') as fp:
#     while True:
#         cur_line=fp.readline()
#         if cur_line=="":
#             break
#         print(cur_line)

# changing file name
# old_name=r"alic_e.JPG"
# new_name="alice.jpg"
# if os.path.isfile(new_name):
#     print("File already exists. Cannot rename")
# else:
#     os.rename(old_name,new_name)
#
# # Changing extention only
# name=" Michael Onyango_Owino"
# print(name)
# name_without_space=name.replace(" ","")
# clean_name=name_without_space.replace("_","")
# print(name_without_space)
# print(clean_name)

with open('Hello.txt','w')as f:
     f.write("Hello")

with open('Hello.txt','r')as f:
     for line in f:
         text=line
         print(text)