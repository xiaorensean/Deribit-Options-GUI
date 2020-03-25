from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys

data = {'col1':['1','2','3','4'],
        'col2':['1','2','1','3'],
        'col3':['1','1','2','1']}


class TableView(QTableWidget):
    
    def __init__(self, title, data, *args):
        QTableWidget.__init__(self, *args)
        self.title = title
        self.data = data
        self.setData()
        #self.left = 100
        #self.top = 100
        #self.width = 600
        #self.height = 400
        self.createTable()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
 
    def setData(self): 
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)
 
    def createTable(self):
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        
        # create table
        self.setData()

        # Show widget
        self.show()


def main(args):
    app = QApplication(args)
    table = TableView("BTC Options Table",data, 4, 3)
    sys.exit(app.exec_())
 
if __name__=="__main__":
    main(sys.argv)