import sqlite3 as sq


base = sq.connect('Underground_shop.db')
curs = base.cursor()


def database_initialization():
    if base:
        print("data base connection secured")

    base.execute('CREATE TABLE IF NOT EXISTS data(img TEXT, balance TEXT, description TEXT, region TEXT, price TEXT)')


async def add_command(state):
    async with state.proxy() as data:
        curs.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?)", tuple(data.values()))
        base.commit()


async def readall():
    return curs.execute("SELECT * FROM data").fetchall()


async def delete_data_from_db(data):
    curs.execute("DELETE FROM data WHERE description == ?", (data,))
    base.commit()


def get_data_from_db():
    properties_list = []
    range_10000, range_3500, range_1000, range_100 = [], [], [], []
    eu_cards, us_cards = [], []

    for line in curs.execute("SELECT * FROM data").fetchall():
        properties_list.append(line)

    for sort in properties_list:
        if sort[3].upper() == "EU":
            eu_cards.append(sort)

        if sort[3].upper() == "US":
            us_cards.append(sort)

        if int(float(sort[1].strip('$').strip())) in range(20, 101):
            range_100.append(sort)

        if int(float(sort[1].strip('$').strip())) in range(100, 1001):
            range_1000.append(sort)

        if int(float(sort[1].strip('$').strip())) in range(1000, 3501):
            range_3500.append(sort)

        if int(float(sort[1].strip('$').strip())) in range(4000, 10001):
            range_10000.append(sort)

    return [{"💸 20$ - 100$": range_100}, {"💸 100$ - 1000$": range_1000}, {"💸 1000$ - 3500$": range_3500},
            {"💸 4000$ - 10000$": range_10000}, {"🇪🇺 EU": eu_cards}, {'🇺🇸 US': us_cards}]
