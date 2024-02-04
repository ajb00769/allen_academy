# CS50W Final Project

*Note: Read this documentation in the Obsidian note taking app for the best experience.*

## Table of Contents

1. [[#Introduction]]
2. [[#About the Application]]
3. [[#About the Developer]]
4. [[#Core Design Principles]]
5. [[#Tech Stack]]
6. [[#Planning, Design, and Architecture]]
	1. [[#Major School Management Activities]]
	2. [[#Application Features]]
		1. [[#Feature Implementation Strategies]]
	3. [[#Software Architecture]]
	4. [[#Data Architecture]]
	5. [[#Application Deployment Strategies]]
	6. [[#Cybersecurity Strategies]]
7. [[#Data Models]]
8. Deployment Instructions
9. Distinctiveness and Complexity
## Introduction

This purpose of this document is to meticulously detail the thought process, design concepts and implementation strategies employed during the development of this application. It serves as a comprehensive guide including instructions in deploying the application.

This document will also showcase my ability to articulate complex software logic in simple, understandable language. I recognize that communication is the key to doing well most professions and I have found that conveying the logic of software in straightforward terms can be a challenging task. Drawing from my own experiences, I aim to make this documentation as accessible and understandable as possible.

The objective of this application is to demonstrate the skills and knowledge that I have accumulated from the CS50 Web course and my personal studies. I believe that this application embodies the principles and concepts taught in the course, and it also reflects the insights that I have gained from my independent study.

Therefore I hope you, the reader, will find this documentation useful and interesting enough for you to try to deploy and test out the application itself.

## About the Application

This web app was created to be a free and open source project, written solely by myself as my final project submission, to manage an entire school's operations digitally with the option of continuous integration and continuous delivery for future features if ever this app gains any popularity whatsoever after I submit this as my final project in the CS50 Web course. This app will become fully open source once I have passed the course.

This app will include many features as enumerated in the [[#Application Features]] section along with the concepts and strategies I've chosen to utilize in implementing said features.

This app will also serves as an avenue and platform for honing my skills in software development by using a high level language such as Python and framework such as Django. I also believe that this is a good experience for me as a future Software Engineer in order to showcase my skills and how they eventually evolve.

In the future I might consider rewriting this entire application using a different language and framework if there is something to gain from doing so such as performance gains required for larger institutions.

## About the Developer

Hi, my name is Allen Jay Bercero from the Philippines.  I am currently employed by a global company specializing in big data and time-sensitive operations. My role is crucial as any delays can significantly impact our business operations. My daily responsibilities involve troubleshooting and resolving SQL incidents, ensuring data accuracy and integrity, and providing comprehensive, round-the-clock support to clients addressing database queries.

I actively participate in client meetings, contributing to discussions and assisting in deployment activities. My role extends to providing application support in production and making optimized code base logic suggestions to the development team for integration into production.

In addition to my daily responsibilities, I am also responsible for studying and understanding the entire software architecture and data flow. I conduct regular architecture reviews to identify and fix architectural problems early. I collaborate with various teams to ensure data accuracy and completeness across platforms.

I also develop and maintain documentation for all data sources, processes, and reporting. I identify opportunities for process improvement and make recommendations to management. I stay updated with the latest trends and technologies in the field of data operations. I also contribute to our internal knowledge base and document resolved incidents.

As an aspiring Software Engineer, I am constantly expanding my knowledge and skills in my free time through project-based learning such as this project. I am committed to leveraging my skills and experience in order to become a more competent and effective Software Engineer. I am eager to bring my passion for software development and my ability to solve complex problems to future projects.

If you are interested in learning more about me, commissioning me for a project, or if you are also from the field of tech and want to talk about some new technology or learn together, then feel free to get in touch with me through my LinkedIn page: https://www.linkedin.com/in/allen-jay-bercero-503b79191/

## Core Design Principles

**Decoupled Services and Service Oriented Architecture** allows for 

Selective Database Denormalization

Scalability and Dynamic Scaling of Services

Stream and Batch Processing

Modularity
Reusability
Abstraction
Single Responsibility Principle

## Tech Stack

##### ReactJS
---
React was briefly discussed in the course in a small section of the lecture. I chose this as the front-end technology for this application not only because of it was tackled a little during the lecture, but also due to the fact that it is popular and maintainable. It will give institutions a much easier time in finding developers that can maintain the front-end of the application due to its popularity, maintainability, and high availability of talent.

While I have little to no past experience of using React, this is a good opportunity for me to learn the framework. Do consider that I did not dwell too much when it comes to the aesthetics since admittedly I'm not skilled in aesthetic design but I did do my best to make it functional and responsive. I will leave the aesthetic and user experience aspect to the freedom and creativity of the organization's talent.

##### Django
---
Although Django is required to be used it offers a lot of abstraction for common web operations such as authentication, security, sessions, and more. Since Django is a Python-based web framework it is easier to write and lets the developer focus at a higher level or on the logic itself without having the need to struggle with complex syntax, allowing for shorter development times and faster integration of new features.

##### PostgreSQL
---


##### Docker
---


##### Kubernetes
---


## Planning, Design, and Architecture

With the improvement of internet connectivity and reliability in recent years compared to how it was in the early 90s and 2000s where you'd be lucky enough to have a 1 mbps connection, architectural concepts such as Service Oriented Architecture (SOA) have become more feasible than ever before. An advantage of SOA for this project is that we can dynamically scale each individual service depending on the traffic.

Here is a sample file structure in implementing SOA in Django:

```
/mywebapp
	Dockerfile
    /mywebapp
        __init__.py
        settings.py
        urls.py
        wsgi.py
    /login
		Dockerfile
        models.py
        ...
    /service1
		Dockerfile
        models.py
        ...
	/service2
		Dockerfile
        models.py
        ...	
	/nginx
		nginx.conf
	/kubernetes
		deployment.yaml
		service.yaml
		ingress.yaml
    manage.py
    docker-compose.yml
```

### Major School Management Activities
1. Staffing
	1. Applying for jobs on a school's website
		1. Applicants can upload their  resume on google drive and just submit the link
2. School Operating Expenses
	I am aware there are other operating expenses for schools such as utility expenses, maintenance, and supplies but for the purposes of this project I want to solely focus on Salaries. Other features can be implemented in the future.
	1. Salaries
3. Student Enrollment
	1. Tuition Fee Calculation and Payment
	2. Class Creation and Scheduling
4. Student Testing and Grading
	1. Entrance Exam Scheduling and Result Posting (Still opt for pen and paper exams)
	2. Student Tests and Quizzes (Online Implementation can involve the quiz starting and ending at a fixed time, no retakes, time limits on questions to prevent cheating for objective tests, browser listens if student switches to another tab or window)
	3. Student Projects
5. Student Discipline
6. Parent Involvement
7. Forecasting and Predictive Analysis



### Application Features

##### Enrollment
---
If a first time enrollee was deemed to have passed the school registrar will proceed to fill in the details of the student in a web form. The account


- Subject and Block Creation
- Department Creation
- Tuition Calculation and Payment Tracking
- School Inventory Management
- Staff Salary Calculator and Attendance Tracker
- Class Scheduling
- Student Grading and Attendance
- Parent Portal
- Upload Subject Syllabus, Pointers with Deadline for Submission
- Online Class Records
- Online Classes Schedules, Assignment Posting, Quizzes
- Notification System (i.e. no class today because of emergency)

#### Feature Implementation Strategies

TODO

### Software Architecture

#### Services

Login and Registration
Enrollment and Class Scheduling
Student Management - i've chosen to separate enrollment and student management services because enrollment is a seasonal event while student management happens all the time, parent portal is also included here, this will be the service that gets the most amount of traffic
School Administration - paying of salaries, managing employees of the school



### Data Architecture

Although it is considered best practice to create foreign key relationships on tables that reference another table's values I opted to skip adding foreign key relationships in some tables in order to prevent introducing additional overhead in write operations in anticipation of future scaling.

I've also chosen to partition tables by category beforehand in order to reduce overhead, specifically by separating students, parents, and staff so that we can reduce overhead when a query or modification is being made for a user or group of users that belong to the same category especially when the stud

### Application Deployment Strategies

Minify and tree shake front end before deployment.

### Cybersecurity Strategies


## Data Models

The column with an asterisk (`*`) is the primary key and the column with a caret (`^`) are the foreign keys.

##### `CURRENT_STUDENTS`

Clustered by `YEAR_LEVEL`

| Column Name | Data Type | Nullable  | Description |
| ---- | ---- | ---- | ---- |
| `STUDENT_ID^` | `INT` | N | **UNIQUE** identifier for each student that's exactly 9 digits long. Starts with the year the student first enrolled followed by a sequential number based on the order of enrollment for that year. |
| `FIRST_NAME` | `NVARCHAR(80)` | N | Student's First Name |
| `MIDDLE_NAME` | `NVARCHAR(80)` | Y | Student's Middle Name |
| `LAST_NAME` | `NVARCHAR(80)` | N | Student's Last Name |
| `SUFFIX` | `VARCHAR(3)` | Y | Valid values are `JR, SR, II, III, IV, V` |
| `DOB` | `DATE` | N | Student's date of birth |
| `HOME_ADDRESS` | `NVARCHAR(255)` | N | Student's home address |
| `STATUS` | `CHAR(1)` | N | Valid values are `'A'`ctive,  `'E'`xpelled, `'N'`ew Account, `'S'`uspended, `'G'`raduated, `'D'`ropped Out, `'X'` did not re-enroll.<br>Default `'N'`. |
| `SCHOLAR_TYPE` | `CHAR(1)` | N | Valid values are: `'N'`ot a scholar, `'H'`alf Scholar, `'F'`ull Scholar. Default `'N'`. |
| `HAS_VIOLATIONS` | `BOOL` | N | Default `false` |
| `YEAR_LEVEL` | `CHAR(3)` | N | Valid values are `ES1-ES6 for Elementary School, MS1-MS4 for Middle School, HS1-HS4 for High School, CL1-CL8 for College Level, PHD for Doctorate Degrees, MST for Masters Degrees, LAW for Law Degrees` |

##### `INACTIVE_STUDENTS`

This table is for alumni or students that are no longer with the school, it will mostly be used for former students to get their diplomas, transcripts same schema as `CURRENT_STUDENTS` except for additional column for inactivity reason 'E'xpelled 'T'ransferred 'D'ropped Out or 'X' did not re-enroll. Table clustered by `REASON`

| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `STUDENT_ID^` | `INT` | N | Student's **UNIQUE** identifier |
| `FIRST_NAME` | `NVARCHAR(80)` | N | Student's First Name |
| `MIDDLE_NAME` | `NVARCHAR(80)` | Y | Student's Middle Name |
| `LAST_NAME` | `NVARCHAR(80)` | N | Student's Last Name |
| `SUFFIX` | `VARCHAR(3)` | Y | Valid values are `JR, SR, II, III, IV, V` |
| `DOB` | `DATE` | N | Student's date of birth |
| `HOME_ADDRESS` | `NVARCHAR(255)` | N | Student's home address |
| `HIGHEST_YR`<br> | `INT` | N | Highest year level attended in the school |
| `LAST_YR_ATT` | `INT` | N | Last year attended |
| `REASON` | `CHAR(1)` | N | Valid values are:`'G'`raduated, `'E'`xpelled, `'D'`ropped out, `'X'` did not re-enroll |

##### `GRADUATES`

Although records exist in `INACTIVE_STUDENTS.REASON` the purpose of this table is to keep track of a student that has graduated in the same school across multiple year levels and degrees. Also serves as a **denormalized** table for quick referencing. Table clustered by `COURSE_CODE`

| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `STUDENT_ID` | `INT` | N | Student's identifier code, not unique because of multiple rows with the same student ID if they graduated across multiple year levels and courses. |
| `FULL_NAME` | `NVARCHAR(255)` | N | Concatenated full name of the student following the format `LAST_NAME, FIRST_NAME MIDDLE_NAME SUFFIX` |
| `COURSE_CODE^` | `NVARCHAR(255)` | N |  |
| `GRAD_YEAR` | `INT` | N | Year the student graduated from the course |
##### `STUDENT_ACCOUNTS`

A one column table containing all taken student ids, table is just used for keeping track of all generated student id numbers so far. Used for user authentication as well.

| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `STUDENT_ID*` | `INT` | N | **UNIQUE** student identifier generated by the system |
| `PW_HASH` | `CHAR(64)` | N | SHA-256 encrypted password |

##### `DEPARTMENTS`

A table that contains all school departments. It is self-referencing in the context of parent-child department relationships.

| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `DEPT_ID*` | `CHAR(3)` | N | **UNIQUE** 3 letter identifier of the department name. User can decide what acronym to give. |
| `DEPT_PARENT^` | `CHAR(3)` | Y | Null if the department itself is the main department, contains the `DEPT_ID` of its parent department if it is a child department. |
| `DEPT_NAME` | `NVARCHAR(120)` | N | **UNIQUE** to prevent potential duplicate department name creation. Fully spelled out name of the department. |
| `DEPT_HEAD^` | `INT` | N | FK `EMPLOYEE_ID` |

##### `EMPLOYEES`

Partition by `EMP_TYPE`

| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `EMPLOYEE_ID^` | `INT` | N | **UNIQUE** |
| `FIRST_NAME` | `NVCARCHAR(80)` | N | Employee's first name |
| `MIDDLE_NAME` | `NVCARCHAR(80)` | Y | Employee's middle name |
| `LAST_NAME` | `NVCARCHAR(80)` | N | Employee's last name |
| `SUFFIX` | `VARCHAR(3)` | Y | Valid values are `JR, SR, II, III, IV, V` |
| `DOB` | `DATE` | N | Employee's date of birth |
| `HOME_ADDRESS` | `NVACHAR(255)` | N |  |
| `EMP_TYPE` | `CHAR(1)` | N | Valid values are: `'T'`eacher, `'D'`ean, , `S`taff, |
| `EMP_STATUS` | `CHAR(1)` | N | Valid values are: `'R'`egular, `'P'`robationary, `S`uspended, `'T'`erminated |
| `STATUS_CHG` | `BOOL` | N | Default `false` |
| `STAT_CHG_BY` | `INT` | Y | Self referencing column, references the employee id of the person who changed the employee's status. |
| `STAT_CHG_DATE` | `DATE` | Y |  |
| `HIRED_BY` | `INT` | N |  |
| `HIRE_DATE` | `DATE` | N |  |
| `SUPERVISOR` | `INT` | N |  |
| `DEPARTMENT^` | `CHAR(3)` | N | Shows what department the staff belongs do. References the department ID in the Departments table |

##### `EMPLOYEE_ACCOUNTS`
| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `EMPLOYEE_ID*` | `INT` | N | **UNIQUE** employee identifier generated by the system |
| `PW_HASH` | `CHAR(64)` | N | SHA-256 encrypted password |

##### `SALARY`
Salary is the monthly wage.

| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `EMPLOYEE_ID^` | `INT` | N |  |
| `SALARY` | `FLOAT` | N | Monthly |
| `CREATED_BY^` | `INT` | N | FK `EMPLOYEE_ID` |
| `CREATE_DATE` | `DATE` | N |  |
| `CHANGED_BY^` | `INT` | N | FK `EMPLOYEE_ID` |
| `CHANGE_DATE` | `INT` | N |  |

##### `EMPLOYEE_ATTENDANCE`
| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `EMPLOYEE_ID^` | `INT` | N |  |
| `DATE_TIME_IN` | `DATETIME` | Y |  |
| `DATE_TIME_OUT` | `DATETIME` | Y |  |

##### `EMPLOYEE_SALARY_HIST`
| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `EMPLOYEE_ID^` | `INT` | N |  |
| `SALARY_PAID` | `FLOAT` | N |  |
| `DATE_PAID` | `DATE` | N |  |
| `PROMOTION_FLAG` | `BOOL` | Y |  |
| `INCREASE_FLAG` | `BOOL` | Y |  |

##### `PARENT_ACCOUNTS`
| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `PARENT_USER_ID` | `INT` |  |  |
| `PW_HASH` | `CHAR(64)` |  |  |

##### `PARENT_USER`
| Column Name | Data Type | Nullable | Description |
| --- | --- | --- | --- |
| `FIRST_NAME` | `NVARCHAR(80)` | N | Parent's First Name |
| `MIDDLE_NAME` | `NVARCHAR(80)` | Y | Parent's Middle Name |
| `LAST_NAME` | `NVARCHAR(80)` | N | Parent's Last Name |
| `PHONE_NUMBER` | `VARCHAR(15)` | N | Parent's Phone Number |
| `RELATIONSHIP` | `CHAR(1)` | N | Relationship to the student ('M'other, 'F'ather, 'S'ibling, 'R'elative) |
| `CHILD_ID` | `INT` | N | Reference to `STUDENT_ID` in `CURRENT_STUDENTS` table |

##### `STUDENT_VIOLATIONS`
| Column Name | Data Type | Nullable | Description |
| --- | --- | --- | --- |
| `STUDENT_ID` | `INT` | N | Reference to `STUDENT_ID` in `CURRENT_STUDENTS` table |
| `VIOLATION_CODE` | `INT` | N | Reference to `VIOLATION_CODE` in `VIOLATION_CODES` table |

##### `VIOLATION_CODES`
| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `VIOLATION_CODE*` | `INT` | N |  |
| `DECODE` | `NVARCHAR(255)` | N |  |

##### `COURSES`
| Column Name | Data Type | Nullable | Description |
| --- | --- | --- | --- |
| `COURSE_CODE*` | `VARCHAR(10)` | N | Unique identifier for the course |
| `COURSE_NAME` | `NVARCHAR(100)` | N | Full name of the course |
| `TOTAL_UNITS` | `INT` | N | Total units required for the course |
| `DEPT_ID^` | `CHAR(3)` | N | Reference to `DEPT_ID` in `DEPARTMENTS` table |

##### `SUBJECTS`
| Column Name | Data Type | Nullable | Description |
| --- | --- | --- | --- |
| `SUBJECT_CODE*` | `VARCHAR(10)` | N | Unique identifier for the subject |
| `SUBJECT_TYPE` | `CHAR(10)` | N | Type of the subject (Major, Minor, Elective) |
| `SUBJECT_NAME` | `NVARCHAR(100)` | N | Full name of the subject |
| `SUBJECT_UNITS` | `INT` | N | Units required for the subject |
| `WK_CLASS_DURA` | `FLOAT` | N | Weekly class duration measured in hours |
| `SUBJECT_TUITION` | `FLOAT` | N | Tuition fee for the subject |
| `DEPT_ID^` | `CHAR(3)` | N | Reference to `DEPT_ID` in `DEPARTMENTS` table |

##### `CLASSES`
| Column Name | Data Type | Nullable | Description |
| --- | --- | --- | --- |
| `CLASS_ID*` | `INT` | N | Unique identifier for the class |
| `SUBJECT_CODE^` | `VARCHAR(10)` | N | Reference to `SUBJECT_CODE` in `SUBJECTS` table |
| `SUBJ_BLOCK` | `VARCHAR(10)` | N | Block name of the subject |
| `PROFESSOR^` | `INT` | N | Reference to `EMPLOYEE_ID` in `EMPLOYEES` table |
| `SEMESTER` | `CHAR(1)` | N | Semester of the class (Spring, Summer, Fall) |
| `SCHOOL_YEAR` | `INT` | N | School year of the class |
| `START_DATE` | `DATE` | N | Start date of the class |
| `END_DATE` | `DATE` | N | End date of the class |
| `COMPLETED` | `BOOL` | N | Whether the class has been completed |
| `ACTIVE_FLAG` | `BOOL` | N | Whether the class is active |

##### `CLASS_SCHEDULES`
| Column Name | Data Type | Nullable | Description |
| --- | --- | --- | --- |
| `SCHEDULE_ID*` | `INT` | N | Unique identifier for the schedule |
| `CLASS_ID^` | `INT` | N | Reference to `CLASS_ID` in `CLASSES` table |
| `DAY_OF_WEEK` | `CHAR(1)` | N | Day of the week (Monday, Tuesday, Wednesday, Thursday, Friday) |
| `START_TIME` | `TIME` | N | Start time of the class |
| `END_TIME` | `TIME` | N | End time of the class |
| `PURGE_FLAG` | `BOOL` | N | Whether the schedule has been purged |

##### `STUDENT_SUBJECTS`
| Column Name | Data Type | Nullable | Description |
| --- | --- | --- | --- |
| `STUDENT_ID^` | `INT` | N | Reference to `STUDENT_ID` in `CURRENT_STUDENTS` table |
| `SUBJECT_ID^` | `INT` | N | Reference to `Subject_Code` in `SUBJECTS` table |
| `YEAR` | `INT` | N | Academic year the subject is being studied |
| `STATUS` | `CHAR(1)` | N | Status of the subject study ('A'ctive, 'P'assed, 'F'ailed) |

##### `GRADES`
| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `GRADE_ID*` | `INT` | N | Unique identifier for each grade entry. |
| `STUDENT_ID^` | `INT` | N | Foreign key referencing `CURRENT_STUDENTS` and `INACTIVE_STUDENTS`. |
| `SUBJECT_ID^` | `INT` | N | Foreign key referencing `SUBJECTS`. |
| `SEMESTER` | `CHAR(1)` | N | Semester of the grade entry. |
| `SCHOOL_YEAR` | `INT` | N | Year of the grade entry. |
| `GRADE_LETTER` | `CHAR(1)` | N | Grade letter (A, B, C, D, F). |
| `GRADE_NUMERIC` | `INT` | N | Numeric representation of the grade (e.g., 90 for A, 80 for B, etc.). |


## Others
- Use django rest API
- apache spark delta lake storage
- react frontend
- microservices and service oriented architecture
- separate hosting for each service