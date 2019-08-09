import pandas as pd
class Relation:
    
    def __init__(self,directory):
        self.directory=directory
        self.weight=pd.Series()
        d1={'Source':[''],'Target':[''],'Weight':['']}
        self.relation=pd.DataFrame(d1,columns=['Source','Target','Weight'],index=['1'])
        self.relation.index.name='Relation'
        self.actual_weight=0
        self.executed=False
        
    def data(self):
        return self.relation
        
    def execut(self):
        if self.executed:
            return 'Já executado'
        
    def importing_id(self):
        self.id=pd.read_csv(self.directory+'/ID.csv',dtype=str)
        self.id=self.id.set_index("ID")
        self.id.fillna('',inplace=True)
        self.id=self.id.applymap(lambda x: x.lower())
        
    def importing(self):
        self.scene=pd.read_csv(self.directory+'/Scene.csv',dtype=str)
        self.scene=self.scene.set_index("Scene")
        self.scene.fillna('',inplace=True)
        for i in self.scene.columns[0:4]:
            self.scene[i] = pd.to_numeric(self.scene[i])
            
    def csv(self):
        if self.executed:
            self.relation.to_csv(self.directory+'/Relation.csv')
        else:
            print('Execute primeiro')
            
    def excel(self,nome):
        if self.executed:
            self.relation.to_csv(self.directory+'/Relation.xls')
        else:
            print('Execute primeiro')