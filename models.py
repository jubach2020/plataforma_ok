# app/models.py


from ntpath import join
import re
from flask_login import UserMixin
from sqlalchemy.sql.expression import desc, true
from sqlalchemy.sql.selectable import Exists
from werkzeug.security import check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import update, insert, delete
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine, distinct
from sqlalchemy.sql import exists
from app import db, login_manager
#from pandas import  iterows

class Departamento(db.Model):
    
    __tablename__ = 'Departamento'
    __table_args__ = {'extend_existing': True} 

    idDepartamento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), unique=True)
    descripcion = db.Column(db.String(45))
 
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
      
    def __repr__(self):
        return f'Usuario({self.nombre}, {self.descripcion})'
        #return '<Departmento: {}>'.format(self.nombre)

    def save(self):
        if not self.idDepartamento:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Departamento.query.get(id)

    @staticmethod
    def get_all():
        return Departamento.query.all()

    def delete_dpto(id):
        dpto = Departamento.query.filter_by(idDepartamento=id).first()
        db.session.delete(dpto)
        db.session.commit()

    def update_dpto(datos):
        try:
            value = Departamento.query.filter(Departamento.idDepartamento == (datos[0])).first()
            value.nombre = str(datos[1])
            value.descripcion = str(datos[2])
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_departamento')

class Usuario(UserMixin, db.Model):
   
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'Usuario'
    __table_args__ = {'extend_existing': True} 

    idUsuario = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(15), index=True, unique=True)
    nombre = db.Column(db.String(50), index=True)
    email = db.Column(db.String(255), index=True, unique=True)  
    password = db.Column(db.String(255))
    idDpto = db.Column(db.Integer) #, db.ForeignKey('Departamento.idDepartamento'))
    #departamento = db.relationship('Departamento', backref='Usuario')
    idRol = db.Column(db.Integer) #, db.ForeignKey('Roles.id_role'))      
    #roles = db.relationship('Roles', backref='Usuario')
    #avatar = db.Column(db.String(255))

    #def __init__(self, nomUsuario,nombre, email, password, idRol, idDepto, avatar):
    def __init__(self, nomUsuario,nombre, email, password, idRol, idDpto):
        self.nombreUsuario = nomUsuario
        self.nombre = nombre
        self.email = email
        self.password = password
        self.idDpto = idDpto
        self.idRol = idRol
        #self.avatar = avatar
  

    #@property
    #def password(self):
       #raise AttributeError('password is not a readable attribute.')
   

    def checkPassword(self, password):
       return check_password_hash(self.password, password) 

    def __repr__(self):
        return f'Usuario({self.nombreUsuario}, {self.nombre},{self.email})'
        #return '<Usuario: {}>'.format(self.nombreUsuario)

    def save(self):
        if not self.idUsuario:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Usuario.query.all()

    @staticmethod
    def get_by_username(username):
        return Usuario.query.filter_by(nombreUsuario=username).first()

    def get_by_userid(userid):
        return Usuario.query.filter_by(idUsuario=userid).first()

    @staticmethod 
    def get_by_email(email):
        return Usuario.query.filter_by(email=email).first() 


    def is_authenticated(self):
	    return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.idUsuario)

    def is_admin(self):
        if self.idRol==1:
            return True
        return False

    def existe_email(correo):
        user = Usuario.query.filter_by(email = correo).first()
        if user is None:
            return False
        else:
            return True

    def existe_username(name):
        user = Usuario.query.filter_by(nombreUsuario = name).first()
        if user is None:
            return False
        else:
            return True

    def delete_user(id):
        user = Usuario.query.filter_by(idUsuario=id).first()
        db.session.delete(user)
        db.session.commit()

    def update_user(datos):
        try:
            value = Usuario.query.filter(Usuario.idUsuario == (datos[0])).first()            
            value.nombreUsuario = str(datos[1])
            value.nombre = str(datos[2])
            value.email = str(datos[3])
            value.idRol = str(datos[4])
            value.idDpto = str(datos[5])
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_user')

    us = []
    def get_user_by_email(email):
        for us in Usuario:
            if us.email == email:
                return us
        return None

    
    #def (userid):
        #user = Usuario.query.filter_by(idUsuario=userid).first()
        #return user.avatar
    
     
    # Set up user_loader
    #@login_manager.user_loader
    #def load_user(idUsuario):
     #   return Usuario.query.get(int(idUsuario))



class Roles(db.Model):
    
    __tablename__ = 'Roles'
    __table_args__ = {'extend_existing': True} 

    id_role = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(60), unique=True)

    def __repr__(self):
        return f'Role({self.rol})'
        #return '<Role: {}>'.format(self.rol)
    
    def __init__(self, id_role, rol):
        self.id_role = id_role
        self.rol = rol
          
    def save(self):
        #if not self.id_role:
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Roles.query.get(id)

    @staticmethod
    def get_all():
        return Roles.query.all()

    def delete_rol(id):
        rol = Roles.query.filter_by(id_role=id).first()
        db.session.delete(rol)
        db.session.commit()

    def update_rol(datos):
        try:
            value = Roles.query.filter(Roles.id_role == (datos[0])).first()
            value.rol = str(datos[1])
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_rol')


