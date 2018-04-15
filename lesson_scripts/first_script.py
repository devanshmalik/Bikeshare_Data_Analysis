names = [x for x in input('Enter the names: ').split(',')]
assignments = [int(x) for x in input('Enter number of assignments left: ').split(',')]
grade = [int(x) for x in input('Enter current grade: ').split(',')]

message = "Hi {},\n\nThis is a reminder that you have {} assignments left to \
submit before you can graduate. You're current grade is {} and can increase \
to {} if you submit all assignments before the due date.\n\n"

for i in range(len(names)):
    print(message.format(names[i], assignments[i], grade[i], grade[i] + 2*assignments[i]))
