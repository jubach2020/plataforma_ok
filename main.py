from flask import Flask, json, url_for, redirect, render_template, request, flash, jsonify
from flask.wrappers import Response
from flask_wtf import FlaskForm
import requests
from requests.api import head
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from passlib.hash import pbkdf2_sha256
from flask import Blueprint, send_from_directory
from app import db
from models import Departamento, Roles, Usuario, Agrupacion, AgrupacionArticulos, AgrupacionCuotas
from models import FarmaciasVerticales, ArtVertical, vademecum, FiltrosVerticales
from models import FiltrosArticulos, Filtros, FiltroLaboratorio, Incentivo, IncentivosArticulos
from flask_login import login_required
from gestorArchivos import GestionExcel
from io import StringIO 
from xml.etree.ElementTree import parse




main = Blueprint('main', __name__) 
app = Flask(__name__)
app.register_blueprint(main) 



@main.route('/administrador/departamentos', methods=['GET', 'POST'])
@login_required
def departamentos():
    if request.method == 'POST':
        nom          = request.form['dptoNom']
        descr        = request.form['dptoDesc']
        departamento = Departamento(nombre=nom,descripcion=descr)
        departamento.save()
        return redirect(url_for('main.departamentos'))
    departamentos = Departamento.get_all()
    return render_template('form_Administracion.html', 
                            titulo="Administración",
                            subtitulo="Departamentos",
                            formulario = "1",
                            departamentos=departamentos)


@main.route('/administrador/borrarDpto', methods=['GET', 'POST'])
@login_required
def borrarDpto():
    idDpto = request.form['id']
    Departamento.delete_dpto(idDpto)
    return 'OK'

@main.route('/administrador/editarDpto', methods=['GET', 'POST'])
@login_required
def editarDpto():
    idDpto   = request.form['id']
    nomDpto  = request.form['nomDpto']
    descDpto = request.form['descDpto']
    datos = [idDpto, nomDpto,descDpto]
    Departamento.update_dpto(datos)
    return redirect(url_for('main.departamentos'))


@main.route('/administrador/roles', methods=['GET', 'POST'])
@login_required
def roles():
    if request.method == 'POST':
        idRol  = request.form['id_role']
        nomRol    = request.form['nomRol']
        newRol = Roles(id_role=idRol, rol=nomRol)
        newRol.save()
        return redirect(url_for('main.roles'))
    roles = Roles.get_all()
    return render_template('form_Administracion.html',
                            titulo="Administración",
                            subtitulo="Roles",
                            formulario = "2",
                            roles=roles)

@main.route('/administrador/borrarRol', methods=['GET', 'POST'])
@login_required
def borrarRol():
    idRol = request.form['id']
    Roles.delete_rol(idRol)
    return 'OK'

@main.route('/administrador/editarRol', methods=['GET', 'POST'])
@login_required
def editarRol():
    idRol = request.form['idRol']
    nomRol = request.form['nomRol'] 
    datos = [idRol, nomRol]
    Roles.update_rol(datos)
    return redirect(url_for('main.roles'))

@main.route('/administrador/empleados', methods=['GET', 'POST'])
@login_required
def empleados():
    if request.method == 'POST':
        empNom     = request.form['empNom']
        nomUsuario = request.form['nomUsuario']
        empMail    = request.form['empMail']         
        idRol      = request.form['empRol']
        empPass    = pbkdf2_sha256.hash(request.form['empPass'])
        idDpto     = request.form['empDpto']
        newUser    = Usuario(nombreUsuario=nomUsuario,nombre=empNom, email=empMail,passw=empPass,idRol=idRol,idDepartamento=idDpto)
        newUser.save()
        return redirect(url_for('main.empleados'))
    usuarios = Usuario.get_all()
    dptos = Departamento.get_all()
    roles = Roles.get_all()
    return render_template('form_Administracion.html',
                            titulo="Administración",
                            subtitulo="Empleados",
                            formulario = "3",
                            usuarios=usuarios,
                            roles=roles,
                            departamentos=dptos)

@main.route('/administrador/editarEmpleado', methods=['GET', 'POST'])
@login_required
def editarEmpleado():
    idUser     = request.form['id']
    empNom     = request.form['empNom']
    nomUsuario = request.form['nomUsuario']
    empMail    = request.form['empMail'] 
    idRol      = request.form['idRol']
    idDpto     = request.form['idDpto'] 
    datos      = [idUser, nomUsuario , empNom, empMail, idRol, idDpto]
    Usuario.update_user(datos)   
    return redirect(url_for('main.empleados'))

    
    
@main.route('/administrador/borrarEmpleado', methods=['GET', 'POST'])
@login_required
def borrarEmpleado():
    id=request.form['id']
    Usuario.delete_user(id)
    return 'OK'
    

@main.route('/administrador/asignacion-roles-empleados', methods=['GET', 'POST'])
@login_required
def asignacionRoles():
    if request.method == 'POST':
        idRol  = request.form['selectRol']
        idUser = request.form['selectEmp']
        return redirect(url_for('main.asignacionRoles'))
    empleados  = Usuario.get_all()
    roles = Roles.get_all()
    return render_template('form_Administracion.html', 
                            titulo="Administración",
                            subtitulo="Asignación de Roles",
                            formulario = "4",
                            empleados=empleados,
                            roles=roles)

# ------------------------------------------------------------



# Funciones de Operaciones------------------------------------
@main.route('/operaciones/mantenimientos/agrupaciones', methods=['GET', 'POST'])
@login_required
def agrupaciones():
    if request.method == 'POST':
        agrupNom     = request.form['agrupNom']
        agrupCol     = request.form['colorAgrup']
        if (not Agrupacion.existe(agrupNom)):
            newAgrup     = Agrupacion(agrupNom, agrupCol)
            newAgrup.save()
            return redirect(url_for('main.agrupaciones'))
        else:
           flash("La agrupación ya existe")
    agrupas = Agrupacion.get_all()
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Mantenimiento",
                            subtitulo="Agrupaciones",
                            formulario = "1",
                            agrupaciones=agrupas)

