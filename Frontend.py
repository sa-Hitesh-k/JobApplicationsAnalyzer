import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE_URL='http://127.0.0.1:8000'

st.title("JOB APPLICATIONS ANALYZER")
st.header("Welcome to JAA")

@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_jobs():
    response=requests.get(f'{BASE_URL}/all-job-roles/')
    return response.json()


@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_job_types():
    response=requests.get(f'{BASE_URL}/all-job-types/')
    return response.json()

@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_platforms():
    response=requests.get(f'{BASE_URL}/all-platforms/')
    return response.json()

@st.cache_data(ttl=3600)
def get_company_names():
    response=requests.get(f'{BASE_URL}/all-companies/')
    return response.json()

@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_jobs_x(selected_job):
    response=requests.get(f"{BASE_URL}/companies-with-x-job/",
                         params={"sel_job": selected_job} )
    return response.json()

@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_jobs_x_with_y(selected_job, selected_job_type_y):
    response=requests.get(f"{BASE_URL}/companies-with-x-job-y-job-type/",
                          params={'sel_job':selected_job, 'sel_job_type': selected_job_type_y})
    return response.json()

@st.cache_data(ttl=3600)  # Cache results for 1 hour
def get_jobs_x_with_y_on_z(selected_job, selected_job_type_z, selected_company):
    response=requests.get(f'{BASE_URL}/companies-with-x-job-y-job-type-on-platform-z/',
                          params={'sel_job':selected_job, 'sel_job_type':selected_job_type_z, 'sel_company':selected_company})
    return response.json()


@st.cache_data(ttl=3600)
def get_ery(sel_comp, sel_job):
    response=requests.get(f'{BASE_URL}/get-ery-for-company-and-jobrole/',
                          params={'sel_comp':sel_comp, 'sel_job':sel_job})
    return response.json()

@st.cache_data(ttl=3600)
def get_job_vs_exp(job_asp, sel_exp):
    response=requests.get(f'{BASE_URL}/exp-vs-sal-exp/',
                          params={'sel_job':job_asp,'sel_exp':sel_exp})
    return response.json()

@st.cache_data(ttl=3600)
def get_status_vs_platform(sel_job):
    response=requests.get(f'{BASE_URL}/platform-vs-status/',
                          params={'sel_job':sel_job})    
    return response.json()

@st.cache_data(ttl=3600)
def get_statu_vs_sal_exp(sel_job):
    response=requests.get(f'{BASE_URL}/salary-expectation-vs-status-for-job/',
                          params={'sel_job':sel_job})
    return response.json()

def make_autopct(arr: list):
    def my_autopct(pct):
        val=(pct/np.sum(arr))*100
        return f'{pct:.1f}%'
    return my_autopct

tab1, tab2, tab3, tab4, tab5, tab6 ,tab7= st.tabs([
    "Job Count: Company vs Job",
    "Job Count: Job Vs Job Type",
    "Know Platform Job Vs Job Type Vs Company",
    "Exp. req. for a job in a Company",
    "Salary Expectation: Experience Vs Job",
    "Platform vs Status",
    "status for sal_exp Vs Job_role"
])


jobs=get_jobs()
with tab1:
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
        with tab12:
            ax_x.barh(df_x['company_name'],df_x['job_count'], color= 'blue', edgecolor='black')

            ax_x.set_title(f'Companies with {selected_job_x} Job')
            ax_x.set_xlabel('Job Count')
            ax_x.set_ylabel('Company Name')
            plt.tight_layout()
            st.pyplot(fig_x)
            st.markdown('Company Name Vs Job Count',text_alignment='center')

job_types=get_job_types()
with tab2:
    with st.container(border=True):
        st.subheader('Select Job Role and Job Type')
        selected_job_x= st.pills('Select Job',jobs,selection_mode='single', key='jy')
        selected_job_type_y=st.pills('Select Job Type', job_types, selection_mode='single', key='jty')

    if (selected_job_x and selected_job_type_y):
        data_y=get_jobs_x_with_y(selected_job_x, selected_job_type_y)
        df_y=pd.DataFrame(data_y)

        fig_y, ax_y=plt.subplots(figsize=(10,6))
        ax_y.barh(df_y['company_name'], df_y['job_count'], color= 'green', edgecolor='blue')

        ax_y.set_title(f'Companies with {selected_job_x} jobs {selected_job_type_y}')
        ax_y.set_xlabel('Job Count')
        ax_y.set_ylabel('Company Name')
        plt.tight_layout()

        st.pyplot(fig_y)

        fig=plt.figure(figsize=(10,10))
        plt.pie(df_y['job_count'], 
                autopct= make_autopct(df_y['job_count']),
                textprops={'fontsize':10},
                labels=df_y['company_name']
                )

        st.pyplot(fig)


