import sys
import re
dict_fname=''.join(sys.argv[1])
rules_fname=''.join(sys.argv[2])
test_fname=''.join(sys.argv[3])
finalResults=[]
#------------------------------------------------------------------------------------------------------------------
def calFileLen(rules_fname):
	count=0
	with open(rules_fname) as doc:
		for line in doc:
			count+=count
	return count
#------------------------------------------------------------------------------------------------------------------	
def readWords(test_words):
	with open(test_fname) as doc:
		for line in doc:
			first=line.split()
			test_words.append([''.join(first).lower()])
	return test_words
#------------------------------------------------------------------------------------------------------------------			
def readRules(rule_book):
	with open(rules_fname) as doc:
		for line in doc:
			templist=re.findall(r"[\w-]+",''.join(line))   
			del templist[4]   
			templist.extend('F')
			rule_book.append(templist)
	return rule_book
#-------------------------------------------------------------------------------------------------------------------
def readDict(dict_words):
	with open(dict_fname) as doc:
		for line in doc:
			first=line.split()
			word=first[0].lower()
			if(word in dict_words):
				rest=first[1:]
				dict_words[word].extend(rest)
			if word not in dict_words:	
				rest=first[1:]
				dict_words[word]=rest
	return dict_words
#-----------------------------------------READ DICTIONARY---------------------------------------------------
dictionary_words={}
dictionary_words=readDict(dictionary_words)
#-----------------------------------------READ RULES--------------------------------------------------------
rule_book=[]
rule_book=readRules(rule_book)
#-----------------------------------------READ TEST DATA----------------------------------------------------
test_words=[]
test_words=readWords(test_words)
#-----------------------------------------REMOVE SUFFIX----------------------------------------------------
def removeSuffix(derive,suff,replacement):
	last=len(suff)
	wordlength=len(derive)
	derive=derive[:wordlength-last]
	if(replacement.isalpha()):
		derive=derive+replacement
	return derive
#-----------------------------------------REMOVE PREFIX---------------------------------------------------
def removePrefix(derive,pref,replacement):
	last=len(pref)
	wordlength=len(derive)
	derive=derive[last:]
	if(replacement.isalpha()):
		derive=replacement+derive
	return derive
#-----------------------------------------IF FOUND IN DICTIONARY WORDS---------------------------------------------------
def found_in_dictionary(original,posOrg,sample,firstLookUp):
	w=original
	pos=posOrg
	if 'ROOT' in dictionary_words[sample]:
		rootindex=dictionary_words[sample].index('ROOT')
		root=dictionary_words[sample][rootindex+1]
	else:
		root=sample

	if firstLookUp:
		source="Dictionary"
	else:
		source="Morphology"
	result=[w+" ",pos+" ","ROOT="+root+" ","SOURCE="+source]
	duplicate=True
	for i in finalResults:
		if result[0]==i[0] and result[1]==i[1]:
			duplicate=False

	if duplicate:
		finalResults.append(result)
#-----------------------------------------CHECK IF WORKS----------------------------------------------------
def checkIfWorks(testSample,index,i,temp_to_check):
	if testSample in dictionary_words:
		finalLength=len(test_words[index])-1
		if test_words[index][finalLength] in dictionary_words[testSample]:
			found_in_dictionary(test_words[index][0],''.join(i[4]),testSample,False)
	else:
		applyRules(testSample,index,temp_to_check)
#-----------------------------------------IF NOT FOUND IN DICTIONARY WORDS-----------------------------------
def applyRules(sample,index):
	in_rule_book=bool(1)
	for i in rule_book:
		if i[0]=='SUFFIX' and sample.endswith(i[1]) and i[5]=='F' and temp_to_check==i[3]:
			i[5]='T'
			in_rule_book=bool(0)
			test_words[index].append(i[4])
			test_words[index].append(i[3])
			derive_sample=removeSuffix(sample,i[1],i[2])
			checkIfWorks(derive_sample,index,i,i[3]) 
	
		elif i[0]=='PREFIX' and sample.startswith(i[1]) and i[5]=='F' and temp_to_check==i[3]:
			i[5]='T'
			in_rule_book=bool(0)
			test_words[index].append(i[4])
			test_words[index].append(i[3])
			derive_sample=removePrefix(sample,i[1],i[2])
			checkIfWorks(derive_sample,index,i,i[3])
		else:
			derive_sample=sample
	return derive_sample,in_rule_book
#-----------------------------------------START DERIVING----------------------------------------------------
for elements in test_words:
	for a in rule_book:
		a[5]='F'
	sample=''.join(elements[0])
	indexOfSample=test_words.index(elements)
	if sample in dictionary_words:
		found_in_dictionary(sample,''.join(dictionary_words[sample][0]),sample,True)
	else:
		derived_sample, in_rule_book=applyRules(sample,indexOfSample)
		if derived_sample == sample and in_rule_book:
			print(''.join([sample+" ","noun ","ROOT="+sample+" ","SOURCE=default"]))

for i in finalResults:
	print ''.join(i)
	