@main.route('/operaciones/mantenimientos/borrarAgr', methods=['GET', 'POST'])
@login_required
def borrarAgr():
    id = request.form['id']
    Agrupacion.delete_agr(id)
    return 'OK'

@main.route('/operaciones/mantenimientos/editarAgrup', methods=['GET', 'POST'])
@login_required
def editarAgrup():
    id = request.form['id']
    nom = request.form['nom']
    col = request.form['color']
    datos = [id, nom, col]
    Agrupacion.update_agr(datos)
    return redirect(url_for('main.agrupaciones'))


@main.route('/operaciones/mantenimientos/agrupacion/get-articulos', methods=['GET', 'POST'])
@login_required
def get_articulos():       
    articulosAgrupados = AgrupacionArticulos.get_articulos_limit()
    return jsonify({ "resultado": articulosAgrupados })


#muestra de la tabla de agrupación de artículos
@main.route('/operaciones/mantenimientos/agrupacion/articulos', methods=['GET', 'POST'])
@login_required
def agrupArticulos():       
    agrupas = Agrupacion.get_all()
    articulosAgrupados  = AgrupacionArticulos.get_articulos()
    #articulosAgrupados = AgrupacionArticulos.get_agregados(idAgr=0)
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Agrupación",
                            subtitulo="Artículos",
                            formulario = "2",
                            artAgrup = articulosAgrupados,
                            agrupaciones=agrupas)

@main.route('/operaciones/mantenimientos/agrupacion/agrArtPost', methods=['GET', 'POST'])
@login_required
def agrArtPost():
    checkedArray = []
    labArray = []
    idAgr = request.form['idAgr']
    i = 0
    AgrupacionArticulos.delete_artAgr_by_idAgr(idAgr)
    checkedArray = (request.form['checkedArray']).split(",")
    labArray = (request.form['labArray']).split(",")
    for cn in checkedArray:
        newArt = AgrupacionArticulos(cn, idAgr, labArray[i])
        newArt.save()
        i=i+1
    flash("Artículos agrupados")
    return 'OK'

@main.route('/operaciones/mantenimientos/agrupacion/agregarAgrListado', methods=['GET', 'POST'])
@login_required
def agregarAgrListado():
    nuevaAgr = request.form['nuevaAgr']
    newAgrup = Agrupacion(nuevaAgr,"")
    newAgrup.save()
    return 'OK'
    
@main.route('/operaciones/mantenimientos/agrupacion/verAgrupacionesAgregadas', methods=['GET', 'POST'])
@login_required
def verAgrupacionesAgregadas():    
    agrId = request.form['idAgr']
    listaAgregados = AgrupacionArticulos.listaAgregados(agrId)
    return jsonify({ "resultado": listaAgregados })
   


@main.route('/operaciones/mantenimientos/filtros', methods=['GET', 'POST'])
@login_required
def filtros():
    if request.method == 'POST':
        filtroNom     = request.form['filtroNom']
        newFiltro     = Filtros(filtroNom)
        newFiltro.save()
        return redirect(url_for('main.filtros'))
    filtros = Filtros.get_all()
    return render_template('form_Operaciones_Filtros.html', 
                            titulo="Operaciones",
                            tipo = "Mantenimiento",
                            subtitulo="Filtros",
                            formulario = "6",
                            filtros=filtros)

@main.route('/operaciones/mantenimientos/filtros/borrarFiltro', methods=['GET', 'POST'])
@login_required
def borrarFiltro():
    id = request.form['id']
    Filtros.delete_filtro(id)
    return 'OK'

@main.route('/operaciones/mantenimientos/filtros/editarFiltro', methods=['GET', 'POST'])
@login_required
def editarFiltro():
    id = request.form['id']
    nom = request.form['nom'] 
    datos = [id, nom]
    Filtros.update_filtro(datos)
    return redirect(url_for('main.filtros'))

#muestra de la tabla de agrupación de artículos
@main.route('/operaciones/mantenimientos/filtros-articulos', methods=['GET', 'POST'])
@login_required
def filtrosArticulos():       
    filtrosAll = Filtros.get_all()
    filArticulos = AgrupacionArticulos.get_articulos()
    return render_template('form_Operaciones_Filtros.html', 
                            titulo="Operaciones",
                            tipo = "Filtros de",
                            subtitulo="Artículos",
                            formulario = "7",
                            filArticulos = filArticulos,
                            filtros=filtrosAll)

@main.route('/operaciones/mantenimientos/filtros-articulos/agrArtFiltro', methods=['GET', 'POST'])
@login_required
def agrArtFiltro():
    checkedArray = []
    labArray = []
    idFil = request.form['idFil']
    i = 0
    FiltrosArticulos.delete_artFil_by_idFil(idFil)
    checkedArray = (request.form['checkedArray']).split(",")
    labArray = (request.form['labArray']).split(",")
    for cn in checkedArray:
        newArt = FiltrosArticulos(cn, idFil, labArray[i])
        newArt.save()
        i=i+1  
    if (i>1):
        flash('Se han agregado los artículos con el filtro seleccionado') 
    else:
        flash('Se agregó el artículos con el filtro seleccionado')
    return 'OK'

@main.route('/operaciones/mantenimientos/filtros-articulos/agregarFilListado', methods=['GET', 'POST'])
@login_required
def agregarFilListado():
    nuevoFil = request.form['nuevoFil']
    newFil = Filtros(nuevoFil)
    newFil.save()
    return 'OK'
    
@main.route('/operaciones/mantenimientos/filtros-articulos/verFiltrosAgregados', methods=['GET', 'POST'])
@login_required
def verFiltrosAgregados():    
    idFil = request.form['idFil']
    listaAgregados = FiltrosArticulos.listaAgregados(idFil)
    return jsonify({ "resultado": listaAgregados })
  
   
