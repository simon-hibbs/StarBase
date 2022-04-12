#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

import sys, os
from PySide.QtCore import *
from PySide.QtGui import *
from log import *
#import qrc_resources
from ConfigParser import SafeConfigParser
from model import Models
from model import Traveller


class ProjectManager(QDialog):
    
    def __init__(self, model, parent=None):
        super(ProjectManager, self).__init__(parent)

        self.setWindowTitle("StarBase Project Manager")
        info_log("Initialising Project Manager")
        self.model = model

        self.projects = []
        self.defaultProject = 0
        self.config = SafeConfigParser()

        dialogLayout = QGridLayout()

        instructions_text = """To open a project select it and click 'Open Project'.
'Add Project' allows you to create/select a directory and add it to the list.
If the directory already contains a project, with will not be over-written. 
"""
        instructionsLabel = QLabel(instructions_text)
        projectListlabel = QLabel('Project List')
        self.projectListWidget = QListWidget()
        self.pathTextLine = QLineEdit()
        
        dialogLayout.addWidget(instructionsLabel,0,0)
        dialogLayout.addWidget(projectListlabel,1,0)
        dialogLayout.addWidget(self.projectListWidget,2,0,8,1)
        dialogLayout.addWidget(self.pathTextLine,10,0)

        self.openProjectButton = QPushButton('Open Project')
        self.newProjectButton = QPushButton('Add Project')
        self.makeDefaultButton = QPushButton('Make Default')
        self.removeProjectButton = QPushButton('Remove Project')
        self.closeButton = QPushButton('Close')
        self.pathButton = QPushButton('Change Path')

##        self.connect(openProjectButton, SIGNAL("clicked()"), self.openProject)
##        self.connect(newProjectButton, SIGNAL("clicked()"), self.newProject)
##        #newProjectButton.setDisabled(True)
##        self.connect(makeDefaultButton, SIGNAL("clicked()"), self.makeDefaultProject)
##        self.connect(removeProjectButton, SIGNAL("clicked()"), self.removeProject)
##        self.connect(closeButton, SIGNAL("clicked()"), self.close)
##        self.projectListWidget.currentRowChanged[int].connect(self.projectSelected)
##        self.connect(self.pathButton, SIGNAL("clicked()"), self.changePath)

        self.openProjectButton.clicked.connect(self.openProject)
        self.newProjectButton.clicked.connect(self.newProject)
        self.makeDefaultButton.clicked.connect(self.makeDefaultProject)
        self.removeProjectButton.clicked.connect(self.removeProject)
        self.closeButton.clicked.connect(self.close)
        self.pathButton.clicked.connect(self.changePath)
        self.projectListWidget.currentRowChanged[int].connect(self.projectSelected)

        dialogLayout.addWidget(self.openProjectButton,2,1)
        dialogLayout.addWidget(self.newProjectButton,3,1)
        dialogLayout.addWidget(self.makeDefaultButton,4,1)
        dialogLayout.addWidget(self.removeProjectButton,5,1)
        dialogLayout.addWidget(self.closeButton,9,1)
        dialogLayout.addWidget(self.pathButton,10,1)

        self.setLayout(dialogLayout)
        self.setMinimumWidth(500)

        self.readProjectsFile()



    def openProject(self):
        """Open the currently selected project in the main Starbase UI.
        """
        try:
            project_path = self.projects[self.projectListWidget.currentRow()]
            self.model.loadProjectData(project_path)
            QDialog.done(self, 1)
        except Exception, e:
            debug_log(str(e))
            debug_log('Current Row: ' + str(self.projectListWidget.currentRow()))
            debug_log('Projects list ' + str(self.projects))

    def newProject(self):
        if len(self.projects) == 0:
            default_path = os.getcwd()
        else:
            default_path = self.projects[self.defaultProject]
        
        dir_name = QFileDialog.getExistingDirectory(self,
                                                    'Select Project Directory',
                                                    default_path,
                                                    QFileDialog.ShowDirsOnly)
        qd = QDir()
        dir_name = str(qd.toNativeSeparators(dir_name))
        #print dir_name
        if dir_name != '':
            if os.path.exists(os.path.join(dir_name, 'starbase.ini')):
                self.projects.append(dir_name)
                project_name = os.path.split(dir_name)[-1]
                self.projectListWidget.addItem(project_name)
                self.writeProjectsFile()
            else:
                project_name = self.createNewProject(2, 2, dir_name)
                self.projects.append(dir_name)
                self.projectListWidget.addItem(project_name)
            
                self.writeProjectsFile()
        

    def makeDefaultProject(self):
        #config = SafeConfigParser()
        #config.read('projects.ini')
        self.defaultProject = self.projectListWidget.currentRow()
        self.config.set('Projects', 'default_project',
                   str(self.defaultProject))
        with open('projects.ini', 'wb') as projects_file:
            self.config.write(projects_file)

    def removeProject(self):
        rownum = self.projectListWidget.currentRow()
        item = self.projectListWidget.takeItem(rownum)
        del item
        self.projects = self.projects[0:rownum] + self.projects[(rownum + 1):]
        if self.defaultProject > len(self.projects):
            self.defaultProject = 0
        self.writeProjectsFile()


    def close(self, result=0):
        #self.model.loadProjectData("starbase.ini")
        QDialog.done(self, result)

    def changePath(self):
        current_path = self.pathTextLine.text()
        dir_name = QFileDialog.getExistingDirectory(self,
                                                    'Select Project Directory',
                                                    current_path,
                                                    QFileDialog.ShowDirsOnly)
        if dir_name == '':
            dir_name = current_path
        project_file = os.path.join(str(dir_name), 'starbase.ini')
        
        if not os.path.exists(project_file):
            warning = QMessageBox()
            warning.setText('Warning: The specified directory does not' + \
                            'contain a StarBase project')
            warning.exec_()

        self.projects[self.projectListWidget.currentRow()] = str(dir_name)
        self.pathTextLine.setText(dir_name)


    def projectSelected(self, row):
        self.pathTextLine.setText(self.projects[row])

    def readProjectsFile(self):
        self.config.read('projects.ini')

        number_of_projects = self.config.getint('Projects', 'number_of_projects')
        debug_log('Number of projects: ' + str(number_of_projects))
        
        for count in range(number_of_projects):
            name_ref = 'project_name_' + str(count)
            path_ref = 'project_directory_' + str(count)
            
            project_name = self.config.get('Projects', name_ref)
            project_path = self.config.get('Projects', path_ref)
            
            check_path = os.path.join(project_path, 'starbase.ini')
            debug_log('Checking path ' + check_path + \
                      ' for project ' + project_name)
            
            if os.path.exists(check_path):
                debug_log('Path exists.')
                self.projects.append(project_path)
                self.projectListWidget.addItem(project_name)
            else:
                debug_log('Path not found, broken project entry!')

        self.defaultProject = self.config.getint('Projects', 'default_project')
        
        if self.defaultProject > (len(self.projects) - 1):
            debug_log('Default project beyond end of list.')
            self.defaultProject = 0

        self.projectListWidget.setCurrentRow(self.defaultProject)

    def writeProjectsFile(self):
        debug_log('Blanking and re-writing application projects file.')
        self.config = SafeConfigParser()
        self.config.add_section('Projects')
        
        number_of_projects = len(self.projects)
        debug_log('Number of projects: ' + str(number_of_projects))
        self.config.set('Projects', 'number_of_projects', str(number_of_projects))
        
        for count in range(number_of_projects):
            name_ref = 'project_name_' + str(count)
            path_ref = 'project_directory_' + str(count)
            
            self.config.set('Projects', name_ref, str(self.projectListWidget.item(count).text()))
            self.config.set('Projects', path_ref, str(self.projects[count]))
            
