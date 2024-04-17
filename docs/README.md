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
8. Developer Set-Up
9. Distinctiveness and Complexity
## Introduction

This purpose of this document is to meticulously detail the thought process, design concepts and implementation strategies employed during the development of this application. It serves as a comprehensive guide including instructions in deploying the application.

This document will also showcase my ability to articulate complex software logic clearly and concisely. Drawing from my own experiences, I aim to make this documentation as accessible and understandable as possible.

The objective of this application is to apply the knowledge that I have gained from the CS50 Web course and from my research and studying. I believe that this application embodies the principles and concepts taught in the course, and it also reflects my willingness to go beyond what was taught and ability to put concepts into practice.

Therefore I hope you, the reader, will find this documentation useful and interesting enough for you to try to deploy and test out the application for yourself.

## About the Application

This ReST API application was created with the intent of being a free and open source project, written solely by myself as my final project submission. This piece of software aims to be a well-designed solution for schools to manage their major functions from account sign-up, enrollment, scheduling, student-parent-employee management and so on. This app's repository will become public after I have submitted it and passed the course.

This application will also serve as an avenue and platform for honing and showcasing my skills in software development by using a high level language such as Python and framework such as Django. I also believe that this is a good way for me to see how my programming ability will evolve as I continue my career.

Hopefully this application will be of some use to some school that's looking to make their school management 

## About the Developer

Hello! I'm Allen, an Application Management Systems Support Engineer with a broad skill set that includes SQL, C, Python, and a keen eye for troubleshooting integration issues, data integrity, and system performance. As of the time of writing my current role involves supporting one of Thailand's largest retail chains with over 2000 branches nationwide, where I've been instrumental in developing hotfixes, applying workarounds, and ensuring data integrity. My work also extends to troubleshooting shell scripts, inspecting packages to find and fix issues, and executing Linux commands to troubleshoot and resolve various system issues. A significant part of my role involves meticulously managing data pipelines, ensuring seamless data flow and addressing any disruptions promptly.

My journey into the world of programming began in October 2022, a departure from my background in Business Administration with a focus on Finance. This shift was sparked by a project undertaken by an old university friend, which eventually evolved into a successful local startup. The complexity and success of this project ignited my fascination with programming, leading me to enroll in the "CS50x: Introduction to Computer Science" course from Harvard University in November 2022. Despite working full-time in digital marketing and PPC for another company, I completed the course in May 2023. This achievement was just the beginning; I continued to expand my knowledge by taking CS50W, Algorithms 1 and 2 online courses from Princeton University, and embarking on multiple personal projects to deepen my understanding of web development, computer science, and programming.

As my passion for programming grew, I sought a career pivot that would allow me to leverage my newfound skills. If you want to connect or discuss programming feel free to reach out to my on LinkedIn!

## Core Design Principles

This application is built on a robust foundation of core design principles that ensure scalability, maintainability, and efficiency. These principles guide the architecture and development practices used, ensuring that the system is both powerful and adaptable to future needs.
### Decoupled Services and Service Oriented Architecture

At the heart of the design is the adoption of a Decoupled Services and Service Oriented Architecture (SOA). This approach allows us to build and scale services independently, enabling us to update, deploy, and scale services without affecting the entire system. This architecture is particularly beneficial in a microservices architecture, where each service can be developed, deployed, and scaled independently.

### REST API Architecture

The REST API architecture is a cornerstone of this project, leveraging Django REST Framework for creating a powerful and flexible API. This framework provides a set of tools and features that simplify the development of RESTful APIs, including authentication, permissions, throttling, caching, filtering, pagination, and versioning. The use of Django REST Framework ensures that the API is both secure and efficient, supporting a wide range of data operations and interactions between the frontend and backend components.

### Selective Database Denormalization and Triggers

I employed Selective Database Denormalization to optimize read performance by reducing the number of joins required to retrieve data. This strategy is complemented by the use of Triggers to maintain data integrity and consistency across the database. Triggers ensure that any changes made to the data are automatically reflected across related tables, reducing the risk of data inconsistency.

### Scalability and Dynamic Scaling of Services

The system is designed with Scalability in mind, allowing it to handle increased loads efficiently through Docker and Kubernetes. The use of these technologies ensures Dynamic Scaling of services to automatically adjust resources based on demand, ensuring that the application remains responsive and available even under heavy load. This approach is crucial for maintaining high performance and user satisfaction.

### Stream and Batch Processing

This application support both Stream and Batch Processing to handle data efficiently. Stream processing is used for real-time data processing, allowing us to react to events as they occur. Batch processing, on the other hand, is used for processing large volumes of data at scheduled intervals via a job scheduler, optimizing resource usage and reducing processing time.

