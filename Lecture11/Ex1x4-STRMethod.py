class StudentTest:
    def __init__(self, name, score1, score2, score3):
        self.name = name
        self.score1 = score1
        self.score2 = score2
        self.score3 = score3

    def sum_score(self):
        return self.score1 + self.score2 + self.score3

    def __str__(self):
        return f'Name: {self.name}, Total of score: {self.sum_score()}'


student = StudentTest('Jantra', 20, 35, 25)
print(student.name, student.sum_score())
print(student)
