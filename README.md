# Roast Me - DE-LON16 Final Project

Welcome to the repository of **Roast Me**, the final group project from the DE-LON16 Data Engineering cohort. This project is a culmination of all the skills we developed during the Generation bootcamp, wrapped up in a realistic, agile, and collaborative simulation of a workplace environment.

## 🚀 Elevator Pitch
Roast Me is a fully scalable cloud-based ETL pipeline, designed not only to address real-world business needs but also to reflect our journey of becoming job-ready data engineers. As a team, we’ve explored and implemented essential tools used in the industry, such as Grafana for monitoring and data visualisation, Amazon Redshift for scalable cloud-based data warehousing, and CloudWatch for infrastructure metrics and alerting. Learning these tools in context has helped us build a production-style solution that can handle growing data demands, reveal trends, and provide actionable insights.

This project doesn’t just demonstrate our technical knowledge — it showcases our ability to collaborate in an agile team, use GitHub Actions for CI/CD, and simulate real stakeholder interactions to deliver a working product.

## 👥 Team Roast Me
- Team members: Grace, Ihsanul, Stephen, Anthony, Bakhta.
- A collaborative group of aspiring data engineers from the DE-LON16 cohort
- Scrum Master: Rotated every sprint to ensure shared leadership and agile facilitation
- Product Owner: Jas, Jess and Brian

## 🧠 Project Overview
**Client Background:**
The client operates a rapidly expanding coffee chain across the UK. They currently use outdated software that only supports individual branch-level reporting. As a result, data aggregation is time-consuming and lacks depth.

**Client Pain Points:**
- Difficulty in identifying trends across branches
- No centralised data analytics
- Time-consuming manual data handling

**Our Mission:**
Deliver a robust ETL pipeline that:
- Extracts daily CSV files from each branch
- Transforms the data (removes PII, normalises to 3NF)
- Loads the cleaned data into a Redshift data warehouse
- Enables reporting and business intelligence insights

## 📦 Repo Structure
```
├── data/                   # Sample dummy CSVs
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/                 # Unit tests
├── diagrams/              # Architecture and DB diagrams
├── scripts/               # SQL scripts and automation
├── docker-compose.yml     # Local development containers
├── README.md
└── .github/workflows/     # GitHub Actions for CI/CD
```

## 🔨 Tech Stack

- **Python** – Core language for ETL scripts and transformation logic
- **Amazon S3** – Storage for uploaded CSVs from branches
- **AWS Lambda** – Serverless compute for ETL jobs
- **Amazon Redshift** – Cloud data warehouse for analytics
- **PostgreSQL** – Used for local testing and schema validation
- **AWS CloudWatch** – Log aggregation and performance monitoring
- **Grafana** – Dashboards for KPIs and data trends
- **AWS CloudFormation** – Infrastructure-as-code to automate resource setup
- **GitHub Actions** – CI/CD pipeline for testing and automation


## 📅 Agile Ways of Working
- **Daily Stand-ups**: Morning check-ins to set goals and unblock teammates
- **End-of-Day Roundups**: Share feelings, progress, and reflections
- **Weekly Retrospectives**: Evaluate team dynamics, celebrate wins, and course-correct
- **Sprint Planning**: Story points, clear ticket assignments, and backlog grooming

## 🎯 Sprint Highlights

### Sprint 1 - Local ETL MVP
- Set up Docker-based local dev environment
- Created initial PoC for extract/load with dummy CSVs
- Transformed CSVs into 3NF database schema
- Created architecture diagram and database schema
- Wrote initial unit tests and CI/CD pipeline

### Sprint 2 - Move to the Cloud
- Migrated pipeline to AWS (S3, Lambda, Redshift)
- Removed all PII from data and enhanced data quality
- Built initial dashboards in Grafana for revenue & volume
- Monitored performance metrics with CloudWatch

### Sprint 3 - Consolidation & Presentation
- Polished CI/CD and ETL process
- Finalised architecture and DB diagrams
- Enhanced communication/documentation process
- Identified areas for skill development (DevOps, visualisation, SQL tuning)
  
📌 **Sprint 4 (active)**  
- Enhancing ETL logic for production-ready transformation
- Packaging deployment-ready Lambda functions
- Refining modular code using helper modules (`/utils`)
- Validating data ingestion and transformation steps

🧠 *This stage focuses on technical application, collaboration, and maintaining deployment readiness.*

🧩 Team Communication & Collaboration
Microsoft Teams – Used for real-time communication, daily stand-ups, and sprint planning meetings.

Lucidchart / Lucidspark – Utilized for visualizing data workflows, database schema, and planning sprint.

GitHub Projects Board – Acts as the central backlog tracker for sprint tasks, PR reviews, and branch workflows.

Collaboration Practices – Team members collaborate using:

✅ Pair programming for focused feature development

🤝 Mob programming for problem-solving and cross-team knowledge sharing

🔄 Regular code reviews and PR discussions to ensure clean, consistent delivery

📌 As a team, we prioritize transparency, shared ownership, and continuous feedback.

## 💡 Definition of Done
- [x] Code merged via PR with at least 1 review
- [x] Unit tests included and passing
- [ ] Functionality demoed locally or via Lambda *(in progress)*
- [x] Documentation updated
- [x] Ticket moved to "Done"


## 🧪 Testing & QA
- [ ] Unit tests for all core ETL functions *(in progress)*
- [x] Manual validation with sample datasets 
- [x] Integration testing with Docker Compose
- [x] GitHub Actions run tests on every push/PR

  


## 🔍 What We Learned (So Far)
💼 Agile collaboration within a remote, cross-functional team

☁️ Building and debugging cloud-native ETL pipelines

🧹 Effective data transformation and cleaning practices

📚 The value of clear documentation, retrospectives, and ongoing communication!

## 🎯 What’s Next (Sprint 5)

📊 Refine dashboard KPIs based on stakeholder feedback

🔄 Enhance error handling and increase pipeline resilience

🛠️ Strengthen CI/CD pipeline to support automated testing and future deployment steps

## 📸 Project Diagrams & Visuals
Find our architecture diagram and DB schema inside the `/diagrams` folder.

---

This README represents not just our technical project, but the journey of a team learning how to build together, reflect, and deliver like professional data engineers.

Thanks for checking out Roast Me ☕

