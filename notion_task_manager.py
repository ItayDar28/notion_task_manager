from notion.client import NotionClient
from datetime import datetime
import time
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    task_name = Column(String(255), nullable=False)
    start = Column(String(255), nullable=False)
    finish = Column(String(255), nullable=False)
    duration = Column(Integer, nullable=False)

    def __init__(self, task_name, start, finish, duration):
        self.task_name = task_name
        self.start = start
        self.finish = finish
        self.duration = duration


class MyNotionTable:

    def __init__(self, token, page_url, session):
        print("start with constructor")
        self.client = NotionClient(token_v2=token)
        self.page = self.client.get_collection_view(url_or_id=page_url)
        self.current_tasks = {}
        self.all_tasks = {}
        self.session = session
        print("finish with constructor")

    def get_all_table_attributes(self):
        att_dic = self.page.collection.get()['schema']
        att_list = []
        for att in att_dic:
            att_list.append((att_dic[att]['name'], att_dic[att]['type']))
        return att_list

    def check_for_tasks_status(self):
        for row in self.page.collection.get_rows():
            if row.start and not row.finish and (row.task_name not in self.current_tasks):
                self.current_tasks[row.task_name] = datetime.now()
            elif row.start and row.finish:
                # then i finished my tasks - write it to db and restart parameters
                try:
                    start = self.current_tasks[row.task_name]
                    print("deleting this item - " + row.task_name)
                except:
                    continue
                finish = datetime.now()
                duration = finish - start
                task = Tasks(row.task_name, str(start), str(finish), duration.total_seconds())
                try:
                    self.session.add(task)
                    self.session.commit()
                except:
                    self.session.rollback()
                row.start = False
                row.finish = False
                row.popularity += 1
                del self.current_tasks[row.task_name]
            else:
                continue

    def run(self):
        while True:
            print(f"this items in dict - {self.current_tasks.keys()}")
            self.check_for_tasks_status()
            time.sleep(5)



if __name__ == '__main__':
    while True:
        print("start new session")
        try:
            engine = create_engine('mysql+mysqlconnector://username: password@ip: port/db name')
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
        except:
            print("error2")
        print("start withh token")
        TOKEN_V_2 = 'your token'
        url = 'url'
        print("start withh table")
        table = MyNotionTable(token=TOKEN_V_2, page_url=url, session=session)
        print("start table.run")
        table.run()

