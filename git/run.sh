#!/bin/bash

telepresence --namespace test-payload --swap-deployment echoserver --expose 5000 --run flask --app /home/user/PycharmProjects/python-declarative/git/main.py run --reload