@main.route('/operaciones/mantenimientos/farmacias-verticales', methods=['GET', 'POST'])
@login_required
def farmaciasVerticales():
    verticales = FarmaciasVerticales.get_verticales()
    farmacias = FarmaciasVerticales.get_all()    
    return render_template('form_Operaciones_farmacias.html', 
                            titulo="Operaciones",
                            tipo = "Listado de Farmacias",
                            subtitulo=" Verticales",
                            formulario = "3",
                            verticales = verticales,
                            farmacias=farmacias)
    
@main.route('/operaciones/mantenimientos/farmacias-verticales/filtrarPorVertical', methods=['GET', 'POST'])
@login_required
def filtrarPorVertical():
    filtro = request.form['filtroVertical']
    tablaFiltrada = FarmaciasVerticales.get_farmacia_by_vertical(filtro)
    return tablaFiltrada


@main.route('/operaciones/mantenimientos/farmacias-verticales/agregarVertical', methods=['GET', 'POST'])
@login_required
def agregarVertical():
    
    nif  = request.form['nif']
    descripcion = request.form['desc']
    Activo = request.form['activo']
    Vertical = request.form['vert']
    Proveedor = request.form['prov']
    Nombre = request.form['nom']
    Mayorista = request.form['may']  
    nuevaFarmacia = FarmaciasVerticales(nif,descripcion,Activo,Vertical,Proveedor,Nombre,Mayorista)
    nuevaFarmacia.save()
    return redirect(url_for('main.farmaciasVerticales'))

@main.route('/operaciones/mantenimientos/farmacias-verticales/editarFarmacia', methods=['GET', 'POST'])
@login_required
def editarFarmacia():
    id   = request.form['id']
    nif  = request.form['nif']
    descripcion = request.form['desc']
    Activo = request.form['activo']
    Vertical = request.form['vert']
    Proveedor = request.form['prov']
    Nombre = request.form['nom']
    Mayorista = request.form['may']

    datos = [id, nif,descripcion,Activo,Vertical,Proveedor,Nombre,Mayorista]
    FarmaciasVerticales.update_far(datos)
    return 'OK'


@main.route('/operaciones/mantenimientos/farmacias-verticales/borrarFar', methods=['GET', 'POST'])
@login_required
def borrarFar():
    id = request.form['id']
    FarmaciasVerticales.borrarFar(id)
    return 'OK'

@main.route('/operaciones/mantenimientos/articulos-verticales', methods=['GET', 'POST'])
@login_required
def articulosVerticales():
    verticales = FarmaciasVerticales.get_verticales()
    artVertical = ArtVertical.get_all()
    vademe = vademecum.get_articulos()
     
    return render_template('form_Operaciones_Articulos.html', 
                            titulo="Operaciones",
                            tipo = "Listado de Articulos",
                            subtitulo=" Verticales",
                            formulario = "4",
                            vademe = vademe,
                            verticales = verticales,
                            artVertical= artVertical)


    
@main.route('/operaciones/mantenimientos/articulos-verticales/agregarArtVertical', methods=['GET', 'POST'])
@login_required
def agregarArtVertical():    
    CN6      = request.form['cn']
    EAN      = request.form['ean']
    PRODUCTE = request.form['prod']    
    STCK_MIN = request.form['min']
    STCK_MAX = request.form['max']
    MULTIPLO = request.form['mul']
    ACTIVO   = request.form['act']
    Sin_AH   = request.form['ah']
    Sin_FEDE = request.form['fede']
    IVA      = request.form['iva']
    codVertical = request.form['vert']
     
    nuevoArtVertical = ArtVertical(CN6, EAN, PRODUCTE, STCK_MIN, STCK_MAX ,MULTIPLO, ACTIVO,Sin_AH,Sin_FEDE,IVA,codVertical)
    nuevoArtVertical.save()
    return 'OK'
    #redirect(url_for('main.articulosVerticales'))


@main.route('/operaciones/mantenimientos/articulos-verticales/verificarCN', methods=['GET', 'POST'])
@login_required
def verificarCN():
   cn = request.form['cn']
   if ArtVertical.existeArt(cn):
    return 'OK'
   else:
    return 'KO'

@main.route('/operaciones/mantenimientos/articulos-verticales/borrarArtVer', methods=['GET', 'POST'])
@login_required
def borrarArtVer():
    id = request.form['id']
    ArtVertical.borrarArt(id)
    return 'OK'


@main.route('/operaciones/mantenimientos/articulos-verticales/editarArtVert', methods=['GET', 'POST'])
@login_required
def editarArtVert():
    id       = request.form['idEditar']
    CN6      = request.form['Artcn6'+id]
    EAN      = request.form['Artean'+id]
    PRODUCTE = request.form['Artprod'+id]    
    STCK_MIN = request.form['Artmin'+id]
    STCK_MAX = request.form['Artmax'+id]
    MULTIPLO = request.form['Artmult'+id]
    ACTIVO   = request.form['Artact'+id]
    Sin_AH   = request.form['Artah'+id]
    Sin_FEDE = request.form['Artfede'+id]
    IVA      = request.form['Artiva'+id]
    codVertical = request.form['Artvert'+id]

    datos = [id,CN6, EAN, PRODUCTE, STCK_MIN, STCK_MAX ,MULTIPLO, ACTIVO,Sin_AH,Sin_FEDE,IVA,codVertical]
    ArtVertical.update_art(datos)
    return redirect(url_for('main.articulosVerticales'))

@main.route('/operaciones/mantenimientos/filtros-verticales', methods=['GET', 'POST'])
@login_required
def filtrosVerticales():
    filtrosVert = FiltrosVerticales.get_filtros_farmacias()
    verticalesAgregadas = FiltrosVerticales.agregadas()    
    return render_template('form_Operaciones_Verticales.html', 
                            titulo="Operaciones",
                            tipo = "Mantenimiento",
                            subtitulo="Filtros Verticales",
                            formulario = "5",
                            filtrosVert = filtrosVert,
                            verticalesAgregadas = verticalesAgregadas)

@main.route('/operaciones/mantenimientos/filtros-verticales/borrarFarVertical', methods=['GET', 'POST'])
@login_required
def borrarFarVertical():
    nif = request.form['id']
    FiltrosVerticales.borrarFar(nif)
    return 'OK'


