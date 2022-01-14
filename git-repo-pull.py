import subprocess
import os
import shutil
import subprocess
import time
from pathlib import Path
import json
import pandas
import configparser


def folder_cleanup(repos_folder):
    print("Cleaning up old repos folder - if exists")
    try:
        shutil.rmtree(repos_folder)
    except Exception as e:
        print("Error: %s : %s" % (repos_folder, e.strerror))

    print("Creating output directory (if it doesn't exist) : " + repos_folder)
    Path(repos_folder).mkdir(parents=True, exist_ok=True)


def clone_git_repos(repo_config_file, repos_folder):
    
    os.chdir(repos_folder)
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(repo_config_file)
    repoList = config['repository']['list'].split()
    for repo in repoList:
        print("Repo Remote-URL: " + repo)
        subprocess.check_output(["git", "clone", "--no-checkout", repo])
        print("\n")
    os.chdir(CURRENT_DIR)


def extract_git_metadata(repo, metadata_output_folder):
    print("Extracting git Metadata from repo : " + repo)
    output_folder_abs_path = os.path.abspath(metadata_output_folder)

    # @@ os.chdir(repo)

    # working -1 
    # out=subprocess.check_output(["git", "-C", repo, "log", "--all", "--stat", "--no-merges", "--reverse", "--pretty=format:{ \"commit_hash\": \"%H\" , \"short_hash\": \"%h\" , \"author\" : \"%an\"  , \"author_email\" : \"%ae\"  , \"author_date\" : \"%aD\" , \"committer_name\" : \"%cn\" , \"committer_email\" : \"%ce\" , \"committer_date\" : \"%cD\" , \"subject_sanitized\" : \"%f\" , \"subject_unsanitized\" : \"%s\"  }"])

    # without the file types last }, is removed for formatting
    # --shortstat added to get only the changes count that's been made in that commit 
    # removed unsanitized commit message - since it's breaking the json message with special characters
    # out=subprocess.check_output(["git", "-C", repo, "log", "--all", "--shortstat" ,"--no-merges", "--reverse", "--pretty=format:{ \"commit_hash\": \"%H\" , \"short_hash\": \"%h\" , \"author\" : \"%an\"  , \"author_email\" : \"%ae\"  , \"author_date\" : \"%aD\" , \"committer_name\" : \"%cn\" , \"committer_email\" : \"%ce\" , \"committer_date\" : \"%cD\" , \"subject_sanitized\" : \"%f\"  "])

    # removed author name and committer name - since it's also having special characters
    repo_name = get_repo_name(repo)

    raw_file_path = os.path.join(output_folder_abs_path, repo_name + "-gitlog.raw")
    print("Raw File : " + raw_file_path)

    # git command : git log --all --shortstat --no-merges --reverse --pretty="format:%H|~|%h|~|%aN|~|%ae|~|%aD|~|%cN|~|%ce|~|%cD|~|%f" –date=iso-strict
    commit_log = subprocess.check_output(["git", "-C", repo, "log", "--all", "--shortstat", "--no-merges", "--reverse",
                                         "--pretty=format:%H|~|%h|~|%aN|~|%ae|~|%ad|~|%cN|~|%ce|~|%cd|~|%f", "--date=format:%Y-%m-%d %H:%M:%S"]).decode("utf-8")                                         
    # git log --date=short --all --shortstat --no-merges --reverse --pretty="format:%H|~|%h|~|%aN|~|%ae|~|%aI|~|%cN|~|%ce|~|%cI|~|%f" –date=iso-strict
    # replacing escape characters (mainly in committer name, author name)   
    commit_log = commit_log.replace('"', "").replace("\\", "")
    with open(raw_file_path, "w+") as outfile:
        outfile.write(commit_log)

    print("Completed Extracting Metadata")

    generate_json_data(raw_file_path, repo_name)


def get_repository_folder_list(repos_folder):
    print("Extracting Repositories List from : " + repos_folder)
    return [os.path.abspath(os.path.join(repos_folder, name)) for name in os.listdir(repos_folder)
            if os.path.isdir(os.path.join(repos_folder, name))]


