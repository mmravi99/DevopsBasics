from pickle import TRUE
import sys
from github import Github
import requests
import json 

# Repositories settings to apply
allowsquashmerge = False
allowrebasemerge = False
allowmergecommit = True
deletebranchonmerge = False

args = sys.argv[1:]
token=sys.argv[1]
repo_name=sys.argv[2]

print("token",token)
print("repo name",repo_name)

g = Github(token)
print(f"Logged in as {g.get_user().name}")

repo = g.get_repo(repo_name)
branch_to_protect = g.get_repo(repo_name).get_branch(repo.default_branch)


################################### Configuring Repository Settings ##############################################
repo.edit(allow_squash_merge=allowsquashmerge,
          allow_merge_commit=allowmergecommit,
          allow_rebase_merge=allowrebasemerge,
          delete_branch_on_merge=deletebranchonmerge
          )
print(f"Configured {repo_name} with the following settings")
print(f"Allow Squash Merge: {allowsquashmerge}")
print(f"Allow Rebase Merge: {allowrebasemerge}")
print(f"Allow Merge Commits: {allowmergecommit}")
print(f"Delete Branch On Merge: {deletebranchonmerge}")


################################### Configuring Branch Protection Rule ##############################################


# Branch Protection Rule Settings to create
requiredapprovingreviewcount = 1
require_conversation_resolution = True
allow_deletions = False
enforceadmins = True
requirecodeownerreviews = True
dismissstalereviews = True
branch_up_to_date = True
requiredstatuschecks = ['pr-lint', 'codemetrics', 'build', 'checkprojectsettings', 'format', 'unittestcoverage',
                           'mutation-testing', 'docker-build']

branch_to_protect.edit_protection(strict=True,
                                  contexts=requiredstatuschecks,
                                  enforce_admins=enforceadmins,
                                  dismiss_stale_reviews=dismissstalereviews,
                                  require_code_owner_reviews=requirecodeownerreviews,
                                  required_approving_review_count=requiredapprovingreviewcount
                                  )
branch_to_protect.edit_required_pull_request_reviews(dismiss_stale_reviews=dismissstalereviews,
                                                     require_code_owner_reviews=requirecodeownerreviews, 
                                                     required_approving_review_count=requiredapprovingreviewcount
                                                     )


print(f"Configured {branch_to_protect} with the following protection rules:")
print(f"Required Approving Reviews: {requiredapprovingreviewcount}")
print(f"Required Code Owner Reviews: {requirecodeownerreviews}")
print(f"Dismiss Stale Reviews: {dismissstalereviews}")
print(f"Require Branch To Be Up To Date Before Merging: {branch_up_to_date}")
print(f"Required Status Checks: {requiredstatuschecks}")
print(f"Enforce for Admins: {enforceadmins}")
print(f"Require Conversation Resolution: {require_conversation_resolution}")
print(f"Allow Deletions: {allow_deletions}")