@main.route('/operaciones/mantenimientos/filtros-verticales/agregar-farmacias', methods=['GET', 'POST'])
@login_required
def agregarFarmacias():
    checkedArray = []
    nifArray     = []
    unitArray    = []
    descArray    = []
    unidad       = "" 
    i = 0    
    
    checkedArray = (request.form['checkedArray']).split(",")
    nifArray = (request.form['nifArray']).split(",")
    unitArray = (request.form['unitArray']).split(",")
    descArray = (request.form['descArray']).split(",")
    print(unitArray)
    for fil in checkedArray:
        
        existe = FiltrosVerticales.existe(unitArray[i]) 
        print(existe)
       
        unidad = unitArray[i]
        if not existe:    
            newFar = FiltrosVerticales(nifArray[i], unitArray[i], descArray[i])          
            if not newFar.save():
                flash('No se ha agregado la farmacia %s' %unidad)
            else:
                flash('Se ha agregado la farmacia %s' %unidad)  
        else:
            flash('Ya existe la farmacia: %s' %unidad )
        i=i+1
    return 'OK'

@main.route('/download-files', methods=['GET'])
def downloadAgrupacionesExcel():
    file_name = 'agrupacionesExcel.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/download-files-cuotas', methods=['GET'])
def downloadIncentivosExcel():
    file_name = 'objetivosIncentivosExcel.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/download-files-agrupacion-articulos', methods=['GET'])
def downloadAgrupacionArtsExcel():
    file_name = 'agrupacionArtsExcel.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/download-files-filtros-vert', methods=['GET'])
def downloadFiltrosVertExcel():
    file_name = 'agrupacionFiltrosVert.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/download-arts-incentivos', methods=['GET'])
def downloadArtsIncentivosExcel():
    file_name = 'incentivosArtsExcel.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/download-files-filtros-art', methods=['GET'])
def downloadFiltrosArtExcel():
    file_name = 'agrupacionFiltrosArt.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/download-farm-verticales', methods=['GET'])
def downloadFarmaciasVertExcel():
    file_name = 'farmaciasVerticalesExcel.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)


@main.route('/download-art-verticales', methods=['GET'])
def downloadArtVertExcel():
    file_name = 'artVerticalesExcel.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/download-listado-lab', methods=['GET'])
def downloadListadoLabs():
    file_name = 'codigosLab.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/download-listado-verticales', methods=['GET'])
def downloadVerticales():
    file_name = 'verticales.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/download-listado-farmacias', methods=['GET'])
def downloadListadoFarm():
    file_name = 'listadoFarmacias.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/download-laboratorios-vert', methods=['GET'])
def downloadListadoLabsVert():
    file_name = 'laboratoriosVertExcel.xlsx'
    directory ='./static/assets/downloads'
    return GestionExcel.downloadExcel(file_name,directory)

@main.route('/uploadLaboratoriosVert', methods=['GET','POST'])
def uploadLaboratoriosVert():
    file = request.files.get('cargarLabsVert') 
    directory ='static\\assets\\uploads'  
    print(file)
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    if  GestionExcel.allowed_file(file.filename):
        GestionExcel.uploadExcel(directory,file,file.filename) 
        data = GestionExcel.excel_to_csv(directory,file.filename)
        FiltroLaboratorio.insertarDatosExcel(data)               
        flash('Se han cargado correctamente los datos')
    else:
        flash('Solo se permiten archivos con extensión xls o xlsx')
    return redirect(request.url)

@main.route('/uploadArtVert', methods=['POST'])
def uploadArtVert():
    file = request.files.get('cargarArtVert') 
    directory ='static\\assets\\uploads'  
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    if  GestionExcel.allowed_file(file.filename):
        GestionExcel.uploadExcel(directory,file,file.filename) 
        data = GestionExcel.excel_to_csv(directory,file.filename)
        ArtVertical.insertarDatosExcel(data)               
        flash('Se han cargado correctamente los datos')
    else:
        flash('Solo se permiten archivos con extensión xls o xlsx')
    return redirect(request.url)


@main.route('/uploadFarmaciasVert', methods=['POST'])
def uploadFarmaciasVert():
    file = request.files.get('cargarFarmaciasVert') 
    directory ='static\\assets\\uploads'  
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    if  GestionExcel.allowed_file(file.filename):
        GestionExcel.uploadExcel(directory,file,file.filename) 
        data = GestionExcel.excel_to_csv(directory,file.filename)
        FiltrosVerticales.insertarDatosExcel(data)               
        flash('Se han cargado correctamente los datos')
    else:
        flash('Solo se permiten archivos con extensión xls o xlsx')
    return redirect(url_for('main.farmaciasVerticales'))


@main.route('/uploadIncentivosArtsExcel', methods=['POST'])
def uploadIncentivosArtsExcel():
    file = request.files.get('cargarIncentivosArt') 
    directory ='static\\assets\\uploads'
  
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    if  GestionExcel.allowed_file(file.filename):
        GestionExcel.uploadExcel(directory,file,file.filename) 
        data = GestionExcel.excel_to_csv(directory,file.filename)
        IncentivosArticulos.insertarDatosExcel(data)               
        flash('Se han cargado correctamente los datos')
    else:
        flash('Solo se permiten archivos con extensión xls o xlsx')
    return redirect(url_for('main.artsIncentivos'))


@main.route('/uploadAgrupaciones', methods=['POST'])
def uploadAgrupacionesExcel():
    file = request.files.get('cargarAgrupaciones') 
    directory ='static\\assets\\uploads'  
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    if  GestionExcel.allowed_file(file.filename):
        GestionExcel.uploadExcel(directory,file,file.filename) 
        data = GestionExcel.excel_to_csv(directory,file.filename)
        Agrupacion.insertarDatosExcel(data)               
        flash('Se han cargado correctamente los datos')
    else:
        flash('Solo se permiten archivos con extensión xls o xlsx')
    return redirect(url_for('main.agrupaciones'))


