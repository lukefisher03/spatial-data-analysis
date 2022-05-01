t = input("What is the number you wish to convert: ")

components = t.split(":")

totalSeconds = int(components[0]) * 60 + int(components[1])
newTime = (totalSeconds - 399) / 60

formattedTime = str(newTime).split(".")

print(formattedTime[0] + ":" + str(int(float("."+formattedTime[1])*60)))

