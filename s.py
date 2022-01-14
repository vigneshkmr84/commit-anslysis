import os

file=open('sample.log', 'r')


file_types = set()
for commit in file:
    if "commit_hash" not in commit and "changed" not in commit:
        # files lines
        filename, file_extension = os.path.splitext(commit)
        file_extension=file_extension.split("|")[0].strip()
        print(file_extension)
        # check for empty extension
        if  file_extension != '':
            file_types.add(file_extension)
    
print("file types ---- ")    
#file_types= file_types.remove('')
print(file_types)