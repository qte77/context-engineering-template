#!/bin/bash
# 1 repo, 2 target ref, 3 current version

tag_to_delete="v$3"
branch_del_api_call="repos/$1/git/refs/heads/$2"
del_msg="'$2' force deletion attempted."
close_msg="Closing PR '$2' to rollback after failure"

echo "Tag $tag_to_delete for $del_msg"
git tag -d "$tag_to_delete"
echo "PR for $del_msg"
gh pr close "$2" --comment "$close_msg"
echo "Branch $del_msg"
gh api "$branch_del_api_call" -X DELETE && \
  echo "Branch without error return deleted."