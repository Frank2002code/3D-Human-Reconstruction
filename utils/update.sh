#!/bin/bash

COMMIT_MSG="${1:-$(date +"%Y-%m-%d %H:%M:%S")}"
git pull https://Frank2002code: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@github.com/Frank2002code/3D-Human-Reconstruction.git main
git status
git add -A
git commit -m "$COMMIT_MSG" || echo "No changes to commit"
git push https://Frank2002code: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@github.com/Frank2002code/3D-Human-Reconstruction.git main