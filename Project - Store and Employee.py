# Kellie Clinton's code

from __future__ import annotations
from sqlalchemy import Column
from sqlalchemy import Table
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

#DB Connection: create_engine(DBMS_name+driver://<username>:<password>@<hostname>/<database_name>)
engine = create_engine("postgresql+psycopg2://postgres:Intern123@localhost/postgres")

#Define Employees/Tables
class Base(DeclarativeBase):
    pass

association_SE_Hires = Table(
    "Hires",
    Base.metadata,
    Column("Store_ID", ForeignKey("Store.id"), primary_key=True),
    Column("Employee_ID", ForeignKey("Employee.id"), primary_key=True),
)

class Store(Base):
    __tablename__ = "Store"

    id: Mapped[int] = mapped_column(primary_key=True)
    SName: Mapped[str] = mapped_column(String(20))
    Phone_Number: Mapped[str] = mapped_column(String(20))
    SAddress: Mapped[str] = mapped_column(String(255))
    Owner_Name: Mapped[str] = mapped_column(String(50))
    Employees: Mapped[List[Employee]] = relationship(
        secondary=association_SE_Hires, back_populates="Stores"
    )
    
    def __repr__(self) -> str: #represents the object as a string 
        employeeList = ''
        for e in self.Employees:
            employeeList = employeeList + ' ' + e.EName
        return f"Store(id={self.id!r}, name={self.SName!r}, Employees={employeeList.strip()!r})"

class Employee(Base):
    __tablename__ = "Employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    EName: Mapped[str] = mapped_column(String(20))
    SSN: Mapped[str] = mapped_column(String(20))
    EAddress: Mapped[str] = mapped_column(String(255))
    Stores: Mapped[List[Store]] = relationship(
        secondary=association_SE_Hires, back_populates="Employees"
    )
    
    def __repr__(self) -> str: #represents the object as a string 
        return f"Employee(id={self.id!r}, name={self.EName!r})"
    
#Create Tables
Base.metadata.create_all(engine)

#Insert Data
with Session(engine) as session:
    e1 = Employee(
        EName="Julie Pumpkin",
        SSN="999-88-7777",
        EAddress="202 Broadway St"
    )
    e2 = Employee(
        EName="Nancy Lemon",
        SSN="212-63-4512",
        EAddress="144 Colfax Rd"
    )
    e3 = Employee(
        EName="Tom Schwarts",
        SSN="747-00-8539",
        EAddress="555 Luna Rd"
    )
    e4 = Employee(
        EName="Rachel Lime",
        SSN="963-52-7219",
        EAddress="998 Plum Grove St"
    )
    e5 = Employee(
        EName="Dan Arnold",
        SSN="417-77-8860",
        EAddress="231 Heather Ct"
    )
    e6 = Employee(
        EName="Sally Seashell",
        SSN="551-27-9437",
        EAddress="741 Kennedy Rd"
    )
    e7 = Employee(
        EName="Joe Davis",
        SSN="321-74-8514",
        EAddress="600 Willow Rd"
    )
    e8 = Employee(
        EName="Victoria Beckham",
        SSN="555-67-9147",
        EAddress="1 Hollywood Blvd"
    )
    e9 = Employee(
        EName="Tom Cruise",
        SSN="111-22-3456",
        EAddress="200 Hollywood Blvd"
    )
    
    s1 = Store(
        SName="Jewel",
        Phone_Number="1+555-123-3456",
        SAddress="123 Main St",
        Owner_Name="Joe Smith",
        Employees=[e1]
    )

    s2 = Store(
        SName="Kroger",
        Phone_Number="1+630-255-4788",
        SAddress="711 Smile St",
        Owner_Name="Bill Gates"
    )
    s3 = Store(
        SName="Target",
        Phone_Number="1+224-124-7489",
        SAddress="411 Sad St",
        Owner_Name="Jill Bob"
    )
    s4 = Store(
        SName="Aldi",
        Phone_Number="1+847-514-6347",
        SAddress="789 Smith Rd",
        Owner_Name="Barb Santos",
        Employees=[e2,e3,e4, e7, e8, e9]
    )
    s5 = Store(
        SName="Win-Dixie",
        Phone_Number="1+630-417-3697",
        SAddress="100 Acre Wood",
        Owner_Name="Piglet Eeyore"
    )
    s6 = Store(
        SName="Walmart",
        Phone_Number="1+847-898-4563",
        SAddress="1725 Slough Avenue",
        Owner_Name="Michael Scott",
        Employees=[e5,e6]
    )

    session.add_all([s1, s2, s3, s4, s5, s6])
    session.commit()
   
