# git-commit analysis


A tool written to analyze large number of repositories, that's self run for enterprise teams, and analyse the producitivity of developers

### Configure the repos:
Add the list of repos in config/repo.confing (only HTTPS link & also ensure the repo has public access)

## Usage:

#### docker-compose method:
If you are allowed to use docker compose in your organization,

``` shell 
docker-compose up
```

This will create the mongodb container, and then will run the python script to generate the consolidated json data which will be seeded to the mongo database.
<!-- This data will be used by the Flask API's and React to populate the Charts for visualization-->

#### Standalone usage: 
First run the script and then generate the consolidated-output.json file 

``` python
python git-repo-pull.py
```

Use the file JSON file generated at ```./commit-data/output/consolidated-output.json``` to load to mongodb.
<!-- Use this json file to load and run the flask and the React frontend -->


### Sample JSON Metadata

``` json
{
	"commit_hash": "5a501aa2163e84268c1feead1f049855d7452232",
	"short_hash": "5a01aa",
	"author_name": "alpha developer",
	"author_email": "alpha@email.com",
	"author_date": "2021-12-22 01:40:33",
	"committer_name": "alpha developer",
	"committer_email": "alpha@email.com",
	"committer_date": "2021-12-22 01:40:33",
	"subject": "Initial-Commit",
	"files_changed": 40,
	"lines_inserted": 1245,
	"lines_deleted": 13090,
	"repo_name": "kafka-streams-project"
}
```
  
**NOTE: For performance improvement on large number of repositories, indexing on mongodb for most used columns is added.**
