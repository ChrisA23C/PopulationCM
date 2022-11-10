import math
import random
import sys
from pathlib import Path
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QMessageBox, QScrollArea,
                             QAction, QFileDialog, QDialog, QApplication,
                             QPushButton, QVBoxLayout, QWidget, QLabel,
                             QTableWidget,QTableWidgetItem, QGridLayout)
from PyQt5.QtGui import QIcon

#Const
address = 'C:' #The default address where the output address where the output
#file will be saved
A = 1 #Draw window system counter
NL = 1000 #Number of curves
KAveraging = 5 #Averaging factor
Forecasting_Years = 30 #Forecasting years
data = {} #Dict with population size options
table = pd.DataFrame() #Table system variable

class MainWindow(QMainWindow): #Main window

    def __init__(self):
        super().__init__()
        self.w = None
        self.initUI()

    def initUI(self):
        self.statusBar()
        self.setWindowIcon(QIcon('Icon.ico'))

        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        change = QAction('Change repository', self)
        change.triggered.connect(self.ChangeRepository)

        saveFile = QAction('Save predictions', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.triggered.connect(self.showSave)

        helping = QAction('Help', self)
        helping.setShortcut('Ctrl+H')
        
        shown = QAction('Draw N', self)
        shown.triggered.connect(self.show_new_window_n)

        shownp = QAction('Draw N predictions', self)
        shownp.triggered.connect(self.show_new_window_np)
        
        showk = QAction('Draw '+'\u03BB'+' (growth coefficient)', self)
        showk.triggered.connect(self.show_new_window_k)
        
        showr = QAction('Draw R (growth rate)', self)
        showr.triggered.connect(self.show_new_window_r)

        showt = QAction('Table', self)
        showt.triggered.connect(self.show_table)

        showtp = QAction('Table Predict', self)
        showtp.triggered.connect(self.show_predict_table)

        prm = QAction('Parametrs',self)
        prm.triggered.connect(self.show_parametrs)

        helping = QAction('Help',self)
        helping.triggered.connect(self.show_helping)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(change)
        fileMenu = menubar.addMenu('&Draw')
        fileMenu.addAction(shown)
        fileMenu.addAction(shownp)
        fileMenu.addAction(showk)
        fileMenu.addAction(showr)
        fileMenu = menubar.addMenu('&Table')
        fileMenu.addAction(showt)
        fileMenu.addAction(showtp)
        fileMenu = menubar.addMenu('&Parametrs')
        fileMenu.addAction(prm)
        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(helping)

        self.setGeometry(30, 30, 550, 450)
        self.setWindowTitle('PopulationCM')
        self.show()

    def show_error_popup(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setWindowTitle('PopulationCM. Error')
        self.msg.setWindowIcon(QIcon('Icon.ico'))
        self.msg.setText("You didn't upload the file  or the data is invalid")
        initmsg = self.msg.exec_()

    def show_new_window_n(self, checked):
        try:
            m('n')
            init()
        except:
            self.show_error_popup()
        

    def show_new_window_np(self, checked):
        try:
            m('n')
            k(False)
            forecasting(Forecasting_Years, NL, KAveraging, 'plot')
            init()
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox. Information)
            self.msg.setWindowTitle('PopulationCM. Predictions')
            self.msg.setWindowIcon(QIcon('Icon.ico'))
            self.msg.setText(msf)
            initmsg = self.msg.exec_()
        except:
            self.show_error_popup()

    def show_new_window_k(self, checked):
        try:
            m('k')
            init()
        except:
            self.show_error_popup()

    def show_new_window_r(self, checked):
        try:
            m('r')
            init()
        except:
            self.show_error_popup()

    def showDialog(self):
        global f
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        if fname[0]:
            f = open(fname[0], 'r')
            try:
                reading(f)
                self.statusBar().showMessage('File uploaded successfully')
            except:
                self.msg = QMessageBox()
                self.msg.setIcon(QMessageBox.Critical)
                self.msg.setWindowTitle('PopulationCM. Error')
                self.msg.setWindowIcon(QIcon('Icon.ico'))
                self.msg.setText("File format doesn't match")
                initmsg = self.msg.exec_()

    def showSave(self):
        global data
        try:
            k(False)
            forecasting(Forecasting_Years, NL, KAveraging, 'table')
            df = pd.DataFrame.from_dict(data)
            df.to_csv(address+'/output.csv')
            self.statusBar().showMessage('File saved successfully')
        except:
            self.show_error_popup()

    def ChangeRepository(self):
        self.dialogc = DialogChange()
        self.dialogc.show()
    
    def show_table(self):
        try:
            self.tableqt = TableView(data, len(data[table.columns[0]]), len(data[table.columns[0]]))
            self.tableqt.show()
        except:
            self.show_error_popup()

    def show_predict_table(self):
        try:
            k(False)
            forecasting(Forecasting_Years, NL, KAveraging, 'table')
            self.tableqt = TableView(data, len(data[table.columns[0]]), len(data[table.columns[0]]))
            self.tableqt.show()
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox. Information)
            self.msg.setWindowTitle('PopulationCM. Predictions')
            self.msg.setWindowIcon(QIcon('Icon.ico'))
            self.msg.setText(msf)
            initmsg = self.msg.exec_()
        except:
            self.show_error_popup()

    def show_parametrs(self):
        self.dialog = Parametrs()
        self.dialog.show()

    def show_helping(self):
        self.helping = Reference()
        self.helping.show()
        
