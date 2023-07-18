from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value) -> None:
        self.value = value
    # @property
    # def value(self):
    #     return self.value

    # @value.setter   # проверка на корректность номера телефона
    # def value(self, value):
    #     if isinstance(Phone(value, int)) and len(Phone(value)) == 12:
    #         self.value = value
    #     else:
    #         print(f"{value} is an invalid mobile number")
    
    # @value.setter # проверка на корректность дня рождения
    # def value(self, value):    
    #     value = datetime.strptime(Birthday(value, "%d.%m.%Y"))
    #     current_year = datetime.now().year
    #     if value.year > current_year or value.year < current_year - 120:
    #         raise ValueError("Incorrect data")

    #     if value > datetime.now():
    #         raise ValueError("Incorrect data")
    #     else:
    #         return value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
     

class Name(Field):
    pass

    
class Phone(Field):
    pass

class Birthday(Field):
    pass

class Record:

    def __init__(self, name : Name, phone=None, birthday=None):
        self.name = name
        self.phone_list = []    #list[Phone()]
        if phone: 
            self.phone_list.append(phone)
        if birthday:  
            self.birthday = datetime.strptime(birthday, "%d.%m.%Y").date()


    def add_phone(self, phone: Phone):
        self.phone_list.append(phone)
        

    def change_phone(self, phone_from: Phone, phone_to: Phone):
        for idx, item in enumerate(self.phone_list):
            if phone_from.number == item.number:
                self.phone_list[idx] = phone_to
        #         return f"old phone {phone_from} change to {phone_to}"
        # return f"{phone_from} not present in phones of contact {self.name}"
    
    def delete_phone(self, number: str):
        # iterate from end to begin (reverse iteration)
        for item in reversed(self.phone_list):
            if item.number == number:
                self.phone_list.remove(item)
    
    def days_to_birthday(self):
        # возвращает количество дней до следующего дня рождения.
        current_date = datetime.now().date()
        self.birthday = self.birthday.replace(year=current_date.year)     
        quantity_days = (current_date - self.birthday).days
        return quantity_days
# если число возвращается положительное то др еще не наступил, если отрицательное то уже прошел
    


    def __str__(self) -> str:
        return f'{self.phone_list}'

    def __repr__(self) -> str:
        return str(self)


class AddressBookIterator:
    def __init__(self, entries, page_size=10):
        self.entries = entries
        self.page_size = page_size
        self.current_page = 0

    def __iter__(self):
        return self

    def __next__(self):
        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size

        if start_index >= len(self.entries):
            raise StopIteration

        page_entries = self.entries[start_index:end_index]
        self.current_page += 1

        return page_entries


class AddressBook(UserDict):

    def add_record(self, record: Record):
        if self.data.get(record.name.value):
            rec = self.data[record.name.value]
            rec.phone_list.extend(record.phone_list)
            rec.birthday.extend(record.birthday) # под вопросом правильность написания
        else:
            self.data[record.name.value] = record

    # -> return Record(name)
    def search_user(self, name_str: str):
        name = Name(name_str)
        if self.data.get(name.value):
            return self.data[name.value]

        # the same:
        #if self.data.get(name_str):
        #    return self.data[name_str]
        return None

# метод iterator, возвращает генератор по записям AddressBook и за одну итерацию 
# возвращает представление для N записей.
    def __iter__(self):             
        return self

    
    def iterator(self):
        return AddressBookIterator(entries = self.data, page_size = 10)


