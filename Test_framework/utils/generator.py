"""一些生成器方法，生成隨機數，手機號，以及連續數字等，以便使用這些數據進行測試"""

import random
from faker import Factory

fake = Factory().create('zh_CN')


def random_phone_number():
    """隨機手機號"""
    return fake.phone_number()


def random_name():
    """隨機姓名"""
    return fake.name()


def random_address():
    """隨機地址"""
    return fake.address()


def random_email():
    """隨機email"""
    return fake.email()


def random_ipv4():
    """隨機IPV4地址"""
    return fake.ipv4()


def random_str(min_chars=0, max_chars=8):
    """長度在最大值與最小值之間的隨機字符串"""
    return fake.pystr(min_chars=min_chars, max_chars=max_chars)

# 產生一個id隨機生成器
def factory_generate_ids(starting_id=1, increment=1):
    """ 返回一個生成器函數，調用這個函數產生生成器，從starting_id開始，步長為increment。 """
    def generate_started_ids():
        val = starting_id
        local_increment = increment
        while True:
            yield val
            val += local_increment
    return generate_started_ids

# 產生一個隨機選項生成器
def factory_choice_generator(values):
    """ 返回一個生成器函數，調用這個函數產生生成器，從給定的list中隨機取一項。 """
    def choice_generator():
        my_list = list(values)
        rand = random.Random()
        while True:
            yield random.choice(my_list)
    return choice_generator


if __name__ == '__main__':
    print(random_phone_number())
    print(random_name())
    print(random_address())
    print(random_email())
    print(random_ipv4())
    print(random_str(min_chars=6, max_chars=8))
    id_gen = factory_generate_ids(starting_id=0, increment=2)()
    for i in range(5):
        print(next(id_gen))

    choices = ['John', 'Sam', 'Lily', 'Rose']
    choice_gen = factory_choice_generator(choices)()
    for i in range(5):
        print(next(choice_gen))