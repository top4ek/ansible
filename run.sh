#!/bin/bash

ansible-playbook --diff -i hosts.yaml roles.yaml