class AgrupacionArticulos(db.Model):
    
    __tablename__ = 'AgrupacionArticulos'
    __table_args__ = {'extend_existing': True} 

    Id = db.Column(db.Integer, primary_key=True)
    cn = db.Column(db.String(20), unique=True)
    idAgrupacion  = db.Column(db.Integer)
    idLaboratorio = db.Column(db.String(25))

    def __repr__(self):
        return f'CN({self.cn})'
        #return '<CN: {}>'.format(self.cn)
    
    def __init__(self, cn, idagr, idLab):
        self.cn = cn 
        self.idAgrupacion = idagr
        self.idLaboratorio = idLab
          
    def listaAgregados(idAgr):
        lista = db.session.query(AgrupacionArticulos.cn).filter_by(idAgrupacion=idAgr).all()
        return lista
   
    def save(self):
        #if not self.Id:
        db.session.add(self)
        db.session.commit()

    def delete_artAgr_by_idAgr(idAgr):
        artAgr = AgrupacionArticulos.query.filter_by(idAgrupacion=idAgr).delete()
       # db.session.delete(artAgr)
        db.session.commit()
   
    def delete_artAgr(id):
        artAgr = AgrupacionArticulos.query.filter_by(Id=id).first()
        db.session.delete(artAgr)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return AgrupacionArticulos.query.get(id)

    @staticmethod
    def get_all():
        return AgrupacionArticulos.query.all()

    def delete_agr_art(id):
        agr = AgrupacionArticulos.query.filter_by(Id=id).first()
        db.session.delete(agr)
        db.session.commit()

    def update_agr_art(datos):
        try:
            value = AgrupacionArticulos.query.filter(AgrupacionArticulos.Id == (datos[0])).first()
            value.cn = str(datos[1])
            value.idAgrupacion = str(datos[2])
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_agrupacion')
    
    def update_idLab(idLab):
        try:
            value = AgrupacionArticulos.query.filter(AgrupacionArticulos.idLaboratorio == (idLab)).first()
            value.idLaboratorio = idLab
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_idLab')

    def get_articulos_limit():
      
        consulta = "SELECT DISTINCT vademecum.CN, vademecum.DESCRIPCION, vademecum.`CODIGO LABORATORIO`, \
                    (select MAX(vadeLaboratorios.NOMBRE) FROM vadeLaboratorios WHERE  \
                    vadeLaboratorios.CODIGO=vademecum.`CODIGO LABORATORIO`) AS Labo, \
					vademecum.`CODIGO FAMILIA BI`, (select vadeFamilias.nomFam FROM vadeFamilias WHERE \
                    vadeFamilias.idFamiliaEco=vademecum.`CODIGO FAMILIA BI`) As Familia, \
                    Verticals.C1, Verticals.C2, Verticals.C3, Verticals.C4, \
                    CONCAT('<div class=',char(34),'divAgregar',char(34),'><div class=',char(34),'form-check form-switch',char(34),'><input class=',char(34),'form-check-input',char(34),' type=',char(34),'checkbox',char(34),' name=',char(34),'flexSwitchCheckChecked',char(34),' id=',char(34),vademecum.CN,char(34),'/><label class=',char(34),'form-check-label',char(34),' for=',char(34),'flexSwitchCheckChecked',char(34),'>Agregar</label> </div></div>') as AgrHTML \
                    FROM vademecum,  Verticals WHERE vademecum.CN=Verticals.`CN6 EAN`"

        server = SSHTunnelForwarder(
            ('185.253.152.91', 12984),
            ssh_username="rO4HggXMbS", 
            ssh_password="huEv62eJ7B",  
            remote_bind_address=('127.0.0.1', 3306))
        server.start()    
        engine = create_engine('mysql+mysqldb://4jiyZjWqxp:M6GMfD77W3@127.0.0.1:%s/ecoextract' % server.local_bind_port)
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()
            for row in rows:
                results.append(list(row))  
                         
        server.stop()        
        return results

    
    def get_articulos():        
        consulta = "SELECT DISTINCT vademecum.CN, vademecum.DESCRIPCION, vademecum.`CODIGO LABORATORIO`, \
                    (select MAX(vadeLaboratorios.NOMBRE) FROM vadeLaboratorios WHERE  \
                    vadeLaboratorios.CODIGO=vademecum.`CODIGO LABORATORIO`) AS Labo, \
					vademecum.`CODIGO FAMILIA BI`, (select vadeFamilias.nomFam FROM vadeFamilias WHERE \
                    vadeFamilias.idFamiliaEco=vademecum.`CODIGO FAMILIA BI`) As Familia, \
                    Verticals.C1, Verticals.C2, Verticals.C3, Verticals.C4, \
                    CONCAT('<div class=',char(34),'divAgregar',char(34),'><div class=',char(34),'form-check form-switch',char(34),'><input class=',char(34),'form-check-input',char(34),' type=',char(34),'checkbox',char(34),' name=',char(34),'flexSwitchCheckChecked',char(34),' id=',char(34),vademecum.CN,char(34),'/><label class=',char(34),'form-check-label',char(34),' for=',char(34),'flexSwitchCheckChecked',char(34),'>Agregar</label> </div></div>') as AgrHTML \
                    FROM vademecum,  Verticals WHERE vademecum.CN=Verticals.`CN6 EAN`"

        server = SSHTunnelForwarder(
            ('185.253.152.91', 12984),
            ssh_username="rO4HggXMbS", 
            ssh_password="huEv62eJ7B",  
            remote_bind_address=('127.0.0.1', 3306))
        server.start()    
        engine = create_engine('mysql+mysqldb://4jiyZjWqxp:M6GMfD77W3@127.0.0.1:%s/ecoextract' % server.local_bind_port)
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()
            for row in rows:
                results.append(list(row))  
                         
        server.stop()        
        return results

    def get_agregados(idAgr):
        consulta=" SELECT DISTINCT vademecum.CN, vademecum.DESCRIPCION, vademecum.`CODIGO LABORATORIO`,  \
                   (select LABOR.NOMBRE FROM LABOR WHERE LABOR.CODIGO=vademecum.`CODIGO LABORATORIO` LIMIT 1,1) AS Labo, \
                   (select Familia.Descripcion FROM Familia WHERE Familia.IdFamilia=vademecum.`CODIGO FAMILIA BI` LIMIT 1,1) As Familia, \
                   Verticals.C1, Verticals.C2, Verticals.C3, Verticals.C4, \
                   CONCAT('<div class=',char(34),'divAgregar',char(34),'><div class=',char(34),'form-check form-switch',char(34),'> \
                   <input class=',char(34),'form-check-input',char(34),' type=',char(34),'checkbox',char(34),' name=',char(34),'flexSwitchCheckChecked',char(34),' id=',char(34),vademecum.CN,char(34),'/> \
                   <label class=',char(34),'form-check-label',char(34),' for=',char(34),'flexSwitchCheckChecked',char(34),'>Agregar</label> </div></div>') as AgrHTML, IF((SELECT count(1) FROM AgrupacionArticulos WHERE AgrupacionArticulos.idAgrupacion=" + idAgr +" \
                   and AgrupacionArticulos.cn=vademecum.CN)=1,'true','false') as agregado \
                   FROM vademecum,  Verticals WHERE vademecum.CN=Verticals.`CN6 EAN` ORDER BY agregado Desc"        
        server = SSHTunnelForwarder(
            ('185.253.152.91', 12984),
            ssh_username="rO4HggXMbS", 
            ssh_password="huEv62eJ7B",  
            remote_bind_address=('127.0.0.1', 3306))
        server.start()    
        engine = create_engine('mysql+mysqldb://4jiyZjWqxp:M6GMfD77W3@127.0.0.1:%s/ecoextract' % server.local_bind_port)
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()
            for row in rows:
                results.append(list(row)) 
                #print(row[9])            
        server.stop()        
        return results

    def insertarDatosExcel(datos):
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        for row in datos.itertuples():  
            if (not Agrupacion.existe(row.Agrupacion)):        
                newAgr = Agrupacion(row.Agrupacion, '')
                newAgr.save()
            else: 
                newAgr = Agrupacion.get_by_Agrupacion(row.Agrupacion)
            cn = row.CN
            idAgr = newAgr.Id
            codlab = row.CodigoLab
            consultaInsert = "INSERT INTO AgrupacionArticulos (cn, idAgrupacion, idLaboratorio) VALUES ( '%s',%i, '%s')  \
                ON DUPLICATE KEY UPDATE cn= '%s' ,idAgrupacion= %i , idLaboratorio='%s'" % (cn,idAgr,codlab , cn, idAgr,codlab)          
            with engine.connect() as con:
                rs = con.execute(consultaInsert)

