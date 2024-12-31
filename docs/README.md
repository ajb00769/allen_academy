# CS50W Final Project
*Note: Read this documentation in the Obsidian note taking app for the best experience.*
## Table of Contents

1. [[#Introduction]]
2. [[#About the Application]]
3. [[#About the Developer]]
4. [[#Core Design Principles]]
5. [[#Tech Stack]]
6. [[#Planning, Design, and Architecture]]
	1. [[#Application Features]]
		1. [[#Feature Implementation Strategies]]
	2. [[#Software Architecture]]
	3. [[#Data Architecture]]
7. [[#Data Models]]
8. [[#Distinctiveness and Complexity]]

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

With the improvement of internet connectivity and reliability in recent years compared to how it was in the early 90s and 2000s where you'd be lucky enough to have a 1 mbps connection, architectural concepts such as Service Oriented Architecture (SOA) have become more feasible than ever before. An advantage of SOA and APIs for this project is that we can dynamically scale each individual service depending on the traffic.


### Application Features

##### Enrollment
---
Student can enroll to courses and subjects and Employees can select classes they want teach in via the app and are able to view their schedules. The app handles possible schedule conflicts, preventing students from enrolling to a class that has overlapping schedules.

##### Registration
---
Registration system operates via an Employee or the Registrar's office generating a unique registration key for students/employees/parents. Validation exists for registration key account types (i.e. A student cannot enroll as an Employee or Parent because their registration key is tied to a particular account type)

##### Login
---
A separate login service handles user authentication and fetching user details.

##### School Administration
---
A service that's dedicated to department, class, and schedule management to exists since it is expected that traffic for POST/write requests to this service will usually be high especially during the enrollment period and during off-enrollment period, traffic will still be high but mostly GET/read requests.

### Software Architecture

#### Services

- Login
- Registration
- Enrollment and Class Scheduling
- School Administration - paying of salaries, managing employees of the school


### Data Architecture

Although it is considered best practice to create foreign key relationships on tables that reference another table's values I opted to skip adding foreign key relationships in some tables in order to prevent introducing additional overhead in write operations in anticipation of future scaling.

I've also chosen to partition tables by category beforehand in order to reduce overhead, specifically by separating students, parents, and staff so that we can reduce overhead when a query or modification is being made for a user or group of users that belong to the same category especially when the stud

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


### `AllAccount`

| Column Name   | Data Type     | Nullable | escription                                                                   |
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

### `EmployeeDetail`
| Column Name       | Data Type   | Nullable | Description                                                                   |
| ----------------- | ----------- | -------- | ----------------------------------------------------------------------------- |
| `account_id^`     | `CHAR(9)`   | N        | **UNIQUE**, Primary key, Foreign key referencing `EmployeeAccount.account_id` |
| `first_name`      | `CHAR(80)`  | N        | Employee's first name                                                         |
| `middle_name`     | `CHAR(80)`  | Y        | Employee's middle name                                                        |
| `last_name`       | `CHAR(80)`  | N        | Employee's last name                                                          |
| `suffix`          | `CHAR(3)`   | Y        | Suffix (e.g., Jr., Sr., II)                                                   |
| `birthday`        | `DATE`      | N        | Employee's date of birth                                                      |
| `address`         | `CHAR(255)` | N        | Employee's address                                                            |
| `phone`           | `CHAR(16)`  | N        | Employee's phone number                                                       |
| `employment_type` | `CHAR(1)`   | N        | Employee's employment type                                                    |
| `status`          | `CHAR(1)`   | N        | Employee's account status                                                     |

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

### `Department`

A table that contains all school departments. It is self-referencing in the context of parent-child department relationships.

| Column Name    | Data Type       | Nullable | Description                                                                                                                        |
| -------------- | --------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `DEPT_ID*`     | `CHAR(3)`       | N        | **UNIQUE** 3 letter identifier of the department name. User can decide what acronym to give.                                       |
| `DEPT_PARENT^` | `CHAR(3)`       | Y        | Null if the department itself is the main department, contains the `DEPT_ID` of its parent department if it is a child department. |
| `DEPT_NAME`    | `NVARCHAR(120)` | N        | **UNIQUE** to prevent potential duplicate department name creation. Fully spelled out name of the department.                      |
| `DEPT_HEAD^`   | `INT`           | N        | FK `EMPLOYEE_ID`                                                                                                                   |
| `CREATED_BY`   |                 |          |                                                                                                                                    |
| `CREATED_ON`   |                 |          |                                                                                                                                    |
| `UPDATED_BY`   |                 |          |                                                                                                                                    |
| `UPDATED_ON`   |                 |          |                                                                                                                                    |

### `Course`
| Column Name    | Data Type       | Nullable | Description                                   |
| -------------- | --------------- | -------- | --------------------------------------------- |
| `COURSE_CODE*` | `VARCHAR(10)`   | N        | Unique identifier for the course              |
| `COURSE_NAME`  | `NVARCHAR(100)` | N        | Full name of the course                       |
| `TOTAL_UNITS`  | `INT`           | N        | Total units required for the course           |
| `DEPT_ID^`     | `CHAR(3)`       | N        | Reference to `DEPT_ID` in `DEPARTMENTS` table |

### `Subject`
| Column Name       | Data Type       | Nullable | Description                                                                               |
| ----------------- | --------------- | -------- | ----------------------------------------------------------------------------------------- |
| `SUBJECT_CODE*`   | `VARCHAR(10)`   | N        | Unique identifier for the subject                                                         |
| `SUBJECT_TYPE`    | `CHAR(10)`      | N        | Type of the subject (Major, Minor, Elective)                                              |
| `SUBJECT_NAME`    | `NVARCHAR(100)` | N        | Full name of the subject                                                                  |
| `SUBJECT_UNITS`   | `INT`           | N        | Units required for the subject                                                            |
| `WK_CLASS_DURA`   | `FLOAT`         | N        | Weekly class duration measured in hours                                                   |
| `SUBJECT_TUITION` | `FLOAT`         | N        | Tuition fee for the subject per unit<br>(total tuition = subject_units * subject tuition) |
| `DEPT_ID^`        | `CHAR(3)`       | N        | Reference to `DEPT_ID` in `DEPARTMENTS` table                                             |
| `COURSE_CODE^`    | `CHAR(10)`      | N        | FK Reference to Course                                                                    |
| `COURSE_YR_LVL`   | `INT`           | N        | Course year level that the subject is offered                                             |

### `ClassSubject`
| Column Name     | Data Type     | Nullable | Description                                     |
| --------------- | ------------- | -------- | ----------------------------------------------- |
| `CLASS_ID*`     | `INT`         | N        | Unique identifier for the class                 |
| `SUBJECT_CODE^` | `VARCHAR(10)` | N        | Reference to `SUBJECT_CODE` in `SUBJECTS` table |
| `SUBJ_BLOCK`    | `VARCHAR(10)` | N        | Block name of the subject                       |
| `PROFESSOR^`    | `INT`         | N        | Reference to `EMPLOYEE_ID` in `EMPLOYEES` table |
| `SEMESTER`      | `CHAR(1)`     | N        | Semester of the class (1st or 2nd)              |
| `SCHOOL_YEAR`   | `INT`         | N        | School year of the class                        |
| `START_DATE`    | `DATE`        | N        | Start date of the class                         |
| `END_DATE`      | `DATE`        | N        | End date of the class                           |
| `COMPLETED`     | `BOOL`        | N        | Whether the class has been completed            |
| `ACTIVE_FLAG`   | `BOOL`        | N        | Whether the class is active                     |

### `ClassSchedule`
| Column Name    | Data Type | Nullable | Description                                                    |
| -------------- | --------- | -------- | -------------------------------------------------------------- |
| `SCHEDULE_ID*` | `INT`     | N        | Unique identifier for the schedule                             |
| `CLASS_ID^`    | `INT`     | N        | Reference to `CLASS_ID` in `CLASSES` table                     |
| `DAY_OF_WEEK`  | `CHAR(1)` | N        | Day of the week (Monday, Tuesday, Wednesday, Thursday, Friday) |
| `START_TIME`   | `TIME`    | N        | Start time of the class                                        |
| `END_TIME`     | `TIME`    | N        | End time of the class                                          |
| `PURGE_FLAG`   | `BOOL`    | N        | Whether the schedule has been purged                           |


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

## Payloads for Testing

### VALID Reg_Key Input
```
{
	"key_type": "EMP",
	"generated_for": "Potter Harry",
	"year_level": "COLT"
}
```

### VALID Registration Input
#### TEACHER
```
{
	"last_name": "Potter",
	"first_name": "Harry",
	"password": "1234",
	"email": "testemail@email.com",
	"address": "test address",
	"birthday": "1997-05-06",
	"phone": "+1800123456789",
	"key_type": "EMP",
	"employment_type": "T",
	"reg_key": "9de6-a918-1a41-945f",
	"teaching_year_lvl": "COLT"
}
```

#### STUDENT
```
{
	"last_name": "Potter",
	"first_name": "Harry",
	"password": "1234",
	"email": "testemail3@email.com",
	"address": "test address",
	"birthday": "1997-05-06",
	"phone": "+1800123456789",
	"key_type": "STU",
	"reg_key": "2423-720b-f230-26a5"
}
```

### VALID Login Input
```
{
	"username": "testemail@email.com",
	"password": "1234"
}
```

### Sample JWT Response
```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNzA1MTI2OSwiaWF0IjoxNzIyNzMxMjY5LCJqdGkiOiI4NmZkMGJjMTc4YTU0ZTk4OGEzNTgwOWEzZmJiNjBiMyIsInVzZXJfaWQiOiIyMDI0MDAwMDAiLCJhY2NvdW50X3R5cGUiOiJFTVAifQ.Ch0iOEeF_rllZ5oYPhrQ_vFnyWK29CISlh88CsfmNuI",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyNzQyMDY5LCJpYXQiOjE3MjI3MzEyNjksImp0aSI6IjI4MTM2MTBhMDJhMDQxZTJiNjlkODgxMGJiMTI5YWNmIiwidXNlcl9pZCI6IjIwMjQwMDAwMCIsImFjY291bnRfdHlwZSI6IkVNUCJ9.EgbG6DUfmjPwliJz2rN6d9iVo5LkPX-BuHQr9n6tXjQ",
    "user": "testemail@email.com"
}
```


### Testing payloads in schadmin

#### `create_dept`

```
{
    "dept_id": "ENGG",
    "dept_name": "Engineering Department",
    "dept_head": "202400000",
    "created_by": "202400000",
	"created_on": "2024-06-14",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyNDUxOTEzLCJpYXQiOjE3MzI0NDExMTMsImp0aSI6ImI5ZTFjMTNkOWM2NjQ2Mzg4Y2Y4ZWExZGY5YmMxNjZhIiwidXNlcl9pZCI6IjIwMjQwMDAwMSIsImFjY291bnRfdHlwZSI6IkVNUCJ9.AwZ8VDSnSEShtUT0fJT-KELDQty7vwyK5bsEcLMVcvY"
}
```

### `create_course`

```
{
	"dept_id": "ENGG",
	"total_units": 127,
	"course_name": "Electrical Engineering",
	"course_code": "BSEE",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyODg4MjY0LCJpYXQiOjE3MjI4Nzc0NjQsImp0aSI6ImVjMDk2MDZiZDJmZjQ2ODJiOTc0OTgxYTc3ZWI0OTk0IiwidXNlcl9pZCI6IjIwMjQwMDAwMCIsImFjY291bnRfdHlwZSI6IkVNUCJ9.1X_mljNCmWKTZuy_WtRhE6y11CiLo4aKWyrnqSJiQX0"
}
```

### `create_subject`

```
{
    "subject_code": "DC",
    "subject_type": "M",
    "subject_name": "Differential Calculus",
    "subject_units": 4,
    "wk_class_dura": 1,
    "subject_tuition": 1904.21,
    "course_code": "BSEE",
    "course_yr_lvl": "COL1",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyODg4MjY0LCJpYXQiOjE3MjI4Nzc0NjQsImp0aSI6ImVjMDk2MDZiZDJmZjQ2ODJiOTc0OTgxYTc3ZWI0OTk0IiwidXNlcl9pZCI6IjIwMjQwMDAwMCIsImFjY291bnRfdHlwZSI6IkVNUCJ9.1X_mljNCmWKTZuy_WtRhE6y11CiLo4aKWyrnqSJiQX0"
}
```

### `create_subject_block`

```
{
	"block_id": "1234",
    "subject_code": "DC",
    "professor": "202400000",
    "semester": 1,
    "start_date": "2024-06-28",
    "end_date": "2024-09-11",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0ODY4NTczLCJpYXQiOjE3MzQ4NTc3NzMsImp0aSI6ImViMWExOWExZmM2NzQ2MzhhMGU0NDViYjEzNDcyZGNhIiwidXNlcl9pZCI6IjIwMjQwMDAwMCIsImFjY291bnRfdHlwZSI6IkVNUCJ9.ck_NB5Cryqz_6vxL9XpHAbwD0D8cGRH3aPVsnyQ2YGU"
}
```

### `create_schedule`

```
{
	"schedule_id": 1337,
    "block_id": "1234",
    "day_of_wk": "Tue",
    "start_time": "10:30",
    "end_time": "12:30",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0ODY4NTczLCJpYXQiOjE3MzQ4NTc3NzMsImp0aSI6ImViMWExOWExZmM2NzQ2MzhhMGU0NDViYjEzNDcyZGNhIiwidXNlcl9pZCI6IjIwMjQwMDAwMCIsImFjY291bnRfdHlwZSI6IkVNUCJ9.ck_NB5Cryqz_6vxL9XpHAbwD0D8cGRH3aPVsnyQ2YGU"
}
```

```
{
	"schedule_id": 808,
    "block_id": "1234",
    "day_of_wk": "Wed",
    "start_time": "10:30",
    "end_time": "12:30",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1MTg1ODk2LCJpYXQiOjE3MzUxNzUwOTYsImp0aSI6ImJmYWEzZjFmMGJiYTQxYTQ5MmE3ZjU4NTM3MzI2MjhlIiwidXNlcl9pZCI6IjIwMjQwMDAwMCIsImFjY291bnRfdHlwZSI6IkVNUCJ9.t-6BeoIBF6bqy-d7Us0xidY2ThtyAfMVgTsSXOqdU2o"
}
```
### Refresh Token

```
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNzA1MTI2OSwiaWF0IjoxNzIyNzMxMjY5LCJqdGkiOiI4NmZkMGJjMTc4YTU0ZTk4OGEzNTgwOWEzZmJiNjBiMyIsInVzZXJfaWQiOiIyMDI0MDAwMDAiLCJhY2NvdW50X3R5cGUiOiJFTVAifQ.Ch0iOEeF_rllZ5oYPhrQ_vFnyWK29CISlh88CsfmNuI"
}
```

### `enroll_course`
```
{
	"account_id": "202400002",
	"course_code": "BSEE",
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMzg0NzQ5LCJpYXQiOjE3MzIzNzM5NDksImp0aSI6IjgxZjVhZWIzNGQ3MTQ0MDViODdkOWZjMTRiNDcwN2Y5IiwidXNlcl9pZCI6IjIwMjQwMDAwMCIsImFjY291bnRfdHlwZSI6IkVNUCJ9.SEVN5P02BSncTqiFTZwRKUfgK5BDoyrFNtIlIpCU_hQ"
}
```

### `get_course_list`

```
{
	"dept_id": "ENGG",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyNzQyMDY5LCJpYXQiOjE3MjI3MzEyNjksImp0aSI6IjI4MTM2MTBhMDJhMDQxZTJiNjlkODgxMGJiMTI5YWNmIiwidXNlcl9pZCI6IjIwMjQwMDAwMCIsImFjY291bnRfdHlwZSI6IkVNUCJ9.EgbG6DUfmjPwliJz2rN6d9iVo5LkPX-BuHQr9n6tXjQ"
}
```

### `get_subject_list`

```
{
	"course_id": "BSEE",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyNzQyMDY5LCJpYXQiOjE3MjI3MzEyNjksImp0aSI6IjI4MTM2MTBhMDJhMDQxZTJiNjlkODgxMGJiMTI5YWNmIiwidXNlcl9pZCI6IjIwMjQwMDAwMCIsImFjY291bnRfdHlwZSI6IkVNUCJ9.EgbG6DUfmjPwliJz2rN6d9iVo5LkPX-BuHQr9n6tXjQ"
}
```

### `get_subject_schedules`

```
{
	"subject_code": "DC",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyNzQyMDY5LCJpYXQiOjE3MjI3MzEyNjksImp0aSI6IjI4MTM2MTBhMDJhMDQxZTJiNjlkODgxMGJiMTI5YWNmIiwidXNlcl9pZCI6IjIwMjQwMDAwMCIsImFjY291bnRfdHlwZSI6IkVNUCJ9.EgbG6DUfmjPwliJz2rN6d9iVo5LkPX-BuHQr9n6tXjQ"
}
```

### `enroll_subject_schedule`

```
{
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1NDg3NzcxLCJpYXQiOjE3MzU0NzY5NzEsImp0aSI6IjA1ZGVmY2U3ODc3YjRlMTA4YjFmZmRiZGM0Y2UzN2E3IiwidXNlcl9pZCI6IjIwMjQwMDAwMSIsImFjY291bnRfdHlwZSI6IlNUVSJ9.lEniXeUM-cgvme6c7LQ30Q4NOiMnsE2z2e-W6ayklR0",
	"block_id": "1234"
}
```

### Distinctiveness and Complexity

What makes this project distinct from the previous/existing exercises/projects is the utilization of APIs and the separation of concerns by deploying each service into a separate server/container.

This makes everything more complex because of how authentication will be handled from each request from the frontend to the backend where I employed the usage of JSON Web Tokens (JWT) which I learned a lot about as I was implementing the project and what best practices should be followed.

I especially learned not to store critical info in user Cookies because Cookies are prone to manipulation, in one instance I was able to gain Employee-level authorization via the frontend just by editing the Account Type cookie which I have since then removed and any/all transactions are authenticated via the backend so that even in the off-chance that a frontend developer makes the same mistake, the backend will block the requests without proper authorization.

Another thing that contributed to the complexity of this project is the deployment of the services which I orchestrated via docker compose and configuring the Dockerfiles and docker-compose files was also a unique learning experience that made the project a tad bit more complex but also enjoyable. I learned to use .env files and it add them in the .gitignore because that's where the secret keys will be stored and will be created as environment variables during deployment.

I may have missed a lot of other things that also contributed to the complexity of the application but overall I believe it's complex enough to meet the requirements! I hope you have a good time perusing my code!