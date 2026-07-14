score1=int(input("Enter your score1: "))
score2 = int(input("Enter your score2: "))
score3 = int(input("Enter your score3: "))

average_score = (score1 + score2 + score3) / 3
if average_score >95:
    print("Congratulations!")
    print("That is a grat average !")
elif average_score <=95:
    print("Your average score is: ", average_score)

