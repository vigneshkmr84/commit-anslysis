from ast import Str
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask.wrappers import Response
import json
from bson import json_util
from bson.json_util import dumps
import os
#from werkzeug.exceptions import HTTPException


connection = ""
db = ""

try:
    connection = MongoClient(host = ["localhost:27017"], serverSelectionTimeoutMS = 2000) 
    print("Connection string " + str(os.getenv("CONN_STR")))
    db = connection['commit-analysis']
    
    print("Connection Successful. Mongo Server version : " + connection.server_info()["version"])
except ConnectionError as e:
    print("Connection Error" + e.strerror)


commit_collection = db.get_collection('commits_data')

# Issue the serverStatus command and print the results
#serverStatusResult = db.command("serverStatus")
#print(serverStatusResult)

app = Flask(__name__)


'''
List out the unique repo's available in the database
'''
@app.route('/repo/unique', methods=['GET'])
def repo_count():
    app.logger.info('Inside repository count api')

    unique = commit_collection.distinct("repo_name")
    print(unique)

    return Response(json.dumps(unique), status=200, mimetype='application/json')

'''
API will return the stats (files_changed, lines added / deleted & total commits)
for single repo provide the repo name; Or by default will provide 
for all repos
'''
@app.route('/stats', methods = ['GET'])
def get_repo_stats():
    repo_name = request.args.get("repo_name")
    
    query = []
    if repo_name == None:
        query = [ { "$group" : { "_id" : "$repo_name" ,
                                "inserted" : { "$sum" : "$lines_inserted" },
                                "deleted" : { "$sum" : "$lines_deleted" },
                                "files" : { "$sum" : "$files_changed" },
                                "commits" : { "$sum" : 1 }
                    } } ]
    else: 
        print("repo name : " + repo_name)
        query = [ { "$match" : { "repo_name" : repo_name } }, 
                { "$group" : { "_id" : "$repo_name" ,
                              "inserted" : { "$sum" : "$lines_inserted" },
                              "deleted" : { "$sum" : "$lines_deleted" },
                              "files" : { "$sum" : "$files_changed" },
                              "commits" : { "$sum" : 1 }
                } } ]
    
    repo_stats = commit_collection.aggregate(query)
    list_obj = list(repo_stats)
    print("Total Size : " + str(len(list_obj)))
    list_obj = json.dumps(list_obj)
    
    return Response( list_obj, status=200, mimetype='application/json' )

"""
API to aggregate the commits performed by all authors on all repos
"""
@app.route("/commits/author", methods=["GET"])
def get_aggregate_by_author():
    
    try:
        # Original Query
        ''' query = [{
            "$group" : { "_id" : "$author_email" ,
            "commitCount" : { "$sum" : 1 } }
        }] '''
        query = [{
            "$group" : 
            { "_id" : "$author_email" ,
            "commitCount" : { "$sum" : 1 },
            "lines_added" : { "$sum" : "$lines_inserted" },
            "lines_deleted" : { "$sum" : "$lines_deleted" }            
            }
        }]
        author_wise_commit = commit_collection.aggregate(query)
        
        list_obj = list(author_wise_commit)
        print("total size : "  + str(len(list_obj)))
        list_obj = json.dumps(list_obj)
        return Response( list_obj, status=200, mimetype='application/json')
    except:
        return Response("Error in fetching data", status=500, mimetype='application/json')



"""
API to fetch the commit timeline 
can be generarlized as well as for a specific author email id
based on the query parameters provided
"""
@app.route("/timeline")
def commit_timeline():
    author_email = request.args.get("author_email")
    
    commit_timeline = []
    commit_query = []
    
    if author_email == None:
        print("Timeline for all repos")
        commit_query = [{   
        "$group" : {
            "_id": { "$dateToString": { "format": "%Y-%m-%d", "date": "$committer_date" }},
            "count": { "$sum": 1 } }
        }]
    else:
        print("Timeline for author : " + author_email)
        commit_query = [{ "$match" : { "author_email" : author_email } },    
        {"$group" : {
            "_id": { "$dateToString": { "format": "%Y-%m-%d", "date": "$committer_date" }},
            "count": { "$sum": 1 } }
        }]
    
    commit_timeline = commit_collection.aggregate(commit_query)
    commit_timeline = list(commit_timeline)
    print("Total data : " + str(len(commit_timeline))) 
    commit_timeline = json.dumps(commit_timeline)
    
    return Response(commit_timeline, status=200, mimetype='application/json')

"""
API to get the developer wise stats for a specific repo
"""
@app.route("/repo/stats")
def repo_commits():
    repo_name = request.args.get("repo_name")
    
    query = [ { "$match" : { "repo_name" : repo_name } }, 
                { "$group" : { "_id" : "$author_name" ,
                              "inserted" : { "$sum" : "$lines_inserted" },
                              "deleted" : { "$sum" : "$lines_deleted" },
                              "files" : { "$sum" : "$files_changed" },
                              "commits" : { "$sum" : 1 }
                } } ]
    
    repo_stats = commit_collection.aggregate(query)
    repo_stats = list(repo_stats)
    print("Total data : " + str(len(repo_stats)))
    repo_stats = json.dumps(repo_stats)
    
    return Response(repo_stats, status=200, mimetype="application/json")

""" Health EndPoint """
@app.route('/health', methods=['GET'])
def health():
    app.logger.info('Health OK')
    return Response('OK', status=200)




if __name__ == '__main__':
    app.logger.info('Starting service default port')
    # app.run(host='0.0.0.0', debug=False)
    app.run(host='0.0.0.0')  # default = with debugger (will not show the custom Error pages)
    
    
''' @app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400
 '''