class Agrupacion(db.Model):
    """
    Create a Agrupacion table
    """

    __tablename__ = 'Agrupacion'
    __table_args__ = {'extend_existing': True} 
    Id = db.Column(db.Integer, primary_key=True)
    Agrupacion = db.Column(db.String(255), unique=True)
    color =  db.Column(db.String(45))
    def __repr__(self):
        return f'Agrupacion({self.Agrupacion}, {self.color})'
        #return '<Agrupacion: {}>'.format(self.Agrupacion)   
    

    def __init__(self, agr, col):
        self.color = col
        self.Agrupacion = agr
          
    def save(self):
        if not self.Id:
            db.session.add(self)
            db.session.commit()

    def existe(agrupNombre):
        exists  =  bool(Agrupacion.query.filter_by(Agrupacion=agrupNombre).first())
        return exists

    def get_by_Agrupacion(agr):
        agr = Agrupacion.query.filter_by(Agrupacion=agr).first()
        return agr

    @staticmethod
    def get_by_id(id):
        return Agrupacion.query.get(id)

    @staticmethod
    def get_all():
        return Agrupacion.query.all()

    def delete_agr(id):
        agr = Agrupacion.query.filter_by(Id=id).first()
        db.session.delete(agr)
        db.session.commit()

    def update_agr(datos):
        try:
            value = Agrupacion.query.filter(Agrupacion.Id == (datos[0])).first()
            value.Agrupacion = str(datos[1])
            value.color = str(datos[2])
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_agrupacion')

    def insertarDatosExcel(datos):        
        for row in datos.itertuples():    
            if (not Agrupacion.existe(row.Agrupacion)):   
                newAgr = Agrupacion(row.Agrupacion, row.color)
                newAgr.save()
           


class FarmaciasVerticales (db.Model):
    
    __tablename__ = 'FarmaciasVerticales'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    nif = db.Column(db.String(15))
    descripcion  = db.Column(db.String(255))
    Activo = db.Column(db.String(2))
    Vertical =  db.Column(db.String(50))
    Proveedor = db.Column(db.String(20))
    Nombre = db.Column(db.String(160))
    Mayorista = db.Column(db.String(50))

    
    def __repr__(self):
        return f'FarmaciasVerticales({self.nif}, {self.descripcion},{self.Activo},{self.Vertical},{self.Proveedor},{self.Nombre},{self.Mayorista})'
    
    def __init__(self, Nif, descripcion, Activo, Vertical, Proveedor ,Nombre, Mayorista):
        self.Nif = Nif
        self.descripcion = descripcion
        self.Activo = Activo
        self.Vertical = Vertical
        self.Proveedor = Proveedor
        self.Nombre = Nombre
        self.Mayorista = Mayorista
          
   
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id):
        return FarmaciasVerticales.query.get(id)

    @staticmethod
    def get_all():
        consulta="SELECT * FROM FarmaciasVerticales"        
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()          
        return rows

        
    def get_farmacia_by_vertical(vert):
        res = FarmaciasVerticales.query.filter_by(Vertical=vert).all()
        return res

    def get_verticales():
        consulta="SELECT DISTINCT Vertical FROM FarmaciasVerticales"        
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()          
        return rows

    def update_far(datos):        
        consulta="UPDATE FarmaciasVerticales SET nif='"+str(datos[1])+"',descripcion='"+str(datos[2])+"',Activo='"+str(datos[3])+ \
                 "',Vertical='"+str(datos[4])+"',Proveedor='"+str(datos[5])+"',Nombre='"+str(datos[6])+"',Mayorista='"+str(datos[7])+"' WHERE "+ \
                 "id="+(datos[0])
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
       
        with engine.connect() as con:
            rs = con.execute(consulta)
       

    def borrarFar(id):    
        consulta="DELETE FROM FarmaciasVerticales WHERE id="+id
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        with engine.connect() as con:
            rs = con.execute(consulta)

    def insertarDatosExcel(datos):        
        for row in datos.itertuples():         
            newFar = FarmaciasVerticales(row.Nif, row.Descripcion, row.Activo, row.Vertical, row.Proveedor, row.Nombre, row.Mayorista)
            newFar.save()

