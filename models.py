from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TxnNames(Base):
    __tablename__ = 'txn_names'

    id = Column(Integer, primary_key=True)
    revenue = Column(Boolean, nullable=False)
    name = Column(String(255), nullable=False)
    sub_group = Column(String(255), nullable=False)
    group = Column(String(255), nullable=False)
    transactions = relationship('Transactions', back_populates='name')

    def __repr__(self):
        return f'<TxnNames: {self.id} - {self.name}>'


class Transactions(Base):

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Numeric, nullable=False)
    revenue = Column(Boolean, nullable=False)
    source = Column(String(255), nullable=False)
    name_id = Column(Integer, ForeignKey('txn_names.id'))
    name = relationship('TxnNames', back_populates='transactions')

    def __repr__(self):
        return f'<Transaction: {self.id}>'