### Modularity, Reusability, and Abstraction

The codebase is designed with Modularity, Reusability, and Abstraction in mind in the context of functions in functional programming. This approach allows us to create components that are independent, reusable, and abstracted from the underlying implementation details. This modular design makes the codebase easier to maintain, extend, and understand.

### Single Responsibility Principle

This piece of software adheres to the Single Responsibility Principle (SRP), ensuring that each component or module in the system has a single responsibility. This principle helps in maintaining a clean and organized codebase, making it easier to manage and extend our application and conforms to decoupling of services.

### Integrity-first - Redundant Data Validation

To ensure data integrity, Redundant Data Validation was implemented between the database and the backend code. This approach involves validating data at multiple points in the data processing pipeline, including at the database level and in the application code. This redundancy helps in catching and correcting errors early in the process, reducing the risk of data corruption.

By adhering to these core design principles, the aim is to build a robust, scalable, and maintainable application that can meet the evolving needs of users and adapt to future challenges.

## Tech Stack

### ReactJS

React was briefly discussed in the course in a small section of the lecture. I chose this as the front-end technology for this application not only because of it was tackled a little during the lecture, but also due to the fact that it is popular and maintainable. It will give institutions a much easier time in finding developers that can maintain the front-end of the application due to its popularity, maintainability, and high availability of talent.

While I have little to no past experience of using React, this is a good opportunity for me to learn the framework. Do consider that I did not dwell too much when it comes to the aesthetics since admittedly I'm not skilled in aesthetic design but I did do my best to make it functional and responsive. I will leave the aesthetic and user experience aspect to the freedom and creativity of the organization's talent.

### Django

Although Django was a project requirement, it nonetheless offers a lot of great features and abstraction for common web operations such as authentication, security, sessions, and more. Since Django is a Python-based web framework it is easier to write and lets the developer focus at a higher level or on the logic itself without having the need to struggle with complex syntax, allowing for shorter development times and faster integration of new features. Hence it was possible for myself alone to develop this application given its scale.

### PostgreSQL

I chose PostgreSQL for my project due to its implementation of Multi-Version Concurrency Control (MVCC), which allows for efficient handling of concurrent transactions without sacrificing data consistency and integrity. This is a significant advantage over other SQL databases that may experience performance degradation due to table locks. MVCC operates by creating multiple versions of a single database record, enabling various transactions to access different versions of one database record without conflicting with one another. This mechanism ensures that transactions can run simultaneously without blocking each other, thereby enhancing the database's performance and responsiveness.

Additionally, I have a preference for open-source solutions because they offer several advantages, including being free and open for public scrutiny. Open-source projects like PostgreSQL benefit from a community-driven development model, which allows for innovation and flexibility. This model ensures that the database can evolve based on the needs and contributions of its users. Additionally, the open-source nature of PostgreSQL means that professional services for it are provided by companies that contribute to the project but do not control its development process, ensuring a healthy ecosystem of support and development

### Docker

I chose Docker for my project due to its ability to create and manage individual containers, which allows for the packaging of applications and their dependencies into separate containers and running them. Docker containers are lightweight and efficient, leveraging the host system’s resources and avoiding the need to duplicate an entire operating system like virtual machines do.

Also, with Docker, scaling up and down is easier because you can simply create a new container with the base image when needed. This approach allows for rapid scaling of applications, as containers can be spun up or down quickly to match the current traffic.


## Planning, Design, and Architecture

With the improvement of internet connectivity and reliability in recent years compared to how it was in the early 90s and 2000s where you'd be lucky enough to have a 1 mbps connection, architectural concepts such as Service Oriented Architecture (SOA) have become more feasible than ever before. An advantage of SOA for this project is that we can dynamically scale each individual service depending on the traffic.

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

### Feature Implementation Strategies

TODO

Classroom attendance, a unique QR code is generated for each student for each class that they will scan as proof of their attendance. The choice of implementing a unique QR code for each student is to prevent students from taking pictures of the QR code and sending it to their absent classmates to take attendance. A timestamp is also recorded when students clock in.

Login Service

Manages login, authentication, and user management

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

## `Register Service`


### `RegistrationKey`
| Column Name      | Data Type   | Nullable | Description                        |
| ---------------- | ----------- | -------- | ---------------------------------- |
| `generated_key^` | `CHAR(19)`  | N        | **UNIQUE**, Primary key            |
| `key_type`       | `CHAR(3)`   | N        | Type of registration key           |
| `generated_for`  | `CHAR(255)` | N        | For whom the key was generated     |
| `key_expiry`     | `DATE`      | N        | Expiry date of the key             |
| `key_used`       | `BOOL`      | N        | Indicates if the key has been used |

