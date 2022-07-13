import re
import json
import pandas as pd
import statistics
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def createSublistForFinallist(name, definition, associations, emotionality):
    """
    This function takes a pseudoword, the definition, the associations and the emotionality (emo or neu)
    and returns a list containing this data.

    Parameters:
    -----------
    name : str
       Contains the pseudoword.
    definition : str
        Contains definition of pseudoword.
    associations : list
        Contains list of associations of the pseudoword.
    emotionality : str
        Contains whether pseudoword is neutral or emotional.
   
    
    Returns:
    --------
    sublist : list
       Contains name, definition, associations and emotionality of the pseudoword. 
    """
    sublist = []

    sublist.append(name)
    sublist.append(emotionality)
    sublist.append(definition)
    sublist.append(associations)

    return sublist

def getBestPercentage(all_indices, topindices):
    bestIx = 0

    for ix in all_indices:

        if ix <= topindices:

            bestIx += 1
    
    return round(bestIx*100/len(all_indices), 0)


def addToChainSublist(sublist, k, all_indices, overallLength, average_index, all_scores, average_score):
    """
    This function takes the number of participants, all indices for the associations of the pseudoword,
    the overall number of all indices, the average index, all scores for the associations of the pseudoword and the average score
    and adds this data to the sublist.

    Parameters:
    -----------
    sublist : list
       Contains the pseudoword.
    k : int
        Contains definition of pseudoword.
    all_indices : list
        Contains list of associations of the pseudoword.
    overallLength : str
        Contains whether pseudoword is neutral or emotional.
    average_index : int
        Contains 
    all_scores : list
        
    average_score : int
   
    
    Returns:
    --------
    sublist : list
       Contains name, definition, associations and emotionality of the pseudoword. 
    """
    flat_list = [el for el in all_indices[0]]
    flat_list.sort()
    sublist.append(k)   
    sublist.append(all_indices[0])
    sublist.append(flat_list)
    sublist.append(int(sum(all_indices[0])/len(all_indices[0])))
    medianIndex = statistics.median(flat_list)
    sublist.append(medianIndex)
    sublist.append(getBestPercentage(flat_list, topindices=98))
    sublist.append(overallLength)
    sublist.append(all_scores[0])
    sublist.append(sum(all_scores[0])/len(all_scores[0]))

    return sublist



def getJsonZeroshot(filename):
    """
    This function takes a pseudoword, the definition, the associations and the emotionality (emo or neu)
    and returns a list containing this data.

    Parameters:
    -----------
    filename : str
        Contains the name of the file.
   
    
    Returns:
    --------
    Returns a json object containing the zero shot output of the model.
    """

    zero_shot_results = open(filename)

    return json.load(zero_shot_results)


def createCSVFile(finallist, overallAvgScore):

    df = pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Definition', 'Features', 'Anzahl Teilnehmer', 'Index der Scores', 'geordnete Indizes', 'Durchschnittsindex', 'Medianindex', 'unter Top 10 Prozent', 'Insgesamte Anzahl der Indizes', 'Scores', 'Durchschnittsscore'])
    df['Gesamtdurchschnittsscore'] = [overallAvgScore]*len(finallist)

    df.to_csv("getIndexMasked.csv", sep='\t', encoding='utf-8')   # HIER CONFIG EINFÜGEN



def getIndexinZeroShot(indices, scores, averageIndex, averageScore, association, zeroshotAssociation, zeroshotScores, k):

    k = 0
    overallAssociations = len(zeroshotAssociation)

    for el in association:


        index = zeroshotAssociation.index(el)
        indices.append(index)

        score = zeroshotScores[index]
        scores.append(score)

        averageIndex += index
        averageScore += score
        k += 1

    return indices, scores, averageIndex, averageScore, k, overallAssociations



