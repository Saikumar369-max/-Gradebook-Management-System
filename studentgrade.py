import json


class Student:
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.grades = {}

    def add_marks(self, subject, marks):
        if 0 <= marks <= 100:
            self.grades[subject] = marks
        else:
            print("Marks must be between 0 and 100.")

    def calculate_gpa(self):
        if not self.grades:
            return 0.0
        total = sum(self.grades.values())
        return total / len(self.grades)

    def show_details(self):
        print(f"\nName: {self.name}\nRoll Number: {self.roll_number}")
        print("Subjects and Marks:")
        for subject, marks in self.grades.items():
            print(f" {subject}: {marks}")
        print("GPA:", self.calculate_gpa())


    def to_dict(self):
        return {
            "name": self.name,
            "roll_number": self.roll_number,
            "grades": self.grades
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(data["name"], data["roll_number"])
        student.grades = data["grades"]
        return student


class Gradebook:
    def __init__(self):
        self.students = {}

    def add_student(self, student):
        if student.roll_number in self.students:
            print(f"Student with roll number {student.roll_number} already exists.")
        else:
            self.students[student.roll_number] = student

    def remove_student(self, roll_number):
        if roll_number in self.students:
            del self.students[roll_number]
            print("Student removed successfully.")
        else:
            print(f"No student found with roll number {roll_number}.")

    def get_student(self, roll_number):
        student = self.students.get(roll_number)
        if student:
            student.show_details()
        else:
            print(f"No student found with roll number {roll_number}.")
    
    def update_marks(self, roll_number, subject, marks):
        student = self.students.get(roll_number)
        if student:
            if 0 <= marks <= 100:
                student.grades[subject] = marks
                print(f"Marks for {subject} updated to {marks} for student {student.name}.")
            else:
                print("Marks must be between 0 and 100.")
        else:
            print(f"No student found with roll number {roll_number}.")
    
    def top_performer(self):
        if not self.students:
            print("No students in gradebook.")
            return
        top_student = max(self.students.values(), key=lambda s: s.calculate_gpa())
        print("\n--- Top Performer ---")
        top_student.show_details()

    def top_k_performers(self, k):
        if not self.students:
            print("No students in gradebook.")
            return
        if k <= 0:
            print("Please enter a positive number for k.")
            return

        total_students = len(self.students)
        if k > total_students:
            print(f"Only {total_students} students available. Showing all of them instead.")

        sorted_students = sorted(
            self.students.values(),
            key=lambda s: s.calculate_gpa(),
            reverse=True
        )
        print(f"\n--- Top {min(k, total_students)} Performers ---")
        for i, student in enumerate(sorted_students[:k], start=1):
            print(f"\nRank {i}:")
            student.show_details()


    def list_all_students(self):
        if not self.students:
            print("There are no students.")
        else:
            print("\n--- All Students ---")
            for student in self.students.values():
                print(f"Name: {student.name}, Roll Number: {student.roll_number}")

    def save_to_file(self, file_name):
        data = [student.to_dict() for student in self.students.values()]
        with open(file_name, "w") as f:
            json.dump(data, f, indent=4)
        print("Gradebook saved successfully.")

    def load_from_file(self, file_name):
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
                self.students = {
                    student_data["roll_number"]: Student.from_dict(student_data)
                    for student_data in data
                }
            print("Gradebook loaded successfully.")
        except FileNotFoundError:
            print("File not found. Starting with an empty gradebook.")
        except json.JSONDecodeError:
            print("Invalid file format. Could not load gradebook.")


def main():
    gb = Gradebook()
    gb.load_from_file("studentsrecords.json")

    while True:
        print("\n--- Gradebook Menu ---")
        print("1. Add student")
        print("2. Remove student")
        print("3. View student details")
        print("4. List all students")
        print("5. Save details")
        print("6. update marks")
        print("7. Top performer")
        print("8. Top K performers")
        print("9. Exit")

        try:
            choice = int(input("Enter your choice (1-9): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            name = input("Enter student name: ")
            try:
                roll = int(input("Enter student roll number: "))
            except ValueError:
                print("Invalid roll number. Must be an integer.")
                continue

            student = Student(name, roll)
            while True:
                subject = input("Enter subject (or 'done' to finish): ")
                if subject.lower() == "done":
                    break
                try:
                    marks = int(input(f"Enter marks for {subject}: "))
                    student.add_marks(subject, marks)
                except ValueError:
                    print("Invalid marks. Must be an integer.")

            gb.add_student(student)

        elif choice == 2:
            try:
                roll = int(input("Enter roll number to remove: "))
                gb.remove_student(roll)
            except ValueError:
                print("Invalid roll number. Must be an integer.")

        elif choice == 3:
            try:
                roll = int(input("Enter roll number to view details: "))
                gb.get_student(roll)
            except ValueError:
                print("Invalid roll number. Must be an integer.")

        elif choice == 4:
            gb.list_all_students()

        elif choice == 5:
            gb.save_to_file("studentsrecords.json")

        elif choice == 6:
            try:
                roll = int(input("Enter roll number: "))
                subject = input("Enter subject: ")
                marks = int(input("Enter new marks: "))
                gb.update_marks(roll, subject, marks)
            except ValueError:
                print("Invalid input. Roll number and marks must be integers.")

        elif choice == 7:
            gb.top_performer()

        elif choice == 8:
            try:
                k = int(input("Enter value of K: "))
                gb.top_k_performers(k)
            except ValueError:
                print("Invalid input. K must be an integer.")

        elif choice == 9:
            print("Exiting...")
            return

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()