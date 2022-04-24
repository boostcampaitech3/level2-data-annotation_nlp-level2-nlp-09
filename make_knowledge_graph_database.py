from tqdm import tqdm
import pandas as pd
from neo4j import GraphDatabase

class Graph():
    def __init__(self, url, data, name, pwd):
        self.url = url
        self.driver = GraphDatabase.driver(self.url, auth=(name, pwd))
        self.data = data
        self.relations = list()
        
    def create_relation(self, tx, subj_name, obj_name, subj_type, obj_type, label):
        # create relations without 'no_relation'
        if label != 'no_relation':  
            
            # change label(Graph DB doesn't allow ':')
            label = label.replace(':','_').replace('/','_')

            # create entities and relationships
            tx.run("MERGE (n: " + obj_type + "{ name : $obj_name })", obj_name=obj_name, obj_type=obj_type)
            tx.run("MERGE (n: " + subj_type + "{ name : $subj_name })", subj_name=subj_name, subj_type=subj_type)
            tx.run("MATCH (a:" + subj_type + "),(b:" + obj_type+ ") WHERE a.name = $subj_name AND b.name = $obj_name MERGE (a)-[r:" + label + "]->(b) RETURN a.name, b.name", obj_name=obj_name, obj_type=obj_type,subj_name=subj_name, subj_type=subj_type, label=label)
                
    def __call__(self):             
        # create relations in order
        for i,j,k in tqdm(zip(self.data.subject_entity, self.data.object_entity, self.data.label)):
            subj_name, obj_name  = eval(i)['word'], eval(j)['word']
            subj_label, obj_label = eval(i)['type'], eval(j)['type']
            label = k
            
            # upload to neo4j graph database
            with self.driver.session() as session:
                session.write_transaction(self.create_relation, subj_name, obj_name, subj_label, obj_label, label)


if __name__ == '__main__':
    data = pd.read_csv('./merged_csv/meged_dataset.csv') #open data
    url = "neo4j://localhost:7687" #set database host
    name = "neo4j"                 #set databse name
    pwd = "1234"                   #set databset password
    KnowledgeGraph = Graph(url, data, name, pwd) #make Knowledge Graph Class
    KnowledgeGraph() 