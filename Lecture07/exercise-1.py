servey_results = [
    ["Python","JavaScript", "C++"],
    ["Python","JavaScript","C#"],
    ["Python","Java"],
    ["Python","C++","JavaScript"],
    ["Python","JavaScript","C++","Java"],
]
#1. Languages chosen by all participats: {'Python'}
#2. Languages only chosen by one participant:{"C#"}
#3. Numver of unique languages: 5
#4. Languages chosen by exatly two participants: {'Java'}
#5. Participants with the same set of languages: [[1,4]]

#choices_sets = [set(p) for p in survey_results]
#common_languages = set.intersection(*choices_sets)
#print("1. Languages chosen by alll participants: ", common_languages)