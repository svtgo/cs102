import psycopg2
import psycopg2.extras
from tabulate import tabulate


conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=adult_data user=postgres password=secret")
cursor = conn.cursor()


def fetch_all(cursor):
    colnames = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return [{colname:value for colname, value in zip(colnames, record)} for record in records]



''' Задание 1'''

'''1. Сколько мужчин и женщин (признак sex) представлено в этом наборе данных?'''

cursor.execute(
    """
    SELECT sex, COUNT(*)
        FROM adult_data
        GROUP BY sex
    """
)
print('Количество мужчин и женщин: ')
print(tabulate(fetch_all(cursor), "keys", "psql"))

'''2. Каков средний возраст (признак age) женщин?'''

cursor.execute("""
    SELECT AVG(age) FROM adult_data WHERE sex = 'Female'
""")
print('Средний возраст женщин: ')
print(tabulate(fetch_all(cursor), "keys", "psql"))

'''3. Какова доля граждан Германии (признак native-country)?'''

cursor.execute(
    """
    SELECT native_country, ROUND((COUNT(*) / (SELECT COUNT(*) FROM adult_data)::numeric), 6)
        FROM adult_data WHERE native_country = 'Germany'
        GROUP BY native_country;
    """
)
print('Доля граждан Германии: ')
print(tabulate(fetch_all(cursor), "keys", "psql"))

'''4-5. Каковы средние значения и среднеквадратичные отклонения возраста тех, 
кто получает более 50K в год (признак salary) и тех, кто получает менее 50K в год?'''

cursor.execute("""
    SELECT COUNT(*),
           AVG(age), STDDEV(age)
    FROM adult_data where salary = '<=50K'
    GROUP BY salary;
""")
print('Средние значения и СКО для тех, кто получает менее 50К: ')
print(tabulate(fetch_all(cursor), "keys", "psql"))

cursor.execute("""
    SELECT COUNT(*),
           AVG(age), STDDEV(age)
    FROM adult_data where salary = '>50K'
    GROUP BY salary;
""")
print('Средние значения и СКО для тех, кто получает более 50К: ')
print(tabulate(fetch_all(cursor), "keys", "psql"))

'''6. Правда ли, что люди, которые получают больше 50k, имеют как минимум высшее образование? 
(признак education – Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters или Doctorate)'''

cursor.execute("""
    SELECT COUNT(*),
    education, salary 
    FROM adult_data where salary = '>50K'
    GROUP BY education, salary;
""")
print('Образование людей, получающих больше 50K:')
print(tabulate(fetch_all(cursor), "keys", "psql"))

'''7. Выведите статистику возраста для каждой расы (признак race) и каждого пола. 
Найдите максимальный возраст мужчин расы Amer-Indian-Eskimo.'''

cursor.execute("""
    SELECT COUNT(*),
           AVG(age), STDDEV(age), MIN(age), MAX(age)
    FROM adult_data WHERE sex = 'Female'
    GROUP BY race
""")
print('Статистика для каждой расы и пола:')
print(tabulate(fetch_all(cursor), "keys", "psql"))

cursor.execute("""
    SELECT MAX(age)
    FROM adult_data WHERE sex = 'Male' AND race = 'Amer-Indian-Eskimo'
    GROUP BY race
""")
print('Максимальный возраст мужчин расы Amer-Indian-Eskimo:')
print(tabulate(fetch_all(cursor), "keys", "psql"))


'''8. Среди кого больше доля зарабатывающих много (>50K): среди женатых или холостых мужчин (признак marital-status)?
Женатыми считаем тех, у кого marital-status начинается с Married (Married-civ-spouse, Married-spouse-absent или Married-AF-spouse), остальных считаем холостыми.'''

cursor.execute("""
    SELECT ROUND((COUNT(*) / (SELECT COUNT(*) FROM adult_data)::numeric), 6), salary, is_married
    FROM adult_data WHERE salary = '>50K'
    GROUP BY is_married, salary
            """)
print(tabulate(fetch_all(cursor), "keys", "psql"))
            
'''9. Какое максимальное число часов человек работает в неделю (признак hours-per-week)? 
Сколько людей работают такое количество часов и каков среди них процент зарабатывающих много?'''

cursor.execute("SELECT MAX(hours_per_week::int) FROM adult_data")

print('Максимальное число часов в неделю:')
print(tabulate(fetch_all(cursor), "keys", "psql"))

cursor.execute(
    """
    SELECT COUNT(*)
        FROM adult_data WHERE hours_per_week = 99
    """
)
print('Таких людей:')
print(tabulate(fetch_all(cursor), "keys", "psql"))

cursor.execute("""
    SELECT COUNT(*)
    FROM adult_data
    WHERE hours_per_week = '99' AND salary = '>50K'
    GROUP BY hours_per_week;
""")

rich = fetch_all(cursor)[0]['count']

cursor.execute("""
    SELECT COUNT(*)
    FROM adult_data
    WHERE hours_per_week = '99'
    GROUP BY hours_per_week;
""")

everyone = fetch_all(cursor)[0]['count']
print('Зарабатывающих много: ', round(rich / everyone * 100 ), '%')


'''10. Посчитайте среднее время работы (hours-per-week) зарабатывающих мало и много (salary) для каждой страны (native-country).'''

cursor.execute(
    """
    SELECT native_country, salary, ROUND(AVG(hours_per_week))
    FROM adult_data
    GROUP BY native_country, salary
    """)

print('Среднее время работы для зарабатывающих мало и много в каждой стране:')
print(tabulate(fetch_all(cursor), "keys", "psql"))


"""
    UPDATE adult_data
    SET is_married = CASE
        WHEN marital_status = 'Married-civ-spouse' THEN 1
        WHEN marital_status = 'Married-spouse-absent' THEN 1
        WHEN marital_status = 'Married-AF-spouse' THEN 1
        ELSE 0
    END;
"""