session = Session(engine)  
stores = session.query(Store)  
for s in stores:  
    print(s)

# Query 1: all Employees of a single store (s4 = "Aldi")
print("## List of Employees##")
#Join Query

result = session.execute(text('SELECT * FROM "Hires"'))
for row in result:
    print(row)    

stmt = (
    select(Employee.EName, text("EName"))
    .join(Store)
    .where(Store.SName == "Aldi")
)
for record in session.execute(stmt):
   print(record)


# Lingjie Liao
# Customer - Transaction (1:N)
# List all transactions made by each customer
# (show customer name, transaction ID, date, and total amount).

from datetime import date
from sqlalchemy import (
    create_engine, Column, Integer, String, Numeric, Date,
    ForeignKey, text
)
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import select

# Create Tables: Customer and Transaction

class Customer(Base):
    __tablename__  = "customer"
    __table_args__ = {"schema": "supermarket"}

    customer_id   = Column(Integer, primary_key=True)
    customer_name = Column(String)
    customer_age  = Column(Integer)

    transactions  = relationship(
        "Transaction",
        back_populates="customer"
    )

    def __repr__(self):
        return f"Customer(id={self.customer_id}, name='{self.customer_name}')"


class Transaction(Base):
    __tablename__  = "transactions"
    __table_args__ = {"schema": "supermarket"}

    transaction_id           = Column(Integer, primary_key=True)
    transaction_date         = Column(Date)
    transaction_total_amount = Column(Numeric(10, 2))

    customer_id = Column(
        Integer,
        ForeignKey("supermarket.customer.customer_id")
    )

    customer = relationship(
        "Customer",
        back_populates="transactions"
    )

    def __repr__(self):
        return (
            f"Transaction(id={self.transaction_id}, "
            f"amount={self.transaction_total_amount})"
        )

Base.metadata.create_all(engine)

# Insert Data

with Session(engine) as session:

    existing_customer = session.execute(select(Customer)).first()

    if not existing_customer:

        c1 = Customer(
            customer_id=1,
            customer_name="Alice",
            customer_age=28
        )

        c2 = Customer(
            customer_id=2,
            customer_name="Bob",
            customer_age=35
        )

        t1 = Transaction(
            transaction_id=101,
            transaction_date=date(2025, 1, 10),
            transaction_total_amount=50.75,
            customer=c1
        )

        t2 = Transaction(
            transaction_id=102,
            transaction_date=date(2025, 1, 11),
            transaction_total_amount=23.40,
            customer=c1
        )

        t3 = Transaction(
            transaction_id=103,
            transaction_date=date(2025, 1, 12),
            transaction_total_amount=89.99,
            customer=c2
        )

        t4 = Transaction(
            transaction_id=104,
            transaction_date=date(2025, 1, 13),
            transaction_total_amount=15.20,
            customer=c1
        )

        t5 = Transaction(
            transaction_id=105,
            transaction_date=date(2025, 1, 14),
            transaction_total_amount=44.10,
            customer=c1
        )

        t6 = Transaction(
            transaction_id=106,
            transaction_date=date(2025, 1, 15),
            transaction_total_amount=120.00,
            customer=c2
        )

        t7 = Transaction(
            transaction_id=107,
            transaction_date=date(2025, 1, 16),
            transaction_total_amount=9.99,
            customer=c2
        )

        t8 = Transaction(
            transaction_id=108,
            transaction_date=date(2025, 1, 17),
            transaction_total_amount=77.77,
            customer=c1
        )

        session.add_all([c1, c2, t1, t2, t3, t4, t5, t6, t7, t8])
        session.commit()

