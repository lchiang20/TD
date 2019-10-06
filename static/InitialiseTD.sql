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


CREATE TABLE `Session` (
  `idPair` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `progressReport` mediumtext NOT NULL,
  `profChange` int(11) NOT NULL DEFAULT '0',
  `coopChange` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`date`,`idPair`),
  KEY `Session_Pair_idPair_fk` (`idPair`),
  CONSTRAINT `Session_Pair_idPair_fk` FOREIGN KEY (`idPair`) REFERENCES `pair` (`idPair`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

