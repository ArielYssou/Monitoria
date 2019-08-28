from faker import Faker
fake = Faker('pt_BR')
fake.seed(1234)

for i in range(10):
    print(fake.name())
