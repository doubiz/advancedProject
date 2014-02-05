#==============
#Imports
#=============

from xml.dom import minidom
import pyttsx
import os
import subprocess
#==============
#End of Imports
#==============

#==============
# Global Vars
#==============

arr = []
userChoices = []
dialog = []
filled= []
finalans = {}
scripte = []
fileName = "audio.xml"

#===================
# End of Global Vars
#===================
#===============================================
#Giving to the computer a voice to speak with :D
#================================
def onStart(name):
   print 'Im speaking please wait'
def onWord(name, location, length):
   print ''
def onEnd(name, completed):
   print 'Im done please interact with me'
def say(sentence):
	engine = pyttsx.init()
	engine.connect('started-utterance', onStart)
	#engine.connect('started-word', onWord)
	engine.connect('finished-utterance', onEnd)
	engine.say(sentence)
	engine.runAndWait()

#=========================
#End of computer Speaking
#========================

#======================
#Exploring Children
#=====================
def parseItem(nodes):
	retVal = "";
	for node in nodes:
		
		retVal += node.firstChild.data.replace(" ","")+ "/"
	return retVal

def  parseItemArray(nodes):
	retVal = []
	x = nodes.firstChild
	print x.tagName
	retVal.append(x)
	# while x.nextSibling:
	# 	retVal.append(x.nextSibling)
	return retVal
#=========================
#End of Exploring Children
#========================


#==================================
#Printing list of available choices
#==================================
def printChoices(input):
	choices = "Available Choices : "
	fixedInput = input.split("/")
	for i in fixedInput:
		choices = choices + " " + i
	return choices	
#=======================================
#End Printing list of available choices
#=======================================


def parseFields():
	xmldoc = minidom.parse(fileName)
	itemlist = xmldoc.getElementsByTagName('field')
	for s in itemlist :
		fieldItem = []
		isQuestion = ""
		fieldName = s.attributes['name'].value
		try:
			fieldType = s.attributes['type'].value
		except:
			fieldType = ""
		prompt = s.getElementsByTagName('prompt')
		promptMessage = prompt
		item = s.getElementsByTagName('item')
		itemVals = parseItem(item)
		noinput= s.getElementsByTagName('noinput')
		noinputVals = parseItem(noinput)
		nomatch = s.getElementsByTagName('nomatch')
		nomatchVals = parseItem(nomatch)
		fieldItem.append(fieldName)
		fieldItem.append(promptMessage)
		fieldItem.append(itemVals)
		fieldItem.append(noinputVals)
		fieldItem.append(nomatchVals)
		fieldItem.append(fieldType)
		#fieldItem.append(filled)
		#print fieldItem
		arr.append(fieldItem)

def getWelcomeMessage():
	xmldoc = minidom.parse(fileName)
	itemlist = xmldoc.getElementsByTagName('block')
	for s in itemlist:
		x = s.getElementsByTagName("audio")
		if x[0]:
			
			audiofile = x[0].attributes['src'].value
			return_code = subprocess.call(["afplay", audiofile])
			
		else:
			dialog.append(s.firstChild.data)

def getfilled():
	xmldoc = minidom.parse(fileName)
	filledlist = xmldoc.getElementsByTagName('filled')
	for itemlist in filledlist:
		conditiondict = {}
		filledName = itemlist.attributes['namelist'].value
		conditiondict['filledName'] = filledName
		ifcond = itemlist.getElementsByTagName('if')
		prompt = itemlist.getElementsByTagName('prompt')
		if ifcond:
			conditiondict['ifcond'] = True
			m = ifcond[0].childNodes
			
			for x in range(1,len(m)):
				#print "hiiii"
				#print x
				if m[x].nodeType == 3:
					x = x + 1
					continue
				if (m[x].tagName == 'if' or m[x].tagName == 'elseif' and m[x].nodeType == 1):
					#print m[x].nodeType
					condcheck = m[x].attributes['cond'].value.replace(" ","").replace("'","").split("==")[1]
					#print condcheck
					x = x+1
				
				elif (m[x].tagName == 'else'):
					condcheck = 'else'
					x = x+1
				if m[x].nodeType == 3:
					x = x + 1
					continue
				if (m[x].tagName == 'prompt' and m[x].nodeType == 1):
					prompt = m[x].firstChild.data
					if x == 1 :
						condcheck = ifcond[0].attributes['cond'].value.replace(" ","").replace("'","").split("==")[1]
					conditiondict[condcheck] = prompt
					x = x+1
		
		else:
			conditiondict['ifcond'] = False
			
			conditiondict['prompt'] = prompt
		#print conditiondict
		filled.append(conditiondict)
	print filled

