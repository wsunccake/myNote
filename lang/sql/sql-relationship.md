# sql relationship

## one-to-one relationship 1:1

```sql
CREATE TABLE Country(
    Pk_Country_Id INT IDENTITY PRIMARY KEY,
    Name VARCHAR(100),
    Officiallang VARCHAR(100),
    Size INT(11),
);

CREATE TABLE UNrepresentative(
    Pk_UNrepresentative_Id INT PRIMARY KEY,
    Name VARCHAR(100),
    Gender VARCHAR(100),
    Fk_Country_Id INT UNIQUE FOREIGN KEY REFERENCES Country(Pk_Country_Id)
);

INSERT INTO Country ('Name','Officiallang',’Size’)
    VALUES ('Nigeria','English',923,768);
INSERT INTO Country ('Name','Officiallang',’Size’)
    VALUES ('Ghana','English',238,535);
INSERT INTO Country ('Name','Officiallang',’Size’)
    VALUES ('South Africa','English',1,219,912);

INSERT INTO UNrepresentative ('Pk_Unrepresentative_Id','Name','Gender','Fk_Country_Id')
    VALUES (51,'Abubakar Ahmad','Male',1);
INSERT INTO UNrepresentative ('Pk_Unrepresentative_Id','Name','Gender','Fk_Country_Id')
    VALUES (52,'Joseph Nkrumah','Male',2);
INSERT INTO UNrepresentative ('Pk_Unrepresentative_Id','Name','Gender','Fk_Country_Id')
    VALUES (53,'Lauren Zuma,'Female',3);

SELECT * FROM Country
SELECT * FROM UNrepresentative;
```


---

## one-to-many relationship 1:M

```sql
CREATE TABLE Car(
    Pk_Car_Id INT PRIMARY KEY,
    Brand VARCHAR(100),
    Model VARCHAR(100)
);

CREATE TABLE Engineer(
    Pk_Engineer_Id INT PRIMARY KEY,
    FullName VARCHAR(100),
    MobileNo CHAR(11),
    Fk_Car_Id INT FOREIGN KEY REFERENCES Car(Pk_Car_Id)
);

INSERT INTO Car ('Brand','Model')
    VALUES ('Benz','GLK350');
INSERT INTO Car ('Brand','Model')
    VALUES ('Toyota','Camry XLE');

INSERT INTO Engineer ('Pk_Engineer_Id','FullName','MobileNo','Fk_Car_Id')
    VALUES(50,'Elvis Young','08038888888',2);
INSERT INTO Engineer ('Pk_Engineer_Id','FullName','MobileNo','Fk_Car_Id')
    VALUES(51,'Bola Johnson','08020000000',1);
INSERT INTO Engineer ('Pk_Engineer_Id','FullName','MobileNo','Fk_Car_Id')
    VALUES(52,'Kalu Ikechi','09098888888',1);
INSERT INTO Engineer ('Pk_Engineer_Id','FullName','MobileNo','Fk_Car_Id')
    VALUES(53,'Smart Wonodu','08185555555',1);
INSERT INTO Engineer ('Pk_Engineer_Id','FullName','MobileNo','Fk_Car_Id')
    VALUES(54,Umaru Suleja','08056676666',1);

SELECT * FROM Car;
SELECT * FROM Engineer;
```


---

## many-to-many relationship M:M

```sql
CREATE TABLE Student(
    StudentID INT(10) PRIMARY KEY,
    Name VARCHAR(100),
);

CREATE TABLE Class(
    ClassID INT(10) PRIMARY KEY,
    Course VARCHAR(100),
);

CREATE TABLE StudentClassRelation(
    StudentID INT(15) NOT NULL,
    ClassID INT(14) NOT NULL,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID),
    UNIQUE (StudentID, ClassID)
);

INSERT INTO Student ('Name')
    VALUES ('Olu Alfonso');
INSERT INTO Student ('Name')
    VALUES ('Amarachi Chinda');

INSERT INTO Class ('Course')
    VALUES ('Biology');
INSERT INTO Class ('Course')
    VALUES ('Chemistry');
INSERT INTO Class ('Type')
    VALUES ('Physics');
INSERT INTO Class ('Type')
    VALUES ('English');
INSERT INTO Class ('Type')
    VALUES ('Computer Science');
INSERT INTO Class ('Type')
    VALUES ('History');

INSERT INTO StudentClassRelation ('StudentID','ClassID')
    VALUES (1,2);
INSERT INTO StudentClassRelation ('StudentID','ClassID')
    VALUES (1,4);
INSERT INTO StudentClassRelation ('StudentID','ClassID')
    VALUES (1,6);
INSERT INTO StudentClassRelation ('StudentID','ClassID')
    VALUES (2,3);
INSERT INTO StudentClassRelation ('StudentID','ClassID')
    VALUES (2,1);
INSERT INTO StudentClassRelation ('StudentID','ClassID')
    VALUES (2,6);
INSERT INTO StudentClassRelation ('StudentID','ClassID')
    VALUES (2,1);

SELECT * FROM Student;
SELECT * FROM Class;
SELECT * FROM StudentClassRelation;
```