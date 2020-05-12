#!/usr/bin/env python
import subprocess, shutil, os, glob

# System command and retrieval of its output
def system(command):
  try:
    return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    print e.output

# Move the newly run files as the new reference
for file in glob.glob('rootfiles/*AOD.root'):
  shutil.move(file, file.replace('AOD.root', 'AOD_ref.root'))

# Commit to git
system('git add rootfiles/*AOD_ref.root')
system('git add log/*.log')
system('git commit -m"New test run finished"')
