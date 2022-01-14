console.log("Creating indexes")

use commit-analysis

db.commits_data.createIndex( {"author_name" : 1} )
db.commits_data.createIndex( {"author_email" : 1} )
db.commits_data.createIndex( {"committer_name" : 1} )
db.commits_data.createIndex( {"committer_email" : 1} )
db.commits_data.createIndex( {"repo_name" : 1} )


console.log("List of available idexes")
db.commits_data.getIndexes()



