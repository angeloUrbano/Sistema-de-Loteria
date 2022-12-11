from faker import Faker
from faker.providers import BaseProvider

fake = Faker()


class nombre_tipo_loteria_class (BaseProvider):

    def name_custom (self):
        return f'{angelo_urbano}'
