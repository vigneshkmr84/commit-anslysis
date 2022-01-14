import json
import os
import subprocess

#out=subprocess.check_output(["git", "-C", "./commit-data/repos/kafka-streams-project", "log", "--all", "--stat" ,"--no-merges", "--reverse", "--pretty=format:{ \"commit_hash\": \"%H\" , \"short_hash\": \"%h\" , \"author\" : \"%an\"  , \"author_email\" : \"%ae\"  , \"author_date\" : \"%aD\" , \"committer_name\" : \"%cn\" , \"committer_email\" : \"%ce\" , \"committer_date\" : \"%cD\" , \"subject_sanitized\" : \"%f\" , \"subject_unsanitized\" : \"%s\"  },"])

#\"commit_hash\": \"%H\" , \"short_hash\": \"%h\" , \"author\" : \"%an\"  , \"author_email\" : \"%ae\"  , \"author_date\" : \"%aD\" , \"committer_name\" : \"%cn\" , \"committer_email\" : \"%ce\" , \"committer_date\" : \"%cD\" , \"subject_sanitized\" : \"%f\" , \"subject_unsanitized\" : \"%s\"  }
#print(out.decode("utf-8"))

#repoName=subprocess.check_output(["git", "-C", "./commit-data/repos/kafka-streams-project", "config",  "--get", "remote.origin.url"])
#repoName=repoName.decode('utf-8').split('/')[-1].split('.')[0]

#repoPath="/Users/vignesh/my-works/git-log-analysis/commit-data/repos/kafka-streams-project"
repoPath="/Users/vignesh/my-works/git-log-analysis/commit-data/repos/rails"
outputFolder="/Users/vignesh/my-works/git-log-analysis/commit-data/output"




def extract_git_metadata(repo, metaDataOutputFolder):
    print("Extracting git Metadata from repo : " + repo)
    outputFolderAbsPath=os.path.abspath(metaDataOutputFolder)
    
    
    # working -1 
    #out=subprocess.check_output(["git", "-C", repo, "log", "--all", "--stat", "--no-merges", "--reverse", "--pretty=format:{ \"commit_hash\": \"%H\" , \"short_hash\": \"%h\" , \"author\" : \"%an\"  , \"author_email\" : \"%ae\"  , \"author_date\" : \"%aD\" , \"committer_name\" : \"%cn\" , \"committer_email\" : \"%ce\" , \"committer_date\" : \"%cD\" , \"subject_sanitized\" : \"%f\" , \"subject_unsanitized\" : \"%s\"  }"])
    
    # without the file types last }, is removed for formatting
    # --shortstat added to get only the changes count that's been made in that commit 
    # removed unsanitized commit message - since it's breaking the json message with special characters
    #out=subprocess.check_output(["git", "-C", repo, "log", "--all", "--shortstat" ,"--no-merges", "--reverse", "--pretty=format:{ \"commit_hash\": \"%H\" , \"short_hash\": \"%h\" , \"author\" : \"%an\"  , \"author_email\" : \"%ae\"  , \"author_date\" : \"%aD\" , \"committer_name\" : \"%cn\" , \"committer_email\" : \"%ce\" , \"committer_date\" : \"%cD\" , \"subject_sanitized\" : \"%f\"  "])
    
    # removed author name and committer name - since it's also having special characters
    
    #for hash in get_all_rev_list(repo):
    # git log --all --shortstat --no-merges --reverse --pretty="format:%H|~|%h|~|%aN|~|%ae|~|%aD|~|%cN|~|%ce|~|%cD|~|%f"
    commitLog=subprocess.check_output(["git", "-C", repo, "log", "--all", "--shortstat", "--no-merges", "--reverse", "--pretty=format:%H|~|%h|~|%aN|~|%ae|~|%aD|~|%cN|~|%ce|~|%cD|~|%f"]).decode("utf-8")
    commitLog=commitLog.replace('"', "").replace("\\", "")
    with open(RAW_FILE, "w+") as outfile:
        outfile.write(commitLog)
    #format(repo)
    
 
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
    
    # returning a empty string if jsonString is empty 
    #print(jsonString)
    return "" if jsonString == "" else jsonString + ", "        
        
def format(rawFile, repoName = 'rails'):
    rawFile = open(rawFile, "r")
    jsonData=""

    for line in rawFile:
        data = ""
        if '|~|' in line:
            #data = line
            line=line.split("|~|")
            commit_hash=line[0]
            short_hash=line[1]
            author_name=line[2]
            author_email=line[3]
            author_date=line[4]
            committer_name=line[5]
            committer_email=line[6]
            committer_date=line[7]
            subject_sanitized=line[8].rstrip("\n")
            #print(subject_sanitized.rstrip("\n"))
            data="{ \"commit_hash\" : \"" +  commit_hash + "\", \"short_hash\" : \"" +  short_hash + "\", \"author_name\" : \"" +  author_name + "\" , \"author_email\" : \"" +  author_email + "\" , \"author_date\" : \"" +  author_date + "\" , \"committer_name\" : \"" +  committer_name + "\" , \"committer_email\" : \"" +  committer_email + "\", \"committer_date\" : \"" +  committer_date + "\", \"subject\" : \"" +  subject_sanitized + "\" }"
            
            nextLine = rawFile.readline() # for reading the next line (which is the --shortstat line )
            nextLine = nextLine.rstrip(nextLine[-1]).strip()
            #print(data)
            # original with changes tracking 
            data = data.rstrip(data[-1]) + ',' + track_changes(nextLine) + '"repo_name": "' + repoName + '" }'
            
            #print(data)
            
            jsonData += data + ", \n"

    with open("/Users/vignesh/my-works/git-log-analysis/commit-data/output/rails.json", "a+") as outfile:
        outfile.write(jsonData)

    
RAW_FILE="/Users/vignesh/my-works/git-log-analysis/commit-data/repos/rails.raw"
extract_git_metadata(repoPath, outputFolder)
format(RAW_FILE)

