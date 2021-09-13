from models import Agrupacion
import os
import pandas as pd
from flask import send_from_directory

from pathlib import Path





class GestionCsv():

    def write_csv(data, col, path):
        df = pd.DataFrame(data, columns= col)
        df.to_csv (path, index = False, header=True)


    def read_csv(path,col):
        df = pd.read_csv(path, usecols=col)
        df = df.fillna('')
        return df


class GestionExcel():

    
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in (['xls', 'xlsx'])

    def read_excel(path, name):
        df = pd.read_excel(path, sheet_name=name, skiprows=1)
        #df = pd.read_excel(r'.\static\assets\uploads\agrupacionesExcel.xls')
        #df.to_csv(r'.\static\assets\uploads\agrupacionesExcel.csv', index = None, header = True)
        return df

    def excel_to_csv(path, filename):
        path = path + "\\"
        pathname = path + filename
        df = pd.read_excel(pathname) 
        filename = Path(path + filename).stem       
        path = path + filename + ".csv"
        df.to_csv(path, index = None, header = None)        
        return df

    def uploadExcel(path, file, filename):
        file.save(os.path.join(path,filename))
        file.flush
        
    
    def downloadExcel(file_name, path):
        return send_from_directory(path, file_name, as_attachment=True)