import pandas as pd

####
#It reads water consumer data from '*.csv'.
#It extracts unique improvement codes.
#For each improvement code, it calculates a weighted average 
#using the calWtAgvValue method and stores the results in the wtAvgGP list.
#It writes the results to a new CSV file 'b.csv', including improvement code, 
#weighted average, and the number of data points.
#The script was designed for processing and 
#summarizing data related to water consumers with different improvement codes and 
#calculating weighted averages for each code. 
#The results are then saved in a CSV file for further analysis or reporting.
####
#global variables.
numPts=0
#constant used as global settings.
maxDeviate=3 #maximum deviation for removing outliers.
gpdFld='TotalGPD'#static field name in the water consumer dataset
sfFld='TotalImprvSF' #static field with the GPD values from the parcel.
imprvFld='IMPROVTYPE'#static field name in the water consumer dataset.
gpdperSF='GPDperSF'#new field to store the GPD per SF calculated value.

class clsDataTool(object):
    def calWtAgvValue(orgDF,imprvType):
        global numPts
        # Filter the rows for the given improvement code.
        dDF=orgDF[orgDF[imprvFld]==imprvType]
        #dDF.loc[:,gpdperSF]=dDF[gpdFld]/dDF[sfFld] #adding new field to the datafield.
        #create new dataframe from the sliced dataframe.
        uDF= pd.DataFrame() #create new dataframe and copy data from sliced dDF
        uDF[gpdFld]=dDF[gpdFld]
        uDF[sfFld]=dDF[sfFld]
        uDF[gpdperSF]=uDF[gpdFld]/uDF[sfFld] 
        #do calculation for mean and standard deviation.
        avgGPDpSF = uDF[gpdperSF].mean()
        stdDev = uDF[gpdperSF].std()
        # Define the threshold for outliers (e.g., two standard deviations away from the mean)
        threshold = maxDeviate * stdDev #set maximum data range.
        # Use boolean indexing to filter out outliers
        fDf = uDF[abs(uDF[gpdperSF] - avgGPDpSF) <= threshold]
        totGPDvalue=fDf[gpdFld].sum()
        totImprvSF=fDf[sfFld].sum()
        numPts=fDf.shape[0]#find number of rows in the dataframe.
        if (totImprvSF==0):
            return 0
        return round(totGPDvalue/totImprvSF,6)

#Read the water consumers table
waterConsumersFilePath=r'WaterConsumers.csv'
print("Reading the water consumer dataset.....")
waterConsumers = pd.read_csv(waterConsumersFilePath,dtype={imprvFld:int})
wConsList = pd.DataFrame(waterConsumers)
#Read the list of improvement Codes
print("Listing unique improvement codes......")
imprvCodes=wConsList[imprvFld]
lstImprv = imprvCodes.drop_duplicates()
sImprvCodes=lstImprv.sort_values()
#process the dataset per improvement type group.
wtAvgGP=[]
for imprvType in sImprvCodes:
    print("Processing for the improvement code:" + str(imprvType))
    wtAvgGPDperSF=clsDataTool.calWtAgvValue(wConsList,imprvType)
    if (wtAvgGPDperSF>0):
        wtAvgGP.append(str(imprvType)+','+str(wtAvgGPDperSF)+","+str(numPts))
#write the table into a csv file
with open(r'wtAvgGPDperSF.csv',mode='w') as csvfile:
    csvfile.write('imprvType,wtAvgGPDperSF,DataPointsCount\n')
    for uD in wtAvgGP:
         csvfile.write(uD + '\n')
print("Computation/writing to CSV file completed....")