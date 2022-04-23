#!/usr/bin/env python

from flask_testing import TestCase
from flask import Flask
from recipeezy import db
from recipeezy.database import User, Post

import os

#manual test blueprint for test_database.py

import sqlite3
from sqlite3 import Error

def create(storedb):
    conn = None
    try:
        conn = sqlite3.connect(storedb)
        print(sqlite3.version)
        return conn
                
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()
    # return conn

def create_table(conn, create_table_sql):
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
    return conn

#not sure how to make this work
# def fill(storedb):
#     conn=sqlite3.connect(storedb)
#     store1= '''INSERT INTO Store VALUES(1, 3000, 'Retail', 'Suburban', 'Washington', 'Denver', 'CO', 80241)'''


# created seperate fill functions for each table
def create_Store(conn, store):
    
    sql = '''INSERT INTO Store VALUES(?,?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, store)
    conn.commit()
    return cur.lastrowid 

def create_product(conn, product):
    
    sql = '''INSERT INTO Product VALUES(?,?,?,(SELECT rowid FROM Category WHERE idCategory=?),?) '''
    # sql = '''INSERT INTO Product VALUES(?,?,?,?,?) ''' 
    cur = conn.cursor()
    cur.execute(sql, product)
    conn.commit()
    return cur.lastrowid

def create_category(conn, category):
    
    sql = '''INSERT INTO Category VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, category)
    conn.commit()
    return cur.lastrowid

def create_Store_product(conn, store_product):
    
    sql = '''INSERT INTO Store_product VALUES((SELECT rowid FROM Product WHERE idProduct=?),
            (SELECT rowid FROM Store WHERE idStore=?),?)'''
    # sql = '''INSERT INTO Store_product VALUES (?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, store_product)
    conn.commit()
    return cur.lastrowid

def main():
    database = r"storedb.db" 
    #create database
    conn = create(database)

    create_store_table = """CREATE TABLE IF NOT EXISTS Store(
                                idStore integer,
                                SquareFeet integer,
                                StoreType varchar,
                                LocationType varchar,
                                Address varchar,
                                City varchar,
                                StoreState varchar,
                                ZipCode varchar
                                );"""
                    
    create_store_product_table = """CREATE TABLE IF NOT EXISTS Store_product(
                                ProductID integer, 
                                StoreID integer,
                                Quantity integer
                                );"""
    
    create_product_table = """CREATE TABLE IF NOT EXISTS Product(
                                idProduct integer,
                                Name integer,
                                Price decimal,
                                CategoryID integer,
                                Description char
                                );"""
                            
    create_category_table = """CREATE TABLE IF NOT EXISTS Category(
                                idCategory integer,
                                Name char,
                                Description char
                                );"""

    # create tables
    if conn is not None:
        # # create projects table
        # create_table(conn, sql_create_projects_table)

        # # create tasks table
        # create_table(conn, sql_create_tasks_table)

        #create Store table
        create_table(conn,create_store_table)
        #create Store Product table
        create_table(conn,create_store_product_table)
        #create Product table
        create_table(conn,create_product_table)
        #create Category table
        create_table(conn,create_category_table)

    else:
        print("Error! cannot create the database connection.")

# Insert data 
    # with conn:
    #    fill(database)
    #     # return conn

    with conn:
        
        category1 = (1, 'Dairy', 'cheeses,milk,yogurt')
        category2 = (2, 'Meats', 'Chicken,beef,pork,seafood')
        category3 = (3, 'Clothing', 'Pants, shirts, shorts')
        category4 = (4, 'Kids toys', 'Playdoh,barbies,Legos')
        create_category(conn, category1)
        create_category(conn, category2)
        create_category(conn, category3)
        create_category(conn, category4)
        
        store1 = (110, 3000, 'Retail', 'Suburban', 'Washington', 'Denver', 'CO', 80241)
        store2 = (220, 6000, 'Grocery', 'City', 'Federal', 'Westminster', 'CO', 80221)
        store3 = (330, 4000, 'ToyStore', 'Mall', 'Cherry', 'Thornton', 'CO', 27401)
        create_Store(conn, store1)
        create_Store(conn, store2)
        create_Store(conn, store3)
        
        product1 = (10, 'Jogger Pants', 10.99, 3, 'Clothing')
        product2 = (20, 'Ribeye Steak', 15.00, 2, 'Meat')
        product3 = (30, 'Mozerella Cheese', 3.00, 1, 'Dairy')
        product4 = (40, 'Action Figure', 20.00, 4, 'Kids Toys')
        create_product(conn, product1)
        create_product(conn, product2)
        create_product(conn, product3)
        create_product(conn, product4)

        store_product1 = (10,110,100)
        store_product2 = (20,220,150)
        store_product3 = (30,220,300)
        store_product4 = (40,330,50)
        create_Store_product(conn, store_product1)
        create_Store_product(conn, store_product2)
        create_Store_product(conn, store_product3)
        create_Store_product(conn, store_product4)        
    

if __name__ == '__main__':
    main()
    # create_connection(r"lab7_db.db")