class ArtVertical (db.Model):
   
    __tablename__ = 'ArtVertical'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    CN6 = db.Column(db.String(12), unique=True)
    EAN  = db.Column(db.String(20), unique=True)
    PRODUCTE = db.Column(db.String(255))
    STCK_MIN =  db.Column(db.Integer)
    STCK_MAX = db.Column(db.Integer)
    MULTIPLO = db.Column(db.Integer)
    ACTIVO = db.Column(db.String(2))
    Sin_AH = db.Column(db.String(15))
    Sin_FEDE = db.Column(db.String(15))
    IVA =  db.Column(db.String(4))
    codVertical =  db.Column(db.String(50))

    
    def __repr__(self):
        return f'ArtVertical({self.CN6}, {self.EAN},{self.PRODUCTE},{self.STCK_MIN},{self.STCK_MAX},\
            {self.MULTIPLO},{self.ACTIVO},{self.Sin_AH},{self.Sin_FEDE},{self.IVA},{self.codVertical})'
    
    def __init__(self, CN6, EAN, PRODUCTE, STCK_MIN, STCK_MAX ,MULTIPLO, ACTIVO,Sin_AH,Sin_FEDE,IVA,codVertical):
        self.CN6      = CN6
        self.EAN      = EAN
        self.PRODUCTE = PRODUCTE
        self.STCK_MIN = STCK_MIN
        self.STCK_MAX = STCK_MAX
        self.MULTIPLO = MULTIPLO
        self.ACTIVO   = ACTIVO
        self.Sin_AH   = Sin_AH
        self.Sin_FEDE = Sin_FEDE
        self.IVA      = IVA
        self.codVertical = codVertical
          
   
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
   
    @staticmethod
    def get_by_id(id):
        return ArtVertical.query.get(id)

    @staticmethod
    def get_all():
        consulta="SELECT * FROM ArtVertical"        
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()          
        return rows

        
    def get_articulos_by_vertical(vert):
        res = ArtVertical.query.filter_by(Vertical=vert).all()
        return res
    
    def get_articulo_by_cn(cn):
        res = ArtVertical.query.filter_by(CN6=cn).first()
        return res

   
    def get_verticales():
        consulta="SELECT DISTINCT codVertical FROM ArtVertical"        
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()          
        return rows

    def existeArt(cn):
        artVert =  ArtVertical.query.filter_by(CN6 = cn).first()
        if artVert is None:
            return True
        else:
            return False

    def update_art(datos):         
        consulta="UPDATE ArtVertical SET CN6='"+str(datos[1])+"',EAN='"+str(datos[2])+"',PRODUCTE='"+str(datos[3])+ \
                 "',STCK_MIN='"+str(datos[4])+"',STCK_MAX='"+str(datos[5])+"',MULTIPLO='"+str(datos[6])+"',ACTIVO='"+str(datos[7])+ \
                 "',Sin_AH='"+str(datos[8])+"',Sin_FEDE='"+str(datos[9])+"',IVA='"+str(datos[10])+"',codVertical='"+str(datos[11])+"' WHERE "+ \
                 "id="+(datos[0])
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')       
        with engine.connect() as con: 
            rs = con.execute(consulta)
       

    def borrarArt(id):    
        consulta="DELETE FROM ArtVertical WHERE id="+id
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        with engine.connect() as con:
            rs = con.execute(consulta)
    
    def insertarDatosExcel(datos):
        for row in datos.itertuples():         
            newFar = ArtVertical(row.CN6, row.EAN, row.PRODUCTE, row.STCK_MIN, row.STCK_MAX ,row.MULTIPLO, row.ACTIVO,row.Sin_AH,row.Sin_FEDE,row.IVA,row.codVertical)
            newFar.save()


class vademecum (db.Model):
   
    __tablename__ = 'vademecum'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    CN = db.Column(db.String(20))
    DESCRIPCION  = db.Column(db.String(255))
    CODIGO  = db.Column(db.String(10))
    FAMILIA = db.Column(db.String(10))

    
    def __repr__(self):
        return f'vademecum({self.CN}, {self.DESCRIPCION},{self.CODIGO},{self.FAMILIA})'
    
    def __init__(self, CN, DESCRIPCION, CODIGO, FAMILIA):
        self.CN = CN
        self.DESCRIPCION = DESCRIPCION
        self.CODIGO = CODIGO
        self.FAMILIA = FAMILIA
       
          
   
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id):
        return vademecum.query.get(id)
        
    def get_articulo_por_cn(cn):
        res = vademecum.query.filter_by(CN=cn).first()
        return res

    @staticmethod
    def get_all():
        consulta="SELECT * FROM vademecum"        
        server = SSHTunnelForwarder(
            ('185.253.152.91', 12984),
            ssh_username="rO4HggXMbS", 
            ssh_password="huEv62eJ7B",  
            remote_bind_address=('127.0.0.1', 33006))
        server.start()    
        engine = create_engine('mysql+mysqldb://4jiyZjWqxp:M6GMfD77W3@127.0.0.1:%s/ecoextract' % server.local_bind_port)
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()
            for row in rows:
                results.append(list(row)) 
                #print(row[9])            
        server.stop()        
        return results

    def get_articulos():
        consulta="SELECT DISTINCT vademecum.CN,  vademecum.DESCRIPCION, vademecum.`CODIGO LABORATORIO`, \
                (select MAX(vadeLaboratorios.NOMBRE) FROM vadeLaboratorios WHERE vadeLaboratorios.CODIGO=vademecum.`CODIGO LABORATORIO`) AS Labo, \
                 vademecum.`CODIGO FAMILIA BI`,(select vadeFamilias.nomFam FROM vadeFamilias \
                 WHERE vadeFamilias.idFamiliaEco=vademecum.`CODIGO FAMILIA BI`) As Familia, Verticals.C1, Verticals.C2, Verticals.C3, Verticals.C4 \
                FROM vademecum,  Verticals WHERE vademecum.CN=Verticals.`CN6 EAN`"
       
        server = SSHTunnelForwarder(
            ('185.253.152.91', 12984),
            ssh_username="rO4HggXMbS", 
            ssh_password="huEv62eJ7B",  
            remote_bind_address=('127.0.0.1', 3306))
        server.start()    
        engine = create_engine('mysql+mysqldb://4jiyZjWqxp:M6GMfD77W3@127.0.0.1:%s/ecoextract' % server.local_bind_port)
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()
            for row in rows:
                results.append(list(row)) 
                           
        server.stop()        
        return results