@main.route('/uploadCuotas', methods=['POST'])
def uploadCuotasExcel():
    file = request.files.get('cargarCuotas') 
    directory ='static\\assets\\uploads'  
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    if  GestionExcel.allowed_file(file.filename):
        GestionExcel.uploadExcel(directory,file,file.filename) 
        data = GestionExcel.excel_to_csv(directory,file.filename)
        AgrupacionCuotas.insertarDatosExcel(data)               
        flash('Se han cargado correctamente los datos')
    else:
        flash('Solo se permiten archivos con extensión xls o xlsx')
    return redirect(url_for('main.asignacionCuotas'))

@main.route('/uploadAgrupacionArt', methods=['GET','POST'])
def uploadAgrupacionArt():
    file = request.files.get('cargarAgrupacionArt') 
    directory ='static\\assets\\uploads'  
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    if  GestionExcel.allowed_file(file.filename):
        GestionExcel.uploadExcel(directory,file,file.filename) 
        data = GestionExcel.excel_to_csv(directory,file.filename)
        AgrupacionArticulos.insertarDatosExcel(data)                 
        flash('Se han cargado correctamente los datos')
    else:
        flash('Solo se permiten archivos con extensión xls o xlsx')
    return (redirect(url_for('main.agrupArticulos')))
           
    
@main.route('/uploadFiltrosVert', methods=['POST'])
def uploadFiltrosVert():
    file = request.files.get('cargarFiltrosVert') 
    directory ='static\\assets\\uploads'  
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    if  GestionExcel.allowed_file(file.filename):
        GestionExcel.uploadExcel(directory,file,file.filename) 
        data = GestionExcel.excel_to_csv(directory,file.filename)
        FiltrosVerticales.insertarDatosExcel(data)               
        flash('Se han cargado correctamente los datos')
    else:
        flash('Solo se permiten archivos con extensión xls o xlsx')
    return redirect(request.url)

@main.route('/uploadFiltrosArt', methods=['POST'])
def uploadFiltrosArt():
    file = request.files.get('cargarFiltrosArt') 
    directory ='static\\assets\\uploads'  
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    if  GestionExcel.allowed_file(file.filename):
        GestionExcel.uploadExcel(directory,file,file.filename) 
        data = GestionExcel.excel_to_csv(directory,file.filename)
        FiltrosArticulos.insertarDatosExcel(data)               
        flash('Se han cargado correctamente los datos')
    else:
        flash('Solo se permiten archivos con extensión xls o xlsx')
    return redirect(url_for('main.filtrosArticulos'))


@main.route('/uploadLabVert', methods=['POST'])
def uploadLabVert():
    file = request.files.get('cargarLabVert') 
    directory ='static\\assets\\uploads'  
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo')
        return redirect(request.url)
    if  GestionExcel.allowed_file(file.filename):
        GestionExcel.uploadExcel(directory,file,file.filename) 
        data = GestionExcel.excel_to_csv(directory,file.filename)
        FiltroLaboratorio.insertarDatosExcel(data)               
        flash('Se han cargado correctamente los datos')
    else:
        flash('Solo se permiten archivos con extensión xls o xlsx')
    return redirect(url_for('main.laboratoriosVerticales'))


       
        
@main.route('/operaciones/mantenimientos/laboratorios-verticales', methods=['GET', 'POST'])
@login_required
def laboratoriosVerticales():
    verticales = FarmaciasVerticales.get_verticales()
    print(verticales)
    labVertical = FiltroLaboratorio.get_all()
    #scriptTablaLab()
    #col =  ['Codigo','Tipo','Nombre','Dir','Ciudad','Prov','CP','Tel']
    #labs = GestionCsv.read_csv('static\\assets\\uploads\\labs.csv', col )
    labs = FiltroLaboratorio.get_laboratorios()
    
    return render_template('form_Operaciones_Laboratorios.html', 
                            titulo="Operaciones",
                            tipo = "Listado de Laboratorios",
                            subtitulo=" Verticales",
                            formulario = "10",
                            labs = labs,
                            verticales = verticales,
                            labVertical= labVertical)
    
    
'''
@main.route('/operaciones/mantenimientos/laboratorios-verticales')
def scriptTablaLab():
    labs = FiltroLaboratorio.get_laboratorios() 
    colCodigo = []
    colTipo   = []
    colNombre = []
    colDir    = []
    colCiudad = []
    colProv   = []
    colCP     = []
    colTel    = []
    for x in range(0, len(labs)):
        i=0
        colCodigo.append(labs[x][i])
        i=i+1     
        colTipo.append(labs[x][i])      
        i=i+1
        colNombre.append(labs[x][i])   
        i=i+1
        colDir.append(labs[x][i]) 
        i=i+1
        colCiudad.append(labs[x][i])   
        i=i+1
        colProv.append(labs[x][i])
        i=i+1
        colCP.append(labs[x][i])
        i=i+1
        colTel.append(labs[x][i])
    data = {
        'Codigo': colCodigo,
        'Tipo'  :  colTipo,
        'Nombre': colNombre,
        'Dir'   : colDir,
        'Ciudad': colCiudad,
        'Prov'  : colProv,
        'CP'    : colCP,
        'Tel'   : colTel }
    columnas = ['Codigo','Tipo','Nombre','Dir','Ciudad','Prov','CP','Tel']
    GestionCsv.write_csv(data, columnas, 'static\\assets\\uploads\\labs.csv')    
'''

@main.route('/operaciones/mantenimientos/laboratorios-verticales/agregarLabVertical', methods=['GET', 'POST'])
@login_required
def agregarLabVertical():    
    Codigo      = request.form['codigo']
    Nombre      = request.form['nom']
    Vertical    = request.form['vert']    
    Color       = request.form['color']    
   
    nuevoLabVertical = FiltroLaboratorio(Codigo, Nombre, Vertical, Color)
    nuevoLabVertical.save()
    return 'OK'

