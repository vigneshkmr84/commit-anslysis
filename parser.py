import configparser
import base64
import subprocess
import os

config = configparser.ConfigParser(allow_no_value=True)

config_file = os.path.join("config", "commit-analysis.config")
config.read(config_file)
ssh_config = config['ssh']


repoList = config['repository']['list'].split()
https = ssh_config.getboolean('https')
base_url = ssh_config.get('baseurl')
raw_url = base_url.replace("\"", "").replace("https://", "")


#SSH_BASE_FOLDER = "./commit-data"
SSH_BASE_FOLDER = "/root"
SSH_KNOWN_HOST_FILE = os.path.join(SSH_BASE_FOLDER, ".ssh", "known_hosts")
SSH_PRIVATE_KEY_FILE = os.path.join(SSH_BASE_FOLDER, ".ssh", "id_rsa")


def check_connectivity(repo_url):
    
    try:
        git_check=subprocess.Popen(["ssh", "-T", repo_url]
                                    , stdout = subprocess.PIPE
                                    , stderr = subprocess.STDOUT)

        stdout, stderr = git_check.communicate(timeout= 5)
       
    except Exception as e:
        print("Exception occurred during connection with repo " + repo_url +  str(e))
        git_check.kill()
        return False;
    
    
    stdout=stdout.decode("utf-8").replace("\n", "")
    print("stdout : " + stdout)
    
    if "denied" in stdout:
        print("Error: Unable to establish Connection")
        return False
    else:
        print("Connection established successfully")
        return True
    

def scan_ssh_host_key(url):
    print("Scanning SSH Host Key of url : " + url)
    
    output = subprocess.check_output(["ssh-keyscan", url])
    output=output.decode("utf-8")
    
    #print(output)
    with open(SSH_KNOWN_HOST_FILE, "w+") as known_hosts:
        known_hosts.write(output)

    
def main():
    if not https:
        print("URL is SSH based. Retrieving Private Key")
    ssh=ssh_config.get("privateKey")
    
    if not ssh:
        print("Private key is empty. Exitting...")
        exit(2)

    private_key = base64.b64decode(ssh)
    print("Writing SSH keys to private file")
    
    # Write details to id_rsa file
    # Original to be used

    with open(SSH_PRIVATE_KEY_FILE, "w+") as sshFile:
        sshFile.write(private_key.decode("utf-8"))
        
    scan_ssh_host_key(raw_url)
    connectivity_status = check_connectivity("git@" + raw_url)
    
    if not connectivity_status:
        print("Unable to establish connection. Exitting...")
        exit(2)
        
    else:
        print("Repo clone url's are all HTTPS based.")
    

print("Initiating Configuration")
print("Raw URI : " + raw_url)
main()


print("List of Repos")
for repo in list(repoList):
    print(repo)
    
print("\n")
print("End of initial setup")