class FiltrosVerticales (db.Model):
    
    __tablename__ = 'FiltrosVerticales'
    __table_args__ = {'extend_existing': True} 

    id        = db.Column(db.Integer, primary_key=True)
    Nif       = db.Column(db.String(20))
    idUnit    = db.Column(db.String(20))
    Farmacia  = db.Column(db.String(255))
        
    def __repr__(self):
        return f'FiltrosVerticales({self.Nif}, {self.idUnit},{self.Farmacia})'
    
    def __init__(self, Nif, idUnit, Farmacia):
        self.Nif = Nif
        self.idUnit   = idUnit
        self.Farmacia = Farmacia
    
    def existe(idUn):        
        exists  =  bool(FiltrosVerticales.query.filter_by(idUnit=idUn).first())
        return exists
   
    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()
            return True
        else: 
            return False     

    @staticmethod
    def get_by_id(id):
        return FiltrosVerticales.query.get(id)

    @staticmethod
    def get_all():
        return FiltrosVerticales.query.all()

    def borrarFar(nif):
        try:
            db.session.query(FiltrosVerticales).filter_by(Nif=nif).delete()
            db.session.commit()
        except:
              db.session.rollback()

    def delete_farm(id):
        try:
            num_rows_deleted = db.session.query(FiltrosVerticales).filter_by(id=id).delete()
            db.session.commit()
        except:
            db.session.rollback()
    
    def agregadas():
        lista = db.session.query(FiltrosVerticales.Nif,FiltrosVerticales.idUnit,FiltrosVerticales.Farmacia).all()   
        return lista    
    
    def get_filtros_farmacias():     
        consulta="SELECT Unit.nif, Unit.id, Unit.description, \
                  CASE Unit.id_group \
                      WHEN 1 THEN 'INICI' \
                      WHEN 2 THEN 'IMPULS' \
                      WHEN 3 THEN 'READY' \
                      WHEN 4 THEN 'REFERENT' \
                  END As Vertix From fidfarma.Unit"   
     
        server = SSHTunnelForwarder(
            ('185.253.152.91', 12984),
            ssh_username="rO4HggXMbS", 
            ssh_password="huEv62eJ7B",  
            remote_bind_address=('127.0.0.1', 3306))
        server.start()    
        engine = create_engine('mysql+mysqldb://4jiyZjWqxp:M6GMfD77W3@127.0.0.1:%s/ecoextract?charset=utf8mb4' % server.local_bind_port)
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()
            for row in rows:
                results.append(list(row))                          
        server.stop()        
        return results

    def insertarDatosExcel(datos):      
        try:
            num_rows_deleted = db.session.query(FiltrosVerticales).delete()
            db.session.commit()
            for row in datos.itertuples():          
                newFiltro = FiltrosVerticales(row.Nif, row.idUnidad, row.Farmacia)
                newFiltro.save()
        except:
            db.session.rollback()      
           


class Filtros(db.Model):
   
    __tablename__  = 'Filtros'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    filtro = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return '<Filtros: {}>'.format(self.Filtros)
    
    def __init__(self, fil):
        self.filtro = fil
          
    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Filtros.query.get(id)

    @staticmethod
    def get_all():
        return Filtros.query.all()

    def delete_filtro(id):
        fil = Filtros.query.filter_by(id=id).first()
        db.session.delete(fil)
        db.session.commit()

    def update_filtro(datos):
        try:
            value = Filtros.query.filter(Filtros.id == (datos[0])).first()
            value.filtro = str(datos[1])
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_filtro')
        
class FiltrosArticulos(db.Model):
   
    __tablename__ = 'FiltrosArticulos'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    cn = db.Column(db.String(20), unique=True)
    idFiltro  = db.Column(db.Integer)
    idLaboratorio = db.Column(db.String(25))

    def __repr__(self):
        return '<CN: {}>'.format(self.cn)
    
    def __init__(self, cn, idFil, idLab):
        self.cn = cn 
        self.idFiltro = idFil
        self.idLaboratorio = idLab
          
    def listaAgregados(idFil):
        lista = db.session.query(FiltrosArticulos.cn).filter_by(idFiltro=idFil).all()        
        return lista
   
    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()

    def delete_artFil_by_idFil(idFil):
        filArt = FiltrosArticulos.query.filter_by(idFiltro=idFil).delete()
        db.session.commit()
   
    def delete_artFil(id):
        filArt = FiltrosArticulos.query.filter_by(id=id).first()
        db.session.delete(filArt)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return FiltrosArticulos.query.get(id)

    @staticmethod
    def get_all():
        return FiltrosArticulos.query.all()

    def delete_fil_art(id):
        filArt = FiltrosArticulos.query.filter_by(id=id).first()
        db.session.delete(filArt)
        db.session.commit()

    def update_fil_art(datos):
        try:
            value = FiltrosArticulos.query.filter(FiltrosArticulos.id == (datos[0])).first()
            value.cn = str(datos[1])
            value.idFiltro = str(datos[2])
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_agrupacion')
    
    def update_idLab(idLab):
        try:
            value = FiltrosArticulos.query.filter(AgrupacionArticulos.idLaboratorio == (idLab)).first()
            value.idLaboratorio = idLab
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_idLab')

    def insertarDatosExcel(datos): 
        for row in datos.itertuples():      
            #newFiltro = Filtros(row.Filtro)    
            #newFiltro.save()
            newFiltroArt = FiltrosArticulos(row.CN, row.Filtro, row.CodigoLab)    
            newFiltroArt.save() 

        
