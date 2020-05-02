class message(object):
    """description of class"""

    def __init__(self, applicationId, sessionId, messageId, content, participants):  #
        self.applicationId = applicationId
        self.sessionId = sessionId
        self.messageId = messageId
        self.content = content
        self.participants = participants

    @property
    def applicationId(self):
        return self.__applicationId

    @applicationId.setter
    def applicationId(self, applicationId):
        self.__applicationId = applicationId

    @property
    def sessionId(self):
        return self.__sessionId

    @sessionId.setter
    def sessionId(self, sessionId):
        self.__sessionId = sessionId

    @property
    def messageId(self):
        return self.__messageId

    @messageId.setter
    def messageId(self, messageId):
        self.__messageId = messageId

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content

    @property
    def participants(self):
        return self.__participants

    @participants.setter
    def participants(self, participants):
        self.__participants = participants

    def print(self):
        print("applicationId: ", self.applicationId)
        print("sessionId: " + self.sessionId, )
        print("messageId: " + self.messageId)
        print("content: " + self.content)
        print("participants: ", self.participants)

    def serialize(self):
        m = {
            'applicationId': self.applicationId,
            'sessionId': self.sessionId,
            'messageId': self.messageId,
            'content': self.content,
            'participants': self.participants
        }
        return m