@main.route('/operaciones/mantenimientos/laboratorios-verticales/editarLab', methods=['GET', 'POST'])
@login_required
def editarLab():
    Id          = request.form['idEditar']
    Codigo      = request.form['labCodigo'+Id]
    Nombre      = request.form['labNombre'+Id]
    Vertical    = request.form['labVertical'+Id]    
    Color       = request.form['labColor'+Id]    
    datos = [Id,Codigo, Nombre, Vertical, Color]
    if (not FiltroLaboratorio.existeLab(Codigo, Vertical)):
        FiltroLaboratorio.update_lab(datos)
    else: 
        flash('El laboratorio ya existe')
    return redirect(url_for('main.laboratoriosVerticales'))

@main.route('/operaciones/mantenimientos/laboratorios-verticales/borrarLab', methods=['GET', 'POST']) 
@login_required
def borrarLab():
    id = request.form['id']
    FiltroLaboratorio.borrarLab(id)
    return 'OK'


@main.route('/operaciones/mantenimientos/laboratorios-verticales/verificarCodigo', methods=['GET', 'POST'])
@login_required
def verificarCodigo():
    codigo      = request.form['codigo']
    vertical    = request.form['vert']
    existe = FiltroLaboratorio.existeLab(codigo, vertical)
    if existe:
        return 'KO'
    else:
        return 'OK'


@main.route('/operaciones/trabajos/asignacion-fcias-art')
@login_required
def asignacionFarmaciasArt():
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Trabajos - ",
                            subtitulo="Asignación de Artículos a Farmacias")

@main.route('/operaciones/trabajos/asignacion-cuotas', methods=['GET', 'POST'])
@login_required
def asignacionCuotas():
    if request.method == 'POST':
        selectLab      = request.form['selectLab']
        selectFar      = request.form['selectFar']       
        cuota          = request.form['cuota']
        base           = request.form['base']
        total          = request.form['total']
        cuotaDos       = request.form['cuotaDos']
    
        
        if (selectFar=='todasFar' and selectLab=='todosLab'):
            AgrupacionCuotas.insertAll(cuota, cuotaDos ,base, total)
        elif (selectFar=='todasFar' and selectLab!='todosLab'):
            AgrupacionCuotas.insertAllFar(cuota, cuotaDos, selectLab, base, total)        
        elif (selectFar!='todasFar' and selectLab=='todosLab'):
            AgrupacionCuotas.insertAllLab(cuota,cuotaDos,selectFar)       
        elif (selectFar!='todasFar'  and selectLab!='todosLab'):
            if (not AgrupacionCuotas.existe(selectFar, selectLab, base, total)):    
                newAsigCuotas = AgrupacionCuotas(selectFar, selectLab, cuota, cuotaDos, base, total)
                newAsigCuotas.save() 
                return 'OK'     
            else:   
                flash("Ya existe una cuota asignada")
                return 'KO'   
        else:
            Id = AgrupacionCuotas.getByData(selectFar, selectLab)
            AgrupacionCuotas.update_asignacion(Id, selectFar, selectLab, cuota, cuotaDos, base, total)   
            return redirect(url_for('main.asignacionCuotas'))
    farmacias = FiltrosVerticales.get_all()    
    laboratorios = FiltroLaboratorio.get_all()    
    asignaciones = AgrupacionCuotas.get_datos()
   
    return render_template('form_Operaciones_Cuotas.html', 
                            titulo="Operaciones",
                            tipo = "Trabajos - ",
                            subtitulo="Asignación de Cuotas", 
                            formulario = "14",
                            laboratorios=laboratorios,
                            farmacias=farmacias,                           
                            asignaciones=asignaciones)



@main.route('/operaciones/trabajos/asignacion-cuotas/borrar-cuota', methods=['GET', 'POST'])
@login_required
def borrarCuota():
    if request.method == 'POST':
        selectLab      = request.form['selectLab']
        selectFar      = request.form['selectFar']   
        base           = request.form['base']
        total          = request.form['total']      
        cuotaDos       = request.form['cuotaDos']
        cuota          = request.form['cuota']
    
        if (selectFar=='todasFar'  and selectLab=='todosLab'):
            AgrupacionCuotas.borrarTodo()
        elif (selectFar!='todasFar' and selectLab=='todosLab'):
            AgrupacionCuotas.borrarLab(selectFar)       
        elif (selectFar=='todasFar' and selectLab!='todosLab'):
            AgrupacionCuotas.borrarFar(selectLab) 
        else: 
            AgrupacionCuotas.borrar(base, total, selectLab, selectFar, cuota, cuotaDos)
    return 'OK'      

@main.route('/operaciones/trabajos/asignacion-cuotas/editar', methods=['GET', 'POST'])
@login_required
def editarAsignacionCuotas():
    Id          = request.form['idEditar']
    idLab       = request.form['labHidden'+Id]
    idUnit      = request.form['farHidden'+Id]
    cuota       = request.form['cuota'+Id]
    cuotaDos    = request.form['cuotaDos'+Id]
    base        = request.form['base'+Id]
    total       = request.form['total'+Id] 

    AgrupacionCuotas.update_asignacion(Id, idUnit,idLab,cuota,cuotaDos, base,total)
    return redirect(url_for('main.asignacionCuotas'))

@main.route('/operaciones/trabajos/asignacion-cuotas/borrarAsig', methods=['GET', 'POST'])
@login_required
def borrarAsig():
    id = request.form['id']
    AgrupacionCuotas.delete_asignacion(id)
    return 'OK'

@main.route('/operaciones/trabajos/articulos-incentivos', methods=['GET', 'POST'])
@login_required
def artsIncentivos():
    articulos = IncentivosArticulos.get_articulos()
    incen = Incentivo.get_all()
    return render_template('form_Operaciones_Incentivos.html', 
                            titulo="Operaciones",
                            tipo = "Asignación",
                            subtitulo="Incentivos a Artículos",
                            formulario = "13",
                            incentivos=incen,
                            articulos = articulos
                            )


