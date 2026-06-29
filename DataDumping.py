from sqlmodel import create_engine, SQLModel, Field, Relationship
from dotenv import load_dotenv
import os
from DF_Creation import getjobsdf
jdata=getjobsdf()
load_dotenv()
db_url=os.getenv("DATABASE_URL")

class jobs(SQLModel, table=True):
    __tablename__="jobs"
    application_id :int =Field(default=None, primary_key=True)
    company_name: str
    job_role:str
    application_date: str
    job_type: str
    platform: str
    status: str
    salary_expectation: int
    experience_required_years: int
    company_rating: float

engine = create_engine(db_url)
SQLModel.metadata.create_all(engine)
try:
    jdata.to_sql('jobs', con=engine, if_exists='replace', index=False)
    print("DataFrame jobs successfully uploaded to the database.")
except ValueError as e:
    print(f"Error uploading DataFrame: {e}")