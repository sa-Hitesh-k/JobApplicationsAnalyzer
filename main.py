from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import create_engine, Session, SQLModel, Field, select, col, func
from dotenv import load_dotenv
import os

def main():
    print("Hello from jobapplicationsanalyzer!")

load_dotenv()
db_url=os.getenv("DATABASE_URL")

engine = create_engine(db_url)
SQLModel.metadata.create_all(engine)

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

app=FastAPI()

origins=['http://localhost:8501']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=['*']
)
def get_session():
    with Session(engine) as session:
        yield session

@app.get("/all-companies/", summary="companies' names", description="Get names of all the companies")
def get_companies_names(sesssion: Session=Depends(get_session)):
    return sesssion.exec(select(jobs.company_name).distinct(jobs.company_name)).all()

@app.get("/all-job-roles/", summary="job roles", description="Get all the jobs")
def get_jobs(sesssion: Session=Depends(get_session)):
    return sesssion.exec(select(jobs.job_role).distinct(jobs.job_role)).all()

@app.get("/all-job-types/", summary="job types", description="Get all the jobs")
def get_companies_names(sesssion: Session=Depends(get_session)):
    return sesssion.exec(select(jobs.job_type).distinct(jobs.job_type)).all()

@app.get("/all-platforms/", summary="platforms", description="See all the platforms")
def get_companies_names(sesssion: Session=Depends(get_session)):
    return sesssion.exec(select(jobs.platform).distinct(jobs.platform)).all()

@app.get("/companies-with-x-job/", summary="companies with x job", description="Know which Company has most of x jobs")
def get_companies_with_x_jobs(sel_job: str, session: Session=Depends(get_session)):
    statement=(
        select(
            jobs.company_name, 
            jobs.job_role, 
            func.count(jobs.job_role).label("job_count")
            )
        .where(jobs.job_role==sel_job)
        .group_by(*[jobs.company_name, jobs.job_role])
        .order_by(func.count(jobs.job_role))
        )
    rows = session.exec(statement).all()
    return [
        {
            "company_name": row.company_name,
            "job_role": row.job_role,
            "job_count": row.job_count,
        }
        for row in rows
        ]

@app.get("/companies-with-x-job-y-job-type/", summary="companies with x job and y job type", description="Know which Company has most of x jobs and y job types")
def get_companies_with_x_jobs_y_job_type(sel_job:str, sel_job_type: str ,session: Session=Depends(get_session)):
    statement=(
        select(
            jobs.company_name, 
            jobs.job_role,
            jobs.job_type ,
            func.count(jobs.job_type).label("job_count")
            )
        .where(jobs.job_role==sel_job, jobs.job_type==sel_job_type)
        .group_by(*[jobs.company_name, jobs.job_role, jobs.job_type])
        .order_by(func.count(jobs.job_type))
        )
    rows = session.exec(statement).all()
    return [
        {
            "company_name": row.company_name,
            "job_role": row.job_role,
            "job_type":row.job_type,
            "job_count": row.job_count,
        }
        for row in rows
        ]

@app.get("/companies-with-x-job-y-job-type-on-platform-z/", summary="companies with x job and y job type on z platform", description="Know which Company has most of x jobs and y job types on z platform")
def get_companies_with_x_jobs_y_job_type(sel_job: str, sel_job_type:str , sel_company: str,session: Session=Depends(get_session)):
    statement=(
        select(
            jobs.job_role,
            jobs.job_type ,
            jobs.platform,
            func.count(jobs.job_type).label("job_count")
            )
        .where(jobs.job_role==sel_job, jobs.job_type==sel_job_type, jobs.company_name==sel_company)
        .group_by(*[jobs.job_role, jobs.job_type, jobs.platform])
        .order_by(func.count("job_count").desc())
        )
    rows = session.exec(statement).all()
    return [
        {
            "job_role": row.job_role,
            "job_type":row.job_type,
            "platform": row.platform,
            "job_count": row.job_count,
        }
        for row in rows
        ]

@app.get('/get-ery-for-company-and-jobrole/')
def get_ery_for_comp_jr(sel_comp: str, sel_job: str, session: Session=Depends(get_session)):
    statement=(
        select(
            jobs.company_name,
            jobs.job_role,
            jobs.experience_required_years,
            func.count("*").label("people_count")
        )
        .where(jobs.company_name==sel_comp, jobs.job_role==sel_job)
        .group_by(*[jobs.company_name, jobs.job_role, jobs.experience_required_years])
        .order_by(func.count("*"))
    )
    rows=session.exec(statement).all()

    statementavg=(
        select(
            func.avg(jobs.experience_required_years)
        )
        .where(jobs.company_name==sel_comp, jobs.job_role==sel_job)
    )
    avg_ery=session.exec(statementavg).all()

    erylist=[
        {
            "company_name": row.company_name,
            "job_role":row.job_role,
            "experience_required":row.experience_required_years,
            "people_count":row.people_count
        }
        for row in rows
    ]
    erylist.append({'average exp req':avg_ery[0]})
    return erylist
    
@app.get('/exp-vs-sal-exp/')
def exp_vs_sal(sel_job: str, sel_exp: int, session: Session=Depends(get_session)):
    
    statement = select(
        func.percentile_cont(0.25)
            .within_group(jobs.salary_expectation)
            .label("q1"),
        func.avg(jobs.salary_expectation).label("avg"),
        func.percentile_cont(0.75)
            .within_group(jobs.salary_expectation)
            .label("q3"),
    ).where(
        jobs.job_role == sel_job,
        jobs.experience_required_years == sel_exp,
    )

    row = session.exec(statement).one()
    return {
        "q1": row.q1,
        "avg": row.avg,
        "q3": row.q3,
    }

@app.get('/platform-vs-status/')
def get_platform_vs_status(sel_job:str, session: Session=Depends(get_session)):
    statement=(
        select(
            jobs.platform,
            jobs.status,
            func.count("*").label("people_count")
        )
        .where(jobs.job_role==sel_job)
        .group_by(*[jobs.platform, jobs.status])
        .order_by(jobs.platform)
    )
    rows=session.exec(statement).all()
    return[
        {
            'platform':row.platform,
            'status':row.status,
            'people_count':row.people_count
        }
        for row in rows
    ]

@app.get('/salary-expectation-vs-status-for-job/')
def sal_vs_stat(sel_job:str, session:Session=Depends(get_session)):
    statement=(
        select(
            jobs.salary_expectation,
            jobs.status,
            func.count("*").label("people_count")
        )
        .where(jobs.job_role==sel_job)
        .group_by(*[jobs.salary_expectation, jobs.status])
        .order_by(jobs.salary_expectation)
    )
    rows=session.exec(statement).all()
    return [
        {
            "salary_expectation":row.salary_expectation,
            "status":row.status,
            "people_count":row.people_count
        }
        for row in rows
    ]

if __name__ == "__main__":
    main()
