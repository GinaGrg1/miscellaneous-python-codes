import random

capitals = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix',
   'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver',
   'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee',
   'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois':
   'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas':
   'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine':
   'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan':
   'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri':
   'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada':
   'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 
   'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh',
   'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
   'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence',
   'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee':
   'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont':
   'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 
   'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

def correctCapital(state):
    return capitals[state]

def answerOptions(state):
    correctCapital = correctCapital(state)
    capitalsList = list(capitals.values())
    incorrectOptions = capitalsList.remove(correctCapital)
    randomincorrectOptions = random.sample(incorrectOptions, 3)
    answerOptions = randomincorrectOptions + [correctCapital]
    return random.shuffle(answerOptions)


for quizNum in range(35):
    
    quizFile = open('capitalsquiz%s.txt' % (quizNum+1), 'w')
    answerkeyFile = open('capitalquiz_answers%s.txt' % (quizNum+1), 'w')

    quizFile.write('Name:\n\nDate:\n\nPeriod:\n\n')
    quizfile.write(' ' * 20 + 'State Capitals Quiz (Form %s)\n\n' % (quizNum+1))
    
    states = list(capitals.keys())
    random.shuffle(states)
    for num, state in enumerate(states):
        quizFile.write('{}. What is the capital of {}?'.format(num+1, state))
        states = answerOptions(state) # [ a, correct, c, d]
        for i, ans in enumerate(states):
            quizFile.write('{}. ans\n'.format('ABCD'[i]))
        correctIndex = correctCapital(state) 
        answerkeyFile.write('{}. {}'.format(num+1, 'ABCD'[states.index(correctIndex)]))
