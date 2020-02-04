from pyqt5_client_2020 import Window
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
    
if __name__ == '__main__':    
    app = QtWidgets.QApplication(sys.argv)
    #MWindow = QtWidgets.QMainWindow()
    ui = Window()
    #th = Thread(ui)
    #th.changePixmap.connect(ui.setImage)
    #th.Change_af.connect(ui.for_auto_focus)
    #th.start()
    
    ui.show()
    #MWindow.show()   
    
    sys.exit(app.exec_())