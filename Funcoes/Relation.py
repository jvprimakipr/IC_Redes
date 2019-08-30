import pandas as pd
class Relation:
    
    def __init__(self,directory):
        self.directory=directory
        self.id=0
        self.scene=0
        self.importing_id()
        self.importing()
        d1={'Source':[''],'Target':[''],'Weight':['']}
        self.relation=pd.DataFrame(d1,columns=['Source','Target','Weight'],index=['1'])
        self.actual_weight=0
        self.executed=False
        self.weight=pd.Series()
        
    def data(self):
        return self.relation
        
    def execut(self):
        if self.executed:
            return 'Já executado'
        else:
            for l in range(self.scene.shape[0]):
                self.actual_weight=((self.scene.iloc[l,2]-self.scene.iloc[l,0])*60+(self.scene.iloc[l,3]-self.scene.iloc[l,1])+1)/60
                self.weight.loc[l]=self.actual_weight
                end=self.scene.iloc[l,4]+5
                for i in range(5,end-1):
                    for j in range(i+1,end):
                        s=self.scene.iloc[l,i]
                        t=self.scene.iloc[l,j]
                        rel=s+' '+t
                        aux=sum(list(self.relation.index==rel))
                        if aux==0:
                            self.relation.loc[rel,:]=[s,t,self.actual_weight]
                        else:
                            self.relation.loc[rel,'Weight']+=self.actual_weight
        self.relation=self.relation.drop('1')
        self.relation=self.relation.sort_index(0)
        self.relation['ID']=list(range(1,self.relation.shape[0]+1))
        self.relation=self.relation.set_index('ID')
        self.executed=True
        
    def importing_id(self):
        self.id=pd.read_csv(self.directory+'/ID.csv',dtype=str)
        self.id=self.id.set_index("ID")
        self.id.fillna('',inplace=True)
        self.id=self.id.applymap(lambda x: x.lower())
        
    def importing(self):
        self.scene=pd.read_csv(self.directory+'/Scene.csv',dtype=str)
        self.scene=self.scene.set_index("Scene")
        self.scene.fillna('',inplace=True)
        for i in self.scene.columns[0:5]:
            self.scene[i] = pd.to_numeric(self.scene[i])
            
    def csv(self):
        if self.executed:
            self.relation.to_csv(self.directory+'/Relation.csv')
        else:
            print('Execute primeiro')
            
    def excel(self):
        if self.executed:
            self.relation.to_excel(self.directory+'/Relation.xls')
        else:
            print('Execute primeiro')