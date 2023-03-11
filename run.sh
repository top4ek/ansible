#!/bin/bash

ansible-playbook --diff -i hosts.yaml playbook.yaml
