import io
import time
from os import path

import yaml
from git import Repo

repo_name = "repo"
branch_name = "master"
commit_id = "c9e61b2cfb266f04d545728972bb1f556bfd9fe8"
git_url = "https://github.com/official-himanshu/JavaPro.git"
revision = branch_name
delay = 5


def pull(repo_name, git_url, revision):
    is_changed = False

    if not path.exists(repo_name):
        repo = Repo.clone_from(git_url, repo_name)
        is_changed = True
    else:
        repo = Repo(repo_name)
    commit = repo.commit()
    prev_sha = commit.hexsha
    try:
        repo.git.fetch(git_url, revision)
        repo.git.checkout(revision)
        try:
            if repo.active_branch:
                repo.git.pull()
        except:
            pass
        new_sha = repo.head.commit.hexsha
        if prev_sha != new_sha:
            is_changed = True
        print(is_changed)
        return is_changed
    except Exception as e:
        print(e)


def get_commit(repo):
    if not path.exists(repo):
        return None
    commit = repo.commit()
    return commit.hexsha


def run():
    while True:
        pull("repo", "https://github.com/official-himanshu/JavaPro.git", "master")
        time.sleep(delay)


# asyncio.run(run())

from flask import Flask, jsonify, request

app = Flask(__name__)


# @app.route("/")
# def _proxy(*args, **kwargs):
#     resp = requests.request(
#         method=request.method,
#         url=request.url.replace(request.host_url, 'https://google.com/imdex.html'),
#         headers={key: value for (key, value) in request.headers if key != 'Host'},
#         data=request.get_data(),
#         cookies=request.cookies,
#         allow_redirects=False)
#
#     excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
#     headers = [(name, value) for (name, value) in resp.raw.headers.items()
#                if name.lower() not in excluded_headers]
#
#     response = Response(resp.content, resp.status_code, headers)
#     return response


@app.route("/chart-decorator", methods=['POST'])
def chart_decorator():
    content = request.json
    # print(yaml.dump(content))
    composite = f"""
apiVersion: metacontroller.k8s.io/v1alpha1
kind: CompositeController
metadata:
  name:  {content["object"]["metadata"]["name"]}
spec:
  generateSelector: true
  resyncPeriodSeconds: 10
  parentResource:
    apiVersion: k-processor.io/v1
    resource: charts
    revisionHistory:
      fieldPaths:
      - spec.template
  childResources:
  - apiVersion: v1
    resource: services
  hooks:
    sync:
      webhook:
        url: http://echoserver.test-payload.svc/chart-composite
        timeout: 10s
"""
    return jsonify({
        "attachments": [
            yaml.full_load(io.StringIO(composite))
        ]
    })


@app.route("/chart-composite", methods=['POST'])
def chart_composite():
    content = request.json
    # print(yaml.dump(content))
    return jsonify({
        "attachments": {

        },
        "status": {
            "error": "received"
        }
    })


app.run(host="0.0.0.0")
