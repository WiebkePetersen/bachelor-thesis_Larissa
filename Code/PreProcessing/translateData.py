from deep_translator import GoogleTranslator
import pandas as pd
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')



def TranslateText(text):
    return GoogleTranslator(source='auto', target='en').translate(text)


def translatedDataToFile(file, definitions:bool):
  
    tmpData = []
    for i in range(len(file)):
        
        if definitions == True:
            emoDefinition = TranslateText(file['Konzept '][i]).lower()
            neuDefinition = TranslateText(file['N_Konzept'][i]).lower()

            tmpData.append([file['Name'][i], emoDefinition, neuDefinition])
            filename = config['PATHS']['TranslatedDefinitions']
            columns = ['word','Konzept ', 'N_Konzept']
        
        else:
            association = TranslateText(file['features'][i]).lower()
            tmpData.append([file['VP_Code'][i], file['word'][i], file['emotionality'][i], file['definition'][i], file['group'][i], association])
            filename = config['PATHS']['TranslatedFeatures']
            columns=['VP_Code','word', 'emotionality', 'definition', 'group', 'features']
    

    translatedDefinitions = pd.DataFrame(tmpData, columns=columns)
    translatedDefinitions.to_csv(filename, sep='\t', encoding='utf-8')



if __name__ == "__main__":

    featuresFile = pd.read_csv(config['PATHS']['newData'], sep='\t', usecols=[1, 2, 3, 4, 5, 6], encoding="utf-8")
    definitionsFile = pd.read_excel(config['PATHS']['RatingDefinitionen'], usecols=[0,1,8])

    translatedDataToFile(featuresFile, definitions=False)
    #translatedDataToFile(definitionsFile, definitions=True)