import pandas as pd
def getjobsdf():
  #fetching the dataset downloaded from kaggle
  #this is present locally
  file_path = "job_applications_tracker_dataset.csv"
  #converting to pandas dataframe
  df = pd.read_csv(file_path)
  return df


if __name__=="__main__":
    jdata=getjobsdf()
