#!/usr/bin/env python3

##
# Script to show GitHub API issues data.
#
# Syntax:
#
#     sixarm-github-api-issues-data.py
# 
# Example:
#
#     $ export GITHUB_PERSONAL_ACCESS_TOKEN=fe7f2bf4057de85eb638dc7356047b0e31d24a4b
#     $ sixarm-github-api-issues-data.py
#     => print a list of all repos
#     $ sixarm-github-api-issues-data.py alpha/bravo
#     => print the issues for the "alpha" owner "bravo" repo.
#
#
# ## Introduction
#
# GitHub technical info:
#
#   * API: https://developer.github.com/v3/
#
#   * PyGitHub: https://pygithub.readthedocs.io/en/latest/introduction.html
#
#
# ## Setup
#
# To generate your own GitHub personal access token:
#
#   * Got to GitHub https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
#   * Sign in as usual
#   * In the upper-right corner of any page, click your profile photo, then click Settings.
#   * In the left sidebar, click Developer settings.
#   * In the left sidebar, click Personal access tokens.
#   * Click Generate new token.
#   * Give your token a descriptive name.
#   * Select scopes; to use your token to access repositories from the command line, select repo.
#   * Click Generate token.
#
#
# ## Dependencies
#
# This script uses `PyGithub`.
#
# Install:
#
#     $ pip install --upgrade PyGithub
#
# ## Troubleshooting
#
# If you get the error message:
#
#     No module named pip
#
# Then install pip:
#
#     $ easy_install pip
#
# If you get the error message:
#
#     ModuleNotFoundError: No module named 'github'
#
# Then try installing using a specific python instance:
#
#     $ python3 -m pip install --upgrade pip
#     $ python3 -m pip install pygithub
#
# If you are using macOS and python 3, 
# and get the error message:
#
#     $ pip3 
#     Traceback (most recent call last):
#     File "/Library/Developer/CommandLineTools/usr/bin/pip3", line 10, in <module>
#     sys.exit(main())
#     TypeError: 'module' object is not callable
#
# Then try uninstalling pip:
#
#     $ python3 -m pip install --upgrade pip
#
# If you are using macOS Catalina, python 3.7, and pip3, and
# you get an error message that shows pip3 is aborting, then
# see: https://github.com/Homebrew/homebrew-core/issues/44996
#
# And try this:
#
#     $ rm -rf python3.7/site-packages/asn1crypto
#     $ pip3 install asn1crypto
#
# ## GitHub Enterprise
#
# If you use Github Enterprise with custom hostname,
# then you need to adjust this script by doing:
#
#     g = Github(base_url="https://{hostname}/api/v3", login_or_token="token")
#
##

import os
import sys
from pprint import pprint
import logging
import json
from github import Github

##
#
# Setup
#
##

def github_personal_access_token():
    x = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if x is None:
        print("This script needs an environment variable GITHUB_PERSONAL_ACCESS_TOKEN.", file=sys.stderr)
        quit()
    return x

def github_client():
    return Github(github_personal_access_token())

def show_user():
    user = GITHUB_CLIENT.get_user()
    pprint(user)
    
def show_repos():
    for repo in GITHUB_CLIENT.get_user().get_repos():
        print(repo.name)

def show_repo(github_owner_repo):
    repo = GITHUB_CLIENT.get_repo(owner_repo)
    print(repo.name)

def show_repo_issues(github_owner_repo):
    repo = GITHUB_CLIENT.get_repo(github_owner_repo)
    for issue in repo.get_issues(state='all'):
        print(issue_as_update_log_tsv(github_owner_repo, issue))

def issue_as_summary(github_owner_repo, issue):
    return f"{github_owner_repo} issue {issue.number} {issue.state} {issue.title}"

def issue_as_update_log_tsv(github_owner_repo, issue):
    return f"{issue.updated_at}\t{issue.url}\t{issue.state}\t{issue.title}"

def show_repo_issues_as_summary(github_owner_repo):
    repo = GITHUB_CLIENT.get_repo(github_owner_repo)
    for issue in repo.get_issues():
        print(f"{github_owner_repo} issue {issue.updated_at} {issue.number} {issue.state} {issue.title} ")

def show_repo_labels(github_owner_repo):
    repo = GITHUB_CLIENT.get_repo(github_owner_repo)
    for label in repo.get_labels():
        print(f"{github_owner_repo} label:{label.name} color:{label.color}")

GITHUB_CLIENT = github_client()

def main():
    if len(sys.argv) <= 1:
        show_repos()
    else:
        github_owner_repo = sys.argv[1]
        show_repo_issues(github_owner_repo)
  
if __name__== "__main__":
    main()