class FiltroLaboratorio (db.Model):
  
    __tablename__ = 'FiltroLaboratorio'
    __table_args__ = {'extend_existing': True} 

    Id = db.Column(db.Integer, primary_key=True)
    Codigo = db.Column(db.String(5))
    Nombre = db.Column(db.String(50))
    Vertical =  db.Column(db.String(50))
    Color    =  db.Column(db.String(10))
    
    
    def __repr__(self):
        return f'FiltroLaboratorio({self.Codigo}, {self.Nombre},{self.Vertical},{self.Color})'
    
    def __init__(self, Codigo, Nombre,  Vertical, Color):
        self.Codigo   = Codigo
        self.Nombre   = Nombre
        self.Vertical = Vertical
        self.Color    = Color
   
    def save(self):
        if not self.Id:
            db.session.add(self)
            db.session.commit()
 
    @staticmethod
    def get_by_id(id):
        return FiltroLaboratorio.query.get(id)

    @staticmethod
    def get_all():
        consulta="SELECT Id, Codigo, Nombre, Vertical, Color FROM FiltroLaboratorio"        
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones',pool_size=20, max_overflow=0)
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()          
        return rows

    @staticmethod
    def get_verticals():      
        consulta="SELECT Vertical FROM FiltroLaboratorio Where Vertical<>'' and Vertical<>'0' Group By Vertical"        
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()          
        return rows
        
    def get_lab_by_vertical(vert):
        res = FiltroLaboratorio.query.filter_by(Vertical=vert).all()
        return res

    def existeLab(cod, vert):
        exists  =  bool(FiltroLaboratorio.query.filter_by(Codigo=cod, Vertical=vert).first())
        return exists
    
    def get_laboratorios():
        consulta="SELECT CODIGO, TIPO, NOMBRE, DIRECCION, CIUDAD , PROVINCIA, CODIGOPOSTAL, TELEFONO FROM LABOR"      
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()
            for row in rows:
                results.append(list(row))                        
        return results
        

    def update_lab(datos):        
        consulta="UPDATE FiltroLaboratorio SET Codigo='"+str(datos[1])+"',Nombre='"+str(datos[2])+"',Vertical='"+str(datos[3])+ \
                 "',Color='"+str(datos[4])+"' WHERE "+ \
                  "Id="+(datos[0])
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
       
        with engine.connect() as con:
            rs = con.execute(consulta)
       

    def borrarLab(id):    
        consulta="DELETE FROM FiltroLaboratorio WHERE Id="+id
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        with engine.connect() as con:
            rs = con.execute(consulta)

    def insertarDatosExcel(datos):        
        for row in datos.itertuples(): 
            print(FiltroLaboratorio.existeLab(row.CodigoLab, row.Vertical))
            if not FiltroLaboratorio.existeLab(row.CodigoLab, row.Vertical):         
                newfiltroLab = FiltroLaboratorio(row.CodigoLab, row.Nombre, row.Vertical, row.Color)    
                newfiltroLab.save() 

################################################################################################################################

class Incentivo(db.Model):
   
    __tablename__ = 'Incentivo'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    importe = db.Column(db.Numeric(6,2))
    
    def __repr__(self):
        return f'Incentivo({self.importe})'
       
    def __init__(self, imp):
        self.importe = imp       
          
    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Incentivo.query.get(id)

    @staticmethod
    def get_all():
        return Incentivo.query.all()

    def existe(imp):
        exists  =  bool(Incentivo.query.filter_by(importe=imp).first())
        return exists

    def get_by_Importe(imp):
        agr = Incentivo.query.filter_by(importe=imp).first()
        return agr

    def delete_incentivo(id):
        Incentivo.query.filter_by(idIncentivo=id).delete()
        db.session.commit()

    def update_incentivo(datos):
        try:
            value = Incentivo.query.filter(Incentivo.id == (datos[0])).first()
            value.importe = str(datos[1])
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_incentivo')