### `AllAccountId`
| Column Name     | Data Type | Nullable | Description             |
| --------------- | --------- | -------- | ----------------------- |
| `generated_id^` | `CHAR(9)` | N        | **UNIQUE**, Primary key |

### `StudentAccount`
| Column Name   | Data Type     | Nullable | Description                                                                  |
| ------------- | ------------- | -------- | ---------------------------------------------------------------------------- |
| `account_id^` | `CHAR(9)`     | N        | **UNIQUE**, Primary key, Foreign key referencing `AllAccountId.generated_id` |
| `email`       | `VARCHAR`     | N        | Unique email address                                                         |
| `password`    | `BINARY(255)` | N        | Binary field for storing password                                            |
| `allow_login` | `BOOL`        | N        | Indicates if the student account is allowed to log in                        |

### `StudentDetail`
| Column Name   | Data Type   | Nullable | Description                                                                  |
| ------------- | ----------- | -------- | ---------------------------------------------------------------------------- |
| `account_id^` | `CHAR(9)`   | N        | **UNIQUE**, Primary key, Foreign key referencing `StudentAccount.account_id` |
| `last_name`   | `CHAR(80)`  | N        | Student's last name                                                          |
| `first_name`  | `CHAR(80)`  | N        | Student's first name                                                         |
| `middle_name` | `CHAR(80)`  | Y        | Student's middle name                                                        |
| `suffix`      | `CHAR(3)`   | Y        | Suffix (e.g., Jr., Sr., II)                                                  |
| `birthday`    | `DATE`      | N        | Student's date of birth                                                      |
| `address`     | `CHAR(255)` | N        | Student's address                                                            |
| `phone`       | `CHAR(16)`  | Y        | Student's phone number                                                       |
| `status`      | `CHAR(1)`   | N        | Student's account status                                                     |

### `EmployeeAccount`
| Column Name       | Data Type       | Nullable | Description                                                                                          |
| ----------------- | --------------- | -------- | ---------------------------------------------------------------------------------------------------- |
| `account_id^`     | `CHAR(9)`       | N        | **UNIQUE**, Primary key, Foreign key referencing `AllAccountId.generated_id`                          |
| `email`           | `VARCHAR`       | N        | Unique email address                                                                                 |
| `password`        | `BINARY(255)`   | N        | Binary field for storing password                                                                     |
| `allow_login`     | `BOOL`          | N        | Indicates if the employee account is allowed to log in                                                |

### `EmployeeDetail`
| Column Name       | Data Type       | Nullable | Description                                                                                          |
| ----------------- | --------------- | -------- | ---------------------------------------------------------------------------------------------------- |
| `account_id^`     | `CHAR(9)`       | N        | **UNIQUE**, Primary key, Foreign key referencing `EmployeeAccount.account_id`                         |
| `first_name`      | `CHAR(80)`      | N        | Employee's first name                                                                                 |
| `middle_name`     | `CHAR(80)`      | Y        | Employee's middle name                                                                                |
| `last_name`       | `CHAR(80)`      | N        | Employee's last name                                                                                 |
| `suffix`          | `CHAR(3)`       | Y        | Suffix (e.g., Jr., Sr., II)                                                                            |
| `birthday`        | `DATE`          | N        | Employee's date of birth                                                                              |
| `address`         | `CHAR(255)`     | N        | Employee's address                                                                                    |
| `phone`           | `CHAR(16)`      | N        | Employee's phone number                                                                               |
| `employment_type` | `CHAR(1)`       | N        | Employee's employment type                                                                            |
| `status`          | `CHAR(1)`       | N        | Employee's account status                                                                             |

### `ParentAccount`
| Column Name   | Data Type     | Nullable | Description                                                                  |
| ------------- | ------------- | -------- | ---------------------------------------------------------------------------- |
| `account_id^` | `CHAR(9)`     | N        | **UNIQUE**, Primary key, Foreign key referencing `AllAccountId.generated_id` |
| `email`       | `VARCHAR`     | N        | Unique email address                                                         |
| `password`    | `BINARY(255)` | N        | Binary field for storing password                                            |
| `allow_login` | `BOOL`        | N        | Indicates if the parent account is allowed to log in                         |