##            check_path = os.path.join(project_path, 'starbase.ini')
##            debug_log('Checking path ' + check_path + \
##                      ' for project ' + project_name)
##            
##            if os.path.exists(check_path):
##                debug_log('Path exists.')
##                self.projects.append(project_path)
##                self.projectListWidget.addItem(project_name)
##            else:
##                debug_log('Path not found, broken project entry!')
        self.config.set('Projects', 'default_project', str(self.defaultProject))
        with open('projects.ini', 'wb') as projects_file:
            self.config.write(projects_file)

        
    def createNewProject(self, width, height, path):

        msgBox = QMessageBox()
        msgBox.setText("Delete directory contents?")
        msgBox.setInformativeText("Do you want to delete the " + \
                                  "contents of: " + path + " first?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.setMinimumWidth(500)
        response = msgBox.exec_()
        if response == QMessageBox.Yes:
            # Delete files under the project directory.
            for the_file in os.listdir(path):
                file_path = os.path.join(path, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception, e:
                    print e
        
        sectors = 'Sector Name,Column,Row\n'
        subsectors = 'Subsector Name,Column,Row\n'
##        worlds = 'World Name,Column,Row,Starport,Size,Atmosphere,' + \
##                 'Hydrographics,Population,Government,Law Level,' + \
##                 'Tech Level,Temperature,Gas Giant,Travel Code,' + \
##                 'Berthing Cost,Naval Base,Scout Base,Research Base,' +\
##                 'TAS,Imperial Consulate,Pirate Base, +Hydro. %,' + \
##                 'Allegiance,Ag,As,Ba,De,Fl,Ga,Hi,Ht,IC,In,Lo,Lt,' + \
##                 'Na,NI,Po,Ri,Va,Wa\n'
        worlds = ''
        for field in Models.FIELD_NAMES:
            worlds = worlds + field + ','
        worlds = worlds + '\n'
        secs_wide = width
        secs_high = height
        
        for sec_row in range(secs_high):
            for sec_column in range(secs_wide):
                sec_name = 'Sec' + str((sec_column + 1) + (sec_row * secs_wide))
                sectors += sec_name + ',' + str(sec_column) + ',' +  str(sec_row) + '\n'

                for sub_row in range(4):
                    for sub_col in range(4):
                        sub_name = sec_name + 'Sub' + str((sub_col + 1) + (sub_row * 4))
                        subsectors += sub_name + ',' + str(sub_col) + ',' + str(sub_row) + '\n'

        with open(os.path.join(path, 'worlds.csv'), 'w') as world_file:
            world_file.write(worlds)

        with open(os.path.join(path, 'sectors.csv'), 'w') as sectors_file:
            sectors_file.write(sectors)

        with open(os.path.join(path, 'subsectors.csv'), 'w') as subsectors_file:
            subsectors_file.write(subsectors)

        sbconf = SafeConfigParser()
        sbconf.add_section('Files')
        sbconf.set('Files', 'worldsfile', 'worlds.csv')
        sbconf.set('Files', 'sectorsfile', 'sectors.csv')
        sbconf.set('Files', 'subsectorsfile', 'subsectors.csv')

        sbconf.add_section('Map')
        sbconf.set('Map', 'sectorgridheight', str(height))
        sbconf.set('Map', 'sectorgridwidth', str(width))

        sbconf.add_section('Overrides')

        sbconf.add_section('Display')
        sbconf.set('Display', 'zoomlevel', '2')
        sbconf.set('Display', 'horizontalscroll', '100')
        sbconf.set('Display', 'verticalscroll', '100')

        with open(os.path.join(path, 'starbase.ini'), 'w') as starbase_file:
            sbconf.write(starbase_file)   

        project_name = os.path.split(path)[-1]
        return project_name
