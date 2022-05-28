from scipy.stats.stats import pearsonr
import pandas as pd
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


sia = pd.read_csv(config['PATHS']['SentimentScoreFeatures'], sep='\t', usecols=[1,2,3,4,5,6], encoding="utf-8")
valence = pd.read_csv(config['PATHS']['valence'], sep=',', encoding="latin-1")


names = ['Wunicher', 'Neif', 'Zimerhubst', 'Zwelde', 'Herklögen', 'Preier', 'Muschürdur', 'Ismiprämpf', 'Glühm', 'Rugliebast',
'Wumeizauch', 'Häugnung', 'Wupforau', 'Bismirbiel', 'Enkmitas', 'Mege', 'Faube', 'Odef', 'Skibt', 'Mölauzegt', 'Troff', 
'Bingsemöl', 'Ferandsor', 'Struk', 'Vul', 'Namistell', 'Weforshank', 'Plüpp', 'Bisknirgo', 'Iberletsch']
finallist = []

for name in names:

    name_rows = sia.loc[sia['Wort'] == name]
    name_rows2 = valence.loc[valence['word'] == name]
    value1Emo = []
    value2Emo = []
    value1Neu = []
    value2Neu = []

    for j in name_rows.index:
        
        for k in name_rows2.index:

            if sia['Emotionalität'][j] == 'emo' and valence['code'][k] == 'emo' and sia['VP_Code'][j] == valence['VP_Code'][k] and valence['time'][k] == 'post':

                value1Emo.append(sia['Sentiment Score'][j])
                value2Emo.append(valence['valence_rating'][k])
            
            if sia['Emotionalität'][j] == 'neu' and valence['code'][k] == 'neu' and sia['VP_Code'][j] == valence['VP_Code'][k] and valence['time'][k] == 'post':

                value1Neu.append(sia['Sentiment Score'][j])
                value2Neu.append(valence['valence_rating'][k])

    finallist.append([name, 'emo', value1Emo, value2Emo, pearsonr(value1Emo, value2Emo)])
    finallist.append([name, 'neu', value1Neu, value2Neu, pearsonr(value1Neu, value2Neu)])

df = pd.DataFrame(finallist, columns=['Wort', 'Emotionalität', 'Sentiment Score', 'Valence Rating', 'Korrelation'])

interpretation = []

for i in range(len(df)):

    if df['Korrelation'][i][0] > 0.66 or df['Korrelation'][i][0] < -0.66:
        interpretation.append('strong')
    if df['Korrelation'][i][0] < 0.66 and df['Korrelation'][i][0] > 0.33:
        interpretation.append('moderate')
    if df['Korrelation'][i][0] > -0.66 and df['Korrelation'][i][0] < -0.33:
        interpretation.append('moderate')
    else:
        interpretation.append('weak')

df['Interpretation'] = interpretation

df.to_csv(config['PATHS']['KorrelationSiaValence'], sep='\t', encoding='utf-8')





