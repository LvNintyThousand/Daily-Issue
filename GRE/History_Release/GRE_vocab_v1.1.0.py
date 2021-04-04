import pandas as pd 
import numpy as np 
import random as rm 

gre = pd.read_excel("GRE Vocalbuary classified.xlsx",header = 0, encoding = "GB2312")
gre.index = np.arange(1, len(gre) + 1)

def test_initialization_lttype():
	print(format("Welcome to CUNY-Baruch Zicklin School of Business GRE Self-testing Program", "*^116"))
	print(format("Designed by Sezaki Takahiro, version 1.2.0", "-^116"))
	print("\n")
	test_list = int(input(" \t 你想要考察哪一个list的单词?"))
	print("\n")
	global test_quantity
	test_quantity = int(input(" \t 你想要考察多少单词？"))
	if test_quantity > len(gre.index):
		test_quantity = len(gre.index)
	word_list = rm.choices(population = gre["List"+" "+str(test_list)].dropna(axis = 0, how = "any"), k = test_quantity)
	
	print(word_list)

	global indices
	indices = dict()
	for i in word_list:
		indices[i] = np.where(gre["List"+" "+str(test_list)]== i)[0].tolist()[0]

	global answers
	answers = dict()
	for i in indices.values():
		answers[i] = gre.at[i+1, "Answer"+" "+str(test_list)]

	return indices, answers

def test_procedure_lttype():
	continueTest = True
	while continueTest:
		global scoreGained
		scoreGained = 0
		global scoreLost
		scoreLost = 0
		print("\n")
		print("\t" + "请回答以下各个单词的中文含义是什么:" + "\n")
		for i in indices.keys():
			print("\t" + i + "\t")
			print("\n")
			usr_answer = input("\t" +"中文含义: \t")
			print("\n" + "\t\t\t\t\t\t\t标准答案是：" + str(answers[indices[i]]))
			print("\n")
			usr_scoring = input("回答是否正确（是/否）: ")
			if usr_scoring == "Y" or usr_scoring == "y" or usr_scoring == "是":
				scoreGained += 1
			else:
				scoreLost += 1
			print("\n")
		print("\t" + "你回答了"+ str(test_quantity) +"个单词的含义；其中"+ str(scoreGained) +"个正确，"+ str(scoreLost) +"个错误。")
		print("\n")
		continueTest = input("是否继续？")
		if continueTest == "Y" or continueTest == "y" or continueTest == "是":
			continueTest = True
		else:
			continueTest = False

test_initialization_lttype()
test_procedure_lttype()

