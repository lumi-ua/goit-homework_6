from collections import UserDict
from datetime import datetime, timedelta

import itertools

class Field:

    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, var):
        self._value = var
    
    def __str__(self) -> str:
        return self._value
    
    def __repr__(self) -> str:
        return str(self)
     

class Name(Field):

    def __init__(self, value) -> None:
        

class Phone(Field):

    def __init__(self, var) -> None:
        self.value = var

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, var):
        if (len(var) == 12) and var.isnumeric():
            #Field.value = var
            super(Phone, self.__class__).value.fset(self, var)
        else:
            raise ValueError(f"{var} is an invalid mobile number")


class Birthday(Field):

    def __init__(self, var) -> None:
        self.value = var

    @property
    def value(self):
        #return Field.value
        return super().value

    @value.setter
    def value(self, var):
        dtv = datetime.strptime(var, "%d.%m.%Y")
        current_year = datetime.now().year
        if dtv.year > current_year or dtv.year < current_year - 120:
            raise ValueError("Invalid birthday range!")
        else:
            #Field.value = dtv
            super(Birthday, self.__class__).value.fset(self, dtv)

        if dtv > datetime.now():
            raise ValueError("Invalid birthday!")
        else:
            #Field.value = dtv
            super(Birthday, self.__class__).value.fset(self, dtv)


class Record:

    def __init__(self, name : Name, phone=None, birthday=None):
        self.name = name
        self.phone_list = []    #list[Phone()]
        if phone: 
            self.phone_list.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phone_list.append(phone)
        
    def set_name(self, name_str: str):
        self.name = Name(name_str)

    def change_phone(self, phone_from: Phone, phone_to: Phone):
        for idx, item in enumerate(self.phone_list):
            if phone_from.number == item.number:
                self.phone_list[idx] = phone_to
                return f"old phone {phone_from} change to {phone_to}"
        return f"{phone_from} not present in phones of contact {self.name}"
    
    def delete_phone(self, number: str):
        # iterate from end to begin (reverse iteration)
        for item in reversed(self.phone_list):
            if item.number == number:
                self.phone_list.remove(item)
    
    def days_to_birthday(self) -> int:
        # возвращает количество дней до следующего дня рождения.
        # если положительное то др еще не наступил, если отрицательное то уже прошел
        current_date = datetime.now().date()
        birthday = self.birthday.value.replace(year=current_date.year).date()
        quantity_days = (birthday - current_date).days
        return quantity_days
    

    def __str__(self) -> str:
        if self.birthday:
            return f'\n{self.name.value}: {self.phone_list}; {self.birthday.value.date()}'
        else:
            return f'\n{self.name.value}: {self.phone_list}'

    def __repr__(self) -> str:
        return str(self)


class AddressBookIterator:
   
    def __init__(self, address_book:UserDict, page_size=10):
        self.address_book = address_book
        self.page_size = page_size
        self.current_page = 0

    def __iter__(self):
        return self

    def get_items(self)->list:
        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size

        if start_index >= len(self.address_book.values()):
            return None

        items = list(itertools.islice(self.address_book.values(), start_index, end_index))

        return items

    def __next__(self):
        self.current_page += 1
        return self.get_items()

    def __str__(self) -> str:
        items = self.get_items()
        if items:
            return f'{items}'
        return []

    def __repr__(self) -> str:
        return str(self)


class AddressBook(UserDict):

    def add_record(self, record: Record):
        if self.data.get(record.name.value):
            rec = self.data[record.name.value]
            rec.phone_list.extend(record.phone_list)
            
            if record.birthday:
                rec.birthday = record.birthday
        else:
            self.data[record.name.value] = record

    def rename_record(self, from_name: str, to_name: str):
        rec = self.data.pop(from_name)
        if rec:
            rec.set_name(to_name)
            self.add_record(rec)
            return True
        return False

    def search_user(self, name: str) -> Record:
        if self.data.get(name):
            return self.data[name]
        return None
    
    # метод iterator, возвращает генератор по записям AddressBook и за одну итерацию 
    # возвращает представление для N записей.
    def iterator(self):
        return AddressBookIterator(address_book=self, page_size = 10)
