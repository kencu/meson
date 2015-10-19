#!/usr/bin/env python3

# Copyright 2014 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This program is a wrapper to run external commands. It determines
what to run, sets up the environment and executes the command."""

import sys, os, subprocess, shutil

def run_command(source_dir, build_dir, subdir, command, arguments):
    env = {'MESON_SOURCE_ROOT' : source_dir,
           'MESON_BUILD_ROOT' : build_dir,
           'MESON_SUBDIR' : subdir
          }
    cwd = os.path.join(source_dir, subdir)
    child_env = os.environ.copy()
    child_env.update(env)

    # Is the command an executable in path?
    exe = shutil.which(command)
    if exe is not None:
        command_array = [exe] + arguments
        return subprocess.Popen(command_array, env=child_env, cwd=cwd)
    # No? Maybe it is a script in the source tree.
    fullpath = os.path.join(source_dir, subdir, command)
    command_array = [fullpath] + arguments
    try:
        return subprocess.Popen(command_array,env=child_env, cwd=cwd)
    except FileNotFoundError:
        print('Could not execute command "%s".' % command)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(sys.argv[0], '<source dir> <build dir> <subdir> <command> [arguments]')
    src_dir = sys.argv[1]
    build_dir = sys.argv[2]
    subdir = sys.argv[3]
    command = sys.argv[4]
    arguments = sys.argv[5:]
    pc = run_command(src_dir, build_dir, subdir, command, arguments)
    pc.wait()
    sys.exit(pc.returncode)