# Query: List all transactions for each customer

print(" List of Transactions ")

with Session(engine) as session:

    stmt = (
        select(
            Customer.customer_name,
            Transaction.transaction_id,
            Transaction.transaction_date,
            Transaction.transaction_total_amount
        )
        .join(Transaction, Customer.customer_id == Transaction.customer_id)
        .order_by(Customer.customer_id, Transaction.transaction_id)
    )

    for record in session.execute(stmt):
        print(record)

# Zubair Zaki's Code
from __future__ import annotations

from datetime import date

from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Numeric,
    Date,
    ForeignKey,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship

engine = create_engine(
    "postgresql+psycopg2://postgres:zubair@localhost:5432/schooldb",
    echo=False,  
)
class Base(DeclarativeBase):
    pass
class Product(Base):
    __tablename__ = "product"

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_type: Mapped[str] = mapped_column(String(50), nullable=False)
    product_name: Mapped[str] = mapped_column(String(40), nullable=False)
    product_price: Mapped[float] = mapped_column(Numeric(7, 2))
    product_unit_of_measure: Mapped[str] = mapped_column(String(40))

    # one product -> many restocks
    restocks: Mapped[list["Restock"]] = relationship(back_populates="product")

    def __repr__(self) -> str:
        return (
            f"<Product(product_id={self.product_id}, "
            f"type='{self.product_type}', "
            f"name='{self.product_name}')>"
        )


class Restock(Base):
    __tablename__ = "restock"

    restock_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_id: Mapped[int] = mapped_column(Integer)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product.product_id"), nullable=False
    )
    restock_quantity: Mapped[int] = mapped_column(Integer)
    restock_date: Mapped[date] = mapped_column(Date)

    # many restocks -> one product
    product: Mapped[Product] = relationship(back_populates="restocks")

    def __repr__(self) -> str:
        return (
            f"<Restock(restock_id={self.restock_id}, "
            f"product_id={self.product_id}, "
            f"store_id={self.store_id}, "
            f"qty={self.restock_quantity}, "
            f"date={self.restock_date})>"
        )


