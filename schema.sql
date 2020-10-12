drop table if exists resume_entries;
create table resume_entries (
    id integer primary key autoincrement,
    name text not null,
    age text not null,
    work_exp text not null,
    education_hs text not null,
    education_college text not null,
    graduated text not null
);