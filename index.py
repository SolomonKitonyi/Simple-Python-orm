import  sqlite3

class Database:
    def __init__(self,db_name):
        # Initialize db
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_students_table()

    # create students table
    def _create_students_table(self):
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            """
        )
        self.connection.commit()

    def execute(self,query,params = ()):
        self.cursor.execute(query,params)
        self.connection.commit()
    def fetchall(self,query,params=()):
        self.cursor.execute(query,params)
        return self.cursor.fetchall()
    def fetchone(self,query,params=()):
        self.cursor.execute(query,params)
        return self.cursor.fetchone()
    
    def close(self):
        self.connection.close()


class Student:
    def __init__(self,db,name=None,age=None,id=None):
        self.db = db
        self.id = id
        self.name = name
        self.age = age

    def save(self):
        # save or update student
        if self.id:
            self.db.execute(
                "UPDATE students SET name = ?,age = ? WHERE id = ?",
                (self.name,self.age,self.id)
            )
        else:
            self.db.execute(
                "INSERT INTO students (name,age) VALUES (?,?)",
                (self.name,self.age)
            )
            self.id = self.db.cursor.lastrowid
            print(self.db.cursor.lastrowid)

    def delete(self):
        self.db.execute("DELETE FROM students WHERE id= ?",(self.id,))

    @staticmethod
    def all(db):
        rows = db.fetchall("SELECT * FROM students")
        return [Student(db,id=row[0],name= row[1],age=row[2]) for row in rows]
    @staticmethod
    def find(db,id):
        row = db.fetchone("SELECT * FROM students WHERE id = ?",(id,))
        return Student(db,id=row[0],name=row[1],age=row[2]) if row else None
    

if __name__==  "__main__":
    db = Database("students.db")

    student1 = Student(db,name="John",age=20)
    student1.save()

    student2 = Student(db,name="Dann",age=19)
    student2.save()
    
    # fetch all students
    print("All students:")
    for student in Student.all(db):
        print(f"ID: {student.id}, Name: {student.name}, Age: {student.age}")

    # update a student
    student1.name = "Joyce"
    student1.age = 32
    student1.save()
    
    stud = Student.find(db,student1.id)
    print(student1.id)
    print("Found_student:")
    print(f"ID:{stud.id} , Name: {stud.name}, Age: {stud.age}")

    student2.delete()

    print("\nAll  students after deletion: ")
    for student in Student.all(db):
        print(f"ID: {student.id}, Name: {student.name}, Age: {student.age}")

    db.close()