def main(): #Calling the main window
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

class Reference(QLabel): #Help window
    def __init__(self, *args):
        QLabel.__init__(self, *args)
        self.read()
 
    def read(self):
        f = open('help.txt', 'r')
        s = f.read()
        f.close()
        
        layout = QGridLayout()
        self.setLayout(layout)
        self.mw = QScrollArea()
        self.mw.setWidget(self)
        self.mw.setWindowTitle('PopulationCM. Help')
        self.mw.setWindowIcon(QIcon('Icon.ico'))
        self.mw.showMaximized()
        
        self.setText(s)
        self.adjustSize()
        self.setIndent(10)
 
class TableView(QTableWidget): #Table window
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.setWindowTitle('PopulationCM. Table')
        self.setWindowIcon(QIcon('Icon.ico'))
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
 
    def setData(self): #Table output
        horHeaders = []
        m = 0
        n = 0
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setColumnCount(len(data))
        for i in data.keys():
            if m == 0: self.setRowCount(len(data.get(i)))
            horHeaders.append(i)           
            for j in data.get(i):
                self.setItem(n, m, QTableWidgetItem(str(j)))
                n += 1
            n = 0
            m += 1
        self.setHorizontalHeaderLabels(horHeaders)


class Parametrs(QtWidgets.QDialog): #Prediction parametrs

    def __init__(self,parent=None):
        super().__init__()
        self.setWindowIcon(QIcon('Icon.ico'))
        self.setWindowTitle('PopulationCM. Prediction parameters')
        self.line_1 = QtWidgets.QLineEdit()
        self.line_2 = QtWidgets.QLineEdit()
        self.line_3 = QtWidgets.QLineEdit()
        self.apply = QtWidgets.QPushButton('Apply')
        self.apply.clicked.connect(self.getting)
        self.form = QtWidgets.QFormLayout()

        self.line_1.insert(str(Forecasting_Years))
        self.line_2.insert(str(NL))
        self.line_3.insert(str(KAveraging))

        self.form.addRow('&Number of years of prediction:',self.line_1)
        self.form.addRow('&Number of curves:',self.line_2)
        self.form.addRow('&Averaging factor:',self.line_3)
        self.form.addRow(self.apply)

        self.msg = QMessageBox()

        self.setLayout(self.form)

    def getting(self):
        global Forecasting_Years, NL, KAveraging
        try:
            Forecasting_Years = int(self.line_1.text())
            NL = int(self.line_2.text())
            KAveraging = int(self.line_3.text())
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle('PopulationCM')
            self.msg.setWindowIcon(QIcon('Icon.ico'))
            self.msg.setText('Changes applied successfully')
            initmsg = self.msg.exec_()
        except:
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setWindowTitle('PopulationCM. Error')
            self.msg.setWindowIcon(QIcon('Icon.ico'))
            self.msg.setText("You must enter integer values")
            initmsg = self.msg.exec_()

class DialogChange(QtWidgets.QDialog):

    def __init__(self,parent=None):
        super().__init__()
        self.setWindowIcon(QIcon('Icon.ico'))
        self.setWindowTitle('PopulationCM. Change Repository')
        self.line_1 = QtWidgets.QLineEdit()
        self.apply = QtWidgets.QPushButton('Apply')
        self.apply.clicked.connect(self.getting)
        self.form = QtWidgets.QFormLayout()

        self.line_1.insert(address)

        self.form.addRow('&Repository (Example: C:/Users/Admin/Downloads):',self.line_1)
        self.form.addRow(self.apply)

        self.setLayout(self.form)

    def getting(self):
        global address
        address = self.line_1.text()
        
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle('PopulationCM')
        self.msg.setWindowIcon(QIcon('Icon.ico'))
        self.msg.setText('Changes applied successfully')
        initmsg = self.msg.exec_()

def linearreg(x, y): # Calculation of coefficients of the linear regression
    size = len(x) #
    # Calculation of the numerator of the first vector
    numeratorw1 = size * sum(x[i] * y[i] for i in range(0, size)) - sum(x) * sum(y)
    # Calculation of the numerator of the first vector
    numeratorw0 = -sum(x) * sum(x[i] * y[i] for i in range(0, size)) + sum((x[i]) ** 2 for i in range(0, size)) * sum(y)
    # Calculation of the denominator of vectors
    denominator = size * sum((x[i]) ** 2 for i in range(0, size)) - (sum(x)) ** 2
    

    # Calculation of coefficients
    w0 = numeratorw0 / denominator
    w1 = numeratorw1 / denominator
    return w0, w1


