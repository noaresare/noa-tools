#!/usr/bin/env

import subprocess
import re

# determines the size of the diff merged for the provided PR id's
import sys
import collections

PR_IDS = [18, 30, 31, 34, 72, 79, 94, 104, 105, 106, 109, 110, 119, 123, 129]

MERGE_REGEXP = re.compile("([0-9a-f]{40}) Merge pull request #(\d+) from")


def get_commit_ids(git_dir, pull_request_ids):
    """
    Yields commit SHA1's given a list of Pull request ID's

    Params:
        git_dir: the directory to run git log in to find the ID's
        pull_request_ids: the list of integer ID's to look for
    Yields:
        SHA1 strings for the provided pull requests
    """
    log = subprocess.check_output(["git", "log", "--pretty=oneline"],
                                  cwd=git_dir)
    merge_map = {}
    for l in log.split("\n"):
        if len(l) == 0:
            continue
        match = MERGE_REGEXP.search(l)
        if match:
            merge_map[int(match.group(2))] = match.group(1)
    for pr_id in pull_request_ids:
        sha1 = merge_map.get(pr_id)
        if not sha1:
            print "Warning; could not find sha1 for PR %d" % pr_id
            continue
        yield pr_id, sha1


def get_merge_diff_length(sha1, git_dir):
    diff = subprocess.check_output(
        ["git", "diff", "{0}~1..{0}".format(sha1)], cwd=git_dir)
    return len(diff.split("\n"))


def main(git_dir, ids):
    sizes = collections.defaultdict(list)
    for pr_id, sha1 in get_commit_ids(git_dir, ids):
        sizes[get_merge_diff_length(sha1, git_dir)].append(pr_id)
    for size in sorted(sizes.keys(), key=lambda x: -x):
        pr_ids = sizes.get(size)
        for pr_id in pr_ids:
            print ("https://github.com/spotify/docker-client/pull/{:<3} (diff size: {} lines)"
                   .format(pr_id, size))

if __name__ == '__main__':
    main(sys.argv[1], (int(pr_id) for pr_id in sys.argv[2:]))