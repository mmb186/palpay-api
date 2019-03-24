from datetime import datetime

from app import db
from app.models.Tabs import Tab
from app.models.Tabs.enums import UserTabStatus


class TabUserStatus(db.Model):
    """
        Model for status and balance of users in a tab
    """
    __tablename__ = 'user_tab_status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tab_id = db.Column(db.Integer, db.ForeignKey('tabs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.FLOAT, nullable=False, default=0)
    status = db.Column(db.Enum(UserTabStatus), nullable=False, unique=False,
                       default=UserTabStatus.PENDING)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                                   onupdate=datetime.utcnow)

    def __init__(self, tab_id, user_id, status=UserTabStatus.PENDING):
        self.tab_id = tab_id
        self.user_id = user_id
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update_status(self, new_status):
        self.status = UserTabStatus.get_status_enum(new_status)
        self.save()

    @classmethod
    def get_all_users_tab_status(cls, tab_id):
        return cls.query.filter_by(tab_id=tab_id).all()

    @classmethod
    def get_by_tab_id_and_user_id(cls, tab_id, user_id):
        return cls.query\
            .filter_by(tab_id=tab_id)\
            .filter_by(user_id=user_id)\
            .first()

    @classmethod
    def get_user_tabs(cls, user_id):
        return db.session\
            .query(Tab.Tab, TabUserStatus)\
            .join(TabUserStatus)\
            .filter(TabUserStatus.user_id == user_id)\
            .filter(Tab.Tab.status != 'INACTIVE')\
            .all()