@main.route('/operaciones/trabajos/agregarIncListado', methods=['GET', 'POST'])
@login_required
def agregarIncListado():
    nuevoInc = request.form['nuevoInc']
    newInc = Incentivo(nuevoInc)
    newInc.save()
    return 'OK'
    

@main.route('/operaciones/trabajos/agrIncPost', methods=['GET', 'POST'])
@login_required
def agrIncPost():
    checkedArray = []
    labArray = []
    idInc = request.form['idInc']
    idInc2 = request.form['idInc2']
    if (idInc==0 or idInc=='nuevo'):
       flash('Debe seleccionar el Incentivo 1') 
    else:
        i = 0  
        checkedArray = (request.form['checkedArray']).split(",")
        labArray = (request.form['labArray']).split(",")
        for cn in checkedArray:
            IncentivosArticulos.delete_art(cn,labArray[i])
            newArt = IncentivosArticulos(cn, idInc, labArray[i], idInc2)
            newArt.save()
            i=i+1
   
    return 'OK'


@main.route('/operaciones/trabajos/verIncentivosAsignados', methods=['GET', 'POST'])
@login_required
def verIncentivosAsignados():    
    incId = request.form['idInc']
    listaAsignados = IncentivosArticulos.listaAsignados(incId)
    if len(listaAsignados)>0:
        return jsonify({ "resultado": listaAsignados , "largo": len(listaAsignados) })
    return 'KO'


@main.route('/operaciones/trabajos/ejecuciones/min-max', methods=['GET', 'POST'])
@login_required
def ejecucionesMinMax():
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Trabajos - Ejecuciones",
                            subtitulo="Mínimos / Máximos")

@main.route('/operaciones/trabajos/ejecuciones/sinonimos', methods=['GET', 'POST'])
@login_required
def sinonimos():
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Trabajos - Ejecuciones",
                            subtitulo="Sinónimos")

@main.route('/operaciones/trabajos/ejecuciones/progFarmatic', methods=['GET', 'POST'])
@login_required
def programacionFarmatic():
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Trabajos - Ejecuciones",
                            subtitulo="Programación Farmatic")

@main.route('/operaciones/trabajos/ejecuciones/mensajes', methods=['GET', 'POST'])
@login_required
def envioMensajes():
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Trabajos - Ejecuciones",
                            subtitulo="Envío de Mensajes")

@main.route('/operaciones/analisis/necesidadesFcias', methods=['GET', 'POST'])
@login_required
def necesidadesFcias():
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Análisis",
			                formulario = "10",
                            subtitulo="Necesidades de Farmacias")

@main.route('/operaciones/analisis/necesidadesFciasFiltro', methods=['GET', 'POST'])
@login_required
def necesidadesFiltros():
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Análisis",
			                formulario = "11",
                            subtitulo="Necesidades de Filtros")

@main.route('/operaciones/analisis/articulos-vericales', methods=['GET', 'POST'])
@login_required
def articulosVerticalesAnalisis():
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Análisis",
                            formulario = "3",
                            subtitulo="Artículos Verticales")

@main.route('/operaciones/analisis/laboratorios-verticales', methods=['GET', 'POST'])
@login_required
def laboratoriosVerticalesAnalisis():
    return render_template('form_Operaciones.html', 
                            titulo="Operaciones",
                            tipo = "Análisis",
                            subtitulo="Laboratorios Verticales")


@main.route('/operaciones/analisis/calculo-cuota', methods=['GET', 'POST'])
@login_required
def cuotaIncentivosAnalisis():  
    cuotaIgualOinfA  = request.form['porcentCuota']         
    response = callApiCuotas()
    with open('./static/assets/downloads/datosJson.txt', 'w') as f:  
        f.writelines(response)
        f.close
   
    with open('./static/assets/downloads/datosJson.txt', 'r') as f:  
        docu = f.read()    
        json_parsed = json.loads(docu)      
   
    ths = json_parsed['response']['result']
    encabezados = ths['column_order']
    datosok = ths['rows']
        
    largoTr = len(encabezados)-4
    largoTd = len(datosok)
   
    encabezadosArray = []
    for item in encabezados: 
        encabezadosArray.append(item.split('::'))    
    head= []
    for i in range(len(encabezadosArray)):
        if (i>3):
            head.append(encabezadosArray[i][1])
    
    headList = []
    for item in head:
        if item not in headList:
            headList.append(item)
    
    largoTh = len(headList)
    listaThControl = []
    indiceCuotaActual = 7   
    for j in range(len(encabezadosArray)+11):
        if ((j==indiceCuotaActual)):
            listaThControl.append(j)
            indiceCuotaActual = indiceCuotaActual + 6        
            
    for k in range(6,largoTr+2,5):
        encabezadosArray[k].insert(3,"Control cuota")
    
    largoListaControl = len(listaThControl)
    largoTotal = largoTr+largoListaControl+4    

    for y in range(largoTd):
        for d in range(7,largoTotal,6):
            if (datosok[y][d-1]=='' or datosok[y][d]==''):
                datosok[y].insert(d,"")
            else:                 
                datosok[y][d-1] = float(datosok[y][d-1].replace('%',''))
                datosok[y][d] = float(datosok[y][d].replace('%',''))
                cuota = datosok[y][d]
                actual = datosok[y][d-1]
                variacion = float(cuotaIgualOinfA)
                porcentaje = (variacion * cuota)/100
                cuotaCalculada = cuota - porcentaje
              
                if (actual<cuotaCalculada):
                    datosok[y].insert(d,"rojo")
                else:
                    if(actual>cuota):
                        datosok[y].insert(d,"verde") 
                    else:  
                        if(actual>cuotaCalculada and  actual<cuota):
                            datosok[y].insert(d,"ambar")   
                        else:
                             datosok[y].insert(d,"")
  
    verticales = FiltroLaboratorio.get_verticals()    
   
    return render_template('form_Seguimientos_Cuotas.html', 
                        titulo="Operaciones",
                        tipo = "Análisis",
                        subtitulo="Seguimiento Incentivos",
                        formulario = "12",
                        verticales=verticales,
                        datos=datosok,
                        headList=headList,
                        encabezadosArray=encabezadosArray,
                        largoTr=largoTr,
                        largoTd=largoTd,
                        largoTh=largoTh,
                        listaThControl=listaThControl,
                        largoListaControl=largoListaControl,
                        largoTotal=largoTotal)

