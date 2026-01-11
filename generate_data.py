from multiprocessing import Pool
from enum import IntEnum
import random
import string
import logging
import logging.config

# I want to benchmark SQLite what the most efficient way is to store enums.
# There are three ways I want to test:
# Storing it in the table as a string like many ORMs do.
# Storing it in a lookup table with a foreign key.
# Assign the enum an integer and store the integer instead.

# Below are thee enums that are stored in the table.

# table with enum as text example:
# id integer primary key
# name text not null
# color text not null
# status text not null
# order_type text not null

# Select statements are dominating factor for most web applications
# I want to run the following queries:

# select * from <table with required joins> where color = ?;
# select * from <table with required joins> where color in (?,?);
# select * from <table with required joins> where color = ? and status = ?;
# select * from <table with required joins> where color = ? and status = ? and order_type = ?;
# select * from <table with required joins> where (status != ? and status != ?) and order_type = ?;

# select id from <table with required joins> where color = ?;
# select id from <table with required joins> where color in (?,?,?);
# select id from <table with required joins> where color = ? and status = ?;
# select id from <table with required joins> where color = ? and status = ? and order_type = ?;
# select id from <table with required joins> where (status != ? and status != ?) and order_type = ?;

# The difference between the wildcard and id is to see so how much difference there is between
# fetching this data.


class Color(IntEnum):
    UNKNOWN = 0
    RED = 1
    BLUE = 2
    YELLOW = 3
    GREEN = 4
    PURPLE = 6
    WHITE = 7


class Status(IntEnum):
    TODO = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    FAILED = 4


class OrderType(IntEnum):
    STORE = 1
    ONLINE = 2
    PHONE = 3


def random_string(min_len=5, max_len=20):
    length = random.randint(min_len, max_len)
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_table_enum_as_string(number: int, flush_size: int = 500):
    entries: list[str] = []

    with open("data/enum_as_string_data.csv", "+w") as f:
        f.write("id,name,color,status,order_type\n")

        for id in range(1, number + 1):
            name = random_string()
            color = random.choice(list(Color))
            status = random.choice(list(Status))
            order_type = random.choice(list(OrderType))

            entries.append(
                f"{id},{name},{color.name},{status.name},{order_type.name}\n"
            )

            if len(entries) == flush_size:
                f.writelines(entries)
                entries.clear()

        if len(entries) != 0:
            f.writelines(entries)
            entries.clear()


def generate_table_enum_as_fk_or_int(
    number: int, table_name: str, flush_size: int = 500
):
    entries: list[str] = []

    with open(f"data/{table_name}_data.csv", "+w") as f:
        f.write("id, name, color, status, order_type\n")

        for id in range(1, number + 1):
            name = random_string()
            color = random.choice(list(Color))
            status = random.choice(list(Status))
            order_type = random.choice(list(OrderType))

            entries.append(f"{id},{name},{color},{status},{order_type}\n")

            if len(entries) == flush_size:
                f.writelines(entries)
                entries.clear()

        if len(entries) != 0:
            f.writelines(entries)
            entries.clear()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    logger.info("Starting with three mp runners")
    with Pool(processes=3) as pool:
        pool.starmap(generate_table_enum_as_string, [(15_000_000,)])
        pool.starmap(
            generate_table_enum_as_fk_or_int,
            [(15_000_000, "enum_as_fk"), (15_000_000, "enum_as_int")],
        )
    logger.info("done...")
