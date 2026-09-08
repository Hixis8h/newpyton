survey_results = [

    ["Python","JavaScript", "C++"], #person1

    ["Python","JavaScript","C#"], #person2

    ["Python","Java"],#person3

    ["Python","C++","JavaScript"],#person4

    ["Python","JavaScript","C++","Java"],#person5

]

survey_set = [set(code) for code in survey_results]
common_languages = set.intersection(*survey_set)
print("Languages chosen by all participats: ",common_languages )


all_languages = set.union(*survey_set)
for person in survey_set: 
    other_languages = all_languages - person
    only_one = person - other_languages
print("Languages only chosen by one participant: ",other_languages)
