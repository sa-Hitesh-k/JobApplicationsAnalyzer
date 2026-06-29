# 📊 Job Applications Analyzer

Transforming Job Application Data into Actionable Insights

An interactive analytics dashboard that processes 500+ job application records and uncovers trends across companies, job roles, platforms, salary expectations, experience requirements, and application outcomes.

---

## 🎯 Project Overview

**Job Applications Analyzer** is a complete end-to-end data analytics pipeline that demonstrates how Python's analytics stack can be used to build production-ready insights from structured data.

The project showcases:
- Data ingestion and storage in PostgreSQL
- RESTful API development with FastAPI
- Data processing and transformation with pandas
- Interactive visualizations with matplotlib
- Real-time dashboard using Streamlit

**Dataset:** 500 job application records (synthetic for demonstration)  
**Insights:** 7 dimensional analyses  
**Technologies:** 7-tech stack (see below)

---

## ✨ Key Insights Available

1. **Company-wise Demand** — Which companies are hiring for specific job roles?
2. **Job Role Distribution** — How are roles distributed across employment types (Internship, Full-Time, Contract, Remote)?
3. **Platform Effectiveness** — Which job platforms (LinkedIn, Naukri, Indeed, Referral) deliver the best results?
4. **Experience Requirements** — What experience level does each job role demand at different companies?
5. **Salary Expectations** — Average salary expectations segmented by experience and job role
6. **Application Status Trends** — How do application statuses vary across job platforms?
7. **Salary vs Status Correlation** — How does application outcome relate to salary expectation brackets?

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| **Database** | PostgreSQL | Persistent data storage |
| **ORM** | SQLModel | Database operations & schema management |
| **Backend API** | FastAPI | RESTful endpoints for data aggregation |
| **Data Processing** | Pandas | Data transformation & pivot tables |
| **Numerical Analysis** | NumPy | Array operations & calculations |
| **Visualizations** | Matplotlib | Charts & graphs |
| **Frontend** | Streamlit | Interactive dashboard & UI |

---

## 📋 Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- `uv` package manager (recommended) or `pip`

### Step 1: Clone & Navigate
```bash
git clone https://github.com/sa-Hitesh-k/JobApplicationsAnalyzer.git
cd JobApplicationsAnalyzer
```

### Step 2: Install Dependencies
```bash
uv pip install -r requirements.txt
```

Or with pip:
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://user:password@localhost:5432/job_analyzer_db
```

### Step 4: Initialize Database
```bash
python DataDumping.py
```

This script:
- Connects to PostgreSQL
- Creates required tables
- Loads the CSV dataset
- Generates aggregated views

---

## 🚀 Running the Application

### Start FastAPI Backend
```bash
uvicorn main:app --reload --port 8501
```
Backend API will be available at: `http://localhost:8501`  
Swagger docs: `http://localhost:8501/docs`

### Start Streamlit Frontend (in another terminal)
```bash
streamlit run Frontend.py
```
Dashboard will open at: `http://localhost:8501`

---

## 📁 Project Structure

```
JobApplicationsAnalyzer/
├── main.py                          # FastAPI backend & endpoints
├── Frontend.py                      # Streamlit dashboard
├── DataDumping.py                  # Database initialization & data loading
├── DF_Creation.py                  # Data transformation utilities
├── job_applications_tracker_dataset.csv  # Source data (gitignored)
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (gitignored)
├── pyproject.toml                 # Project metadata
├── README.md                      # This file
└── .gitignore                     # Git ignore rules
```

---

## 🔌 API Endpoints

All endpoints return JSON responses. Base URL: `http://localhost:8501`

### Get All Job Applications
```
GET /all-applications
```
Returns: Complete dataset with all columns

### Get Aggregated Insights
```
GET /insights/{insight_type}
```

Insight types:
- `company_vs_role` — Company and job role distribution
- `role_vs_type` — Job role vs employment type
- `platform_vs_role` — Platform effectiveness by role
- `experience_vs_role` — Experience requirements
- `salary_vs_experience` — Salary patterns
- `platform_vs_status` — Platform vs application status
- `status_vs_salary` — Outcome vs salary brackets

Example:
```bash
curl http://localhost:8501/insights/platform_vs_status
```

---

## 💡 Usage Examples

### Example 1: View Platform Effectiveness
1. Open dashboard
2. Select "Know Platform Effectiveness: Platform Vs Statuses" from sidebar
3. Explore which platforms have highest selection rates

### Example 2: Analyze Salary Trends
1. Select "Salary Expectation: Experience Vs Job"
2. Filter by job role using sidebar pills
3. See average salary expectations by experience level

### Example 3: Compare Companies
1. Select "Job Count: Company vs Job"
2. Identify which companies are actively hiring
3. Cross-reference with salary expectations

---

## 📊 Data Schema

### Main Tables

**jobs**
```
application_id (PK)
company_name
job_role
application_date
job_type (Internship/Full-Time/Contract/Remote)
platform (LinkedIn/Naukri/Indeed/Referral/Company Website)
status (Applied/Phone Screen/Interview Scheduled/Assessment Pending/Selected/Rejected)
salary_expectation (numeric)
experience_required (numeric in years)
company_rating (numeric)
```

---

## ⚠️ Important Notes

### Dataset Origin
**This dataset is synthetic for demonstration purposes.** The focus of this project is to showcase:
- Data pipeline architecture (not data quality)
- Scalable system design principles
- Full-stack implementation skills

### Production Considerations
For production use with real data:
1. Implement data validation & cleaning pipelines
2. Add authentication & role-based access control
3. Implement rate limiting on API endpoints
4. Add query caching for performance
5. Set up database backups
6. Monitor API performance & uptime

---

## 🚢 Deployment

### Deploy Backend (Render)
1. Push to GitHub
2. Connect Render to repository
3. Set environment variables in Render dashboard
4. Deploy from `main` branch

### Deploy Frontend (Streamlit Cloud)
1. Connect GitHub repo to Streamlit Cloud
2. Point to `Frontend.py`
3. Add `.env` secrets in Streamlit settings
4. Deploy

---

## 🔮 Future Enhancements

- [ ] Add real-world data from multiple job portals via scraping
- [ ] Implement predictive modeling for success probability
- [ ] Add user authentication for personalized dashboards
- [ ] Integrate with actual job APIs (LinkedIn, Indeed)
- [ ] Add export functionality (PDF reports, CSV)
- [ ] Implement advanced filtering & search
- [ ] Add time-series analysis for trend prediction
- [ ] Mobile-responsive design improvements

---

## 🤝 Contributing

This is a portfolio project. For improvements or suggestions, feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Hitesh**  
GitHub: [@sa-Hitesh-k](https://github.com/sa-Hitesh-k)  
Portfolio: [View Projects](#)

---

## 📧 Support

For issues, questions, or feedback:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at `/docs` endpoint

---

## 🎓 Learning Resources Used

- FastAPI Official Documentation
- Pandas Data Manipulation Guide
- Streamlit Component Library
- PostgreSQL Query Optimization
- SQLModel ORM Patterns

---

**Happy Analyzing! 📈**
