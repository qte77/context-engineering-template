#!/bin/bash
# 1 base ref, 2 target ref, 3 title suffix
# 4 current version, 5 bumped

pr_title="PR $2 $3"
pr_body="PR automatically created from \`$1\` to bump from \`$4\` to \`$5\` on \`$2\`. Tag \`v$5\` will be created and has to be deleted manually if PR gets closed without merge."

gh pr create \
  --base $1 \
  --head $2 \
  --title "${pr_title}" \
  --body "${pr_body}"
  # --label "bump"
