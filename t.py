import os
import subprocess

# line=" 2 files changed, 8 insertions(+), 1 deletion(-)"
# print(line)
# lines=line.strip().split(',')

# print(len(lines))

# dictionary = {}
# for object in lines:
#     print(object.strip())
#     object = object.strip()
#     if "changed" in object: 
#         dictionary["lines_changed"]= object.strip().split(' ')[0]
#     if "insertion" in object: 
#         dictionary["inserted_lines"]= object.strip().split(' ')[0]
#     if "deletion" in object: 
#         dictionary["deleted_lines"]= object.strip().split(' ')[0]

# jsonObject = json.dumps(dictionary)  
# print(str(jsonObject).replace("}", "").replace('{', ''))

# #print(lines[0].strip().split(' ')[0])
# #print(lines[1].strip().split(' ')[0])
# #print(lines[2].strip().split(' ')[0])


# #"changed"
# #"insertion"
# #"deletion"

folder="./commit-data/output"
absPath = os.path.abspath(folder);
print(absPath)


out=subprocess.check_output(["git", "-C", "./commit-data/repos/kafka-streams-project", "log"])
#print(out.decode('utf-8'))


print(os.getcwd())
print(os.path.abspath(os.getcwd()))

def get_raw_metadata_files():
    ''' for file in os.listdir("/mydir"):
        if file.endswith(".txt"):
            print(os.path.join("/mydir", file)) '''
    return [ os.path.abspath(os.path.join(META_DATA_OUTPUT_FOLDER, name)) 
            for name in os.listdir(META_DATA_OUTPUT_FOLDER)
                if os.path.isfile(os.path.join(META_DATA_OUTPUT_FOLDER, name)) and name.endswith(".raw")]
    
CURRENT_DIR=os.path.abspath(os.getcwd())
ROOT_FOLDER=CURRENT_DIR + "/commit-data"
REPO_CONFIG_FILE="./config/repo.config"
REPOS_FOLDER=ROOT_FOLDER + "/repos"
META_DATA_OUTPUT_FOLDER=ROOT_FOLDER + "/output"
CONSOLIDATED_JSON_OUTPUT_FILE=META_DATA_OUTPUT_FOLDER + "/" + "consolidated-output.json"

print("===========")
for f in get_raw_metadata_files():
    print(f)