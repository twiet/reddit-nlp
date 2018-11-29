import os
from math import log

StopTrainingLine = 200000
TrainingPath = './Probabilities.py'
ContentsDir = './contents'
LabelsDir = './labels'

def Learn():
	labels = {}
	labelsOrdered = {}
	totalCount = 0
	for name in os.listdir(LabelsDir):
		path = os.path.join(LabelsDir, name)
		suffix = name.split('.')[1]
		labelsOrdered[suffix] = []
		with open(path, 'r') as fd:
			fd.readline()
			for lineNumber, line in enumerate(fd):
				if lineNumber > StopTrainingLine:
					break
				label = line.strip() # remove new lines
				label = label.lower() # lexicalize
				count = labels.get(label, 0)
				count += 1
				totalCount += 1
				labels[label] = count
				labelsOrdered[suffix].append(label)

	labelProbabilities = {}
	for label in labels:
		labelProbabilities[label] = -1 * log(float(labels[label]) / float(totalCount))
	types = {}
	wordProbabilities = {key: [{}, 0] for key in labelProbabilities}
	for name in os.listdir(ContentsDir):
		path = os.path.join(ContentsDir, name)
		suffix = name.split('.')[1]
		with open(path, 'r') as fd:
			for lineNumber, line in enumerate(fd):
				if lineNumber > StopTrainingLine:
					break
				label = labelsOrdered[suffix][lineNumber]
				wordsGivenLabel = wordProbabilities[label][0]
				lineOfTokens = line.strip().split(' ')
				for token in lineOfTokens:
					if token not in types:
						types[token] = True
					token = token.lower() # lexicalize
					count = wordsGivenLabel.get(token, 0)
					wordsGivenLabel[token] = count + 1
					wordProbabilities[label][1] += 1

	typeCount = len(types.keys())
	for label in wordProbabilities:
		totalWordsInLabel = wordProbabilities[label][1]
		wordsGivenLabel = wordProbabilities[label][0]
		for word in wordsGivenLabel:
			wordsGivenLabel[word] = -1 * log(float(wordsGivenLabel[word] + 1) / 
											 float(totalWordsInLabel + typeCount + 1))
	with open(TrainingPath, 'w') as fd:
		fd.write('TypeCount = {}\n'.format(typeCount))
		fd.write('WordProbabilities = {}'.format(wordProbabilities))

def CheckClassification(correctLabel, generatedLabel, correctDict, trueTotals, guessedTotals):
	if correctLabel == generatedLabel:
		count = correctDict.get(correctLabel, 0)
		correctDict[correctLabel] = count + 1
	count = trueTotals.get(correctLabel, 0)
	trueTotals[correctLabel] = count + 1
	count = guessedTotals.get(generatedLabel, 0)
	guessedTotals[generatedLabel] = count + 1

def PrintEvaluation(prefix, correct, trueTotals, guessedTotals):
	print "{} RESULTS".format(prefix)
	precisionsSum = 0
	recallsSum = 0
	f1Sum = 0
	weightedPSum = 0
	weightedRSum = 0
	weightedF1Sum = 0
	for label in sorted(trueTotals.keys()):
		print label
		try:
			precision = float(correct.get(label, 0)) / float(guessedTotals[label])
		except KeyError: # label was never guessed
			precision = float(0)
		recall = float(correct.get(label, 0)) / float(trueTotals[label])
		f1 = (precision + recall) / 2.0
		print 'Samples: {}'.format(trueTotals[label])
		print 'Precision: {}'.format(precision) 
		print 'Recall: {}'.format(recall)
		print 'F1: {}'.format(f1)
		precisionsSum += precision
		recallsSum += recall
		f1Sum += f1

		weightedPSum += precision * trueTotals[label]
		weightedRSum += recall * trueTotals[label]
		weightedF1Sum += f1 * trueTotals[label]
		print 
	print 'UNWEIGHTED {} AVERAGES'.format(prefix)
	numCategories = len(trueTotals.keys())
	print 'Precision: {}'.format(precisionsSum / numCategories)
	print 'Recall: {}'.format(recallsSum / numCategories)
	print 'F1: {}'.format(f1Sum / numCategories)

	totalSamples = 0
	for label in trueTotals:
		totalSamples += trueTotals[label]
	print 'WEIGHTED {} AVERAGES'.format(prefix)
	numCategories = len(trueTotals.keys())
	print 'Precision: {}'.format(weightedPSum / totalSamples)
	print 'Recall: {}'.format(weightedRSum / totalSamples)
	print 'F1: {}'.format(weightedF1Sum / totalSamples)	

