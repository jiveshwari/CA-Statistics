import pandas as pd
from sklearn.model_selection import train_test_split
import os

def extractScore(score):
    # check for nan
    if score != score:
        return 0.0 
    return float(score.split(" (")[0])    

def createArgObject(ann1,ann2,ann3):
    arg = {}
    arg["id"] = ann1['#id']
    arg["issue"] = ann1['issue']
    arg["stance_on_topic"] = ann1['stance']
    arg["text"] = ann1['argument']
    arg["argumentative"] = [ann1['argumentative'],ann2['argumentative'],ann3['argumentative']]
    arg["argument_quality_scores"] = [extractScore(ann1['overall quality']),extractScore(ann2['overall quality']),extractScore(ann3['overall quality'])]
    arg["effectiveness_scores"] = [extractScore(ann1['effectiveness']),extractScore(ann2['effectiveness']),extractScore(ann3['effectiveness'])]
    return arg

def majority(ann_1,ann_2,ann_3):
    if ann_1 == 'y' and (ann_2 == 'y' or ann_3 == 'y'):
        return True
    elif ann_2 == 'y' and (ann_1 == 'y' or ann_3 == 'y'):
        return True
    elif ann_3 == 'y' and (ann_1 == 'y' or ann_2 == 'y'):
        return True
    else:
        return False

def generateOutputDataset(data):
    outputSet = []
    for row in range(0,len(data), 3):
        ann1 = data.iloc[row]
        ann2 = data.iloc[row+1]
        ann3 = data.iloc[row+2]
        # we consider arguments as argumentative if two annotators think it is argumentative i.e., majority            
        if majority(ann1['argumentative'],ann2['argumentative'], ann3['argumentative']): 
            argObject = createArgObject(ann1,ann2,ann3)
            outputSet.append(argObject)
    return outputSet
 
def main():

    # read csv data
    path = 'data/dagstuhl-15512-argquality-corpus-annotated.csv'
    file = open(path,encoding='latin-1')
    
    # create df
    data = pd.read_csv(file,sep='\t')
    
    # prepare output dataset
    outputDataSet = generateOutputDataset(data)
    outputDataSetDf = pd.DataFrame(outputDataSet)
    
    # split data sets
    train, test = train_test_split(outputDataSetDf, test_size=0.2, random_state=42)
    train, val = train_test_split(train, test_size=0.125, random_state=42)

    # Get the shape of all the datasets
    print("fulldataset: ",len(outputDataSetDf))
    print("train: ",len(train))
    print("val: ",len(val))
    print("test: ",len(test))
    
    # output to json 
    outputPath = 'output/'
    outputDataSetDf.to_json(outputPath+'fulldataset.json',orient="records")
    train.to_json(outputPath+'train.json',orient="records")
    test.to_json(outputPath+'test.json',orient="records")
    val.to_json(outputPath+'val.json',orient="records")
    return


if __name__ == '__main__':
    main()


''' 
    Split data using train_test_split. As it only splits the data into two sets,
    we need to use train_test_split twice to form three sets (train,test,validation).
    First we split the whole dataset (320 arguments) into 80% train and 20% test sets
    Then we split 80% train set into 70% train and 10% validation sets. 
'''