def predict(w0, w1, x_scale):
    # w0 = -733.1284
    # w1 = 0.3951
    y_pred = [w0 + val * w1 for val in x_scale]
    return y_pred


def reading(name): #Reading a file
    global xglobal, yglobal, table, data
    xglobal = [] # Time-array x-axis
    table = pd.read_csv(name, delimiter=';')

    for i in range(1, len(table)):
        if type(table.at[i, table.columns.values[0]]) == str:
            xglobal.append(float((table.at[i, table.columns.values[0]]).replace(',', '.')))
        else:
            xglobal.append(float((table.at[i, table.columns.values[0]])))
    yglobal = [] # Population array y-axis
    for j in range(1, len(table)):
        if type(table.at[j - 1, table.columns.values[1]]) == str:
            yglobal.append(float((table.at[j - 1, table.columns.values[1]]).replace(',', '.')))
        else:
            yglobal.append(float((table.at[j - 1, table.columns.values[1]])))
    data = {table.columns[0] : xglobal, table.columns[1] : yglobal} 

def l(arr1, arr2):  # Линейная регрессия
    y_predict = predict(*linearreg(arr1, arr2), arr1)
    plt.figure(A)
    plt.plot(arr1, y_predict, label='Расчетные значения')


def r():  # Удельная скорость роста численности
    global A
    plt.title('PopulationCM')
    ygloballn = []
    ygloballn = [math.log(yglobal[i + 1]) - math.log(yglobal[i]) for i in range(0, len(yglobal) - 1) if i != 0]
    plt.figure(A)
    plt.scatter(yglobal[:-2], ygloballn)
    plt.ylabel('Specific population growth rate')
    plt.xlabel('Number')
    plt.hlines(sum(ygloballn) / len(ygloballn), min(yglobal), max(yglobal), color='r')
    l(yglobal[:-2], ygloballn)


def n():  # Численность популяции
    global A
    plt.title('PopulationCM')
    return xglobal, yglobal


def k(ret):  # Коэффициент роста численности
    global A
    global yglobal
    global yglobalk
    plt.title('PopulationCM')
    yglobalk = []
    for i in range(1, len(yglobal) - 1): yglobalk.append(yglobal[i] / yglobal[i - 1])
    if ret == True: return xglobal[2:], yglobalk


def forecasting(n,x,km,key): #prediction
    global xglobal,yglobal,data,table,msf
    xglobalf = xglobal.copy()
    yglobalf = yglobal.copy()
    length = len(xglobalf)
    kd = 0
    Block = False
    d = 1
    for i in range(len(xglobalf)): xglobalf[i] = int(xglobalf[i])
    for i in range(len(yglobalf)): yglobalf[i] = int(yglobalf[i])
    for i in range (1,n): xglobalf.append(xglobalf[-1] + 1)
    if key == 'table': data = {table.columns[0] : xglobalf}
    for j in range(1,x+1):
        for i in range(1, n):
            k = random.sample(range(0, len(yglobalk) - 1), km)
            summa = 0
            for j in k: summa += 1-yglobalk[j+1]+yglobalk[j]
            y = summa / km
            Rt = y
            yglobalf.append(round(Rt * yglobalf[-1]))
            if Rt * yglobalf[-2]<2:
                if Block == False:
                    kd +=1
                    Block = True
                if key == 'plot': break
                elif key == 'table': yglobalf[-1]=0
        if key == 'plot':
            plt.figure(A)
            plt.plot(xglobalf[:len(yglobalf)],yglobalf)
        if key == 'table':
            data[str(d)] = yglobalf
            d+=1
        yglobalf = yglobalf[:length]
        Block = False
    msf = 'Extinction probability = '+str(round(kd/x*100,1))+'%. Died = '+str(kd)
    plt.hlines(0, xglobalf[0], xglobalf[-1], color='r')
    plt.title('PopulationCM')
    plt.xlabel('Years')
    plt.ylabel('Number')
    return xglobalf, yglobalf


def m(mode): # Visualisation
    global A
    plt.figure(A)
    plt.xlabel('Years')
    if mode == 'n':
        plt.plot(*n())
        l(*n())
        plt.ylabel('Number')
    elif mode == 'r':
        r()
        plt.ylabel('Specific population growth rate')
    elif mode == 'k':
        plt.plot(*k(True))
        l(*k(True))
        plt.ylabel('Growth coefficient')
    A += 1


def init(): # Inizialization
    plt.show()

if __name__ == '__main__': #Start
    main()