def is_git_directory(path):
    return subprocess.call(['git', '-C', path, 'status'], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w')) == 0


def get_repo_name(repo):
    repo_name = subprocess.check_output(["git", "-C", repo, "config", "--get", "remote.origin.url"])
    return repo_name.decode('utf-8').split('/')[-1].split('.')[0]


def track_changes(commit_stats):
    lines = commit_stats.strip().split(',')
    #dictionary = {}
    dictionary = { "files_changed" : 0, "lines_inserted" : 0, "lines_deleted" : 0}
    
    for single_line in lines:

        single_line = single_line.strip()
        if "changed" in single_line:
            dictionary["files_changed"] = int(single_line.strip().split(' ')[0])
        if "insertion" in single_line:
            dictionary["lines_inserted"] = int(single_line.strip().split(' ')[0])
        if "deletion" in single_line:
            dictionary["lines_deleted"] = int(single_line.strip().split(' ')[0])
    json_object = json.dumps(dictionary)
    json_string = str(json_object).replace('}', '').replace('{', '')

    # returning a empty string if jsonString is empty 
    return "" if json_string == "" else json_string + ", "


def generate_json_data(raw_file, repo_name):
    raw_file = open(raw_file, "r")
    json_data = ""

    for line in raw_file:
        data = ""
        if '|~|' in line:
            # data = line
            line = line.split("|~|")
            commit_hash = line[0]
            short_hash = line[1]
            author_name = line[2]
            author_email = line[3]
            author_date = line[4]
            committer_name = line[5]
            committer_email = line[6]
            committer_date = line[7]
            subject_sanitized = line[8].rstrip("\n")

            data = "{ \"commit_hash\" : \"" + commit_hash + "\", \"short_hash\" : \"" + short_hash + "\", \"author_name\" : \"" + author_name + "\" , \"author_email\" : \"" + author_email + "\" , \"author_date\" : \"" + author_date + "\" , \"committer_name\" : \"" + committer_name + "\" , \"committer_email\" : \"" + committer_email + "\", \"committer_date\" : \"" + committer_date + "\", \"subject\" : \"" + subject_sanitized + "\" }"
            
            # ISODate format 
            #data = "{ \"commit_hash\" : \"" + commit_hash + "\", \"short_hash\" : \"" + short_hash + "\", \"author_name\" : \"" + author_name + "\" , \"author_email\" : \"" + author_email + "\" , \"author_date\" : ISODate(\"" + author_date + "\") , \"committer_name\" : \"" + committer_name + "\" , \"committer_email\" : \"" + committer_email + "\", \"committer_date\" : \"" + committer_date + "\", \"subject\" : \"" + subject_sanitized + "\" }"
            
            # for reading the next line (which is the --shortstat line )
            next_line = raw_file.readline()
            next_line = next_line.rstrip(next_line[-1]).strip()

            data = data.rstrip(data[-1]) + ',' + track_changes(next_line) + '"repo_name": "' + repo_name + '" }'

            json_data += data + ", \n"

    with open(CONSOLIDATED_JSON_OUTPUT_FILE, "a+") as outfile:
        outfile.write(json_data)


''' def write_json_data(jsonData, jsonFile):
    print("Writing JSON data to file : " + jsonFile)
    #jsonFile=open(jsonFile, "w+")  
    with open(jsonFile, "a+") as outFile:
        outFile.write(jsonData) '''

''' def get_json_metadata_files():
    #print(META_DATA_OUTPUT_FOLDER)
    return [ os.path.abspath(os.path.join(META_DATA_OUTPUT_FOLDER, name)) for name in os.listdir(META_DATA_OUTPUT_FOLDER)
                if os.path.isfile(os.path.join(META_DATA_OUTPUT_FOLDER, name)) and name.endswith(".json")] '''


def formatting_final_json():
    os.chdir(CURRENT_DIR)
    print("Formatting final JSON File")

    with open(CONSOLIDATED_JSON_OUTPUT_FILE, 'rb+') as finalJsonFile:
        finalJsonFile.seek(-3, os.SEEK_END)
        finalJsonFile.truncate()

    with open(CONSOLIDATED_JSON_OUTPUT_FILE, "a") as finalJsonFile:
        finalJsonFile.write(']')


def create_consolidated_json_file():
    with open(CONSOLIDATED_JSON_OUTPUT_FILE, "w+") as jsonFile:
        jsonFile.write("[")

def write_to_csv():
    print("Converting json to CSV file : " + CONSOLIDATED_CSV_OUTPUT_FILE)
    jsonData = pandas.read_json(CONSOLIDATED_JSON_OUTPUT_FILE)
    
    jsonData.to_csv(CONSOLIDATED_CSV_OUTPUT_FILE, index=False, header=None)

def iterate_repos(folder_list, metadata_folder):
    for singleRepo in folder_list:
        if is_git_directory(singleRepo):
            extract_git_metadata(singleRepo, metadata_folder)
            print("\n")
        else:
            print("Folder is not a git repo. Skipping...")


# =================

# Will give the current working dir (for starting reference)
CURRENT_DIR = os.path.abspath(os.getcwd())
ROOT_FOLDER = os.path.join(CURRENT_DIR, "commit-data")
REPO_CONFIG_FILE = os.path.join(os.getcwd(), "config", "commit-analysis.config")
REPOS_FOLDER = os.path.join(ROOT_FOLDER, "repos")
META_DATA_OUTPUT_FOLDER = os.path.join(ROOT_FOLDER, "output")
CONSOLIDATED_JSON_OUTPUT_FILE = os.path.join(META_DATA_OUTPUT_FOLDER, "consolidated-output.json")
CONSOLIDATED_CSV_OUTPUT_FILE = os.path.join(META_DATA_OUTPUT_FOLDER, "consolidated-output.csv")


def main():
    folder_cleanup(REPOS_FOLDER)
    folder_cleanup(META_DATA_OUTPUT_FOLDER)
    create_consolidated_json_file()
    start_time = time.time()
    clone_git_repos(REPO_CONFIG_FILE, REPOS_FOLDER)
    end_time = time.time()
    print("\nTime taken for Cloning %s secs" % (str(round(end_time - start_time, 2))))

    iterate_repos(get_repository_folder_list(REPOS_FOLDER), META_DATA_OUTPUT_FOLDER)
    formatting_final_json()
    write_to_csv()
    
    print("Consolidated Json File : " + CONSOLIDATED_JSON_OUTPUT_FILE)
    print("\n")
    print("Completed extracting all metadata from the given list of repos")


main()
