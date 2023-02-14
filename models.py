from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    sub_groups = relationship('SubGroups', back_populates='group')
    transactions = relationship('Transactions', back_populates='group')

    def __repr__(self):
        return f'<Group: {self.id} - {self.name}>'


class SubGroups(Base):
    __tablename__ = 'sub_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('Groups', back_populates='sub_groups')
    transactions = relationship('Transactions', back_populates='sub_groups')

    def __repr__(self):
        return f'<SubGroup: {self.id} - {self.name} of {self.group.name}>'


class Transactions(Base):

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    amount = Column(Numeric, nullable=False)
    revenue = Column(Boolean, nullable=False)
    source = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('Groups', back_populates='transactions')
    sub_group_id = Column(Integer, ForeignKey('sub_groups.id'))
    sub_group = relationship('SubGroups', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction: {self.id}>'