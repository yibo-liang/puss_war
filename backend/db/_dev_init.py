from db.ability import dev_init as a
from db.apostle import dev_init as b
from db.card import dev_init as c
from db.cat import dev_init as d
from db.deck import dev_init as e
from db.user import dev_init as f
from db._db_interface import NoSQLDatabase


def main():
    print("Initialise Database")
    db = NoSQLDatabase("puss_war")
    db.init()
    db.empty_db()

    a()
    b()
    c()
    d()
    e()
    f()


if __name__ == "__main__":
    main()
