import os
import os.path as osp
import argparse
import re

EXT_LIST = ['.py', '.cpp', '.h', '.cu']
REGEX_PATTERN = (r"(os\.environ\[[\"\'](?P<pyEnviron>[a-zA-Z0-9_]+?)[\"\'])|"
                 r"(os\.environ\.get\([\"\'](?P<pyEnvironGet>[a-zA-Z0-9_]+?)[\"\'])|"
                 r"(getenv\([\"\'](?P<cppGetenv>[a-zA-Z0-9_]+?)[\"\']\))")

env_vars = set()


def process(path):
    with open(path, 'r') as f:
        for line in f.readlines():
            m = re.search(REGEX_PATTERN, line)
            if m:
                for var in m.groupdict().values():
                    if var is not None:
                        env_vars.add(var.strip())


def main(args):
    for root, dirs, files in os.walk(args.pytorch_root):
        for f in files:
            name, ext = osp.splitext(f)
            if ext in EXT_LIST:
                full_path = osp.join(root, f)
                process(full_path)

    for env_var in sorted(env_vars):
        print(f"|`{env_var}`| | |")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pytorch-root', type=str)
    main(parser.parse_args())
