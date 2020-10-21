drop table if exists resume_entries;
create table resume_entries (
    name text not null,
    age text not null,
    work_exp text not null,
    education_hs text not null,
    education_college text not null,
    graduated text not null
);



drop table if exists uploaded_resumes;
create table uploaded_resumes (
    resume blob not null


);

drop table if exists user;
create table user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(255) DEFAULT NULL,
    password varchar(255) DEFAULT NULL,
    UNIQUE (username)
);

/*default admin user - password:admin (password is already hashed in below code)*/
INSERT INTO user (username, password)
VALUES ('admin','pbkdf2:sha256:150000$G2L505H1$fb07749916f47042d5afafdbc54257f1008e07267731e6a2c170c699b4f72baa');