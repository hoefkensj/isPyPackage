#!/usr/bin/env python

yellow=[255,255,0]
red=[255,0,0]
reset='\x1b[m'
def rgb(color,string,last=[0,0,0]):
	ansi='\x1b[38;2;{};{};{}m'
	c=ansi.format(*color)
	result='{C}{S}{R}'.format(C=c,S=string,R=reset)
	last=c
	return result