companies=get_company_names()
with tab3:
    with st.container(border=True):
        st.subheader('Select Job Role, Job Type and Company')
        selected_job_z= st.pills('Select Job',jobs,selection_mode='single', key='jz')
        selected_job_type_z=st.pills('Select Job Type', job_types, selection_mode='single', key='jtz')
        selected_company=st.pills('Select Company',companies,selection_mode='single',key='cz')

    if (selected_job_z and selected_job_type_z and selected_company):
        data_z=get_jobs_x_with_y_on_z(selected_job_z,selected_job_type_z,selected_company)
        df_z=pd.DataFrame(data_z)

        if (len(df_z)!=0):
            fig_z, ax_z=plt.subplots(figsize=(10,3))
            ax_z.barh(df_z['platform'], df_z['job_count'], color= 'purple', edgecolor='black')

            ax_z.set_title(f'Platforms on which {selected_job_z} {selected_job_type_z} are posted by {selected_company}')
            ax_z.set_xlabel('Job Count')
            ax_z.set_ylabel('Platform')
            plt.tight_layout()

            st.pyplot(fig_z)

            fig=plt.figure(figsize=(10,10))
            plt.pie(df_z['job_count'],
                    autopct= make_autopct(df_z['job_count']),
                    textprops={'fontsize':10},
                    labels=df_z['platform'])
            
            st.pyplot(fig)
            st.markdown(f'             Pie Chart representation of {selected_company} posting {selected_job_z} {selected_job_type_z} ')
        
        else:
            st.subheader(f"Looks like {selected_company} didn't post any {selected_job_z} job of type {selected_job_type_z} according to the database")

with tab4:
    with st.container(border=True):
        st.subheader('Select Job role and Company')
        selected_job_ery=st.pills('Select Job', jobs,selection_mode='single',key='j_ery')
        selected_company_ery=st.pills('Select Company', companies, selection_mode='single',key='c_ery')

    if (selected_job_ery and selected_company_ery):
        data_ery=get_ery(selected_company_ery, selected_job_ery)
        df_ery=pd.DataFrame(data_ery)

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

with tab5:
    with st.container(border=True):
        selected_job_asp=st.pills('Select The Job you aspire', jobs, selection_mode='single',key='j_asp')
        experience=st.pills('Select experience',np.arange(0,5),selection_mode='single',key='exp')
    if (selected_job_asp and experience is not None):
        salary_range=get_job_vs_exp(selected_job_asp, experience)
        with st.container(border=True):
            st.markdown(f'For Getting a role of <strong>{selected_job_asp}</strong> with <strong>{experience}</strong> years of experience .', unsafe_allow_html=True)
            st.markdown(f'The market sentiment looks like this:')
            st.markdown(f'According to the data the <i>Minimum</i> and <i>Maximum</i> Salary you could expect and The Average: ',unsafe_allow_html=True)
            st.metric(
                f'Min: {salary_range['q1']:.2f} and Max: {salary_range['q3']:.2f}',
                f'Avg: {salary_range['avg']:.2f}',
                border=True,
            )

with tab6:
    with st.container(border=True):
        selected_job_p_vs_s=st.pills('Select The Job you aspire', jobs, selection_mode='single',key='j_pvss')
    if (selected_job_p_vs_s):
        plat_and_stat=get_status_vs_platform(selected_job_p_vs_s)
        df_p_vs_s=pd.DataFrame(plat_and_stat)
        # st.write(df_p_vs_s)
        ptable=pd.pivot_table(df_p_vs_s, index='platform',columns='status', values='people_count', fill_value=0)
        # st.write(ptable)
        fig=ptable.plot( kind='bar', stacked=True, figsize=(12,18),
                           title='Platform Vs Status')
        # fig = df_p_vs_s.plot(kind='bar', stacked=True, figsize=(12, 6), title='Platform vs Status')
        fig.set_xlabel('Platform')
        fig.set_ylabel('People Count')
        st.pyplot(fig.figure)
        st.write(ptable.loc['Company Website','Rejected']/ptable.loc['Company Website'].sum())
        st.write(ptable.loc['LinkedIn','Rejected']/ptable.loc['LinkedIn'].sum())
        st.write(ptable.iloc[0].loc['Rejected'])

with tab7:
    with st.container(border=True):
        select_job_know_status=st.pills('Select The Job you aspire', jobs, selection_mode='single',key='j_ks')
    if select_job_know_status:
        stat_vs_sal_exp=get_statu_vs_sal_exp(select_job_know_status)
        df_sal_vs_sal_exp=pd.DataFrame(stat_vs_sal_exp)

        bins = [30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 140000]
        labels = ['30k-40k', '40k-50k', '50k-60k','60k-70k', '70k-80k', '80k-90k', '90k-100k', '100k-110k', '110k-120k', '120k-130k', '140k-150k']
        df_sal_vs_sal_exp['salary_bracket'] = pd.cut(df_sal_vs_sal_exp['salary_expectation'], bins=bins, labels=labels)

        # Group by the new bracket and status

        bins = [30000, 50000, 70000, 90000, 110000, 130000, 140000]
        labels = ['30k-50k', '50k-70k', '70k-90k',  '90k-110k', '110k-130k', '140k+']
        df_sal_vs_sal_exp['salary_bracket'] = pd.cut(df_sal_vs_sal_exp['salary_expectation'], bins=bins, labels=labels)


        bracket_stats = df_sal_vs_sal_exp.groupby(['salary_bracket', 'status']).size().unstack(fill_value=0)

        # st.write(bracket_stats)

        fig_sal_vs_sal_exp=bracket_stats.plot( kind='bar', stacked=True, figsize=(12,18), title='Salary Expectation Vs People Count and statuses')
        fig_sal_vs_sal_exp.set_xlabel('Salary Brackets')
        fig_sal_vs_sal_exp.set_ylabel('People Count')

        st.pyplot(fig_sal_vs_sal_exp.figure)
