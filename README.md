# Supermarket Management System (Database Design & SQL Implementation)

Welcome to the **Supermarket Management System** database portfolio! This project details the end-to-end relational database design and implementation for a modern retail supermarket environment (`SUPERMARKET`). It tracks day-to-day retail operations across customers, products, stores, employees, transaction records, and inventory replenishment tracks.

*Note: This project was originally built as a collaborative term assignment by team **Dashers**, where I served as the **Technical Advisor**, spearheading the structural formatting, consistency check, and many-to-many ORM implementations.*

---

## 📌 Project Deliverables & Highlights
* **Entity-Relationship Blueprint:** Designed a comprehensive ER diagram with full minimum/maximum cardinality constraints tracking interconnected business workflows.
* **Relational Schema Engineering:** Mapped conceptual entities into a fully normalized, high-integrity physical relational schema using strong referential integrity controls.
* **Database Scripting:** Generated production-ready DDL (Data Definition Language) and DML (Data Manipulation Language) scripts implemented in **PostgreSQL**.
* **Object-Relational Mapping (ORM):** Engineered programmatic data structures using Python's **SQLAlchemy** framework to support multi-table relational object environments.

---

## 📐 Database Architecture & Uncaptured Constraints
The physical design models real-world business constraints directly into table layers:
1. **Financial Auditing:** Product prices and employee compensation models must reflect strictly positive dollar configurations.
2. **Identity Integrity:** Candidate keys like `Employee_SSN` enforce absolute uniqueness at the structural level.
3. **No Self-Checkout Boundary:** System logic mandates that every active transaction must point to a specific, non-virtual physical employee resource.

---

## 🗄️ Relational Schema Definition

### Core Business Relationships:
* **`Store`** (`Store_ID`, Store_Address, Store_Phone_Number, Store_Name, Store_Owner_Name)
* **`Employee`** (`Employee_ID`, Employee_Address, Employee_Name, Employee_SSN)
* **`Hires`** (`Store_ID`, `Employee_ID`)
  * *Foreign Key (`Store_ID`) References Store(`Store_ID`)*
  * *Foreign Key (`Employee_ID`) References Employee(`Employee_ID`)*
* **`Customer`** (`Customer_ID`, Customer_Name, Customer_Membership, Customer_Address, Customer_Age)
* **`Product`** (`Product_ID`, Product_Type, Product_Name, Product_Price, Product_Unit_of_Measure)
* **`Transaction`** (`Transaction_ID`, Transaction_Workstation, Transaction_Date, Transaction_Total_Amount, Transaction_Payment_Method, Employee_ID, Customer_ID, Store_ID)
  * *Foreign Key (`Employee_ID`) References Employee(`Employee_ID`)*
  * *Foreign Key (`Customer_ID`) References Customer(`Customer_ID`)*
  * *Foreign Key (`Store_ID`) References Store(`Store_ID`)*
* **`Includes`** (`Transaction_ID`, `Product_ID`, Product_Quantity)
  * *Foreign Key (`Transaction_ID`) References Transaction(`Transaction_ID`)*
  * *Foreign Key (`Product_ID`) References Product(`Product_ID`)*
* **`Restock`** (`Restock_ID`, Restock_Date, Restock_Quantity, Store_ID, Product_ID)
  * *Foreign Key (`Store_ID`) References Store(`Store_ID`)*
  * *Foreign Key (`Product_ID`) References Product(`Product_ID`)*

---

## 🔍 Core Analytical Queries (PostgreSQL)

### 📈 Sum and Count of Transactions for Each Employee per Store *(My Structural Contribution)*
This high-value operational query determines the financial scale handled by store associates. It calculates the largest total revenue transaction chunks per employee at specific storefront locations exceeding a \$5 baseline margin, ordering historical outputs dynamically:

```sql
SELECT S.Store_Name, E.Employee_Name, SUM (T.Transaction_Total_Amount) AS Total_Transaction_Amount, COUNT (E.Employee_ID) AS Employee_Wrung_Up_Count
FROM Transaction T, Store S, Employee E
WHERE T.Employee_ID = E.Employee_ID AND
      T.Store_ID = S.Store_ID AND
      T.Transaction_Date = '01/01/2025'
GROUP BY S.Store_ID, E.Employee_ID
HAVING SUM(T.Transaction_Total_Amount) > 5
ORDER BY SUM(T.Transaction_Total_Amount) DESC;
```

### 🛍️ Additional Strategic Metrics Built:
* **Transaction Summary & Total Value Evaluation:** Aggregates distinct items and matrix item list calculations per unique register file to sequence the top-value carts.
* **Product Inventory Restock Batches:** Tracks bulk quantity movements and maps aggregate average volumes to prevent supply chain exhaustion bottlenecks.
* **Customer Lifetime Spending Summary:** Combines client loyalty records with total order frequencies to classify VIP member segments (Gold/Silver/Bronze tiers).

---

## 🐍 Python SQLAlchemy ORM Implementation
To transition the system from standard relational scripts to object-oriented code, I structured the complex **Many-to-Many (`N:M`) Association Mapping** linking the `Hires` table context dynamically across independent object layers:

```python
# Programmatic Class Setup for N-N Store Hires Layer
association_SE_Hires = Table(
    "Hires",
    Base.metadata,
    Column("Store_ID", ForeignKey("Store.id"), primary_key=True),
    Column("Employee_ID", ForeignKey("Employee.id"), primary_key=True),
)
```
