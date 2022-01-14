import json

#file=open('gitlog.raw', 'r')
file=open('commit-data/output/kafka-streams-project-gitlog.raw', 'r')


def track_changes(commit_stats):
    lines=commit_stats.strip().split(',')
    dictionary = {}
    #print("Starting with : " + lines)
    for object in lines:
        #print(object.strip())
        object = object.strip()
        if "changed" in object: 
            dictionary["files_changed"]= object.strip().split(' ')[0]
        if "insertion" in object: 
            dictionary["lines_inserted"]= object.strip().split(' ')[0]
        if "deletion" in object: 
            dictionary["lines_deleted"]= object.strip().split(' ')[0]
    jsonObject = json.dumps(dictionary) 
    jsonString = str(jsonObject).replace('}', '').replace('{', '')
    return jsonString
    
    
#repoName=subprocess.check_output(["basename" ,  "-s",  ".git", "`git config --get remote.origin.url`"])
#repoName=subprocess.check_output(["git",  "config",  "--get", "remote.origin.url"])
#repoName=repoName.decode('utf-8').split('/')[-1].split('.')[0]
repoName="kafka-streams-project"
#repoName=repoName.split('/')[-1].split('.')[0]
#print("Git repo : "  + repoName)


#mainJson = { "commits" : []}

jsonData=""

for line in file:
    data = ""
    if 'commit_hash' in line:
        data = line
    
        nextLine = file.readline()
        nextLine = nextLine.rstrip(nextLine[-1]).strip()
        # original with changes tracking 
        #data = data.rstrip(data[-1]) + ',' + track_changes(nextLine) + ', "repo_name": "' + repoName + '"' + '}'
        
        data = data.rstrip(data[-1]) + ', "repo_name": "' + repoName + '"' + '}'
        #print(type(data))
        #mainJson["commits"].append(json.loads(data))
        jsonData += data + ", \n"
        #print (data)

file.close()

#mainJson=json.dumps(mainJson)



#print(mainJson)
print("writing json data to file - commits.json")
jsonFile=open('commits.json', 'w')
jsonFile.write(jsonData)

jsonFile.close()
