from flask_sqlalchemy import SQLAlchemy

from .__init__ import db


class UserTable(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    user_id = db.Column(db.Integer)
    authkey = db.Column(db.String())
    login = db.Column(db.Integer)
    read_access = db.Column(db.Integer)
    write_access = db.Column(db.Integer)

    def __init__(self, name, user_id, authkey, login, read_access, write_access):
        self.name = name;
        self.user_id = user_id
        self.authkey = authkey
        self.login = login
        self.read_access = read_access
        self.write_access = write_access


def delete_all():
    try:
        db.session.query(UserTable).delete()
        db.session.commit()
        print("Delete all done")
    except Exception as e:
        print("Failed " + str(e))
        db.session.rollback()


def get_user_row_if_exists(user_id):
    get_user_row = UserTable.query.filter_by(user_id=user_id).first()
    if get_user_row != None:
        return get_user_row
    else:
        print("User doesn't exist")
        return False


def add_user_and_login(name, user_id):
    row = get_user_row_if_exists(user_id)
    if row:
        row.login = 1
        db.session.commit()
    else:
        print("Addomg user " + name)
        new_user = UserTable(name, user_id, None, 1, 0, 0)
        db.session.add(new_user)
        db.session.commit()
    print("User " + name + " login added")


def user_logout(user_id):
    row = get_user_row_if_exists(user_id)
    if row:
        row.login = 0
        db.session.commit()
        print("User " + row.name + " logged out")


def view_all():
    row = UserTable.query.all()
    for n in range(0, len(row)):
        print(str(row[n].id) + " | " + row[n].name + " | " + str(row[n].user_id) + " | " + str(row[n].authkey) + " | "
              + str(row[n].login))


def get_all_logged_in_users():
    row = UserTable.query.filter_by(loging=1).all()
    online_user_record = {"user_record": []}
    print("Logged in useres")
    for n in range(0, len(row)):
        if row[n].read_access:
            read = "checked"
        else:
            read = "unchecked"
        if row[n].write_access:
            write = "checked"
        else:
            write = "unchecked"
        online_user_record["user_record"].append([row[n].name, row[n].user_id, read, write])
        print(str(row[n].id) + " | " + row[n].name + " | " + str(row[n].user_id) + " | " + str(row[n].authkey) + " | "
              + str(row[n].read_access) + " | " + str(row[n].write_access))
        return online_user_record

