import pandas as pd
import numpy as np
import re
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
        self.id=self.id.set_index('ID')
        self.id.fillna('',inplace=True)
        self.id_lower=self.id.applymap(lambda x: x.lower())
        
    def importing_scene(self):
        self.scene=pd.read_csv(self.directory+'/Scene.csv',dtype=str)
        self.scene=self.scene.set_index('Scene')
        self.scene.fillna('',inplace=True)
        for i in self.scene.columns[0:5]:
            self.scene[i] = pd.to_numeric(self.scene[i])
            
    def importing_relation(self):
        self.relation=pd.read_csv(self.directory+'/Relation.csv',dtype=str)
        self.relation=self.relation.set_index('ID')
        self.relation['Weight'] = pd.to_numeric(self.relation['Weight'])
    
    def all_shortest_paths(self):
        #Floyd-Warshall
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
        self.shortest_path = pd.DataFrame(columns=['Source','Target','Distance','Path'])
        self.shortest_path.index.name='ID'
        for i in range(self.N):
            for j in range(self.N):
                self.shortest_path.loc[self.shortest_path.shape[0]+1] = [self.nodes[i], self.nodes[j], int(dist[i,j]), path[i,j].split(' ')]
        
    def importing_path(self):
        self.shortest_path=pd.read_csv(self.directory+'/Path.csv',dtype=str)
        self.shortest_path=self.shortest_path.set_index('ID')
        self.shortest_path['Distance'] = pd.to_numeric(self.shortest_path['Distance'])
        self.shortest_path['Path'] = self.shortest_path['Path'].apply(lambda x: eval(x))
        
    def shortest_path_csv(self):
        self.shortest_path.to_csv(self.directory+'/Path.csv')
        
    def shortest_path_excel(self):
        self.shortest_path.to_excel(self.directory+'/Path.csv')
    
    def ind(self,num):
        a='00'+str(num)
        b=a[-3:-1]+a[-1]
        return b
    
    def convert(self,name):
        if type(name)==int:
            return self.ind(name)
        elif type(name)==str:
            if name.isnumeric():
                return self.ind(name)
            name=name.lower()
            L1=list(self.id_lower.index[self.id_lower['Label'] == name])
            L2=list(self.id_lower.index[self.id_lower['Nick'] == name])
            if len(L1)==1:
                return L1[0]
            elif len(L2)==1:
                return L2[0]
            else:
                for i in self.id_lower.index:
                    pattern = re.search(name,self.id_lower.loc[i,'Label'])
                    if pattern:
                        return i
                    pattern = re.search(name,self.id_lower.loc[i,'Nick'])
                    if pattern:
                        return i
        return False
        
    def reconvert(self,myid):
        return self.id.loc[myid,'Label']
    
    def shortest_path_between(self,name1,name2):
        id1 = self.convert(name1)
        id2 = self.convert(name2)
        if id1 is not False and id2 is not False:
            aux = self.shortest_path[self.shortest_path['Source'] == id1]
            mypath = aux[aux['Target'] == id2].iloc[0,3]
            names = [self.reconvert(x) for x in mypath]
            return str(len(names)-1)+' graus de distância: '+' -> '.join(names)
        elif id1 is False:
            print('Personagem 1 não existe')
        else:
            print('Personagem 2 não existe')
            
    def max_shortest_path(self,mode='path'):
        maxim = max(self.shortest_path['Distance'])
        if mode == 'number':
            return maxim
        aux = self.shortest_path[self.shortest_path['Distance'] == maxim]
        if mode == 'dataframe':
            return aux
        print(str(maxim)+' graus de distância')
        if mode == 'relation':
            for i in range(len(aux.index)):
                print(self.reconvert(aux.iloc[i,0])+' -> '+self.reconvert(aux.iloc[i,1]))
        if mode == 'path':
            for i in range(len(aux.index)):
                names = [self.reconvert(x) for x in aux.iloc[i,3]]
                print(' -> '.join(names))
        