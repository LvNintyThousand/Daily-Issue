import pandas as pd 
import numpy as np 
import random as rm 

def test_initialization_lttype():

	continueTest = True
	while continueTest:
		print("\n")
		test_list = int(input(" \t 你想要考察哪一个list的单词?"))
		print("\n")
		global test_quantity_lttype
		test_quantity_lttype = int(input(" \t 你想要考察多少单词？"))
		if test_quantity_lttype > len(gre["List"+" "+str(test_list)]):
			test_quantity_lttype = len(gre["List"+" "+str(test_list)])
		word_list = rm.choices(population = gre["List"+" "+str(test_list)], k = test_quantity_lttype)

		global indices
		indices = dict()
		for i in word_list:
			indices[i] = gre["List"+" "+str(test_list)].index(i)

		global answers
		answers = dict()
		for i in indices.values():
			answers[i] = gre["Answer"+" "+str(test_list)][i]

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
		print("\t" + "你回答了"+ str(test_quantity_lttype) +"个单词的含义；其中"+ str(scoreGained) +"个正确，"+ str(scoreLost) +"个错误。")
		print("\n")
		continueTest = input("是否继续？")
		if continueTest == "Y" or continueTest == "y" or continueTest == "是":
			continueTest = True
		else:
			continueTest = False

def test_initialization_wltype():
	
	continueTest = True
	while continueTest:
		print("\n")
		test_list = input(" \t 你想要考察哪几个list的单词（请用英文逗号进行划分）?").strip(',')
		global test_list_range
		test_list_range = list(filter(lambda a: a != ",", test_list))

		gre_subset = dict()
		for i in test_list_range:
			gre_subset["List"+" "+str(i)] = gre_index["List"+" "+str(i)]
		gre_flattened = []
		for sublist in gre_subset.values():
			for val in sublist:
				gre_flattened.append(val)

		print("\n")
		global test_quantity_wltype
		test_quantity_wltype = int(input(" \t 你想要考察多少单词？"))
		if test_quantity_wltype > len(gre_flattened):
			test_quantity_wltype = len(gre_flattened)
		word_list = rm.choices(population = gre_flattened, k = test_quantity_wltype)

		global indices
		indices = dict()
		for i in word_list:
			for j in range(0, len(i)):
				if j == 2:
					indices[i[j]] = [i[0], i[1]]

		global answers
		answers = dict()
		for i in indices.keys():
			answers[i] = gre["Answer"+" "+str(indices[i][0])][indices[i][1]]

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
			print("\n" + "\t\t\t\t\t\t\t标准答案是：" + str(answers[i]))
			print("\n")
			usr_scoring = input("回答是否正确（是/否）: ")
			if usr_scoring == "Y" or usr_scoring == "y" or usr_scoring == "是":
				scoreGained += 1
			else:
				scoreLost += 1
			print("\n")
		print("\t" + "你回答了"+ str(test_quantity_wltype) +"个单词的含义；其中"+ str(scoreGained) +"个正确，"+ str(scoreLost) +"个错误。")
		print("\n")
		continueTest = input("是否继续？")
		if continueTest == "Y" or continueTest == "y" or continueTest == "是":
			continueTest = True
		else:
			continueTest = False

def data_initialization():

	gre_original = pd.read_excel("GRE Vocalbuary classified.xlsx",header = 0, encoding = "GB2312")
	gre_original.index = np.arange(1, len(gre_original) + 1)

	global gre
	global gre_index
	gre = dict()
	gre_index = dict()
	for i in gre_original.columns.tolist():
		gre[i] = gre_original[i].dropna(axis = 0, how = "any").tolist()
		gre_index[i] = []
		for j in range(0, len(gre[i])):
			gre_index[i].append([int(i[-1]), j, gre[i][j]])

def test_mode_choices():

	continueMode = True
	while continueMode:
		usr_mode_choice = input("\t请输入你想测试的模式：（单元测试模式 or 综合测试模式）")
		if usr_mode_choice == "单元测试模式":
			test_initialization_lttype()
		elif usr_mode_choice == "综合测试模式":
			test_initialization_wltype()
		continueMode = input("\t是否继续该模式进行测试？")
		if continueMode == "Y" or continueMode == "y" or continueMode == "是":
			continueMode = True
		else:
			continueMode = False

def main():

	print(format("Welcome to CUNY-Baruch Zicklin School of Business gre_original Self-testing Program", "*^116"))
	print(format("Designed by Sezaki Takahiro, version 1.2.0", "-^116"))
	print("\n")
	data_initialization()
	test_mode_choices()

main()