class IncentivosArticulos(db.Model):
   
    __tablename__ = 'IncentivosArticulos'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    cn = db.Column(db.String(20), unique=True)
    idIncentivo  = db.Column(db.Integer)
    idLaboratorio = db.Column(db.String(25))
    idIncentivoDos  = db.Column(db.Integer)

    def __repr__(self):
        return f'CN({self.cn}, {self.idIncentivo}, {self.cn}, {self.idLaboratorio}, {self.idIncentivoDos})'
       
    
    def __init__(self, cn, idinc, idLab, idincDos):
        self.cn = cn 
        self.idIncentivo = idinc
        self.idLaboratorio = idLab
        self.idIncentivoDos = idincDos
          
    def listaAsignados(idInc):
        lista = db.session.query(IncentivosArticulos.cn).filter_by(idIncentivo=idInc).all()
        results = []
        for row in lista:
                results.append(list(row))  
        return results
   
    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()

    def delete_art(cn,idLab):
        artInc = IncentivosArticulos.query.filter_by(cn=cn, idLaboratorio=idLab).delete()
        db.session.commit()
   
    def delete_artInc(id):
        artInc = IncentivosArticulos.query.filter_by(id=id).first()
        db.session.delete(artInc)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Incentivo.query.get(id)

    @staticmethod
    def get_all():
        return IncentivosArticulos.query.all()

    def delete_inc_art(id):
        inc = IncentivosArticulos.query.filter_by(id=id).first()
        db.session.delete(inc)
        db.session.commit()

    def update_inc_art(id,cn ):
        try:
            value = IncentivosArticulos.query.filter(cn = cn).first()
            value.cn = str()        
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_inc_art')

    '''
    def update_incDos(cn,inc,idlab,inc2 ):
        try:
            idIncentivo = IncentivosArticulos.get_id(cn,inc,idlab,)
            value = IncentivosArticulos.query.filter(cn = cn , idIncentivo=inc2 , idLaboratorio=idlab).first()    
            value.idIncentivo = str('inc',)
        except:       
             print('Error en update de incentivo') 
    '''
    def update_idLab(idLab):
        try:
            value = IncentivosArticulos.query.filter(IncentivosArticulos.idLaboratorio == (idLab)).first()
            value.idLaboratorio = idLab
            db.session.flush()
            db.session.commit()          
        except:
            print('Error en update_idLab')
    
    def get_articulos():        
        
        consulta = "SELECT DISTINCT vademecum.CN, vademecum.DESCRIPCION, vademecum.`CODIGO LABORATORIO`, \
                    (select MAX(vadeLaboratorios.NOMBRE) FROM vadeLaboratorios WHERE  \
                    vadeLaboratorios.CODIGO=vademecum.`CODIGO LABORATORIO`) AS Labo, \
					vademecum.`CODIGO FAMILIA BI`, (select vadeFamilias.nomFam FROM vadeFamilias WHERE \
                    vadeFamilias.idFamiliaEco=vademecum.`CODIGO FAMILIA BI`) As Familia, \
                    Verticals.C1, Verticals.C2, Verticals.C3, Verticals.C4 \
                    FROM vademecum,  Verticals WHERE vademecum.CN=Verticals.`CN6 EAN`"
       
        server = SSHTunnelForwarder(
            ('185.253.152.91', 12984),
            ssh_username="rO4HggXMbS",
            ssh_password="huEv62eJ7B",  
            remote_bind_address=('127.0.0.1', 3306))
        server.start()    
        engine = create_engine('mysql+mysqldb://4jiyZjWqxp:M6GMfD77W3@127.0.0.1:%s/ecoextract' % server.local_bind_port)
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()
            for row in rows:
                results.append(list(row))  
                         
        server.stop()        
        return results
       


    def get_agregados(idAgr):
        consulta="SELECT DISTINCT vademecum.CN, vademecum.DESCRIPCION, vademecum.`CODIGO LABORATORIO`,  \
                   (select LABOR.NOMBRE FROM LABOR WHERE LABOR.CODIGO=vademecum.`CODIGO LABORATORIO` LIMIT 1,1) AS Labo, \
                   (select Familia.Descripcion FROM Familia WHERE Familia.IdFamilia=vademecum.`CODIGO FAMILIA BI` LIMIT 1,1) As Familia, \
                    Verticals.C1, Verticals.C2, Verticals.C3, Verticals.C4, \
                    IF((SELECT count(1) FROM AgrupacionArticulos WHERE AgrupacionArticulos.idAgrupacion=" + idAgr +" and AgrupacionArticulos.cn=vademecum.CN)=1,'true','false') as agregado\
                    FROM vademecum,  Verticals WHERE vademecum.CN=Verticals.`CN6 EAN` ORDER BY agregado DESC"

        server = SSHTunnelForwarder(
            ('185.253.152.91', 12984),
            ssh_username="rO4HggXMbS", 
            ssh_password="huEv62eJ7B",  
            remote_bind_address=('127.0.0.1', 3306))
        server.start()    
        engine = create_engine('mysql+mysqldb://4jiyZjWqxp:M6GMfD77W3@127.0.0.1:%s/ecoextract' % server.local_bind_port)
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()
            for row in rows:
                results.append(list(row)) 
        server.stop()        
        return results

    def insertarDatosExcel(datos): 
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
        for row in datos.itertuples():  
            if (not Incentivo.existe(row.Incentivo)):        
                newInc = Incentivo(row.Incentivo)
                newInc.save()
            else: 
                newInc = Incentivo.get_by_Importe(row.Incentivo)
            cn = row.CN
            idInc = newInc.id
            codlab = row.CodigoLab
            if (row.IncentivoDos!=0):
                newIncDos = Incentivo.get_by_Importe(row.IncentivoDos)
                idInc2 = newIncDos.id
            else:
                idInc2 = 0           
            IncentivosArticulos.delete_art(row.CN,row.CodigoLab)
            consultaInsert = "INSERT INTO IncentivosArticulos (cn, idIncentivo, idLaboratorio, idIncentivoDos) VALUES ( '%s',%i, '%s',%i)  \
                              ON DUPLICATE KEY UPDATE cn= '%s' ,idIncentivo= %i , idLaboratorio='%s' , \
                              idIncentivoDos= %i" % (cn,idInc,codlab, idInc2 , cn, idInc,codlab, idInc2)          
                
            engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones')
            with engine.connect() as con:
                 con.execute(consultaInsert)
            


             

