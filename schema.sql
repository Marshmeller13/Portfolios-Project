drop table if exists resume_entries;
create table resume_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    refid INTEGER REFERENCES user(id),
    name text not null,
    age text not null,
    work_exp text not null,
    education_hs text not null,
    education_college text not null,
    graduated text not null,
    skills text not null,
    awards text not null,
    contact text not null
);
drop table if exists profiles;
create table profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES user(id),
    theme blob,
    name text,
    profile_pic blob,
    job text,
    school1 text,
    school1_info blob,
    school2 text,
    school2_info blob,
    school3 text,
    school3_info blob,
    language1 text,
    language2 text,
    language3 text,
    language4 text,
    language5 text,
    language6 text,
    language7 text,
    exp1 text,
    company1 text,
    dur1 blob,
    desc1 blob,
    exp2 text,
    company2 text,
    dur2 blob,
    desc2 blob,
    address blob,
    phone blob,
    email blob,
    website blob

);


drop table if exists uploaded_resumes;
create table uploaded_resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES user(id),
    position text not null,
    resume blob not null


);

drop table if exists user;
create table user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

/*default admin user - password:admin (password is already hashed in below code)*/
INSERT INTO user (username, password)
VALUES ('admin','pbkdf2:sha256:150000$G2L505H1$fb07749916f47042d5afafdbc54257f1008e07267731e6a2c170c699b4f72baa');