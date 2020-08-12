#!/usr/local/bin/python3
import argparse
import os
import shutil
from datetime import datetime

DEFAULT_TARGET_DIR = 'renamed'

parser = argparse.ArgumentParser(
    description='Renames files by adding timestamp (in format Y-m-d_H-M-S) to original or given name.'
)

parser.add_argument(
    '-b',
    '--basename',
    default=None,
    help='provide a base file name. If not provided - original file name'
)
parser.add_argument(
    '-e',
    '--ext',
    default='jpg',
    help='provide a file extention, which should be renamed (default: jpg)'
)
parser.add_argument(
    '-s',
    '--source_dir',
    default=None,
    help='source directory'
)
parser.add_argument(
    '-t',
    '--target_dir',
    default=DEFAULT_TARGET_DIR,
    help='target directory'
)
parser.add_argument(
    '-m',
    '--move',
    default=False,
    type=bool,
    help='if true - files will be moved to target directory'
)

args = parser.parse_args()

curr_dir = os.getcwd()
if args.move:
    print('Moving files...')
    action = shutil.move
else:
    print('Copying files...')
    action = shutil.copy2

if args.source_dir:
    if os.path.isabs(args.source_dir):
        work_dir = args.source_dir
    else:
        work_dir = os.path.join(curr_dir, args.source_dir)
else:
    work_dir = curr_dir

if not os.path.isdir(work_dir):
    raise FileNotFoundError('Source directory not found')

if args.move and args.target_dir == DEFAULT_TARGET_DIR:
    target_dir = work_dir
else:
    if os.path.isabs(args.target_dir):
        target_dir = args.target_dir
    else:
        target_dir = os.path.join(work_dir, args.target_dir)


if not os.path.exists(target_dir):
    os.mkdir(target_dir)

files_in_work_dir = os.listdir(work_dir)
work_files_list = []
target_file_name_list = []
for fn in files_in_work_dir:
    ext = os.path.splitext(fn)[-1][1:].lower()
    if ext == args.ext:
        count = 0
        work_files_list.append(fn)
        if args.basename:
            basename = args.basename
        else:
            basename = os.path.splitext(fn)[0]
        new_fn = basename + '_' + \
            datetime.fromtimestamp(os.stat(os.path.join(work_dir, fn)).st_birthtime).strftime('%Y-%m-%d_%H-%M-%S') + \
            '-' + str(count) + os.path.splitext(fn)[-1]
        while new_fn in target_file_name_list:
            count += 1
            new_fn = basename + '_' + \
                datetime.fromtimestamp(os.stat(os.path.join(work_dir, fn)).st_birthtime).strftime('%Y-%m-%d_%H-%M-%S') + \
                '-' + str(count) + os.path.splitext(fn)[-1]

        target_file_name_list.append(new_fn)
        new_full_fn = os.path.join(target_dir, new_fn)
        action(os.path.join(work_dir, fn), new_full_fn)


print('{0} files with extention {1} {3} {2}'.format(
    len(target_file_name_list),
    args.ext.upper(),
    target_dir,
    'moved (and renamed) to' if args.move else 'copied (and renamed) to'
    )
)
