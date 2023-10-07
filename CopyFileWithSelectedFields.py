import pandas as pd

####
#This method takes three parameters:
    #csvIn: The input CSV file path.
    #uFields: A string containing the names of the fields to include in the output, separated by commas.
    #csvOut: The output CSV file path.
#This code is designed to process a list of CSV files specified in FilesTobeProcessed.csv. 
#For each file, it extracts the source file path, output file path, and the names of fields to include,#
#then exports the selected fields from the source file to the output file.
####
class clsGeneral(object):
    def exportSelectedFields(csvIn,uFields,csvOut):
        # Read the CSV file into a DataFrame
        uData = pd.read_csv(csvIn)
        # Create a DataFrame
        df = pd.DataFrame(uData)
        # Create a new DataFrame containing only the selected columns
        flds = uFields.split(',')
        df_selected = df[flds]
        # Export the selected data to a CSV file
        df_selected.to_csv(csvOut, index=False)

# Iterate through rows
# Read the CSV file into a DataFrame and list the file details for IN/OUT files.
#replace the path below with your file.
uFile=r'K:\2023\SimulatedSSOs_study\HCAD_Dataset\FilesTobeProcessed.csv'
csvFileList = pd.read_csv(uFile)
uCSVinfo = pd.DataFrame(csvFileList)
#print(csvFileList)
for index, row in uCSVinfo.iterrows():
    csvIn =row["SourceFile"]
    csvOut =row["OutFile"]
    flds=row["FieldsToInclude"] # Supply the name of fields separated by comma.
    print("Processing file:" + csvIn)
    clsGeneral.exportSelectedFields(csvIn,flds,csvOut)
print("Export process completed....")
