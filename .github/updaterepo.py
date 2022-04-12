import sys
from github import Github
import requests
import json 

    

# Repo Settings
allow_squash_merge = False
allow_rebase_merge = True
allow_merge_commit = False
allow_auto_merge = True
delete_branch_on_merge = True
vulnerability_alert = True
automated_security_fixes = True

# Branch Protection Rule Settings
required_approving_review_count = 1
require_conversation_resolution = True
allow_deletions = False
enforce_admins = True
require_code_owner_reviews = True
dismiss_stale_reviews = False
branch_up_to_date = True


# args = sys.argv[1:]

# if len(args) == 0:
#     token = input("Github PAT: ")
#     repo_name = input("Repo to configure (organization/repo): ")
# else:
#     token = "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"
#     repo_name = "philips-internal/synergy-ui-template"

#token=input("enter PAT")
token = "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"

#repo_name = input("Repo to configure (organization/repo): ")
repo_name="philips-internal/synergy-ui-template"

g = Github(token)
print(f"Logged in as {g.get_user().name}")

repo = g.get_repo(repo_name)
branch_to_protect = repo.default_branch


################################### Configuring Repository Settings ##############################################

repo_url = "https://api.github.com/repos/"+repo_name
headers = headers = {"Authorization": f"token {token}", "accept": "application/vnd.github.luke-cage-preview+json"}
repo_settings = {'allow_squash_merge': allow_squash_merge, 'allow_merge_commit': allow_merge_commit,
                   'allow_rebase_merge': allow_rebase_merge, 'allow_auto_merge': allow_auto_merge,
                   'delete_branch_on_merge': delete_branch_on_merge}

r = requests.patch(repo_url, json=repo_settings, headers=headers)
print (r)

print(f"Configured {repo_name} with the following settings")
print(f"Allow Squash Merge: {allow_squash_merge}")
print(f"Allow Rebase Merge: {allow_rebase_merge}")
print(f"Allow Merge Commits: {allow_merge_commit}")
print(f"Allow Auto Merge: {allow_auto_merge}")
print(f"Delete Branch On Merge: {delete_branch_on_merge}")

################################### Configuring Branch Protection Rule ##############################################
required_status_checks = ['pr-lint', 'codemetrics', 'build', 'checkprojectsettings', 'format', 'unittestcoverage',
                          'mutation-testing', 'docker-build']

branch_protection = {'enforce_admins': enforce_admins,
                     'required_pull_request_reviews':
                         {'dismissal_restrictions': {},
                          'dismiss_stale_reviews': dismiss_stale_reviews,
                          'require_code_owner_reviews': require_code_owner_reviews,
                          'required_approving_review_count': 1},
                     'restrictions': None,
                     'required_status_checks': {'strict': branch_up_to_date,
                                                'contexts': required_status_checks},
                     'allow_deletions': allow_deletions,
                     'required_conversation_resolution': require_conversation_resolution}

r = requests.put(repo_url + f'/branches/{branch_to_protect}/protection', json=branch_protection, headers=headers)
print(r)

print(f"Configured {branch_to_protect} with the following protection rules:")
print(f"Required Approving Reviews: {required_approving_review_count}")
print(f"Required Code Owner Reviews: {require_code_owner_reviews}")
print(f"Dismiss Stale Reviews: {dismiss_stale_reviews}")
print(f"Require Branch To Be Up To Date Before Merging: {branch_up_to_date}")
print(f"Required Status Checks: {required_status_checks}")
print(f"Enforce for Admins: {enforce_admins}")
print(f"Require Conversation Resolution: {require_conversation_resolution}")
print(f"Allow Deletions: {allow_deletions}")