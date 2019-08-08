class Relation:
    def __init__(self,directory):
        self.directory=directory
        d={'Weight':['']}
        self.DF=pd.DataFrame(d,columns=['Weight'],index=[0])
        d1={'Origem':[''],'Destino':[''],'Peso':['']}
        self.relacao=pd.DataFrame(d1,columns=['Origem','Destino','Peso'],index=['0'])
        self.peso_atual=0
        self.executado=0
        
    def importing_id(self):
        self.DF_ID=pd.read_csv(self.directory+'/ID.csv',dtype=str)
        self.DF_ID=self.DF_ID.set_index("ID")
        self.DF_ID.fillna('',inplace=True)
        self.DF_ID=self.DF_ID.applymap(lambda x: x.lower())
        
    def importing_scene(self):
        self.DF_scene=pd.read_csv(self.directory+'/Scene.csv',dtype=str)
        self.DF_scene=self.DF_scene.set_index("Scene")
        self.DF_scene.fillna('',inplace=True)
        for i in self.DF_scene.columns[0:4]:
            self.DF_scene[i] = pd.to_numeric(self.DF_scene[i])