# fix the license header of .java files

import os
import tempfile

BAD = """ *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at""".split("\n")

GOOD = """ *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at""".split("\n")


def write_with_substitution(file_object, lines, match_offset):
    """
    Write lines to output_filename, replacing the occurrence of BAD at
    match_offset with GOOD

    Params:
        file_object: the file object to write the lines to
        lines: a list of lines to output
        match_offset: offset into lines where the first BAD line is found
    """
    for i in xrange(len(lines)):
        if i < match_offset:
            file_object.write(lines[i] + "\n")
        elif i == match_offset:
            file_object.write("\n".join(GOOD))
            file_object.write("\n")
        elif i > match_offset + len(BAD) - 1:
            file_object.write(lines[i])
            if i < len(lines) - 1:
                file_object.write("\n")


def replace_lines(file_name):
    """
    Look for the lines in BAD in file_name, replacing them if found with
    GOOD.
    """
    with open(file_name) as f:
        lines = f.read().split("\n")
        for i in xrange(len(lines)):
            match_offset = -1
            matched_lines = 0
            while True:
                if matched_lines == len(BAD):
                    break
                if i + matched_lines == len(lines):
                    break
                if lines[i + matched_lines] != BAD[matched_lines]:
                    break
                if match_offset == -1:
                    match_offset = i
                matched_lines += 1
                if matched_lines == len(BAD):
                    f = tempfile.NamedTemporaryFile(
                        dir=os.path.dirname(file_name))
                    try:
                        write_with_substitution(f, lines, match_offset)
                    finally:
                        f.close()
                    os.rename(f.name, file_name)
                    return

def replace_in_tree(dir_name):
    for root, dirs, files in os.walk(dir_name):
        for f in files:
            if not f.endswith(".java"):
                continue
            replace_lines(os.path.join(root, f))


if __name__ == '__main__':
    replace_in_tree(".")