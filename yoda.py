import random
import re
import json
import datetime


class Yoda:
    def __init__(self):
        self.patterns = None
        self.rules = None
        self.loadJson()

    def openRecord(self):
        basename = "chat/chat"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix])
        return open((filename + ".txt"), "w")

    def saveChat(self, file, yoda, client):
        yoda = "Yoda: " + yoda
        client = "Client: " + client
        file.write(f"{yoda}\n{client}\n")

    def loadJson(self):
        with open("./settings/rules.json", "r") as f:
            self.rules = json.load(f)
        with open("./settings/patterns.json", "r") as f:
            self.patterns = json.load(f)
        with open("./settings/reflections.json", "r") as f:
            self.reflections = json.load(f)

    def getResponseFor(self, question):
        for pattern in self.patterns:
            match = re.match(pattern, question)
            if match:
                response = random.choice(self.rules[pattern])
                group = match.groupdict()
                if "manyItem" in group:
                    response = response % (str(random.randint(1, 10000)), group["manyItem"])
                elif "muchItem" in group:
                    response = response % (random.choice(["few", "a little", "a lot"]), group["muchItem"])
                elif "subject" in group:
                    response = response % self.reflect(group["subject"])
                return response

    def normalise(self, question):
        normalised_question = question.lower()
        normalised_question = re.sub("[^0-9a-zA-Z ]+", " ", normalised_question)
        return normalised_question

    def startChat(self):
        with self.openRecord() as recorder:
            yoda = "Seek advice you must"
            print(yoda)
            client = input()
            while(client != "q"):
                self.saveChat(recorder, yoda, client)
                client = self.normalise(client)
                yoda = self.getResponseFor(client)
                print(yoda)
                client = input()
            self.saveChat(recorder, yoda, client)

    def reflect(self, fragment):
        tokens = fragment.lower().split()
        for i, token in enumerate(tokens):
            if token in self.reflections:
                tokens[i] = self.reflections[token]
        return ' '.join(tokens)


if __name__ == '__main__':
    yoda = Yoda()
    yoda.startChat()
