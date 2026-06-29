import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE_URL='https://jobapplicationsanalyzer.onrender.com'

st.title("📊 JOB APPLICATIONS ANALYZER")

# function to get all the job roles from the database 
@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_jobs():
    response=requests.get(f'{BASE_URL}/all-job-roles/')
    return response.json()

# function to get all the job types from the database 
@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_job_types():
    response=requests.get(f'{BASE_URL}/all-job-types/')
    return response.json()

# function to get all the platforms from the database 
@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_platforms():
    response=requests.get(f'{BASE_URL}/all-platforms/')
    return response.json()

# function to get all the Company names from the database 
@st.cache_data(ttl=3600)
def get_company_names():
    response=requests.get(f'{BASE_URL}/all-companies/')
    return response.json()

# function to get all the job roles by companies from the database 
@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_jobs_x(selected_job):
    response=requests.get(f"{BASE_URL}/companies-with-x-job/",
                         params={"sel_job": selected_job} )
    return response.json()

# function to get all the job roles and job types by companies from the database 
@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_jobs_x_with_y(selected_job, selected_job_type_y):
    response=requests.get(f"{BASE_URL}/companies-with-x-job-y-job-type/",
                          params={'sel_job':selected_job, 'sel_job_type': selected_job_type_y})
    return response.json()

# function to get all the job roles and job types on a platform from the database 
@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_jobs_x_with_y_on_z(selected_job, selected_job_type_z, selected_company):
    response=requests.get(f'{BASE_URL}/companies-with-x-job-y-job-type-on-platform-z/',
                          params={'sel_job':selected_job, 'sel_job_type':selected_job_type_z, 'sel_company':selected_company})
    return response.json()

# function to get all the experince required for a job in a company from the database 
@st.cache_data(ttl=3600) # Cache results for 1 hour
def get_ery(sel_comp, sel_job):
    response=requests.get(f'{BASE_URL}/get-ery-for-company-and-jobrole/',
                          params={'sel_comp':sel_comp, 'sel_job':sel_job})
    return response.json()

# function to get all the average salary expectation for a job and experience level from the database 
@st.cache_data(ttl=3600) # Cache results for 1 hour
def get_job_vs_exp(job_asp, sel_exp):
    response=requests.get(f'{BASE_URL}/exp-vs-sal-exp/',
                          params={'sel_job':job_asp,'sel_exp':sel_exp})
    return response.json()

# function to get all the platform vs statuses data from the database 
@st.cache_data(ttl=3600) # Cache results for 1 hour
def get_status_vs_platform(sel_job):
    response=requests.get(f'{BASE_URL}/platform-vs-status/',
                          params={'sel_job':sel_job})    
    return response.json()

# function to get all the salaries vs people count with statuses from the database 
@st.cache_data(ttl=3600) # Cache results for 1 hour
def get_statu_vs_sal_exp(sel_job):
    response=requests.get(f'{BASE_URL}/salary-expectation-vs-status-for-job/',
                          params={'sel_job':sel_job})
    return response.json()

# function to calculate the percentages from list of job count
def make_autopct(arr: list):
    def my_autopct(pct):
        val=(pct/np.sum(arr))*100
        return f'{pct:.1f}%'
    return my_autopct

# creating sidebar of insights
st.sidebar.title("Insights Navigator")

# sidebar elements (all the insights with info page)
selected_insight = st.sidebar.radio("Select Insight", 
    [
    "Info",
    "Job Count: Company vs Job",
    "Job Count: Job Vs Job Type",
    "Know Platform Effectiveness: Job Vs Job Type Vs Company",
    "Experience required: Job vs Company",
    "Salary Expectation: Experience Vs Job",
    "Know Platform Effectiveness: Platform vs Statuses",
    "Status: Salary Experience Vs Job Role"
]
)
# calling all jobs, job types and companies
jobs=get_jobs()
job_types=get_job_types()
companies=get_company_names()