### `ParentDetail`
| Column Name    | Data Type   | Nullable | Description                                                                 |
| -------------- | ----------- | -------- | --------------------------------------------------------------------------- |
| `account_id^`  | `CHAR(9)`   | N        | **UNIQUE**, Primary key, Foreign key referencing `ParentAccount.account_id` |
| `first_name`   | `CHAR(80)`  | N        | Parent's first name                                                         |
| `middle_name`  | `CHAR(80)`  | Y        | Parent's middle name                                                        |
| `last_name`    | `CHAR(80)`  | N        | Parent's last name                                                          |
| `suffix`       | `CHAR(3)`   | Y        | Suffix (e.g., Jr., Sr., II)                                                 |
| `birthday`     | `DATE`      | N        | Parent's date of birth                                                      |
| `address`      | `CHAR(255)` | N        | Parent's address                                                            |
| `phone`        | `CHAR(16)`  | N        | Parent's phone number                                                       |
| `relationship` | `CHAR(1)`   | N        | Relationship to the student                                                 |
| `student`      | `CHAR(9)`   | N        | Foreign key referencing `StudentDetail.account_id`                          |

------------- everything below is for other services/for future editing --------------
### `DEPARTMENTS`

A table that contains all school departments. It is self-referencing in the context of parent-child department relationships.

| Column Name    | Data Type       | Nullable | Description                                                                                                                        |
| -------------- | --------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `DEPT_ID*`     | `CHAR(3)`       | N        | **UNIQUE** 3 letter identifier of the department name. User can decide what acronym to give.                                       |
| `DEPT_PARENT^` | `CHAR(3)`       | Y        | Null if the department itself is the main department, contains the `DEPT_ID` of its parent department if it is a child department. |
| `DEPT_NAME`    | `NVARCHAR(120)` | N        | **UNIQUE** to prevent potential duplicate department name creation. Fully spelled out name of the department.                      |
| `DEPT_HEAD^`   | `INT`           | N        | FK `EMPLOYEE_ID`                                                                                                                   |

### `SALARY`
Salary is the monthly wage.

| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `EMPLOYEE_ID^` | `INT` | N |  |
| `SALARY` | `FLOAT` | N | Monthly |
| `CREATED_BY^` | `INT` | N | FK `EMPLOYEE_ID` |
| `CREATE_DATE` | `DATE` | N |  |
| `CHANGED_BY^` | `INT` | N | FK `EMPLOYEE_ID` |
| `CHANGE_DATE` | `INT` | N |  |

### `EMPLOYEE_ATTENDANCE`
| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `EMPLOYEE_ID^` | `INT` | N |  |
| `DATE_TIME_IN` | `DATETIME` | Y |  |
| `DATE_TIME_OUT` | `DATETIME` | Y |  |

### `EMPLOYEE_SALARY_HIST`
| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `EMPLOYEE_ID^` | `INT` | N |  |
| `SALARY_PAID` | `FLOAT` | N |  |
| `DATE_PAID` | `DATE` | N |  |
| `PROMOTION_FLAG` | `BOOL` | Y |  |
| `INCREASE_FLAG` | `BOOL` | Y |  |

### `STUDENT_VIOLATIONS`
| Column Name | Data Type | Nullable | Description |
| --- | --- | --- | --- |
| `STUDENT_ID` | `INT` | N | Reference to `STUDENT_ID` in `CURRENT_STUDENTS` table |
| `VIOLATION_CODE` | `INT` | N | Reference to `VIOLATION_CODE` in `VIOLATION_CODES` table |

### `VIOLATION_CODES`
| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `VIOLATION_CODE*` | `INT` | N |  |
| `DECODE` | `NVARCHAR(255)` | N |  |

### `COURSES`
| Column Name    | Data Type       | Nullable | Description                                   |
| -------------- | --------------- | -------- | --------------------------------------------- |
| `COURSE_CODE*` | `VARCHAR(10)`   | N        | Unique identifier for the course              |
| `COURSE_NAME`  | `NVARCHAR(100)` | N        | Full name of the course                       |
| `TOTAL_UNITS`  | `INT`           | N        | Total units required for the course           |
| `DEPT_ID^`     | `CHAR(3)`       | N        | Reference to `DEPT_ID` in `DEPARTMENTS` table |

### `SUBJECTS`
| Column Name | Data Type | Nullable | Description |
| --- | --- | --- | --- |
| `SUBJECT_CODE*` | `VARCHAR(10)` | N | Unique identifier for the subject |
| `SUBJECT_TYPE` | `CHAR(10)` | N | Type of the subject (Major, Minor, Elective) |
| `SUBJECT_NAME` | `NVARCHAR(100)` | N | Full name of the subject |
| `SUBJECT_UNITS` | `INT` | N | Units required for the subject |
| `WK_CLASS_DURA` | `FLOAT` | N | Weekly class duration measured in hours |
| `SUBJECT_TUITION` | `FLOAT` | N | Tuition fee for the subject |
| `DEPT_ID^` | `CHAR(3)` | N | Reference to `DEPT_ID` in `DEPARTMENTS` table |

