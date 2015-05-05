#!/usr/bin/env python
import json

import os
import subprocess


def get_repos(top_dir):
    for root, dirs, files in os.walk(top_dir):
        for directory in dirs:
            if directory.endswith(".git"):
                yield os.path.join(root, directory)


def get_committer_age(top_dir):
    for repo_dir in get_repos(top_dir):
        p = subprocess.Popen(
            'git log -1 --pretty=%at;%ar;%ae'.split(' '), cwd=repo_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdin, stderr = p.communicate()
        if stderr:
            print "Failed to get log for %s: %s" % (repo_dir, stderr.strip())
            continue
        values = stdin.strip().split(';')
        yield {'seconds': values[0], 'age': values[1], 'email': values[2],
               'repo': repo_dir}


if __name__ == '__main__':
    for d in sorted(get_committer_age("."), key=lambda x: -int(x['seconds'])):
        print json.dumps(d, indent=2)

