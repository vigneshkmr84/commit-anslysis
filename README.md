# git-commit analysis

__Table of Contents:__
  - [Configure the repos:](#configure-the-repos)
  - [Usage:](#usage)
      - [docker-compose method:](#docker-compose-method)
      - [Standalone usage:](#standalone-usage)
    - [Sample JSON Metadata](#sample-json-metadata)
  - [Performance Analysis:](#performance-analysis)



A tool written to analyze large number of repositories, that's self run for enterprise teams, and analyse the producitivity of developers.

## Configure the repos:    

Add the list of repos in ```config/commit-analysis.config``` (If adding SSH url's then add base64 encoded private key as well. For HTTPS URL's make sure the repo has Open Access permissions)

<details>
  <summary markdown="span">Sample SSH Configuration</summary>

``` property
[ssh]
https=False
baseurl=https://github.com
privateKey=<Base64_PrivateKey>

[repository]
list=
    git@github.com:vigneshkmr84/kafka-streams-project.git
    git@github.com:vigneshkmr84/spring-boot-security-jwt.git
    git@github.com:vigneshkmr84/kafka-validator-service.git
```

</details>

<details>
  <summary markdown="span">Sample HTTPS Configuration</summary>

``` shell
[ssh]
https=True
baseurl=https://github.com

[repository]
list =
    https://github.com/vigneshkmr84/kafka-streams-project.git
    https://github.com/vigneshkmr84/spring-boot-security-jwt.git
    https://github.com/vigneshkmr84/kafka-validator-service.git
```

</details>

<br>

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

Use the file JSON file generated at ```commit-data/output/consolidated-output.json``` & ```commit-data/output/consolidated-output.csv``` to load to mongodb.

You can load the CSV File to load to MYSQL db as well or any other RDBMS accordingly
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

<details>
  <summary markdown="span">How Data is Stored in MongoDB</summary>

``` json
{
    _id: ObjectId("61e1647a3caa0b6db689cd84"),
    commit_hash: '5a501aa2163e84268c1feead1f049855d7452232',
    short_hash: '5a501aa',
    author_name: 'alpha developer',
    author_email: 'alpha@email.com',
    author_date: ISODate("2021-12-22T01:40:33.000Z"),
    committer_name: 'alpha developer',
    committer_email: 'alpha@email.com',
    committer_date: ISODate("2021-12-22T01:40:33.000Z"),
    subject: 'Initial-Commit',
    files_changed: 40,
    lines_inserted: 1245,
    lines_deleted: 13090,
    repo_name: 'kafka-streams-project'
  }

```
</details>

<br>


## Performance Analysis:

Data Extraction is the key factor in performance. When extracting, if the lines added/ deleted & files updated are included there is certainly a dip in performance (more time to extract the data points). Here are some performance analysis numbers 

| Metadata type | Repository | Commits | Time to clone repo (sec) | Time to extract metadata (sec) | CSV Size (MB) | JSON Size (MB) |
| :---        |  :---:  | :---:    | :---: | :---: | :---: | ---: |
| w lines |  [rust](https://github.com/rust-lang/rust) |  161,062 | 1268.68 | 284.81 | 25 | 54
| w/o lines | [rust](https://github.com/rust-lang/rust) |  161,062 | | |



*NOTE: For performance improvement on large number of repositories, indexing on mongodb is done for most used frequently columns.*