# Info page
if selected_insight=="Info":
    st.markdown("""
    ### Transforming Job Application Data into Actionable Insights

    This interactive analytics dashboard explores a dataset of **500 job application records**
    and uncovers trends across companies, job roles, platforms, salary expectations,
    experience requirements, and application outcomes.

    The project demonstrates a complete data analytics pipeline:

    - 🗄️ **PostgreSQL** for data storage
    - ⚡ **FastAPI** for backend APIs
    - 🔗 **SQLModel** for database operations
    - 🐼 **Pandas** for data processing
    - 🔢 **NumPy** for numerical analysis
    - 📈 **Matplotlib** for visualizations
    - 🎨 **Streamlit** for the interactive dashboard

    ---

    ### Key Insights Available

    ✅ Company-wise demand for specific job roles

    ✅ Job role distribution by employment type
    (Internship, Full-Time, Contract, Remote)

    ✅ Platform effectiveness analysis
    (LinkedIn, Naukri, Indeed, Referral, Company Website)

    ✅ Experience requirements for a job role in companies

    ✅ Salary expectation analysis for experience and job role
                
    ✅ Application status trends across platforms

    ✅ Status of applicantions accross Salary expectation brackets Vs Job Roles
                
    ---

    ### Project Goal

    The objective of this project is to demonstrate how modern Python's analytics power
    can be used to build an end-to-end analytics application, from database storage and
    API development to data visualization and interactive exploration.

    Use the navigation panel on the left to explore individual insights.
    """)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Records", "500")

    with col2:
        st.metric("Insights", "7")

    with col3:
        st.metric("Technologies", "7")

    st.info(
    "Select an insight from the navigation panel to begin exploring the dataset."
    )
    with st.container(border=True):
        st.markdown('<strong>Note:</strong> This dataset is <strong>synthetic</strong> for demonstration purposes. The focus of this project is on building a scalable data pipeline architecture with <i>FastAPI</i>, <i>PostgreSQL</i> and <i>Streamlit</i>.', unsafe_allow_html=True)

# First insight
elif selected_insight=="Job Count: Company vs Job":
    with st.container(border=True):
        st.subheader('Select Job Role')
        selected_job_x= st.pills('Select Job',jobs,selection_mode='single',key="jx")

    if selected_job_x:
        data_x=get_jobs_x(selected_job_x)
        df_x=pd.DataFrame(data_x)

        fig_x, ax_x= plt.subplots(figsize=(10,6))
        tab11, tab12=st.tabs(['Pie Chart Representation', 'Bar Chart Representation'])
        with tab11:
            fig=plt.figure(figsize=(10,10))
            plt.pie(df_x['job_count'],
                    autopct= make_autopct(df_x['job_count']),
                    textprops={'fontsize':10},
                    labels=df_x['company_name'])

            st.pyplot(fig)
            st.markdown(f'Percentage of <strong>{selected_job_x}s</strong> in different companies', text_alignment='center', unsafe_allow_html=True)
        with tab12:
            ax_x.barh(df_x['company_name'],df_x['job_count'], color= 'blue', edgecolor='black')

            ax_x.set_title(f'Companies with {selected_job_x} Job')
            ax_x.set_xlabel('Job Count')
            ax_x.set_ylabel('Company Name')
            plt.tight_layout()
            st.pyplot(fig_x)
            st.markdown('Company Name Vs Job Count',text_alignment='center')

            st.markdown(f'Job count of <strong>{selected_job_x}s</strong> in different companies', text_alignment='center', unsafe_allow_html=True)


