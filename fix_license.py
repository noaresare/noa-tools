# fix the license header of .java files

import os

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


def write_with_substitution(output_filename, lines, match_offset):
    """
    Write lines to output_filename, replacing the occurrence of BAD at
    match_offset with GOOD

    Params:
        output_filename: the filename to write the lines to
        lines: a list of lines to output
        match_offset: offset into lines where the first BAD line is found
    """
    with open(output_filename, "w") as f:
        for i in xrange(len(lines)):
            if i < match_offset:
                f.write(lines[i] + "\n")
            elif i == match_offset:
                f.write("\n".join(GOOD))
                f.write("\n")
            elif i > match_offset + len(BAD) - 1:
                f.write(lines[i])
                if i < len(lines) - 1:
                    f.write("\n")


def replace_lines(file_name):
    with open(file_name) as f:
        lines = f.read().split("\n")
        for i in xrange(len(lines)):
            match_offset = -1
            matched_lines = 0
            while True:
                if (matched_lines == len(BAD)
                        or i + matched_lines == len(lines)):
                    break
                if lines[i + matched_lines] != BAD[matched_lines]:
                    break
                if match_offset == -1:
                    match_offset = i
                matched_lines += 1
                if matched_lines == len(BAD):
                    write_with_substitution(file_name + ".fixed", lines,
                                            match_offset)
                    os.rename(file_name + ".fixed", file_name)
                    return

if __name__ == '__main__':
    for root, dirs, files in os.walk("."):
        for f in files:
            if not f.endswith(".java"):
                continue
            replace_lines(os.path.join(root, f))
