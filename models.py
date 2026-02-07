
#поздно подумал про объектную модель, поэтому она не используется, но выглядит так

class Owner:
    """Класс владельца питомца"""
    def __init__(self, owner_id, full_name, phone):
        self.id = owner_id
        self.full_name = full_name
        self.phone = phone

    def __repr__(self):
        return f"<Owner: {self.full_name}>"

class Pet:
    """Класс питомца"""
    def __init__(self, pet_id, name, species, age, owner_id):
        self.id = pet_id
        self.name = name
        self.species = species
        self.age = age
        self.owner_id = owner_id

    def __repr__(self):
        return f"<Pet: {self.name} ({self.species})>"

class Appointment:
    """Класс записи на прием"""
    def __init__(self, app_id, pet_id, date_time, reason, status):
        self.id = app_id
        self.pet_id = pet_id
        self.date_time = date_time
        self.reason = reason
        self.status = status

    def __repr__(self):
        return f"<Appointment: {self.date_time} - {self.status}>"