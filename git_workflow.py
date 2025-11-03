"""
git_workflow.py

This module documents and provides helper functions to automate the git workflow
described in the user's task. It does NOT run git commands automatically (safety)
but prints the exact commands to run and can simulate conflict editing.

The intended manual steps (to run in your local repo) are:
1) git checkout -b practice-6-main
2) create files and git add / commit / push origin practice-6-main
3) using git worktree create 5 branches based on practice-6-main:
   git worktree add ../wt-duplicate-1 practice-6-main
   cd ../wt-duplicate-1
   git checkout -b practice-6-main-duplicate-1
   modify files, commit, push origin practice-6-main-duplicate-1
   create PR -> practice-6-main
   repeat for duplicates 2..5
4) For PRs 2..5, intentionally cause conflicts by editing the same lines,
   then resolve using git rebase:
   git fetch origin
   git checkout practice-6-main-duplicate-2
   git rebase origin/practice-6-main
   # resolve conflicts, git add, git rebase --continue
   git push --force-with-lease origin practice-6-main-duplicate-2
   then complete PR merge.

This file also includes helpers to show how to programmatically edit specific lines
so you can create different variations of files across branches.
"""

import difflib
from pathlib import Path
import shutil
import os
import textwrap

def print_git_steps():
    steps = [
        'git checkout -b practice-6-main',
        'git add .',
        'git commit -m "Initial: add three python files for practice-6"',
        'git push -u origin practice-6-main',
        '',
        '# Create worktrees and duplicate branches:',
        'git worktree add ../wt-duplicate-1 practice-6-main',
        'cd ../wt-duplicate-1',
        'git checkout -b practice-6-main-duplicate-1',
        '# edit files, commit, push and open PR to practice-6-main',
    ]
    print('\n'.join(steps))

def simulate_edit_file(path: Path, target_line_no: int, new_text: str):
    """Edit a file by replacing a specific line number (1-based) with new_text.
    Returns True if successful.
    """
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    lines = path.read_text(encoding='utf-8').splitlines()
    if target_line_no < 1 or target_line_no > len(lines):
        raise IndexError("target_line_no out of range")
    old = lines[target_line_no-1]
    lines[target_line_no-1] = new_text
    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"Edited {path} line {target_line_no}:\n- old: {old}\n- new: {new_text}")
    return True

def show_diff(a: str, b: str):
    """Return a unified diff between two strings (content)."""
    a_lines = a.splitlines(keepends=True)
    b_lines = b.splitlines(keepends=True)
    diff = difflib.unified_diff(a_lines, b_lines, fromfile='old', tofile='new')
    return ''.join(diff)

def create_branch_worktree(base_repo: str, worktree_dir: str, branch_name: str):
    """Demonstration: print commands to create a worktree and branch."""
    print(f"# Commands to create worktree and branch {branch_name}:")
    print(f"git worktree add {worktree_dir} practice-6-main")
    print(f"cd {worktree_dir} && git checkout -b {branch_name}")

if __name__ == '__main__':
    print('--- Git steps ---')
    print_git_steps()
    # Demonstrate simulate_edit_file (works on local filesystem)
    demo_path = Path('/mnt/data/sample_utils.py')
    if demo_path.exists():
        try:
            simulate_edit_file(demo_path, 10, '# Modified line for duplicate branch demo')
        except Exception as e:
            print('Simulation error:', e)
    else:
        print('Demo file not found at', demo_path)