# --------------------------------------------------
# 4) MAIN: create tables, insert data, run query
# --------------------------------------------------
if __name__ == "__main__":
    # Create the tables if they don't exist
    Base.metadata.create_all(engine)

    # -------- INSERT DATA (only run on an empty table) --------
    with Session(engine) as session:
        # ----- Products -----
        p1 = Product(
            product_id=1001,
            product_type="Beverage",
            product_name="Coca-Cola Can",
            product_price=1.25,
            product_unit_of_measure="per can",
        )
        p2 = Product(
            product_id=1002,
            product_type="Beverage",
            product_name="Orange Juice",
            product_price=3.50,
            product_unit_of_measure="per bottle",
        )
        p3 = Product(
            product_id=1003,
            product_type="Snack",
            product_name="Potato Chips",
            product_price=2.00,
            product_unit_of_measure="per pack",
        )
        p4 = Product(
            product_id=1004,
            product_type="Grocery",
            product_name="Whole Wheat Bread",
            product_price=2.75,
            product_unit_of_measure="per loaf",
        )
        p5 = Product(
            product_id=1005,
            product_type="Grocery",
            product_name="Brown Rice",
            product_price=5.00,
            product_unit_of_measure="per kg",
        )
        p6 = Product(
            product_id=1006,
            product_type="Personal Care",
            product_name="Toothpaste",
            product_price=4.25,
            product_unit_of_measure="per tube",
        )
        p7 = Product(
            product_id=1007,
            product_type="Electronics",
            product_name="AA Batteries",
            product_price=7.00,
            product_unit_of_measure="per pack",
        )
        p8 = Product(
            product_id=1008,
            product_type="Stationery",
            product_name="Ballpoint Pen",
            product_price=1.10,
            product_unit_of_measure="per piece",
        )

        session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])
        session.commit()

        # ----- Restocks -----
        r1 = Restock(
            restock_id=9001,
            store_id=1,
            product_id=1001,
            restock_quantity=50,
            restock_date=date(2025, 1, 1),
        )
        r2 = Restock(
            restock_id=9002,
            store_id=1,
            product_id=1003,
            restock_quantity=30,
            restock_date=date(2025, 1, 2),
        )
        r3 = Restock(
            restock_id=9003,
            store_id=2,
            product_id=1002,
            restock_quantity=40,
            restock_date=date(2025, 1, 3),
        )
        r4 = Restock(
            restock_id=9004,
            store_id=3,
            product_id=1004,
            restock_quantity=25,
            restock_date=date(2025, 1, 4),
        )
        r5 = Restock(
            restock_id=9005,
            store_id=4,
            product_id=1005,
            restock_quantity=60,
            restock_date=date(2025, 1, 5),
        )
        r6 = Restock(
            restock_id=9006,
            store_id=5,
            product_id=1006,
            restock_quantity=20,
            restock_date=date(2025, 1, 5),
        )
        r7 = Restock(
            restock_id=9007,
            store_id=5,
            product_id=1007,
            restock_quantity=15,
            restock_date=date(2025, 1, 6),
        )
        r8 = Restock(
            restock_id=9008,
            store_id=6,
            product_id=1008,
            restock_quantity=80,
            restock_date=date(2025, 1, 7),
        )
        r9 = Restock(
            restock_id=9009,
            store_id=4,
            product_id=1001,
            restock_quantity=40,
            restock_date=date(2025, 1, 8),
        )
        r10 = Restock(
            restock_id=9010,
            store_id=2,
            product_id=1004,
            restock_quantity=25,
            restock_date=date(2025, 1, 9),
        )

        session.add_all([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10])
        session.commit()

    # -------- QUERY: list all restocks with product details --------
    with Session(engine) as session:
        stmt = (
            select(
                Restock.restock_id,
                Restock.restock_date,
                Restock.restock_quantity,
                Restock.store_id,
                Product.product_name,
                Product.product_type,
            )
            .join(Product, Restock.product_id == Product.product_id)
            .order_by(Restock.restock_date, Restock.restock_id)
        )

        rows = session.execute(stmt).all()

        print("Restock Activity Report:")
        for restock_id, rdate, qty, store_id, pname, ptype in rows:
            print(
                f"Restock ID: {restock_id}, "
                f"Date: {rdate}, "
                f"Store: {store_id}, "
                f"Product: {pname} ({ptype}), "
                f"Quantity: {qty}"
            )
# ABINAYA RAMESH's code
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date

# DB Connection
engine = create_engine("postgresql+psycopg2://postgres:2110@localhost/customerdb")

class Base(DeclarativeBase):
    pass

class Store(Base):
    __tablename__ = "store"

    store_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_phone_number: Mapped[str] = mapped_column(String(50))
    store_address: Mapped[str] = mapped_column(String(200))
    store_name: Mapped[str] = mapped_column(String(100))
    store_owner_name: Mapped[str] = mapped_column(String(100))

    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="store", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Store(ID={self.store_id}, Name={self.store_name}, 
        Owner={self.store_owner_name})"

class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transaction_date: Mapped[Optional[Date]] = mapped_column(Date)
    transaction_workstation: Mapped[str] = mapped_column(String(20))
    transaction_total_amount: Mapped[float] = mapped_column(Float)
    transaction_payment_method: Mapped[str] = mapped_column(String(30))

    store_id: Mapped[int] = mapped_column(ForeignKey("store.store_id"))

    store: Mapped["Store"] = relationship(back_populates="transactions")

    def __repr__(self) -> str:
        return f"Transaction(ID={self.transaction_id}, 
        Amount={self.transaction_total_amount})"

# Create Tables
Base.metadata.create_all(engine)

