from zope.interface import Interface, Attribute

class IPeople(Interface):
    """Интерфейс определяет поведение человека.
    """
    passport = Attribute("Номер паспорта")
    name = Attribute("Имя человека")
    family = Attribute("Фамилия человека")

    def fio():
        """Печатает Ф.И.О. человека
        """

class IGroup(Interface):
    name = Attribute("Название группы")
    def add(people):
        """Add a person into the group.
        """


class IStorableObject(Interface):
    """Данный объекты могут быть записаны в
    компонент, реализующий IDBConnection.
    """

    def save_into(conn, id):
        pass

    def load_from(conn):
        pass


class IDBConnection(Interface):
    """Интерфейс, описывающий ресерс для
    сохранения объектов.
    """

    def save(object):
        """Сохранить объект.
        Возвратить id объекта.
        """

    def load(id):
        """Загрузить объект.
        """