""" 
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import numpy as np

a = [0.1779, 0.8248, -0.4404, 0.2023, -0.7506, 0.5171, 0.9612, 0.7003, -0.3182, -0.5033, 0.0, -0.6369, -0.2023, 0.836, 0.9477, -0.743, -0.9423, -0.9287, -0.2732, 0.7184, -0.1027, -0.6597, 0.9786, -0.8519, 0.8779, 0.3818, -0.8979, -0.8885, 0.9274, -0.8442, 0.0516, -0.5423, 
0.0, -0.6369, 0.3612, 0.1027, -0.5136, -0.9081, 0.0, 0.6908, 0.6597, 0.5267, 0.7648, 0.4404, 0.0, -0.836, -0.296, -0.4404, 0.4588, -0.7623, 0.8934, 0.0, 0.9118, 0.7269, -0.1446, 0.9136, 0.4215, -0.8316, 0.0258, -0.8689, 0.4019, -0.4588, -0.5423, 0.802, -0.2732
,0.5994, 0.25, 0.4404, 0.6486, 0.4588, -0.6369, -0.4106, -0.872, 0.8225, 0.7351, 0.743, 0.0, 0.7906, 0.9451, -0.8176, -0.5574, 0.8126, -0.7003, -0.128, -0.9022, -0.8176, -0.128, 0.6808, 0.9382, 0.0, 0.836, 0.128, 0.2732, 0.872, -0.836, 0.5994, 0.8658, 0.926
,0.1531, -0.8225, 0.926, -0.1531, -0.3246, 0.5267, 0.2732, 0.7269, 0.7845, -0.1779, -0.872, 0.5574, 0.1027, -0.2023, 0.5719, -0.6808, -0.8979, -0.3182, 0.0, 0.4215, -0.5859, -0.7506, -0.9201, 0.8807, -0.128, 0.93, 0.8481, 0.7506, 0.7717, -0.8519, 0.5994, 0.25, -0.836
,0.7717, 0.1779, 0.7717, -0.6908, -0.3612, 0.2263, -0.9136, 0.0, 0.6369, -0.0516, 0.0, 0.802, -0.9287, 0.7906, 0.9661, -0.3818, 0.9482, 0.7506, -0.8807, 0.6249, 0.6124, -0.6124, 0.2263, 0.5859, 0.6597, -0.8481, -0.6486, 0.6486, -0.765, 0.7351, -0.8935, -0.765
,0.9231, 0.9022, -0.5994, -0.6249, 0.8779, 0.9118, -0.2023, 0.8807, -0.93, 0.0, 0.0, 0.4939, 0.8834, -0.25, 0.0, -0.6249, 0.25, 0.7269, 0.5106, -0.836, 0.0, -0.8271, -0.8176, 0.8934, -0.6588, -0.3182, 0.6597, 0.7269, -0.8934, -0.7101, 0.3818, 0.7964
,-0.6124, -0.128, -0.3182, -0.5859, 0.7351, 0.8834, 0.9686, 0.2878, -0.4019, 0.8442, -0.946, 0.7906, -0.7269, 0.1779, 0.0, 0.34, -0.7269, -0.9683, 0.765, 0.4215, 0.9274, -0.91, -0.5267, -0.891, -0.3612, 0.8807, 0.9468, 0.6369, 0.3818, 0.93, -0.7579, -0.9022, -0.3818
,-0.5267, 0.9062, 0.6486, -0.9246, -0.8316, 0.0772, 0.2023, -0.4215, 0.9371, 0.6124, 0.8176, 0.8074, -0.872, 0.0, 0.886, 0.8555, 0.2263, 0.6124, 0.8442, 0.34, 0.8979, 0.8957, 0.7964, -0.3182, 0.7579, 0.296, 0.9485, -0.4019, 0.765, 0.8176, 0.0, 0.7579
,-0.6597, -0.4588, -0.7308, 0.0516, -0.6705, -0.4063, -0.6597, 0.9169, -0.4767, -0.1779, 0.0, 0.7964, -0.6908, 0.34, -0.7845, -0.9042, -0.9289, -0.9001, 0.8074, 0.6705, 0.8658, -0.8689, 0.6597, -0.7269, 0.9186, -0.8625, -0.0772, -0.5379, -0.8555, 0.8225, -0.6249, 0.9538
,0.6486, 0.2732, -0.6124, -0.8625, 0.959, 0.9118, 0.4767, 0.9442, 0.743, 0.8555, 0.891, -0.3818, 0.0, 0.9403, 0.0, 0.2732, 0.8885, 0.5106, -0.4215, 0.936, 0.5267, -0.2732, -0.7688, 0.1531, -0.0516, -0.4922, 0.7506, -0.9186, -0.4404, 0.7184, -0.6249, 0.0, 0.9432
,0.5574, -0.4404, -0.8979, 0.3818, 0.7003, 0.2732, 0.9485, -0.2263, 0.0, 0.7291, 0.5574, 0.91, 0.765, 0.8176, 0.7783, 0.8966, 0.9776, -0.802, 0.7845, 0.802, -0.34, 0.9274, 0.6486, 0.6705, -0.836, -0.8074, 0.7964, 0.4404, -0.7096, 0.9042, 0.0
,0.0, 0.296, -0.9287, -0.6808, 0.5574, 0.8481, 0.5719, 0.9531, 0.743, -0.6705, 0.25, -0.4449, -0.1531, -0.7351, 0.4588, -0.4019, -0.4404, -0.1027, 0.8402, -0.9493, 0.4404, -0.9726, 0.6808, -0.296, 0.5719, 0.9022, 0.875, 0.9524, 0.7269, 0.4973, 0.0, 0.6808, 0.0
,0.0258, -0.9607, -0.0772, -0.875, 0.6908, 0.921, 0.34, 0.8591, 0.9217, 0.34, 0.6369, -0.0258, 0.9153, 0.875, 0.9001, -0.296, 0.886, 0.3818, 0.8934, 0.9423, 0.6808, 0.8402, 0.4767, -0.4449, -0.128, 0.0, 0.8126, -0.4939, 0.4588, 0.9287, 0.9169, -0.9022
,-0.0258, 0.1774, 0.9081, -0.2263, 0.4019, 0.9382, 0.9628, 0.0, 0.802, -0.8834, 0.7783, 0.8979, 0.0, 0.5574, 0.0, 0.25, 0.7096, 0.3182, -0.5719, 0.7269, 0.8779, -0.8555, -0.9669, 0.9153, -0.6249, 0.9468, 0.5859, 0.4215, -0.5106, -0.4215, -0.5106, -0.5267, 0.8074
,0.34, 0.6369, 0.5574, 0.9442, 0.6124, -0.7455, 0.7717, 0.7269, 0.0, 0.9326, 0.3612, -0.3612, -0.2263, -0.7096, -0.8658, 0.1877, 0.8934, -0.9325, 0.6908, 0.0772, 0.7474, 0.9001, 0.8591, -0.4998, 0.9633, 0.9682, 0.9478, -0.0475, -0.4767, 0.3612, 0.2732, -0.5106
,-0.3818, 0.0258, 0.8225, -0.9154, 0.6808, -0.7579, 0.875, 0.34, 0.802, -0.4404, 0.9628, 0.7096, 0.4019, 0.8442, -0.4588, 0.4404, 0.9612, 0.128, 0.7579, 0.9231, -0.7717, 0.802, -0.8934, 0.872, 0.9246, 0.8555, -0.8402, 0.8807, 0.4767, -0.6705, -0.7351, 0.1027, 0.4588
,0.9287, 0.5719, 0.9186, 0.9517, 0.9538, -0.7717, -0.34, 0.0516, -0.836, -0.9633, 0.4404, 0.0, -0.6908, -0.5423, -0.0516, -0.765, 0.9825, 0.296, -0.8126, 0.5267, -0.6808, 0.8979, 0.9246, -0.9337, -0.8807, 0.9393, -0.7906, 0.8402, -0.1779, 0.8316, 0.8689, 0.8807, 0.0258
,0.4939, 0.8126, 0.9136, -0.9217, -0.3612, 0.9751, -0.0516, -0.4939, -0.0609, -0.6136, 0.1531, 0.5574, -0.1779, -0.8885, 0.7003, 0.7028, -0.9618, 0.9287, -0.9207, 0.9186, 0.7351, -0.7269, 0.9081, -0.836, -0.1779, -0.743, 0.5267, -0.1531, -0.7506, -0.875, -0.9403, -0.5267
,-0.7184, -0.2732, 0.91, 0.0, 0.2484, -0.926, -0.5859, -0.6486, 0.4404, 0.9719, -0.4588, -0.4019, -0.1779, 0.836, 0.9538, -0.8885, -0.7964, -0.4215, -0.9741, -0.7506, 0.4215, 0.5106, -0.9022, -0.8689, 0.8807, 0.5859, 0.8807, 0.9186, 0.946, 0.4404, 0.5267, -0.8779
,0.8126, 0.7099, 0.4019, -0.743, 0.296, 0.886, 0.0, -0.4019, 0.296, 0.128, -0.6908, -0.743, -0.5423, 0.9201, 0.0, 0.5106, -0.8807, 0.0, 0.8126, 0.8934, 0.5574, 0.936, 0.9801, -0.8885, 0.886, -0.7783, -0.6597, 0.9081, -0.0258, 0.743, 0.0, -0.7783, 0.802
,0.9042, -0.9674, 0.1531, 0.0, 0.7096, 0.0258, 0.7906, 0.34, 0.8438, 0.0, 0.8271, -0.4019, 0.4767, -0.6486, 0.7269, 0.3612, 0.9451, -0.7506, 0.9186, 0.9571, 0.9081, -0.1779, 0.6597, -0.8834, -0.3818, 0.886, -0.9153, 0.2023, 0.8173, 0.926, 0.9062, 0.5267
,-0.3182, 0.25, -0.3182, 0.6705, -0.8225, 0.8807, -0.7184, 0.8885, -0.7003, 0.552, 0.9468, -0.4215, -0.5719, 0.5106, -0.0516, 0.8555, -0.6249, 0.4939, 0.0, -0.4404, 0.6052, 0.0, 0.6249, 0.8519, -0.7964, 0.8658, 0.6808, 0.0, 0.8702, -0.5994, -0.7096, -0.4767, 0.0
,-0.296, 0.5859, -0.9287, -0.872, -0.3612, 0.5267, 0.3612, 0.4767, -0.3018, 0.5267, 0.0516, 0.0, -0.6597, 0.8126, 0.6124, -0.296, -0.5267, 0.9022, 0.2023, 0.9136, 0.9201, -0.8481, 0.8442, 0.9337, -0.7096, -0.7717, 0.3818, 0.9678, 0.0, 0.926, 0.8316, 0.3818, -0.7096
,0.7096, 0.8176, -0.4019, 0.34, -0.5859, 0.5423, 0.5267, -0.7269, 0.6808, 0.807, 0.0, -0.6705, -0.2263, 0.872, -0.0516, 0.8225, -0.9513, 0.5719, -0.7506, -0.7601, 0.2263, 0.9729, 0.9801, 0.6705, 0.7096, -0.4588, 0.7096, -0.5719, -0.8957, 0.3182, -0.8184, -0.4019
,0.9451, -0.2732, 0.7351, 0.6808, 0.9349, 0.8689, -0.4939, 0.9661, 0.7906, -0.8579, -0.8555, 0.0, 0.9001, 0.7845, 0.8658, 0.8934, 0.9719, 0.9313, -0.8474, -0.9451, -0.8074, -0.4404, -0.9432, -0.9001, 0.9042, 0.0, -0.802, 0.3182, -0.7506, -0.3818, 0.9552, 0.9382
,0.6369, 0.899, 0.8442, -0.891, 0.6486, -0.7351, -0.5106, 0.0772, 0.7351, -0.8074, -0.1027, 0.9468, 0.0, -0.9042, 0.6369, 0.9001, 0.936, -0.8625, 0.6705, 0.7184, -0.7749, 0.9217, 0.7906, 0.128, -0.6369, 0.7579, 0.0, 0.765, -0.4019, -0.4019, -0.9153, -0.128, -0.7096
,-0.6124, -0.9169, -0.5423, -0.7269, 0.4404, 0.0, 0.967, -0.9628, 0.8957, 0.9432, -0.8465, -0.6705, 0.7003, -0.8689, -0.7184, -0.34, 0.4019, 0.9791, -0.7506, 0.9118, 0.0, 0.8957, 0.0772, 0.9805, -0.8126, 0.128, -0.802, 0.7845, -0.7269, 0.2023, -0.765, 0.7964, 0.0
,0.0, 0.8402, -0.1779, -0.9776, -0.7913, 0.9349, -0.0915, 0.5719, -0.2263, -0.0772, 0.7269, -0.9153, -0.4767, 0.9382, 0.4767, -0.296, 0.1027, -0.0572, 0.0, 0.4588, 0.7351, 0.886, 0.9423, -0.4215, 0.8519, 0.9442, -0.5106, 0.5106, 0.5994, 0.959, 0.0, 0.4767, -0.8176
,-0.9231, 0.2732, 0.5267, -0.8225, 0.886, 0.765, 0.9501, -0.296, 0.5994, -0.1872, -0.3612, 0.7964, 0.8625, -0.6808, 0.9371, -0.8176, -0.4767, 0.802, 0.0772, 0.3818, 0.969, -0.743, 0.9638, 0.9186, -0.5267, 0.8586, -0.7845, -0.25, 0.34, -0.836, 0.9442, 0.7845
,-0.3182, -0.7605, -0.926, 0.1027, -0.7184, -0.2263, 0.5994, 0.1531, -0.2023, 0.93, 0.6908, 0.8834, -0.4019, -0.6124, 0.0, 0.0, -0.6124, -0.4215, 0.8519, -0.9423, 0.7845, -0.8481, -0.947, 0.8834, 0.765, -0.8935, -0.3818, -0.3612, 0.4939, -0.25, -0.8834, 0.5267, 0.6705
,0.7003, -0.4019, 0.8528, -0.5994, 0.8442, -0.743, -0.9169, 0.0, 0.4019, -0.7269, 0.4215, -0.7351, -0.765, -0.8658, 0.7003, -0.8176, 0.9854, -0.4588, -0.9612, 0.7906, -0.8316, -0.6124, 0.7096, 0.9371, 0.4019, -0.7717, -0.1451, -0.886, -0.8658, -0.8689, -0.7906, 0.7579
,0.5574, 0.34, -0.4215, 0.8225, 0.9169, -0.7845, -0.2755, -0.4019, 0.9393, 0.0258, 0.4939, 0.9382, 0.4588, 0.836, 0.0, 0.0, 0.93, 0.0772, 0.2732, -0.6749, -0.8039, -0.4215, 0.558, 0.128, -0.7208, -0.7096, 0.8316, 0.5859, 0.9153, 0.2023, 0.8658, 0.0258, -0.5994
,0.4767, -0.1779, -0.6124, 0.9676, -0.4767, 0.872, 0.9231, -0.6808, 0.0516, 0.6249, 0.0, 0.0258, -0.296, 0.5719, 0.34, 0.4215, -0.5719, 0.4767, 0.872, -0.9153, 0.743, 0.9524, 0.9592, -0.0258, 0.5574, 0.926, -0.34, -0.5267, -0.7717, 0.0, -0.765, -0.296, 0.4588
,0.34, 0.9744, 0.7906, -0.2732, 0.8934, 0.8934, -0.6369, 0.7964, 0.0772, -0.6728, 0.8271, -0.4939, 0.7096, 0.9661, 0.8225, -0.8316, -0.9758, 0.3612, 0.6908, 0.2732, 0.7598, 0.4019, -0.6249, 0.7017, 0.7783, -0.8979, -0.296, -0.743, -0.7964, 0.8957, -0.4215, -0.6597
,0.128, -0.5994, 0.0, 0.9313, 0.6788, 0.8625, 0.296, -0.7851, 0.7184, 0.8316, -0.8176, 0.886, 0.9118, 0.0516, 0.0, 0.0, 0.9812, 0.0516, 0.0, 0.6808, 0.8176, -0.8074, 0.5627, 0.0772, 0.926, 0.4588, -0.6249, 0.8271, 0.25, -0.3612, -0.3818, 0.4939, 0.9231
,0.891, -0.7783, -0.4215, -0.5719, 0.0, -0.2023, 0.9758, -0.7184, 0.4599, 0.0, 0.7003, 0.4767, 0.9062, 0.9274, 0.5574, -0.9392, 0.4019, -0.5962, -0.6808, -0.1779, 0.9432, -0.9169, 0.765, -0.4019, 0.2023, 0.4404, 0.8625, 0.128, 0.5965, 0.5994, 0.0, -0.7783, 0.8834
,-0.34, -0.8176, 0.0, 0.8271, -0.6249, -0.875, 0.8176, 0.3818, 0.7184, 0.8316, 0.4404, -0.875, 0.6249, 0.5423, 0.0, 0.7003, -0.7096, -0.9118, 0.0, 0.6249, -0.9423, 0.6124, -0.8688, 0.93, 0.8074, -0.0976, 0.8979, 0.0, 0.765, 0.6369, -0.1027, -0.9501, 0.9403
,-0.9493, 0.9623, -0.7717, -0.9313, 0.34, -0.4404, 0.9468, 0.9382, 0.4588, 0.7351, -0.3182, 0.836, 0.743, -0.2732, -0.8271, -0.3182, 0.2023, 0.0258, -0.8271, 0.836, 0.6908, -0.8885, -0.7717, -0.0258, -0.9093, 0.9524, -0.0516, 0.1513, -0.5106, 0.8481, 0.9085, 0.6249
,0.4019, 0.6486, -0.5106, 0.9403, 0.9231, 0.802, 0.4404, -0.7269, -0.3612, -0.4215, 0.9042, 0.9545, 0.0, 0.875, 0.0, 0.7579, 0.8126, 0.6908, 0.3182, -0.7184, 0.6369, 0.0, -0.743, 0.765, 0.91, -0.0572, 0.6908, 0.6369, -0.6808, 0.743, 0.8126, 0.9118, 0.34
,-0.1027, 0.7096, 0.8885, -0.4404, -0.9186, 0.5804, 0.4404, -0.7717, 0.5106, 0.886, 0.0, -0.9382, 0.7003, 0.5574, -0.6124, -0.8316, -0.972, 0.8591, 0.2263, 0.1027, -0.7506, 0.743, -0.5355, 0.9844, 0.7696, 0.3182, 0.0, 0.9738, 0.6808, 0.7269, -0.9277, 0.5106
,0.0, -0.6412, 0.0516, -0.8807, 0.9709, -0.5574, -0.1999, -0.7506, -0.8049, -0.0571, 0.0, 0.6808, 0.3182, -0.5277, 0.0, -0.7096, 0.8519, 0.7506, -0.5106, 0.7579, -0.7717, 0.9169, 0.6124, -0.836, 0.25, 0.7845, -0.8807, 0.4588, -0.6597, -0.5574, -0.1531, 0.2732, -0.2023
,-0.5423, -0.8316, 0.5106, 0.875, 0.7184, 0.5719, 0.4215, -0.9349, -0.872, -0.1027, -0.836, 0.8555, 0.7845, -0.2023, 0.8176, 0.7096, 0.9062, 0.9875, 0.9136, -0.7783, -0.5859, 0.6908, 0.8732, -0.8807, -0.6705, 0.4215, 0.4588, -0.5859, 0.959, 0.3818, -0.872, -0.8442, 0.0
,0.4939, 0.8641, 0.9349, 0.8074, 0.9313, 0.765, -0.6249, 0.7003, 0.7269, 0.9477, 0.9062, 0.4588, -0.7506, 0.5859, -0.4939, -0.3818, -0.296, -0.6249, 0.0, 0.9382, -0.9349, -0.6124, 0.7184, 0.6369, 0.6908, 0.3975, 0.5859, 0.8779, 0.25, 0.2023, -0.4404, 0.4404, -0.743
,0.3182, -0.8779, 0.5719, 0.0, 0.3182, 0.6597, 0.9509, -0.6705, 0.0, -0.5974, 0.2263, 0.891, -0.9136, -0.8658, -0.91, 0.0258, 0.9801, -0.6808, -0.9042, -0.7096, -0.5106, -0.9501, 0.8591, -0.9287, -0.6124, 0.9712, 0.9477, -0.8176, 0.8555, 0.3612, 0.5994, -0.3612
,-0.9001, 0.8555, 0.4767, -0.9517, -0.936, -0.8225, -0.4215, 0.765, -0.7269, -0.5994, -0.296, -0.6908, 0.5994, 0.93, 0.0, 0.4939, -0.7003, -0.8658, 0.0, -0.34, 0.9595, -0.4767, 0.8316, 0.0516, 0.3182, 0.9601, 0.6908, 0.0, 0.7845, -0.9081, -0.8225, 0.9081, 0.8481
,0.0, -0.7351, 0.5859, 0.0772, 0.6369, -0.4756, 0.8689, 0.9531, 0.5994, 0.7906, 0.0, 0.9607, 0.0772, -0.4019, -0.765, -0.8402, -0.9186, -0.8689, 0.946, -0.5267, -0.8519, 0.9595, -0.4939, -0.8074, -0.6486, 0.8957, 0.91, 0.0, 0.9022, -0.802, 0.9081, -0.7717
,-0.8625, 0.0, 0.9638, -0.7579, 0.9794, -0.8689, -0.4767, 0.4404, 0.765, 0.9735, -0.431, -0.836, 0.93, -0.296, 0.0, 0.4939, -0.8225, -0.1531, 0.4585, -0.8807, 0.0516, -0.0258, 0.8689, 0.7783, -0.6705, 0.9638, 0.3818, 0.6808, -0.5719, -0.5574, -0.5423, 0.0, 0.743
,0.6486, -0.2263, 0.34, 0.9062, 0.0, 0.7964, 0.7184, 0.9423, 0.0772, -0.9501, 0.0, -0.5859, -0.9517, -0.6705, -0.1027, -0.5423, -0.8991, -0.7579, 0.9719, 0.8126, -0.6808, 0.5423, -0.7717, 0.6249, 0.6369, 0.9136, -0.0258, 0.1779, -0.8442, -0.1027, 0.8481, 0.765
,0.1027, 0.0, 0.5994, 0.6124, 0.9432, -0.6908, -0.3612, 0.8979, -0.6369, -0.6204, -0.7606, 0.8979, 0.7506, 0.0, 0.0, 0.9062, 0.7906, 0.7506, 0.7906, -0.9485, -0.9217, -0.6369, -0.8131, 0.836, -0.7579, 0.8176, 0.7906, 0.9136, 0.0, 0.802, 0.8885, 0.9287, -0.296
,-0.7096, 0.0, -0.34, 0.296, 0.9246, 0.8442, 0.7579, 0.7184, 0.0, 0.891, -0.836, -0.9612, 0.9702, 0.1779, -0.8521, -0.8689, 0.6369, 0.7579, 0.9062, -0.8271, -0.6908, 0.8316, 0.9545, 0.8442, -0.8225, -0.8481, -0.7579, 0.9403, 0.5994, 0.8834, -0.34, 0.3818
,0.9485, 0.7311, 0.0, 0.2732, 0.9022, 0.5719, -0.7351, 0.9371, 0.5106, 0.9686, 0.0, -0.3612, 0.0, -0.8399, 0.0, 0.91, -0.8658, 0.0, -0.5423, -0.8555, 0.9623, -0.8885, 0.9001, -0.4588, -0.9153, 0.0, 0.5267, 0.5859, 0.5994, 0.765, 0.8885, 0.886
,-0.5719, -0.926, 0.296, -0.8176, 0.0, -0.765, 0.765, 0.9468, -0.9001, 0.0, 0.9612, 0.34, 0.6249, -0.9022, -0.7269, 0.1027, 0.4215, 0.9883, -0.0772, 0.9382, -0.34, 0.8807, -0.1645, 0.9246, 0.9517, 0.2828, -0.3612, 0.6249, -0.8885, 0.6369, 0.5106, 0.9245, -0.3612
,-0.4019, -0.1027, 0.9468, -0.8378, -0.9325, -0.7096, -0.5994, -0.5994, -0.4842, -0.936, -0.0915, 0.34, 0.1027, -0.743, 0.0, -0.1027, -0.8316, -0.9274, 0.8979, -0.5719, 0.9169, 0.802, 0.1027, -0.9559, -0.1779, 0.0232, -0.9403, -0.296, -0.7964, -0.8442, 0.9217, 0.0, 0.8225
,-0.6908, 0.9477, -0.4019, -0.5423, -0.3818, 0.7783, 0.9022, -0.1779, 0.5994, 0.8442, 0.3818, -0.7579, 0.9482, -0.1779, 0.9781, -0.5211, 0.9858, -0.9287, 0.9612, -0.0258, -0.4215, -0.6249, 0.4019, 0.875, 0.9371, 0.5106, -0.8176, 0.0, 0.8519, 0.8625, -0.9565, 0.0
,0.926, 0.0, -0.4404, 0.6486, 0.4215, -0.6597, 0.0, -0.7783, -0.9313, -0.5106, -0.4404, -0.296, 0.5267, -0.7351, 0.0, -0.7506, 0.93, 0.6808, 0.0, 0.875, -0.5719, -0.4588, -0.6369, -0.8074, -0.8442, -0.1779, 0.0, -0.7184, 0.2732, -0.875, -0.765, -0.7783, -0.7579
,0.4767, 0.9719, 0.7351, 0.7184, -0.7184, 0.2023, 0.1916, 0.9246, 0.6597, 0.765, 0.7096, 0.4767, 0.6369, 0.3612, 0.6486, 0.6369, -0.7717, 0.9153, -0.8658, 0.2023, 0.8481, 0.0547, -0.938, 0.7269, -0.6486, -0.9042, 0.9643, 0.0, 0.6369, 0.0258, 0.2732, 0.7003, 0.9186
,0.7506, 0.0, 0.9231, 0.7184, -0.3818, -0.34, -0.886, 0.2023, 0.5267, 0.9801, 0.0, 0.9726, 0.926, -0.8074, -0.8402, 0.9246, 0.9201, 0.9022, -0.7506, 0.0, 0.765, -0.6621, 0.8481, 0.91, -0.6124, -0.8225, 0.3182, 0.7845, -0.25, -0.296, -0.7453, 0.9709
,-0.6908, 0.0, -0.3612, 0.9301, -0.8934, 0.0, 0.6486, -0.4767, -0.296, 0.7269, -0.0258, -0.9382, 0.0, 0.8519, 0.8271, 0.2732, 0.886, -0.4215, 0.0, 0.9678, -0.9601, -0.9413, 0.9716, -0.7884, -0.34, 0.6597, 0.8225, 0.34, -0.4019, 0.7964, 0.5574, 0.8658, 0.0
,-0.886, 0.5859, 0.7783, 0.8591, 0.9559, -0.5106, -0.379, 0.8834, -0.4019, 0.6908, 0.3612, 0.9413, -0.296, -0.5267, -0.5267, 0.8807, -0.6908, 0.0, 0.0, -0.7964, -0.7351, 0.8807, 0.8885, 0.1531, 0.9468, -0.8885, 0.8807, -0.6908, 0.9022, 0.7184, 0.7717, 0.8807, -0.872
,-0.8126, -0.9674, 0.4215, 0.4767, -0.8885, 0.8714, -0.3182, -0.7756, 0.6124, -0.836, -0.3612, -0.8176, -0.9423, -0.8402, 0.9468, -0.765, 0.9878, 0.4548, -0.8957, -0.0516, 0.3806, -0.714, 0.8271, -0.8945, 0.4215, 0.836, -0.9042, 0.2263, 0.4019, 0.6369, -0.4939, 0.6705]

b = [-3, -2, -2, -2, -2, -1, -2, -1, -2, -2, -2, 2, -2, -2, -2, -2, -1, 1, -2, -3, 2, -3, -3, -2, 0, 2, 1, 1, 0, -2, -2, -2,
-2, -1, -2, -1, 1, -2, -2, -1, -1, -2, -1, -1, -2, 0, -1, -1, -2, -2, -1, 0, 0, -2, -2, 1, -1, -1, -1, -1, -1, -2, -2, -3, 0,
3, 3, 2, 1, 1, 3, 1, 3, 1, 2, -2, 2, 0, 2, 3, 2, 2, -3, 2, 3, 2, 2, 3, 2, 2, 0, 2, 3, 1, 3, 3, 3, 2,
1, 2, 0, 3, 1, 2, 0, 1, -1, 0, 1, 1, 0, 1, 2, 1, 1, 1, 1, 2, 2, 3, 2, -1, 1, 2, 1, 3, 1, 1, 2, 1, 2,
-3, -3, -2, -2, -3, -2, -2, -3, -3, -2, -3, 1, -2, -3, -2, -3, 0, -1, -2, -2, 2, 3, -3, -2, 1, -2, -1, 0, -1, -3, -3, -3,
-1, -1, -2, 1, -1, 0, -2, -1, -1, -1, -1, -2, 1, 0, -2, -2, 0, -2, -2, -1, -2, -1, 1, -1, -1, -1, -1, -1, -1, -2, -3, 2,
3, 3, 3, 3, 2, 3, 2, 2, 2, 3, 3, 2, 1, 0, 3, 2, 3, 3, 2, 3, 0, 2, 3, 3, 2, 1, 2, 3, 0, 2, 3, 3, 2,
2, 1, 2, 3, 0, 1, 0, 2, 0, 2, 3, 0, 0, 2, 1, 2, 0, 1, 2, 1, 1, -1, 1, 0, 1, 1, 1, 0, 0, 0, 2, 2,
3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 3, 3, 1, 3, 0, 3, -3, 3, 3, -1, 2, 3, 3, 3, -1, 3, 3, 0, 1, 3, 3, 3,
1, 1, 2, 2, 2, 2, 2, 2, 2, 0, 2, 3, 2, 2, 1, 3, 1, 2, 2, 3, 2, 0, 1, 0, 1, 3, 1, 2, 2, 1, 1, 2, 1,
-2, -1, 0, -1, -1, 1, -1, -1, -1, 1, -2, 2, -1, 0, -1, -1, 0, -1, -3, -2, -3, -2, -2, 0, -1, 2, 1, 0, -2, -2, -1,
-1, -1, -2, -1, 0, 0, -1, -1, -1, -2, -1, -1, -1, -1, 0, -1, -1, -1, -1, -2, -1, -1, -1, 2, -1, -1, -2, -1, -1, -1, -1, -3, 1,
-3, -2, -2, -3, -2, -2, -3, -3, -3, -2, -3, 0, -2, -3, -3, -2, -2, -1, -2, -3, 2, 3, -3, -2, 1, 2, -2, 0, -1, -1, -2, -3,
-1, -1, 0, 0, 0, 0, -1, 0, -1, -2, 0, 0, -1, -2, 0, -1, -1, 0, -1, 0, 0, 0, 0, 1, 0, -1, 0, -2, 0, 0, -1, -1, 0,
2, 2, 2, 1, 1, 1, 0, 2, 2, 2, 2, 0, 2, 2, 1, 2, -1, 1, 2, 2, 2, 3, -1, 2, 1, 2, 3, 0, 3, 2, 3, 2,
0, 2, 1, 1, 1, 0, -1, 1, 1, 0, 1, -3, 1, -1, 0, 1, 0, 0, 0, 0, 1, 2, -1, 0, -1, -1, 0, 2, 0, -1, 0, 0, 1,
-2, -1, -2, -1, 0, -1, -2, -1, -2, -2, 0, -1, -2, -2, 0, 0, -1, -1, -1, 0, 0, 1, -2, -2, -1, -1, -1, -1, 0, -1, 0, -3, 0,
1, 0, -1, -2, 0, 0, 0, 1, 0, 0, 0, -3, -1, 0, 0, -1, -1, -1, 0, -2, 2, 3, 2, 0, 1, -1, 0, 0, 1, -1, -1, 0,
-2, 0, -2, -2, -2, 0, 0, 0, -2, 0, -1, -3, 0, -2, -1, -2, 3, 1, -1, -1, 2, 3, -2, 0, 1, 2, 2, 0, 1, -3, 1, -2,
-1, 1, -1, 0, 2, -1, 0, -1, 0, -2, 1, 3, -1, -2, 0, 0, 0, 2, 1, 0, 1, 0, -1, 1, 0, 0, 1, 2, 0, 0, 1, 0, 2,
-3, -3, -2, -2, -2, -2, -3, -1, -2, -1, -1, -1, 1, -2, -2, -3, -3, 0, 0, -2, -2, 2, -2, -2, -2, -1, 2, -2, 1, -1, -3, -3,
0, -2, -1, -1, -1, 0, 0, -1, -1, -1, -1, -2, -1, -1, 0, -1, -2, 0, 0, 0, 0, -1, -2, 1, 0, -1, -1, -2, -1, -2, -1, -2, 2,
2, 3, 2, 3, 3, 1, 1, 2, 1, 2, 2, 3, 3, 1, 1, 2, 2, 1, 2, 3, 2, 2, 2, -1, 2, 2, 1, 3, 1, 2, 2, 1, 2,
2, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, -1, -1, 2, 1, 1, 2, 0, 1, -1, 1, 2, 0, 1, 0, 3, 0,
3, 2, 1, 2, 1, -2, 1, 3, 3, 3, 2, 3, 1, 3, 1, 2, -2, 1, 3, 2, 1, 3, 3, 3, 0, 2, 3, 1, 2, 3, 3, 2,
0, 0, 1, 2, 3, 2, 0, 1, 1, 0, 2, 0, 0, 1, 2, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, -1,
-2, -1, -2, -2, -1, -2, -1, -2, -2, -1, 2, -2, 0, -2, -1, -3, -1, -2, -1, -2, 0, 2, 2, -2, -2, 0, 2, -1, 1, 1, 0, -1, -2,
0, -1, -1, 0, 0, 0, 0, 0, 1, 0, 0, 1, -1, -2, 0, -1, -1, 0, -1, -1, 0, -2, -2, -1, 0, 1, 0, -2, 0, 0, 0, 0, 0,
-2, -2, -2, -2, -1, -3, -1, -2, -2, -1, -1, 1, -2, -3, -1, -2, 2, -1, -3, -2, 2, -1, -2, -1, -1, 1, 1, 0, 0, -1, -3, -2,
-1, -1, -3, 0, 2, -1, -2, -1, -1, -1, 1, -1, -1, -1, 0, -1, -1, -1, -1, -1, 0, -1, -1, 0, 0, -1, -1, -2, -1, -1, 0, -1, 2,
3, 2, 2, 2, 1, 1, 1, 2, 2, 0, 2, 0, 2, 3, 3, 3, 2, 2, 3, 2, 2, 3, 3, 2, -1, 2, 1, 1, 2, 3, 2, 2,
1, 2, 1, 2, 0, 1, 0, 1, 1, 0, 0, 2, 0, 0, 0, 1, 0, 0, 2, 1, 2, 1, 3, -1, 1, 0, 2, 2, 1, 1, 3, 0, -1,
1, 1, 2, 3, 2, 1, 2, 0, -1, 1, 2, 3, 2, 1, 0, 0, 1, -1, 1, 3, 2, 0, 3, 1, 2, 1, 1, 1, 2, 0, 2, 3, 0,
2, 1, 1, 1, 0, 0, 0, 0, 0, 2, 0, 1, 0, 1, -2, 1, 1, -1, 0, 1, 1, 1, 2, 0, 0, 2, 2, 1, 2, 2, 1, 1,
2, 3, 2, 3, 2, 2, 3, 2, 1, 2, 3, 2, 2, 1, 3, 2, 2, 1, 3, 3, 2, 3, 3, 1, 2, 3, 3, 3, 3, 2, 2, 1, 1,
3, 2, 1, 2, 2, 0, 2, 1, 2, 2, 1, 0, 0, 1, 0, 2, 3, 2, 1, 3, 2, 2, 2, 1, 3, -1, 2, 2, -1, 1, 2, 2, 3,
2, 3, 3, 3, 0, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 3, 2, 3, 3, 0, 2, 2, 2, 3, 2, 1, 2, 1, 1,
3, 0, 1, 1, 2, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2, 2, 2, 2, 0, 2, 0, 1, 2, 1, 3, 2,
-2, -3, -2, -3, -1, -2, -2, -2, -1, -2, -1, -3, -3, -1, -1, -2, -2, -1, -3, -2, -1, -2, -2, 1, -2, -3, -3, -3, -3, -2, -3, -3, 1,
2, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 0, 2, 3, 0, 1, -1, 2, 2, 0, 0, 1, 0, 0,
2, 3, -1, 3, 2, 1, 1, 2, 3, 1, 2, 3, 2, 2, 3, 1, 1, 1, 2, 3, 1, 1, 3, 0, 2, 3, 2, 3, 2, 1, 3, 2, 2,
-1, -1, -1, -1, 1, -1, 0, 2, 0, 0, 0, 0, 1, 0, -1, 0, 0, 1, 0, 2, 0, 1, 3, 0, 1, 0, 0, 2, 1, 2, 0, 1, -1,
-2, -1, -1, -2, -1, -1, -2, -1, -1, -2, 0, 1, -2, 0, 0, -1, -1, 2, -1, 0, 0, 1, -2, 0, 0, -1, 1, -2, -2, -1, -2, -1, 2,
1, 1, 1, -1, 2, 3, 0, 1, 0, 0, 1, 0, -1, 0, 1, 1, 1, 1, 2, 2, 2, 3, 1, 1, -1, 1, 2, -1, 1, 0, 3, 2,
-2, -1, -2, -3, 1, -2, -2, -2, -2, -1, -1, -3, -3, -2, -1, -3, -2, -2, -2, -2, -1, 2, 0, 0, -2, -3, -2, -2, -2, -2, -3, -3, 1,
-1, -2, -2, -1, 0, 0, -2, -1, -1, 2, -2, 0, -1, 0, 1, -1, -3, 0, -1, 0, 2, -3, 1, -1, 0, 2, -1, 1, 2, -1, -1, -2,
2, 3, 3, 3, 2, 2, 3, 2, 2, -2, 3, 3, 3, 2, 3, 2, 3, 1, 0, 3, 3, 1, 3, 1, 2, 3, 3, 3, 3, -1, 3, 3, 0,
3, 2, 2, 2, 1, 2, 0, 3, 2, 1, 1, 1, 0, 2, 2, 3, 0, 2, 3, 2, 1, 3, 3, 2, 0, 1, 3, 0, 3, 1, 3, 1,
-2, -2, -3, -2, -1, 0, -2, -2, -2, -3, -2, -1, -2, -2, 0, -2, -1, -2, -2, -2, 0, -1, -2, 2, -2, -2, -3, -2, -2, -2, -3, -3, 1,
-1, 0, 0, -2, -1, 0, 1, -1, 0, 0, 0, 0, 0, -2, 0, -2, 0, 1, 0, -1, -1, 3, -2, 0, 0, -2, 1, 0, 2, -1, 0, -1,
1, 3, 3, 3, 2, 2, 2, 2, 3, 2, 3, 2, 2, 3, 3, 3, 2, 1, 2, 3, 2, 2, 2, 1, 2, 2, 2, 2, 2, 3, 3, 2,
1, 2, 2, 1, 2, 2, 0, 1, 1, 3, 2, 1, 1, 0, 2, 1, 2, 0, 2, 2, 3, 3, 3, 2, 1, 0, 2, 2, 0, 1, 2, 3, 1,
3, 3, 3, 3, 3, 1, 2, 2, 2, 2, 3, 3, 3, 2, 3, 2, 2, 3, 2, 3, 3, 3, 3, -1, 2, 3, 3, 3, 2, 1, 3, 2, 1,
3, 2, 2, 3, 3, 1, 2, 3, 3, 2, 2, 1, 0, 2, -1, 3, 2, 2, 3, 2, 2, 3, 3, 2, 0, 1, 3, 0, 2, 3, 3, 0,
-1, -1, -1, -1, 1, -1, -2, -1, 1, -1, -1, -1, -1, -3, 0, -2, -2, -2, -2, -1, -1, -2, -1, 1, -1, -1, -2, -2, -1, -2, -1, -3, 1,
-1, -1, 1, -2, -1, -2, 0, 1, -1, -1, 2, -1, 1, -1, -1, -1, -2, -1, 0, 1, -2, 1, 1, -2, -1, 2, 1, 1, 0, 3, -3, 2, -1,
3, 3, 3, 3, 3, 3, 0, 3, 3, 2, 2, 1, 0, 3, 2, 3, 3, 1, 3, 2, 1, 3, 3, 2, 1, 2, 3, 1, 3, 3, 2, 2,
2, 2, 1, 3, 3, 0, 0, 2, 2, 1, 1, 3, 2, 2, 1, 2, 2, 0, 2, 2, 1, 3, 1, 0, 0, 1, 3, 2, 0, 0, 2, 0, 0,
2, 3, 1, 2, 3, 2, 2, 2, 2, 1, 3, 3, 3, 1, 2, 1, 2, 0, 2, 3, 3, 3, 3, 0, 3, 2, 3, 3, 3, 1, 3, 3, 2,
1, 1, 1, -1, 0, 0, 1, 2, 2, 2, 1, -1, 1, 2, -2, 0, 1, 1, 2, 2, 2, 3, 3, 0, 0, 2, -2, 0, 0, 1, 3, 0]


print(pearsonr(a, b))

c= [-0.1780765444663414,0.0017224142096460213,-0.15283521230277194,-0.2544833734814341,0.13858781314460283,0.07602572861896824,-0.37283506096389585,
-0.04953898566300369,0.09050778605393121,-0.07167863266635902,-0.02621608872972775,0.05643143530160222,-0.03935367588976637,0.12720976252629496,-0.032218416366305985,
0.03663990677707286,0.12669995975520731,-0.021194043722278150, 0.20672424988181953,-0.15609285659025873,-0.2208329377839607,0.10690085643672245,-0.2852190455012311,
-0.1445468037440492,-0.3815419804760978,-0.07045555895088323,-0.02307029382402951,-0.26787017490347453,0.0164115228261678,0.25374348517952133,0.04063894039133076,0.24087298774077606,-0.13970823521206754,
-0.4745524223172207,-0.2219451121059417,-0.09765297176767375,-0.03374871828757724,-0.09889235309740085,0.05581303235710701,-0.12616848682259235,0.12391908391622702,
-0.04485161202590634,-0.25479375968183104,0.12667758211283342,0.00048049474131407754,0.023851891088238333,-0.21271842719905737,0.17097210388836304,-0.14669188068023864,
0.21270226809210266,0.022427282898568268,0.08916916109755572,0.28321897532112605,-0.36020531937823796,-0.04421156919080231,-0.12399014490788829,-0.08360993171905108,
-0.06254897121996057,0.12338846852215211,-0.07544686670628185]




y_mean = [np.mean(c)]*len(c)
fig,ax = plt.subplots()
plt.plot(c)
plt.ylabel('Pearson Korrelationskoeffizienten')
plt.ylim([-1,1])
plt.xlabel('Anzahl der einzelnen Werte für jedes Pseudowort')
mean_line = ax.plot(y_mean, label='Mean', linestyle='--')

ax.axhspan(-1, -0.66, facecolor='azure', alpha=0.5)
ax.axhspan(-0.66, -0.33, facecolor='lightblue', alpha=0.5)
ax.axhspan(-0.33, 0.33, facecolor='darkgrey', alpha=0.5)
ax.axhspan(0.33, 0.66, facecolor='lightblue', alpha=0.5)
ax.axhspan(0.66, 1, facecolor='azure', alpha=0.5)

plt.show()
 """