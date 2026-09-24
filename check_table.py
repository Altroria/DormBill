from sqlalchemy import create_engine, inspect

engine = create_engine('mysql+pymysql://root:495648@localhost:3306/dormbill')
inspector = inspect(engine)

cols = inspector.get_columns('room_main_meter_records')
for c in cols:
    print(f"{c['name']}: {c['type']}")
