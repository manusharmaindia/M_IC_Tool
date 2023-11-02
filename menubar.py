from PyQt5.QtWidgets import (
    QAction, QMenuBar,QToolBar
)



# Create a MenuBar class
class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_menus()

    def create_menus(self):
        # Create the "File" menu
        file_menu = self.addMenu("File")

        # Create an action to open a PDF file
        open_action = QAction("Open PDF", self.parent)
        open_action.triggered.connect(self.parent.open_pdf)
        file_menu.addAction(open_action)







        # Create a "Save" action in the "File" menu
        # save_action = QAction("Save", self.parent)
        # save_action.setShortcut("Ctrl+S")  # Define a shortcut key for saving
        # save_action.triggered.connect(self.parent.save_pdf)
        # file_menu.addAction(save_action)






        # Create the "View" menu
        view_menu = self.addMenu("View")

        toggle_toolbar_action = QAction("Show/Hide Toolbar", self.parent, checkable=True)
        toggle_toolbar_action.setChecked(True)  # Default: Toolbar is visible
        toggle_toolbar_action.triggered.connect(self.toggle_toolbar)  # Connect to the toggle_toolbar method in the MenuBar class
        view_menu.addAction(toggle_toolbar_action)

        # Create an action to open the Search Dialog
        search_action = QAction("Search Dialog", self.parent)
        search_action.setShortcut("Ctrl+F")  # Use a shortcut key
        search_action.triggered.connect(self.parent.open_search_dialog)
        view_menu.addAction(search_action)


    def toggle_toolbar(self):
        # Show or hide the toolbar based on the action's state
        toolbar = self.parent.findChild(QToolBar, "PDFViewerToolbar")
        if toolbar:
            toolbar.setVisible(self.parent.sender().isChecked())


