import pandas as pd
import numpy as np
class Graph:
    
    def __init__(self,directory):
        self.directory=directory
        self.importing_id()
        self.importing_scene()
        self.importing_relation()
        self.N = len(self.id.index)
        self.nodes = list(self.id.index)
        self.E = len(self.relation.index)
        
    def importing_id(self):
        self.id=pd.read_csv(self.directory+'/ID.csv',dtype=str)
        self.id=self.id.set_index("ID")
        self.id.fillna('',inplace=True)
        
    def importing_scene(self):
        self.scene=pd.read_csv(self.directory+'/Scene.csv',dtype=str)
        self.scene=self.scene.set_index("Scene")
        self.scene.fillna('',inplace=True)
        for i in self.scene.columns[0:5]:
            self.scene[i] = pd.to_numeric(self.scene[i])
            
    def importing_relation(self):
        self.relation=pd.read_csv(self.directory+'/Relation.csv',dtype=str)
        self.relation=self.relation.set_index('ID')
        self.relation["Weight"] = pd.to_numeric(self.relation["Weight"])
    
    def get_shortest_path(self):
        dist = np.full((self.N,self.N,self.N),np.inf,dtype=float)
        path = np.full((self.N,self.N,self.N),'',dtype=np.dtype('U50'))
        for i in range(self.N):
            dist[0,i,i] = 0
            path[0,i,i] = self.nodes[i]
        for i in range(self.E):
            source = self.nodes.index(self.relation.iloc[i,0])
            target = self.nodes.index(self.relation.iloc[i,1])
            dist[0,source,target] = 1
            path[0,source,target] = self.relation.iloc[i,0] + ' ' + self.relation.iloc[i,1]
            dist[0,target,source] = 1
            path[0,target,source] = self.relation.iloc[i,1] + ' ' + self.relation.iloc[i,0]
        for k in range(1,self.N):
            for i in range(self.N):
                for j in range(self.N):
                    if dist[k-1,i,j] <= dist[k-1,i,k-1] + dist[k-1,k-1,j]:
                        dist[k,i,j] = dist[k-1,i,j]
                        path[k,i,j] = path[k-1,i,j]
                    else:
                        dist[k,i,j] = dist[k-1,i,k-1] + dist[k-1,k-1,j]
                        path[k,i,j] = path[k-1,i,k-1] + path[k-1,k-1,j][3:]
        dist = dist[self.N-1]
        path = path[self.N-1]
        self.shortest_path = pd.DataFrame(columns=['Distance','Path'])
        self.shortest_path.index.name='ID'
        for i in range(self.N):
            for j in range(self.N):
                index = self.nodes[i] + ' ' + self.nodes[j]
                self.shortest_path.loc[index] = [int(dist[i,j]),path[i,j].split(" ")]
        
    def shortest_path_csv(self):
        self.shortest_path.to_csv(self.directory+'/Path.csv')
        
    def shortest_path_excel(self):
        self.shortest_path.to_excel(self.directory+'/Path.csv')