def callApiCuotas():
    params = (
                    ('ZOHO_ACTION', 'EXPORT'),
                    ('ZOHO_ERROR_FORMAT', 'XML'),
                    ('ZOHO_API_VERSION', '1.0'),
                    ('authtoken', '4934c5a7fd9adff068f95234d3f107fa'),
                    ('ZOHO_OUTPUT_FORMAT', 'JSON'),
                  
                )
    
    cookies = {
            'CSRF_TOKEN': 'b4fb4b12-b8e6-4ef5-a1f6-530c34090541',
            'ZROPJSESSIONID': '51285CA78BB31CE572DA6EC5252C2F79',
            '_zcsr_tmp': 'b4fb4b12-b8e6-4ef5-a1f6-530c34090541',
            }
    headers = {
    } 
   
    response = requests.get('https://95.217.88.30:8443/api/info@ecoceutics.info/Init_DW/rpt_Cuotas_Incentius_Global', headers=headers, params=params, cookies=cookies, verify=False)
    return response.text

@main.route('/operaciones/analisis/seguimiento-incentivos', methods=['GET', 'POST'])
@login_required
def segIncentivosAnalisis():     
    cuotaIgualOinfA  = 2 
    response = callApiCuotas()

    with open('./static/assets/downloads/datosJson.txt', 'w') as f:  
        f.writelines(response)
        f.close
   
    with open('./static/assets/downloads/datosJson.txt', 'r') as f:  
        docu = f.read()    
        json_parsed = json.loads(docu)      
   
    ths = json_parsed['response']['result']
    encabezados = ths['column_order']
    datosok = ths['rows']
        
    largoTr = len(encabezados)-4
    largoTd = len(datosok)
   
    encabezadosArray = []
    for item in encabezados: 
        encabezadosArray.append(item.split('::'))    
    head= []
    for i in range(len(encabezadosArray)):
        if (i>3):
            head.append(encabezadosArray[i][1])
    
    headList = []
    for item in head:
        if item not in headList:
            headList.append(item)
    
    largoTh = len(headList)
    listaThControl = []
    indiceCuotaActual = 7   
    for j in range(len(encabezadosArray)+11):
        if ((j==indiceCuotaActual)):
            listaThControl.append(j)
            indiceCuotaActual = indiceCuotaActual + 6        
            
    for k in range(6,largoTr+2,5):
        encabezadosArray[k].insert(3,"Control cuota")
    
    largoListaControl = len(listaThControl)
    largoTotal = largoTr+largoListaControl+4    

    for y in range(largoTd):
        for d in range(7,largoTotal,6):
            if (datosok[y][d-1]=='' or datosok[y][d]==''):
                datosok[y].insert(d,"")
            else:                 
                datosok[y][d-1] = float(datosok[y][d-1].replace('%',''))
                datosok[y][d] = float(datosok[y][d].replace('%',''))
                cuota = datosok[y][d]
                actual = datosok[y][d-1]
                variacion = float(cuotaIgualOinfA)
                porcentaje = (variacion * cuota)/100
                cuotaCalculada = cuota - porcentaje
              
                if (actual<cuotaCalculada):
                    datosok[y].insert(d,"rojo")
                else:
                    if(actual>cuota):
                        datosok[y].insert(d,"verde") 
                    else:  
                        if(actual>cuotaCalculada and  actual<cuota):
                            datosok[y].insert(d,"ambar")   
                        else:
                             datosok[y].insert(d,"")
    print(datosok)
    verticales = FiltroLaboratorio.get_verticals()    
   
    return render_template('form_Seguimientos_Cuotas.html', 
                        titulo="Operaciones",
                        tipo = "Análisis",
                        subtitulo="Seguimiento Incentivos",
                        formulario = "12",
                        verticales=verticales,
                        datos=datosok,
                        headList=headList,
                        encabezadosArray=encabezadosArray,
                        largoTr=largoTr,
                        largoTd=largoTd,
                        largoTh=largoTh,
                        listaThControl=listaThControl,
                        largoListaControl=largoListaControl,
                        largoTotal=largoTotal)


@main.route('/operaciones/analisis/articulos-incentivos', methods=['GET', 'POST'])
@login_required
def agrupIncentivos():
    agrupas = Agrupacion.get_all()
    incen = Incentivo.get_all()
    return render_template('form_Operaciones_Incentivos.html', 
                            titulo="Operaciones",
                            tipo = "Agrupación",
                            subtitulo="Incentivos",
                            formulario = "13",
                            incentivos=incen,
                            agrupaciones = agrupas
                            )

@main.route('/operaciones/analisis/incentivos', methods=['GET', 'POST'])
@login_required
def incentivosAnalisis():
    if request.method == 'POST':
        incenImp     = request.form['incenImporte']
        newInc     = Incentivo(incenImp)
        newInc.save()
        return redirect(url_for('main.incentivosAnalisis'))
    incen = Incentivo.get_all()
    return render_template('form_Operaciones_Incentivos.html', 
                            titulo="Operaciones",
                            tipo = "Análisis",
                            subtitulo="Incentivos",
                            formulario = "11",
                            incentivos=incen)

@main.route('/operaciones/analisis/borrar-incentivo', methods=['GET', 'POST'])
@login_required
def borrarInc():
    id = request.form['id']
    Incentivo.delete_incentivo(id)
    return 'OK'

@main.route('/operaciones/analisis/editar-incentivo', methods=['GET', 'POST'])
@login_required
def editarIncentivo():
    id = request.form['id']
    imp = request.form['imp'] 
    datos = [id, imp]
    Incentivo.update_incentivo(datos)
    return redirect(url_for('main.incentivosAnalisis'))
# ----------------------------------------------------------


if __name__=='__main__':
    app.run(debug=True)