class AgrupacionCuotas(db.Model):
   
    __tablename__ = 'AgrupacionCuotas'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    idUnit = db.Column(db.String(10))
    idLab  = db.Column(db.String(25))
    cuota = db.Column(db.Numeric(4,2))
    cuotaDos = db.Column(db.Numeric(4,2))
    agrupBase = db.Column(db.String(255))
    agrupTotal = db.Column(db.String(255))
    

    def __repr__(self):
         return f'AgrupacionCuotas({self.idUnit}, {self.idLab},{self.cuota}, {self.cuotaDos}, {self.agrupBase},{self.agrupTotal})'
        #return '<CN: {}>'.format(self.cn)
    
    

    def __init__(self, idUnit, idLab, cuota, cuotaDos, agrupBase, agrupTotal):
        self.idUnit      = idUnit 
        self.idLab       = idLab
        self.cuota       = cuota   
        self.cuotaDos    = cuotaDos   
        self.agrupBase   = agrupBase
        self.agrupTotal  = agrupTotal
       
   
    #faltan otros
    # datos = [selectFar,selectLab,selectVert,cuota,selectIncCuota]
    
    def insertAll(cuota,cuotaDos, base, total):
        laboratorios = FiltroLaboratorio.get_all()  
        farmacias = FiltrosVerticales.get_all()   
        
        for lab in laboratorios:
            if (lab.Codigo!="todosLab"):
                for far in farmacias:
                    if (far.idUnit!="todasFar"):
                        newAsigCuotas = AgrupacionCuotas(far.idUnit, lab.Codigo, cuota,cuotaDos, base, total)
                        newAsigCuotas.save()
                    else: continue                   
            else: continue  

    def borrarTodo():
        try:
            agrCuotas = db.session.query(AgrupacionCuotas).delete()
            db.session.commit()
        except:
            db.session.rollback()
     

    def borrarFarVertical(idL):
        try:
            AgrupacionCuotas.query.filter_by(idLab=idL).delete()          
            db.session.commit()
        except:
            db.session.rollback()

    

    def borrarVertLab(idF):
        try:
            AgrupacionCuotas.query.filter_by(idUnit=idF).delete()          
            db.session.commit()
        except:
            db.session.rollback()

    
    
    def borrarVert(lab,far):
        try:
           AgrupacionCuotas.query.filter_by(idUnit=far, idLab=lab).delete()          
           db.session.commit()
        except:
            db.session.rollback()

    def borrarFar(lab) :
        try:
            AgrupacionCuotas.query.filter_by(idLab=lab).delete()          
            db.session.commit()
        except:
            db.session.rollback()

    def borrarLab(base,far):
        try:
            AgrupacionCuotas.query.filter_by(idUnit=far, agrupBase=base).delete()          
            db.session.commit()
        except:
            db.session.rollback()   

    def borrar(base,total, lab, far, cuot, cuDos) :
        print(base,total, lab, far, cuot, cuDos)
        try:
            AgrupacionCuotas.query.filter_by(agrupBase=base, agrupTotal=total, idLab=lab,idUnit=far, cuota=cuot, cuotaDos=cuDos).delete()          
            db.session.commit()
        except:
            db.session.rollback()

    def insertAllFar(cuota, cuotaDos,idLab, base, total):
        farmacias = FiltrosVerticales.get_all() 
        for far in farmacias:
            if (far.idUnit!="todasFar"):
                newAsigCuotas = AgrupacionCuotas(far.idUnit, idLab, cuota, cuotaDos, base, total)
                newAsigCuotas.save()
            else: continue 


    def insertAllFarLab(cuota, cuotaDos, base,total):
        laboratorios = FiltroLaboratorio.get_all()  
        farmacias    = FiltrosVerticales.get_all()    
        for lab in laboratorios:
            if (lab.Codigo!="todosLab"):
                for far in farmacias:
                    if (far.idUnit!="todasFar"):
                        newAsigCuotas = AgrupacionCuotas(far.idUnit, lab.Codigo, cuota, cuotaDos, base, total)
                        newAsigCuotas.save()
                    else: continue
            else: continue
                   
       

    
    def insertAllVertLab(cuota,far):
        laboratorios = FiltroLaboratorio.get_all()   
        verticales   = FarmaciasVerticales.get_verticales()  

        for lab in laboratorios:
            if (lab.Codigo!="todosLab"):
                for ver in verticales:
                    if (ver.Vertical!="todosVert"):
                        newAsigCuotas = AgrupacionCuotas(far, lab.Codigo, cuota, ver.Vertical)
                        newAsigCuotas.save() 
                    else: continue
            else: continue 

       
    
    def insertAllLab(cuota,cuotaDos,vert,far):        
        laboratorios = FiltroLaboratorio.get_all()     
        for lab in laboratorios:
            if (lab.Codigo!="todosLab"):
                newAsigCuotas = AgrupacionCuotas(far, lab.Codigo, cuota, cuotaDos, vert)
                newAsigCuotas.save()   
            else: continue
       
    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.flush()
            db.session.commit()
      

    def get_datos():
        consulta="SELECT DISTINCT AgrupacionCuotas.id, AgrupacionCuotas.idUnit, AgrupacionCuotas.idLab, \
                  FiltrosVerticales.Farmacia as farmacia, AgrupacionCuotas.agrupTotal as total, \
                  AgrupacionCuotas.agrupBase as base, AgrupacionCuotas.cuota, AgrupacionCuotas.cuotaDos, FiltroLaboratorio.Nombre FROM AgrupacionCuotas  \
                  LEFT JOIN FiltroLaboratorio on  AgrupacionCuotas.idLab = FiltroLaboratorio.Codigo LEFT JOIN  \
                  FiltrosVerticales on AgrupacionCuotas.idUnit = FiltrosVerticales.idUnit \
                  WHERE IFNULL(AgrupacionCuotas.id,0)<>0"
                           
        engine = create_engine('mysql+mysqldb://root:Ubach@2020!@127.0.0.1:3306/Operaciones',pool_size=20, max_overflow=0)
        results = []
        with engine.connect() as con:
            rs = con.execute(consulta)
            rows = rs.fetchall()          
        return rows


    def delete_asignacion(id):
        asig = AgrupacionCuotas.query.filter_by(id=id).first()
        db.session.delete(asig)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return AgrupacionCuotas.query.get(id)

    @staticmethod
    def get_all():
        return AgrupacionCuotas.query.all()

    def update_cuota(Id,cuota, cuotaDos):       
        value = AgrupacionCuotas.query.filter_by(id=Id).first()       
        value.cuota  = cuota 
        value.cuotaDos  = cuotaDos           
        db.session.flush()
        db.session.commit()  

    def update_asignacion(Id, selectFar,selectLab,cuota, cuotaDos, base, total):   
        value = AgrupacionCuotas.query.filter_by(id=Id).first()
        value.idUnit = selectFar
        value.idLab  = selectLab
        value.cuota  = cuota 
        value.cuotaDos  = cuotaDos        
        value.agrupBase    = base
        value.agrupTotal   = total         
        db.session.flush()
        db.session.commit()  

    def getByData(unidad, lab, bas, tot):
        asig = AgrupacionCuotas.query.filter_by(idUnit=unidad, idLab=lab,agrupBase=bas, agrupTotal=tot).first()
        return asig.id
    

    def existe(far, lab, bas, tot):
        exists  =  bool(AgrupacionCuotas.query.filter_by(idUnit=far, idLab=lab, agrupBase=bas, agrupTotal=tot).first())
        return exists

    def insertarDatosExcel(datos): 
         for row in datos.itertuples():          
            if (not AgrupacionCuotas.existe(row.unidad, row.laboratorio.upper(), row.base, row.total)):  
                acuot = AgrupacionCuotas(row.unidad, row.laboratorio.upper(), row.cuota, row.cuotaDos, row.base, row.total)
                acuot.save()
            else:
                Id = AgrupacionCuotas.getByData(row.unidad, row.laboratorio.upper(),row.base, row.total)
                AgrupacionCuotas.update_asignacion(Id, row.unidad, row.laboratorio.upper(), row.cuota, row.cuotaDos, row.base, row.total)

################################################################################################################################