# ------------------------------
# INSERT DATA
# ------------------------------
with Session(engine) as session:

    # Store Data
    s1 = Store(store_id=1, store_phone_number="1+555-123-3456", 
               store_address="123 Main St", store_name="Jewel", 
               store_owner_name="Joe Smith")
    s2 = Store(store_id=2, store_phone_number="1+630-255-4788", 
               store_address="711 Smile St", store_name="Kroger", 
               store_owner_name="Bill Gates")
    s3 = Store(store_id=3, store_phone_number="1+224-124-7489", 
               store_address="411 Sad St", store_name="Aldi", 
               store_owner_name="Jill Bob")
    s4 = Store(store_id=4, store_phone_number="1+847-514-6347", 
               store_address="789 Smith Rd", store_name="Win-Dixie", 
               store_owner_name="Barb Santos")
    s5 = Store(store_id=5, store_phone_number="1+630-417-3697", 
               store_address="100 Acre Wood", store_name="Walmart", 
               store_owner_name="Piglet Eeyore")
    s6 = Store(store_id=6, store_phone_number="1+847-898-4563", 
               store_address="1725 Slough Avenue", store_name="Target", 
               store_owner_name="Michael Scott")

    session.add_all([s1, s2, s3, s4, s5, s6])

    # Transaction Data
    t1 = Transaction(transaction_id=1, transaction_date=date(2025,1,1), 
                     transaction_workstation="WS-001", 
                     transaction_total_amount=60,  
                     transaction_payment_method="Credit Card", store_id=1)
    t2 = Transaction(transaction_id=2, transaction_date=date(2025,1,1), 
                     transaction_workstation="WS-002", 
                     transaction_total_amount=10,  
                     transaction_payment_method="Check",store_id=2)
    t3 = Transaction(transaction_id=3, transaction_date=date(2025,1,1), 
                     transaction_workstation="WS-003", 
                     transaction_total_amount=45,  
                     transaction_payment_method="Credit Card", store_id=3)
    t4 = Transaction(transaction_id=4, transaction_date=date(2025,1,1), 
                     transaction_workstation="WS-004", 
                     transaction_total_amount=105, 
                     transaction_payment_method="Credit Card", store_id=1)
    t5 = Transaction(transaction_id=5, transaction_date=date(2025,1,1),
                    transaction_workstation="WS-005",
                    transaction_total_amount=25,  
                    transaction_payment_method="Direct Deposit", store_id=4)
    t6 = Transaction(transaction_id=6, transaction_date=date(2025,1,1), 
                     transaction_workstation="WS-005", 
                     transaction_total_amount=3,   
                     transaction_payment_method="Credit Card", store_id=5)
    t7 = Transaction(transaction_id=7, transaction_date=date(2025,1,1), 
                     transaction_workstation="WS-003", 
                     transaction_total_amount=112, 
                     transaction_payment_method="Check",store_id=2)
    t8 = Transaction(transaction_id=8, transaction_date=date(2025,1,1), 
                     transaction_workstation="WS-005", 
                     transaction_total_amount=56,  
                     transaction_payment_method="Cash",store_id=3)
    t9 = Transaction(transaction_id=9, transaction_date=date(2025,1,1), 
                     transaction_workstation="WS-001", 
                     transaction_total_amount=47, 
                     transaction_payment_method="Credit Card", store_id=5)
    t10 = Transaction(transaction_id=10,transaction_date=date(2025,1,2), 
                      transaction_workstation="WS-002", 
                      transaction_total_amount=87,  
                      transaction_payment_method="Cash",store_id=6)

    session.add_all([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10])
    session.commit()

# ------------------------------
# QUERIES 1:

session = Session(engine)

stmt = (
    select(Transaction)
    .join(Transaction.store)
    .where(Transaction.transaction_payment_method == "Credit Card")
)

results = session.scalars(stmt).all()

print("Transactions paid by Credit Card:")
for t in results:
    print(
        f"Transaction ID: {t.transaction_id}, "
        f"Amount: {t.transaction_total_amount}, "
        f"Store: {t.store.store_name}"
    )

