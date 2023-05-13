#!/bin/bash

ansible-playbook --connection=local --limit $1 --diff -i hosts.yaml playbook.yaml
