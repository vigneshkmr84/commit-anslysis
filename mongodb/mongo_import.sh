data = "{ \"commit_hash\" : \"" + commit_hash + "\", \"short_hash\" : \"" + short_hash + "\", \"author_name\" : \"" + author_name + "\" , \"author_email\" : \"" + author_email + "\" , \"author_date\" : ISODate(\"" + author_date + "\") , \"committer_name\" : \"" + committer_name + "\" , \"committer_email\" : \"" + committer_email + "\", \"committer_date\" : \"" + committer_date + "\", \"subject\" : \"" + subject_sanitized + "\" }"




mongoimport --host localhost --db commit-analysis --collection sample_test --type csv --headerline --file /Users/vignesh/my-works/git-log-analysis/commit-data/output/consolidated-output.csv --columnsHaveTypes

# original columns 
# commit_hash,short_hash,author_name,author_email,author_date,committer_name,committer_email,committer_date,subject,files_changed,lines_inserted,repo_name,lines_deleted

mongoimport --host localhost --db commit-analysis --collection sample_test --type csv --fields=commit_hash.string(),short_hash.string(),author_name.string(),author_email.string(),author_date.date(2021-12-16 15:04:05),committer_name.string(),committer_email.string(),committer_date.date(),subject.string(),files_changed.int32(),lines_inserted.int32(),repo_name.string(),lines_deleted.int32() --columnsHaveTypes --file /Users/vignesh/my-works/git-log-analysis/commit-data/output/consolidated-output.csv


mongoimport --host localhost --db commit-analysis --collection sample_test --type csv --headerline --columnsHaveTypes --file /Users/vignesh/my-works/git-log-analysis/commit-data/output/consolidated-output.csv

#--fields=commit_hash.string(),short_hash.string(),author_name.string(),author_email.string(),author_date.date(),committer_name.string(),committer_email.string(),committer_date.date(),subject.string(),files_changed.int32(),lines_inserted.int32(),repo_name.string(),lines_deleted.int32()
--columnsHaveTypes


mongoimport --type csv --host localhost --db commit-analysis --collection sample_test --columnsHaveTypes --fields "commit_hash.string(),short_hash.string(),author_name.string(),author_email.string(),author_date.date(2006-01-02),committer_name.string(),committer_email.string(),committer_date.date(2006-01-02),subject.string(),files_changed.int32(),lines_inserted.int32(),repo_name.string(),lines_deleted.int32()" --file /Users/vignesh/my-works/git-log-analysis/commit-data/output/consolidated-output.csv

./mongoimport --host localhost --db commit-analysis --collection sample_test --type csv --file /Users/vignesh/my-works/git-log-analysis/commit-data/output/consolidated-output.csv --headerline --columnsHaveTypes 



# working version 2 (use without the headers in the csv file)
mongoimport --type csv --host localhost --db commit-analysis --collection sample_test --columnsHaveTypes --fields "commit_hash.string(),short_hash.string(),author_name.string(),author_email.string(),author_date.date_ms(yyyy-MM-dd),committer_name.string(),committer_email.string(),committer_date.date_ms(yyyy-MM-dd),subject.string(),files_changed.int32(),lines_inserted.int32(),lines_deleted.int32(),repo_name.string()" --file /Users/vignesh/my-works/git-log-analysis/commit-data/output/consolidated-output.csv

# final Working
mongoimport --type csv --host localhost --db commit-analysis --collection sample_test --columnsHaveTypes --fields "commit_hash.string(),short_hash.string(),author_name.string(),author_email.string(),author_date.date(2006-01-02 15:04:05),committer_name.string(),committer_email.string(),committer_date.date(2006-01-02 15:04:05),subject.string(),files_changed.int32(),lines_inserted.int32(),lines_deleted.int32(),repo_name.string()" --file /Users/vignesh/my-works/git-log-analysis/commit-data/output/consolidated-output.csv