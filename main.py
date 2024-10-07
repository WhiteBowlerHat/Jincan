# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
from moviepy.editor import VideoFileClip, AudioFileClip

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
from pytubefix import YouTube
from pytubefix.cli import on_progress
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "JINCAN"
        description = "JINCAN - A toolbox for fun !"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_tools.clicked.connect(self.buttonClick)
        
        widgets.btn_tool1_imgcrypt.clicked.connect(self.buttonClick)
        widgets.btn_tool2_ytbdl.clicked.connect(self.buttonClick)


        widgets.ytdlDownloadBtn.clicked.connect(self.buttonClick)
        widgets.ytdlOpenFolderBtn.clicked.connect(self.buttonClick)
        


        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # EXTRA TOOL BOX
        def openCloseToolBox():
            UIFunctions.toggleToolBox(self, True)
        widgets.btn_tools.clicked.connect(openCloseToolBox)
        widgets.toolBoxCloseColumnBtn.clicked.connect(openCloseToolBox)
        widgets.ytdlURLField.textChanged.connect(self.ytdl_text_change)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
    

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            UIFunctions.toolbox_close(self)

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            UIFunctions.toolbox_close(self)

        # SHOW NEW PAGE
        if btnName == "btn_tools":
            #widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_tool2_ytbdl":
            widgets.stackedWidget.setCurrentWidget(widgets.youtube_downloader)
        
        if btnName == "btn_tool1_imgcrypt":
            widgets.stackedWidget.setCurrentWidget(widgets.fog_project)

        if btnName == "ytdlOpenFolderBtn":
            folder_path = QFileDialog.getExistingDirectory(self, "Select Input Folder")
            if folder_path:
                widgets.ytdlOutFolderLabel.setText(folder_path)

                
        if btnName == "ytdlDownloadBtn":         
            url = widgets.ytdlURLField.text()
            yt = YouTube(url, on_progress_callback = on_progress)
            path = widgets.ytdlOutFolderLabel.text()
            itag = widgets.ytdlAvailResList.currentData()

            print(path)

           
            if os.path.isdir(path):
                    output_path = path
            else:
                output_path="."

            video=yt.streams.get_by_itag(itag)

            if video.is_progressive == False:
                audio=yt.streams.filter(only_audio=True)[0]
                audio.download(output_path, filename="tmp_aud.mp4")
                video.download(output_path, filename="tmp_vid.mp4")
                
                video_clip = VideoFileClip(output_path+"/tmp_vid.mp4")
                audio_clip = AudioFileClip(output_path+"/tmp_aud.mp4")
                # Set the audio of the video clip
                final_video = video_clip.set_audio(audio_clip)

                # Write the final video to file
                final_video.write_videofile(output_path+"/"+video.title+".mp4", codec="libx264", audio_codec="aac")
                os.remove(output_path+"/tmp_vid.mp4")
                os.remove(output_path+"/tmp_aud.mp4")
            else:          
                video.download(output_path)     

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

    def ytdl_text_change(self):
            url = widgets.ytdlURLField.text()
        #try:
            yt = YouTube(url)
            size=""
            res =""
            for s in yt.streams.filter(type="video"):
                res+=str(s.resolution)+" | "
                size+=str(s.filesize_mb)+"MB | "
            #size = yt.streams.get_highest_resolution().filesize_mb
            
            title = yt.title
            author = yt.author
            descr = yt.description

            widgets.ytdlTitleLabel.setText(title)
            widgets.ytdlChannelLabel.setText(author)
            widgets.ytdlSizeLabel.setText(str(size)+"MB")
            widgets.ytdlDescriptionLabel.setPlainText(descr)
            widgets.ytdlResolutionLabel.setText(res)
            widgets.ytdlAvailResList.clear()
            for s in yt.streams.filter(mime_type="video/mp4"):
                if s.is_progressive == True:
                    widgets.ytdlAvailResList.addItem(s.resolution+"("+str(s.filesize_mb)+"MB) Fast", s.itag)
                else :
                    widgets.ytdlAvailResList.addItem(s.resolution+"("+str(s.filesize_mb)+"MB) Slow", s.itag)
            print(yt.streams)
        # except:
        #     widgets.ytdlTitleLabel.setText("None")
        #     widgets.ytdlChannelLabel.setText("None")
        #     widgets.ytdlSizeLabel.setText("None")
        #     widgets.ytdlDescriptionLabel.setPlainText("None")
        #     widgets.ytdlResolutionLabel.setText("None")

            
        

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