# Second Insight
elif selected_insight=="Job Count: Job Vs Job Type":
    with st.container(border=True):
        st.subheader('Select Job Role and Job Type')
        selected_job_y= st.pills('Select Job',jobs,selection_mode='single', key='jy')
        selected_job_type_y=st.pills('Select Job Type', job_types, selection_mode='single', key='jty')

    if (selected_job_y and selected_job_type_y):
        data_y=get_jobs_x_with_y(selected_job_y, selected_job_type_y)
        df_y=pd.DataFrame(data_y)

        fig_y, ax_y=plt.subplots(figsize=(10,6))
        tab21, tab22=st.tabs(['Pie Chart Representation', 'Bar Chart Representation'])

        with tab21:
            fig=plt.figure(figsize=(10,10))
            plt.pie(df_y['job_count'], 
                    autopct= make_autopct(df_y['job_count']),
                    textprops={'fontsize':10},
                    labels=df_y['company_name']
                    )

            st.pyplot(fig)
            st.markdown(f'Percentage of <strong>{selected_job_y}</strong> and <strong>{selected_job_type_y}</strong> job type by different companies',unsafe_allow_html=True, text_alignment='center')
        with tab22:
            ax_y.barh(df_y['company_name'], df_y['job_count'], color= 'green', edgecolor='blue')

            ax_y.set_title(f'Companies with {selected_job_y} jobs {selected_job_type_y}')
            ax_y.set_xlabel('Job Count')
            ax_y.set_ylabel('Company Name')
            plt.tight_layout()

            st.pyplot(fig_y)
            st.markdown(f'Count of <strong>{selected_job_y}</strong> and <strong>{selected_job_type_y}</strong> job type by different companies',unsafe_allow_html=True, text_alignment='center')


# Third Insight
elif (selected_insight=="Know Platform Effectiveness: Job Vs Job Type Vs Company"):
    st.header("Know Platform Effectiveness")
    with st.container(border=True):
        st.subheader('Select Job Role, Job Type and Company')
        selected_job_z= st.pills('Select Job',jobs,selection_mode='single', key='jz')
        selected_job_type_z=st.pills('Select Job Type', job_types, selection_mode='single', key='jtz')
        selected_company=st.pills('Select Company',companies,selection_mode='single',key='cz')

    if (selected_job_z and selected_job_type_z and selected_company):
        data_z=get_jobs_x_with_y_on_z(selected_job_z,selected_job_type_z,selected_company)
        df_z=pd.DataFrame(data_z)
        tab31, tab32=st.tabs(['Pie Chart Representation', 'Bar Chart Representation'])

        if (len(df_z)!=0):# to check whether the selected commpany has even posted such job_role and/or job_type

            with tab31:
                fig=plt.figure(figsize=(10,10))
                plt.pie(df_z['job_count'],
                        autopct= make_autopct(df_z['job_count']),
                        textprops={'fontsize':10},
                        labels=df_z['platform'])
                
                st.pyplot(fig)
                st.markdown(f'Percentage of <strong>{selected_job_z}</strong> <strong>{selected_job_type_z}</strong> job type posted by <strong>{selected_company}</strong>', unsafe_allow_html=True, text_alignment='center')
            
            with tab32:
                fig_z, ax_z=plt.subplots(figsize=(10,6))
                ax_z.barh(df_z['platform'], df_z['job_count'], color= 'purple', edgecolor='black')

                ax_z.set_title(f'Platforms on which {selected_job_z} {selected_job_type_z} are posted by {selected_company}')
                ax_z.set_xlabel('Job Count')
                ax_z.set_ylabel('Platform')
                plt.tight_layout()

                st.pyplot(fig_z)
                st.markdown(f'Count of <strong>{selected_job_z}</strong> <strong>{selected_job_type_z}</strong> job type posted by <strong>{selected_company}</strong>', unsafe_allow_html=True, text_alignment='center')
        
        else:
            st.subheader(f"Looks like {selected_company} didn't post any {selected_job_z} job of type {selected_job_type_z} according to the database")

# Fourth Insight
elif (selected_insight=="Experience required: Job vs Company"):
    st.header("Get to know Average Experience required in a Company")
    with st.container(border=True):
        st.subheader('Select Job role and Company')
        selected_job_ery=st.pills('Select Job', jobs,selection_mode='single',key='j_ery')
        selected_company_ery=st.pills('Select Company', companies, selection_mode='single',key='c_ery')

    if (selected_job_ery and selected_company_ery):
        data_ery=get_ery(selected_company_ery, selected_job_ery)
        df_ery=pd.DataFrame(data_ery)
        # getting average experience .Since it is in end right of dataframe
        avg_exp = df_ery['average exp req'].tail(1).iloc[0]
        st.metric(
            f"Average Experience Required in years for {selected_job_ery} in {selected_company_ery}",
            f"{avg_exp:.2f}",
            border=True,
            height='stretch'
        )
        
        fig_ery, ax_ery= plt.subplots(figsize=(10,6))

        ax_ery.barh(df_ery['experience_required'], df_ery['people_count'], color='yellow', edgecolor='black')

        ax_ery.set_title('Experience VS No. of people who got in')
        ax_ery.set_ylabel('Experience Required in Years')
        ax_ery.set_xlabel('People Count')
        plt.tight_layout()

        st.pyplot(fig_ery)