def Evaluate():
	from Probabilities import WordProbabilities, TypeCount
	
	trainClassifications = []
	testClassifications = []
	for name in os.listdir(ContentsDir):
		path = os.path.join(ContentsDir, name)
		with open(path, 'r') as fd:
			for lineNumber, line in enumerate(fd):
				if lineNumber <= StopTrainingLine:
					classifications = trainClassifications
				else:
					classifications = testClassifications
				lineOfTokens = line.strip().split(' ')
				classification = ''
				bestWeight = None
				for label in WordProbabilities:
					wordsGivenLabel = WordProbabilities[label][0]
					totalWordsInLabel = WordProbabilities[label][1]
					weight = 0

					for token in lineOfTokens:
						token = token.lower() # lexicalize
						if token not in wordsGivenLabel:
							score = -1 * log(float(1) / float(TypeCount + totalWordsInLabel + 1))
						else:
							score = wordsGivenLabel[token]
						weight += score
					if bestWeight == None or weight < bestWeight:
						bestWeight = weight
						classification = label
				classifications.append(classification)

	trainCorrect = {}
	trueTrainTotals = {}
	guessedTrainTotals = {}
	testCorrect = {}
	trueTestTotals = {}
	guessedTestTotals = {}
	testIndex = 0
	for name in os.listdir(LabelsDir):
		path = os.path.join(LabelsDir, name)
		with open(path, 'r') as fd:
			fd.readline()
			for lineNumber, line in enumerate(fd):
				label = line.strip()
				if lineNumber < StopTrainingLine:
					CheckClassification(label, trainClassifications[lineNumber], trainCorrect, 
										trueTrainTotals, guessedTrainTotals)
				else:
					CheckClassification(label, testClassifications[testIndex], testCorrect, 
										trueTestTotals, guessedTestTotals)
					testIndex += 1

	# print "TRAINING RESULTS"
	# precisionsSum = 0
	# recallsSum = 0
	# f1Sum = 0
	# for label in sorted(trueTrainTotals.keys()):
	# 	print label
	# 	try:
	# 		precision = float(trainCorrect.get(label, 0)) / float(guessedTrainTotals[label])
	# 	except KeyError: # label was never guessed
	# 		precision = float(0)
	# 	recall = float(trainCorrect.get(label, 0)) / float(trueTrainTotals[label])
	# 	f1 = (precision + recall) / 2.0
	# 	print 'Precision: {}'.format(precision) 
	# 	print 'Recall: {}'.format(recall)
	# 	print 'F1: {}'.format(f1)
	# 	precisionsSum += precision
	# 	recallsSum += recall
	# 	f1Sum += f1
	# 	print 
	# print 'TRAINING AVERAGES'
	# numCategories = len(trueTrainTotals.keys())
	# print 'Precision: {}'.format(precisionsSum / numCategories)
	# print 'Recall: {}'.format(recallsSum / numCategories)
	# print 'F1: {}'.format(f1Sum / numCategories)
	PrintEvaluation('TRAINING', trainCorrect, trueTrainTotals, guessedTrainTotals)
	print
	PrintEvaluation('TEST', testCorrect, trueTestTotals, guessedTestTotals)

	

if __name__ == '__main__':
	import sys

	args = sys.argv[1:]
	if args[0] == 'learn':
		Learn()
	elif args[0] == 'evaluate':
		Evaluate()
	else:
		print "bad args"