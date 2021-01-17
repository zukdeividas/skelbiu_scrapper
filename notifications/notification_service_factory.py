from notifications.messenger_service import MessengerService

class NotificationServiceFactory:
    def create(self, type, settings):
        if type == "messenger":
            return MessengerService(settings)
        
        raise Exception("Not implemented type {}".format(type))