# Insight Five
elif (selected_insight=="Salary Expectation: Experience Vs Job"):
    st.header('Get to know the Salary Expectation of candiadates by selecting Job role and Experience level')
    with st.container(border=True):
        selected_job_asp=st.pills('Select The Job you aspire', jobs, selection_mode='single',key='j_asp')
        experience=st.pills('Select experience',np.arange(0,5),selection_mode='single',key='exp')
    if (selected_job_asp and experience is not None):
        salary_range=get_job_vs_exp(selected_job_asp, experience)
        with st.container(border=True):
            st.markdown(f'For Getting a role of <strong>{selected_job_asp}</strong> with <strong>{experience}</strong> years of experience .', unsafe_allow_html=True)
            st.markdown('The market sentiment looks like this:')
            st.markdown('According to the data the <i>Minimum</i> and <i>Maximum</i> Salary you could expect and The Average: ',unsafe_allow_html=True)
            st.metric(
                f"Min: {salary_range['q1']:.2f} and Max: {salary_range['q3']:.2f}",
                f"Avg: {salary_range['avg']:.2f}",
                border=True,
            )

# Insight Six
elif (selected_insight=="Know Platform Effectiveness: Platform vs Statuses"):
    st.header('Increase your chances of selection from statistics of how many people got in by applying through which platform')
    with st.container(border=True):
        selected_job_p_vs_s=st.pills('Select The Job you aspire', jobs, selection_mode='single',key='j_pvss')
    if (selected_job_p_vs_s):
        plat_and_stat=get_status_vs_platform(selected_job_p_vs_s)
        df_p_vs_s=pd.DataFrame(plat_and_stat)

        # getting a pivot table to get platform as index and statuses as columns
        ptable=pd.pivot_table(df_p_vs_s, index='platform',columns='status', values='people_count', fill_value=0)
        # creating a stacked bar graph
        fig=ptable.plot( kind='bar', stacked=True, figsize=(12,18),
                           title='Platform Vs Status')

        # setting x and y labels
        fig.set_xlabel('Platform')
        fig.set_ylabel('People Count')
        st.pyplot(fig.figure)

# Insight Seven
elif (selected_insight=="Status: Salary Experience Vs Job Role"):
    st.header('Get to Know the best salary bracket of selection')
    with st.container(border=True):
        select_job_know_status=st.pills('Select The Job you aspire', jobs, selection_mode='single',key='j_ks')
    if select_job_know_status:
        stat_vs_sal_exp=get_statu_vs_sal_exp(select_job_know_status)
        df_sal_vs_sal_exp=pd.DataFrame(stat_vs_sal_exp)

        # Grouping by the new bracket and status. Creating salary brakcets of 20k.
        bins = [30000, 50000, 70000, 90000, 110000, 130000, 150000]
        labels = ['30k-50k', '50k-70k', '70k-90k',  '90k-110k', '110k-130k', '130k-140k']
        df_sal_vs_sal_exp['salary_bracket'] = pd.cut(df_sal_vs_sal_exp['salary_expectation'], bins=bins, labels=labels)

        # Creating new dataframe by grouping by salary_bracket and statuses
        bracket_stats = df_sal_vs_sal_exp.groupby(['salary_bracket', 'status']).size().unstack(fill_value=0)

        fig_sal_vs_sal_exp=bracket_stats.plot( kind='bar', stacked=True, figsize=(12,18), title='Salary Expectation Vs People Count and statuses')
        fig_sal_vs_sal_exp.set_xlabel('Salary Brackets')
        fig_sal_vs_sal_exp.set_ylabel('People Count')

        st.pyplot(fig_sal_vs_sal_exp.figure)
