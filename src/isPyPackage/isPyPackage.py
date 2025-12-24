#!/usr/bin/env python
import sys
import os
from contextlib import suppress
from Configs.cfg import ini


class Package:
	def isModule(path, *ismod):
		"""
		:param path: full path to the file
		:param ismod: NOT USED : is here to avoid using before assignment exeception
		:return: Bool : True if the path repesents a python module
		"""
		with suppress(IsADirectoryError):
			with open(path, "r") as f:
				ismod = (
					(shebang := f.readline()).startswith("#!") and "python" in shebang
				) or False
		return ismod

	def isPackage(path):
		"""
		:param path: path to test for it being a python package (has __init__.py)
		:return: boolean (true for is package false if not )
		# True if True in [True for item in os.listdir(dirpath) if  item == "__init__.py" ] else False =>>>
		# test = any([True for item in os.listdir(dirpath) if  item == "__init__.py" ]) =>>>
		"""
		return "__init__.py" in os.listdir(path)

	def isParent(path):
		dirs = [
			os.path.join(path, directory)
			for directory in os.listdir(path)
			if os.path.isdir(os.path.join(path, directory))
		]

		return any([Package.isPackage(directory) for directory in dirs])

	def getGitPackageName(path):
		gitfolder = os.path.join(path, ".git")
		gitconfig = ini.readfile(path=gitfolder, name="config", delimiter="=")
		gitconfig = dict(gitconfig['remote "origin"'])
		return os.path.split(gitconfig["url"].removesuffix(".git")[1])

	def find_master():
		"""
		!!! warning breaks when __init__. is in everyfolder of the path up until /  !!!
		gets the folder(path) that is the highest up in the path that still is a python package
		"""
		pathself = sys.argv[0]
		pself = pathself
		parent_dir_pself = os.path.split(pself)[0]
		pdirps = parent_dir_pself
		lst_parent_folders_pself = pdirps.split("/")
		lspath = []
		cur = os.getcwd()
		while len(cur) > 1:
			lspath += [cur]
			split = os.path.split(cur)
			cur = split[0]
			name = split[1]

		for directory in lspath:
			if Package.isPackage(directory):
				pkg = {"Name": os.path.split(directory)[1], "Path": directory}

				if ".git" in os.listdir(directory):
					gitname = Package.getGitPackageName(directory)
					pkg["GitName"] = (gitname,)
				continue
			if Package.isParent(directory):
				master = pkg
				break

		return master


MasterPkg = Package.find_master()


# for index, folder in enumerate(reversed(lst_parent_folders_pself)):
# 	if os.path.exists('/'.join(lst_parent_folders_pself[:(len(lst_parent_folders_pself) - index)])):
# 		for path in ['/'.join(lst_parent_folders_pself[:(len(lst_parent_folders_pself) - index)]):
# 			for package in ([path, package.isPackage(path)]:
# 				result+=package[0]


# return [for package in ([path, package.isPackage(path)] for path in ['/'.join(lst_parent_folders_pself[:(len(lst_parent_folders_pself) - index)]) for index, folder in enumerate(reversed(lst_parent_folders_pself)) if os.path.exists('/'.join(lst_parent_folders_pself[:(len(lst_parent_folders_pself) - index)]))][:-1]) if package[1] == True][-1]
