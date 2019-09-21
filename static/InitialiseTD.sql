Create DATABASE TutoringDragons;
Use TutoringDragons;
create table Student
(
    idStudent   int auto_increment,
    firstName   varchar(50)    not null,
    lastName    varchar(45)    not null,
    email       varchar(45)    not null,
    absences    int default 0  not null,
    profScore   int default 0  not null,
    coopScore   int default 45 not null,
    parentEmail varchar(45)    null,
    teacher     varchar(45)    not null,
    constraint idStudent_UNIQUE
        unique (idStudent)
);

alter table Student
    add primary key (idStudent);

create table Tutor
(
    idTutor   int auto_increment,
    firstName varchar(50)          not null,
    lastName  varchar(45)          not null,
    email     varchar(45)          not null,
    admin     tinyint(1) default 0 not null,
    constraint idTutor_UNIQUE
        unique (idTutor)
);

alter table Tutor
    add primary key (idTutor);

create table Pair
(
    idPair    int auto_increment
        primary key,
    idStudent int not null,
    idTutor   int not null,
    constraint Pair_Student_idStudent_fk
        foreign key (idStudent) references Student (idStudent),
    constraint Pair_Tutor_idTutor_fk
        foreign key (idTutor) references Tutor (idTutor)
);

create index Pair_idPair_index
    on Pair (idPair);

create table Session
(
    idPair         int           not null,
    date           int           not null,
    progressReport mediumtext    not null,
    profChange     int default 0 not null,
    coopChange     int default 0 not null,
    primary key (date, idPair),
    constraint Session_Pair_idPair_fk
        foreign key (idPair) references Pair (idPair)
);


