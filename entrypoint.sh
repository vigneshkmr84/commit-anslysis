#!/bin/bash

# Importing CSV Data
mongoimport --type csv --host mongodb --db commit-analysis --collection commits_data --columnsHaveTypes --fields "commit_hash.string(),short_hash.string(),author_name.string(),author_email.string(),author_date.date(2006-01-02 15:04:05),committer_name.string(),committer_email.string(),committer_date.date(2006-01-02 15:04:05),subject.string(),files_changed.int32(),lines_inserted.int32(),lines_deleted.int32(),repo_name.string()" --file /tmp/consolidated-output.csv

# Creating indexes 
mongosh mongodb://mongodb/commit-analysis < /tmp/index.js