def createListForCsvFile(featuresFile, name_emo, name_neu, generated_emo, generated_neu, splitted):

    finallist = []

    for i in range(len(name_emo)):

        name = name_emo[i]

        tmp_associations_emo = []

        generatedEmo = generated_emo[i]


        name_rows = featuresFile.loc[featuresFile['word'] == name]

        for j in name_rows.index:

            if str(name_rows["emotionality"][j]) == "emo":

                if splitted == False:

                    cleanAsso = re.sub(r'\s*\+\s*', ', ', str(name_rows['features'][j]))
                    tmp_associations_emo.append(cleanAsso)
                
                else: 
                    tmp_associations_emo.append(str(name_rows['features'][j]))

            
        if tmp_associations_emo != []:
            finallist.append(createSublistForFinallist(name, generatedEmo, tmp_associations_emo, emotionality='emo'))
        


    for i in range(len(name_neu)):

        name = name_neu[i]
        generatedNeu = generated_neu[i]
        
        tmp_associations_neu = []

        name_rows = featuresFile.loc[featuresFile['word'] == name]

        for j in name_rows.index:

            if str(name_rows["emotionality"][j]) == "neu":

                if splitted == False:

                    cleanAsso = re.sub(r'\s*\+\s*', ', ', str(name_rows['features'][j]))
                    tmp_associations_neu.append(cleanAsso)

                else: 
                    tmp_associations_neu.append(str(name_rows['features'][j]))

        if tmp_associations_neu != []:
            finallist.append(createSublistForFinallist(name, generatedNeu, tmp_associations_neu, emotionality='neu'))
    
    with open("finallist.json", "w") as fl:
        json.dump(finallist, fl)
    
    return finallist




def ZeroShotChainResultToFile(finallist):
    zeroShotResults = getJsonZeroshot("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\BERT Daten\\TemporaereDaten\\zero_shot_english_masked_emo.json") 
    zeroShotResults2 = getJsonZeroshot("C:\\Users\\laris\\Desktop\\GitHub\\bachelor-thesis\\Daten\\BERT Daten\\TemporaereDaten\\zero_shot_english_masked_neu.json")
    finalzeroshot = []
    for i in range(len(zeroShotResults)):
        finalzeroshot.append(zeroShotResults[i])
        finalzeroshot.append(zeroShotResults2[i])
    

        

    overall_avg_score = 0

    for sublist in finallist:

        all_indices = []
        all_scores = []
        averageIndex = 0
        averageScore = 0
        anzahlProbanden = 0
        overallLength = 0


        for i in range(len(finalzeroshot)):

            indices = []
            scores = []
            k = 0
            
        
            zeroshot = list(finalzeroshot[i].values())
        

            itemsWithSameGeneratedAssosiation = []

            for zeroshotsub in finalzeroshot:
                if list(zeroshotsub.values())[0] == sublist[2]:
                    itemsWithSameGeneratedAssosiation.append(list(zeroshotsub.values()))
            
            if len(itemsWithSameGeneratedAssosiation) > 1:
                index = -1
                for items in itemsWithSameGeneratedAssosiation:
                    if all(x in items[1] for x in sublist[3]):
                        index = itemsWithSameGeneratedAssosiation.index(items)

                zeroshot = itemsWithSameGeneratedAssosiation[index]


            schoneinmal = False
            if zeroshot[0] == sublist[2] and schoneinmal == False:

                anzahlProbanden = len(sublist[3])
                indices, scores, averageIndex, averageScore, k, overallAssociations = getIndexinZeroShot(indices, scores, averageIndex, averageScore, sublist[3], zeroshot[1], zeroshot[2], k)

                all_indices.append(indices)
                all_scores.append(scores)
                averageIndex = int(averageIndex / len(all_indices[0]))
                averageScore = averageScore / len(all_scores[0])
                overallLength = overallAssociations
                schoneinmal = True


        sublist = addToChainSublist(sublist, anzahlProbanden, all_indices, overallLength, averageIndex, all_scores, averageScore)

        overall_avg_score += averageScore

    overall_avg_score = overall_avg_score/(len(finallist))

    createCSVFile(finallist, overall_avg_score)





zero_shot_results = open(config['PATHS']['unmasked_en'])
generated = json.load(zero_shot_results)



generated_emo = []
generated_neu = []
name_emo = []
name_neu = []

for dict in generated:

    if "emotional" in list(dict.keys())[0]:

        generated_text = list(dict.values())[0]
        print(generated_text)
        name_emo.append(list(dict.keys())[0].split(",")[0])
        string = ""
        for asso in generated_text:
            string = string + asso.strip() + ", "

        generated_emo.append(string[:-2])

    if "neutral" in list(dict.keys())[0]:

        generated_text = list(dict.values())[0]
        name_neu.append(list(dict.keys())[0].split(",")[0])
        string2 = ""
        for asso2 in generated_text:
            string2 = string2 + asso2.strip() + ", "
        generated_neu.append(string2[:-2])


featuresFile = pd.read_csv(config['PATHS']['TranslatedFeatures'], sep='\t', usecols=[1, 2, 3, 6], encoding="utf-8")   # HIER CONFIG EINFÜGEN

result=createListForCsvFile(featuresFile, name_emo, name_neu, generated_emo, generated_neu, splitted=False)
ZeroShotChainResultToFile(result)