def getScript():
	xmldoc = minidom.parse(fileName)
	filledlist = xmldoc.getElementsByTagName('script')
	x = ""
	for f in filledlist:
		for s in f.childNodes:
			x = x + s.data
	scripte.append(x)
	print scripte

	
def evaluateScript(callingScript):
	#calculatePrice(city,travellers)
	#print scripte[0] + "helllooooll"
	boundVariables = ""
	variables = callingScript.split("(")[1].split(")")[0].split(",")
	for v in variables:
		#print v, ", ", finalans[v]
		temp = ""
		try:
		 	int(finalans[v])
		 	temp = finalans[v]
		except:
		 	temp = "'%s'" % finalans[v]	
		boundVariables = boundVariables + temp + ","
	boundVariables += "3"
	#print boundVariables
	finalcall = callingScript.split("(")[0] + "(" + boundVariables + ")" 

	f = open("javapython.txt", "w")
	f.write(scripte[0])
	f.write("\n")
	f.write(finalcall)
	f.flush()
	f.close()
	os.system("javac JavaScriptExecutor.java")
	value = os.system('java JavaScriptExecutor "javapython.txt" "javaoutput.txt"')
	f = open("javaoutput.txt", "r")
	value = f.read()
	f.close()
	print value , "heloo"
	return str(value) 

def retFilled(i):
	for item in filled:
		if arr[i][0] == item['filledName']:
			if item['ifcond']:
				print item[finalans[arr[i][0]]]
				return item[finalans[arr[i][0]]]
			else:
				retText = ""
				for x in item['prompt']:
					for y in x.childNodes:
						if y.nodeType == 3:
							retText = retText + y.data
						elif (y.nodeType == 1 and y.tagName == 'value'):
							expr = y.attributes['expr'].value
							if "(" in expr:
								retText = retText + evaluateScript(expr)
							else:
								retText = retText + finalans[expr]
				print retText
				return retText

def generateQuestion(i):
	fieldName = arr[i][0].split("_")[0]
	fieldPrompt = arr[i][1]
	print fieldPrompt
	retText = ""

	if (fieldName == "confirm"):
		retText = fieldPrompt[0].firstChild.data + " " + userChoices[-1]
	else:
		for x in fieldPrompt[0].childNodes:
			print x 
			if x.nodeType == 3:
				retText = retText + x.data
			elif (x.nodeType == 1 and x.tagName == 'value'):
				expr = x.attributes['expr'].value
				retText = retText + finalans[expr]

	print retText +"retText"
	return retText

def validateAnswer(userInput , i):
	ret = []
	retText = ""
	noinput = arr[i][3]
	nomatch = arr[i][4]

	if (userInput == ""):
		if noinput:
			retText = noinput
		else:
			retText = "no input"
		ret.append(retText)
		ret.append(i)
		return ret

	if(arr[i][5]):
		if(arr[i][5] == 'number'):
			if int(userInput):
				userChoices.append(userInput)
				finalans[arr[i][0]] = userInput
				i = i+1
				ret.append(retText)
				ret.append(i)
				return ret
			else:	
				if nomatch:
					retText = nomatch
				else:
					retText = "please enter a valid number"


	availableChoices = printChoices(arr[i][2]).split(" ")
	if availableChoices:
		if (userInput in availableChoices):	
			if (arr[i][0].split("_")[0] == "confirm" and userInput == "no"):
				i = i-1
				del userChoices[-1]
			else:	
				userChoices.append(userInput)
				finalans[arr[i][0]] = userInput
				i = i+1
			
				
		else:
			if nomatch:
				retText = nomatch
			else:
				retText = "please enter a valid choice"
	else:
		retText = "next promt"
	ret.append(retText)
	ret.append(i)
	return ret

def main():
	getScript()
	getWelcomeMessage()
	if dialog:
		print dialog[0]
		say(dialog[0])
	
	parseFields()
	getfilled()
	i = 0
	while (i < len(arr)):

		say(generateQuestion(i))
	 	choices = printChoices(arr[i][2])
	 	print choices
	 	userInput = raw_input().replace(" ","")

	 	validated = validateAnswer(userInput , i)
	 	if validated[0]:
	 		say(validated[0])
	 	say(retFilled(i))
	 	i = validated[1]
	 	
	#print userChoices
	print finalans

if  __name__ =='__main__':
			main()
