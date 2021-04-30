#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 15:27:18 2021

@author: adi
"""
import os
from neo4j import GraphDatabase
from flask import Flask, g, Response, request

port = os.getenv("PORT", 9000)
app = Flask(__name__, static_url_path='/static/')


class startthisthing:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_count_clusters(self):
        with self.driver.session() as session:
            number = session.write_transaction(self.getcount)
            return (number)

    @staticmethod
    def getcount(tx):
       result = tx.run("MATCH (n:CLUSTER) RETURN count(n)")
       return result.single()[0]


#return html as string variable
@app.route("/")
def get_index():
    return "<!DOCTYPE html><header><title>Adi's Neo4j</title></header><html><body>Number of clusters: "+str(greeter.print_count_clusters())+"</body></html>"

if __name__ == "__main__":
    greeter = startthisthing("bolt://localhost:7687", "adi1", "adi_pw")
    
    #verify the number that will be printed
    num = greeter.print_count_clusters()
    print(num)
    
    app.run(port=port)

    
