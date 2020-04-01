# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:51:53 2020

@author: User
"""
from PyQt5.QtWidgets import QApplication,QMainWindow,QAction,qApp,QDesktopWidget
from PyQt5.QtWidgets import QWidget,QGridLayout,QLabel
from PyQt5.QtGui import QIcon
import CovidCrawler,sys

MENU_CODE={'CONFIRMED':1,'ACTIVE':2,'DEATH':3,'RELEASED':4,'INCREASEMENT':5} #confirm selected menu to use refresh
class CovidWindow(QMainWindow):#Covid Windows
    selected_menu=0
    class CovidWidget(QWidget): #Windows Center Layout
        def __init__(self):
            super().__init__()
            self.init_layout()
            self.center()
            self.resize(700,560)
            self.show()
            
        def init_layout(self):
            self.grid=QGridLayout()
            self.setLayout(self.grid)
            self.nation_label=QLabel("국가") #fixed labed
            self.changing_label=QLabel(" ") #chaing label by selected
            
            self.grid.addWidget(self.nation_label,0,0)
            self.grid.addWidget(self.changing_label,0,1)
            
            self.data_label=[] #data saved label
            
            for i in range(CovidCrawler.MAX_TOP): #make label
                new_labels=[QLabel(" "),QLabel(" ")]
                self.grid.addWidget(new_labels[0],i+1,0)
                self.grid.addWidget(new_labels[1],i+1,1)
                self.data_label.append(new_labels)
        def center(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
        
        def set_changing_text(self,text):
            self.changing_label.setText(text)
            
        def set_data_text(self,data,selected_menu):
            label_idx=0 #Label position
            for d in data:
                nation=str(label_idx+1)+". "+CovidCrawler.CC_MAPPING[d['cc']] if d['cc'] in CovidCrawler.CC_MAPPING else str(label_idx+1)+". "+d['cc']
                # To show rangking
                
                if selected_menu==MENU_CODE['CONFIRMED']:
                    measure=d['confirmed']
                elif selected_menu==MENU_CODE['ACTIVE']:
                    measure=d['active']
                elif selected_menu==MENU_CODE['DEATH']:
                    measure=d['death']
                elif selected_menu==MENU_CODE['RELEASED']:
                    measure=d['released']
                else:
                    measure=d['confirmed']-d['confirmed_prev']
                    
                self.data_label[label_idx][0].setText(nation)
                self.data_label[label_idx][1].setText(str(measure))
                
                label_idx+=1
                    
                    
    def __init__(self):
        super().__init__()
        self.central_widget=self.CovidWidget()
        self.covid_crawler=CovidCrawler.CovidCrawler()
        self.init_ui()
        
    def init_ui(self): #init menu
        self.set_menu()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('COVID19 세계현황')
        self.resize(800,640)
        self.show_confirmed()
        self.center()
        self.show()
        
    
    def set_menu(self):
        confirmed_action=QAction('확진자 수',self)
        confirmed_action.setStatusTip('현재 국가 별 확진자 수를 보여줍니다.(상위 20개국만)')
        confirmed_action.triggered.connect(self.show_confirmed)
        
        active_action=QAction('치료중',self)
        active_action.setStatusTip('현재 국가 별 치료중인 사람의 수를 보여줍니다.(상위 20개국만)')
        active_action.triggered.connect(self.show_active)
        
        death_action=QAction('사망자 수',self)
        death_action.setStatusTip('현재 국가 별 사망자 수를 보여줍니다.(상위 20개국만)')
        death_action.triggered.connect(self.show_death)
        
        released_action=QAction('완치자 수',self)
        released_action.setStatusTip('현재 국가 별 완치자 수를 보여줍니다.(상위 20개국만)')
        released_action.triggered.connect(self.show_released)
        
        increasement_action=QAction('확진자 증가 수',self)
        increasement_action.setStatusTip('현재 확진자 증가 수를 보여줍니다.(상위 20개국만)')
        increasement_action.triggered.connect(self.show_increasement)
        
        increasement_action=QAction(QIcon('refresh.png'),'최신정보로 갱신',self)
        increasement_action.setStatusTip('최신 정보를 불러옵니다.')
        increasement_action.triggered.connect(self.refresh)
        
        exit_action = QAction(QIcon('exit.png'),'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('프로그램 종료.')
        exit_action.triggered.connect(qApp.quit)
        
        menubar=self.menuBar()
        menubar.setNativeMenuBar(False)
        menu=menubar.addMenu('&Menu')
        
        menu.addAction(confirmed_action)
        menu.addAction(active_action)
        menu.addAction(death_action)
        menu.addAction(released_action)
        menu.addAction(increasement_action)
        menu.addAction(exit_action)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def show_confirmed(self):
        confirmed_info=self.covid_crawler.get_confirmed()
        self.selected_menu=MENU_CODE['CONFIRMED']
        self.central_widget.set_changing_text("확진자 수")
        self.central_widget.set_data_text(confirmed_info,self.selected_menu)
    def show_active(self):
        active_info=self.covid_crawler.get_actvie()
        self.selected_menu=MENU_CODE['ACTIVE']
        self.central_widget.set_changing_text("치료중")
        self.central_widget.set_data_text(active_info,self.selected_menu)
    def show_death(self):
        death_info=self.covid_crawler.get_death()
        self.selected_menu=MENU_CODE['DEATH']
        self.central_widget.set_changing_text("사망자")
        self.central_widget.set_data_text(death_info,self.selected_menu)
    def show_released(self):
        released_info=self.covid_crawler.get_released()
        self.selected_menu=MENU_CODE['RELEASED']
        self.central_widget.set_changing_text("완치")
        self.central_widget.set_data_text(released_info,self.selected_menu)
    def show_increasement(self):
        increasement_info=self.covid_crawler.get_confirmed_increasement()
        self.selected_menu=MENU_CODE['INCREASEMENT']
        self.central_widget.set_changing_text("전날 대비 증가 수")
        self.central_widget.set_data_text(increasement_info,self.selected_menu)
    
    def refresh(self):
        if self.covid_crawler.crawl_data():
            if self.selected_menu==MENU_CODE['CONFIRMED']:
                self.show_confirmed()
            elif self.selected_menu==MENU_CODE['ACTIVE']:
                self.show_active()
            elif self.selected_menu==MENU_CODE['DEATH']:
                self.show_death()
            elif self.selected_menu==MENU_CODE['RELEASED']:
                self.show_released
            else:
                self.show_increasement()
                

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CovidWindow()
    sys.exit(app.exec_())
        
        
        
        