from faker import Faker

import faker_commerce

fake = Faker()
fake.add_provider(faker_commerce.Provider)
print(fake.ecommerce_name())  # prints a product name