import os
import json
import string

def list_all_files(path):
    d = {'name': os.path.basename(path)}    
    if os.path.isdir(path):
    	d['id'] = path
    	d['type'] = "dir"
    	d['children'] = [list_all_files(os.path.join(path,x)) for x in os.listdir(path)]
    else:    	
    	d['id'] = string.replace(path, "\\", "/")
    	d['type'] = "file"
    return d

# print(list_all_files("E:/MY-PROJECTS/pythonRest-ANPR/static/tests/"))