### `CLASSES`
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

### `CLASS_SCHEDULES`
| Column Name | Data Type | Nullable | Description |
| --- | --- | --- | --- |
| `SCHEDULE_ID*` | `INT` | N | Unique identifier for the schedule |
| `CLASS_ID^` | `INT` | N | Reference to `CLASS_ID` in `CLASSES` table |
| `DAY_OF_WEEK` | `CHAR(1)` | N | Day of the week (Monday, Tuesday, Wednesday, Thursday, Friday) |
| `START_TIME` | `TIME` | N | Start time of the class |
| `END_TIME` | `TIME` | N | End time of the class |
| `PURGE_FLAG` | `BOOL` | N | Whether the schedule has been purged |

### `STUDENT_SUBJECTS`
| Column Name   | Data Type | Nullable | Description                                                |
| ------------- | --------- | -------- | ---------------------------------------------------------- |
| `STUDENT_ID^` | `INT`     | N        | Reference to `STUDENT_ID` in `CURRENT_STUDENTS` table      |
| `SUBJECT_ID^` | `INT`     | N        | Reference to `Subject_Code` in `SUBJECTS` table            |
| `YEAR`        | `INT`     | N        | Academic year the subject is being studied                 |
| `STATUS`      | `CHAR(1)` | N        | Status of the subject study ('A'ctive, 'P'assed, 'F'ailed) |

### `GRADES`
| Column Name | Data Type | Nullable | Description |
| ---- | ---- | ---- | ---- |
| `GRADE_ID*` | `INT` | N | Unique identifier for each grade entry. |
| `STUDENT_ID^` | `INT` | N | Foreign key referencing `CURRENT_STUDENTS` and `INACTIVE_STUDENTS`. |
| `SUBJECT_ID^` | `INT` | N | Foreign key referencing `SUBJECTS`. |
| `SEMESTER` | `CHAR(1)` | N | Semester of the grade entry. |
| `SCHOOL_YEAR` | `INT` | N | Year of the grade entry. |
| `GRADE_LETTER` | `CHAR(1)` | N | Grade letter (A, B, C, D, F). |
| `GRADE_NUMERIC` | `INT` | N | Numeric representation of the grade (e.g., 90 for A, 80 for B, etc.). |


### DEVELOPMENT NOTES and Considerations:

- create an unclustered index on email since it will be frequently used during login validation
- explore database partitioning especially for student scholarship types
- come up with a credits table which will be used to check if a student can enroll into the subject or year-level because year levels and some subjects have pre-requisites
- create separate relationship table for violations and scholarship status
- passing dates into the API must follow this format: "1995-12-31" or "YYYY-MM-DD"
- frontend must pass  key type based on the frontend directory. there should be a different frontend registration directory for each account type. if the user enters the correct registration key under the wrong account type portal (i.e. student is in the staff registration portal and entered their student key they will get an error that their registration key belongs to a different registration portal - without specifying which portal so we will have 3 layers of protection (1) uniqueness of the registration key, (2) registration key and the name of the person it was generated for must match, (3) registration key must be registered under the correct portal)


## Triggers
```
CREATE OR REPLACE FUNCTION purge_used_reg_keys()
RETURNS TRIGGER AS $$
BEGIN
	IF NEW.key_used = true THEN
		DELETE FROM register_registrationkey WHERE generated_key = OLD.generated_key;
	END IF;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER purge_used_reg_keys_trigger
AFTER UPDATE ON register_registrationkey
FOR EACH ROW
EXECUTE FUNCTION purge_used_reg_keys();

```

## Error Code Mapping

| Error Code  | Description                                                                                                                    |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `AAR-00001` | A required parameter was not given any arguments.                                                                              |
| `AAR-00002` | Arguments passed into the parameter is invalid. Could be that it's not a valid choice or not in the valid format or data type. |
| `AAR-99999` | Unhandled error in endpoint. Please contact the developer of the API with the error message from the log file.                 |


### .ENV file format:

APP_SECRET_KEY=""
DEBUG_MODE=True
DJANGO_ALLOWED_HOSTS="0.0.0.0"

DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD=""
DB_HOST="db"
DB_PORT="5432"

LOGFILE="register_api_logs.log"