from PyQt5.QtWidgets import (
    QAction, QLineEdit, QToolBar, QMessageBox, QLineEdit, QPushButton
)

from PyQt5.QtGui import QIcon, QClipboard

from PyQt5.QtWidgets import QLineEdit, QPushButton, QApplication

class Toolbar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_actions()
   
    def create_actions(self):
        prev_page_action = QAction(QIcon('icons/previous.png'), "Previous Page", self.parent)
        # prev_page_action = QAction("Previous Page", self.parent)
        prev_page_action.triggered.connect(self.previous_page)
        self.addAction(prev_page_action)

        # Create a field to enter a specific page number on the toolbar
        self.page_number_input = QLineEdit()
        self.page_number_input.setPlaceholderText("Enter Page Number")
        self.page_number_input.setMaximumWidth(50)
        self.addWidget(self.page_number_input)

        # Connect the returnPressed signal to the compute_expression method
        self.page_number_input.returnPressed.connect(self.jump_to_page)

        next_page_action = QAction(QIcon('icons/next.png'), "Next Page", self.parent)
        next_page_action.triggered.connect(self.next_page)
        self.addAction(next_page_action)





        # jump_to_page_action = QAction(QIcon('icons/goto.png'), "Jump to Page", self.parent)
        # jump_to_page_action.triggered.connect(self.jump_to_page)
        # self.addAction(jump_to_page_action)

        rotate_clockwise_action = QAction(QIcon('icons/clockwise.png'), "Rotate +90", self.parent)
        rotate_clockwise_action.triggered.connect(self.rotate_page_clockwise)
        self.addAction(rotate_clockwise_action)

        rotate_clockwise_action = QAction(QIcon('icons/anti-clockwise.png'), "Rotate -90", self.parent)
        rotate_clockwise_action.triggered.connect(self.rotate_page_Anti_clockwise)
        self.addAction(rotate_clockwise_action)

        zoom_in_action = QAction(QIcon('icons/zoom-in.png'), "Zoom In", self.parent)
        zoom_in_action.triggered.connect(self.zoom_in)
        self.addAction(zoom_in_action)

        zoom_out_action = QAction(QIcon('icons/zoom-out.png'), "Zoom Out", self.parent)
        zoom_out_action.triggered.connect(self.zoom_out)
        self.addAction(zoom_out_action)

        # Create a field to enter the zoom value on the toolbar
        self.zoom_input = QLineEdit()
        self.zoom_input.setPlaceholderText("Enter Zoom Value (%)")
        self.zoom_input.setMaximumWidth(50)  # Set the maximum width
        self.addWidget(self.zoom_input)

        apply_zoom_action = QAction(QIcon('icons/magnifier.png'), "Apply Zoom", self.parent)
        apply_zoom_action.triggered.connect(self.apply_zoom)
        self.addAction(apply_zoom_action)





        # Create a field to enter an expression
        self.expression_input = QLineEdit()
        self.expression_input.setPlaceholderText("Enter Expression")
        self.expression_input.setMaximumWidth(240)
        self.addWidget(self.expression_input)

        # Create a field to display the result
        self.result_display = QLineEdit()
        self.result_display.setPlaceholderText("Result")
        # self.result_display.setReadOnly(True)  # Make it read-only
        self.result_display.setMaximumWidth(80)
        self.addWidget(self.result_display)


        # Create a button to copy the result
        copy_button = QPushButton("Copy", self.parent)
        copy_button.clicked.connect(self.copy_result)
        self.addWidget(copy_button)


        # Connect the returnPressed signal to the compute_expression method
        self.expression_input.returnPressed.connect(self.compute_expression)


        # Create a "Comment" push button
        comment_button = QPushButton("Comment", self.parent)
        comment_button.clicked.connect(self.start_comment)
        self.addWidget(comment_button)

    def start_comment(self):
        self.parent.comment_mode = True  # Enable comment mode
        self.parent.comment_text = ""  # Initialize comment text

        # Connect the click event on the PDF page to create a comment
        self.parent.scroll_area.viewport().installEventFilter(self.parent)






    def rotate_page_clockwise(self):
        if self.parent.current_page is not None:
            # self.parent.rotate_page(rotation_angle=90)
            self.parent.current_page.set_rotation((self.parent.current_page.rotation + 90) % 360)
            self.parent.show_page(self.parent.current_page_number)

    def rotate_page_Anti_clockwise(self):
        if self.parent.current_page is not None:
            # self.parent.rotate_page(rotation_angle=90)
            self.parent.current_page.set_rotation((self.parent.current_page.rotation - 90) % 360)
            self.parent.show_page(self.parent.current_page_number)

    
    def previous_page(self):
        if self.parent.current_page_number > 0:
            self.parent.show_page(self.parent.current_page_number-1)

    def next_page(self):
        if self.parent.current_page_number < len(self.parent.pdf_document) - 1:
            self.parent.show_page(self.parent.current_page_number+1)



    def jump_to_page(self):
        page_number_text = self.page_number_input.text()
        try:
            page_number = int(page_number_text)
            if 1 <= page_number <= len(self.parent.pdf_document):
                self.parent.show_page(page_number - 1)
        except ValueError:
            pass

    
    def zoom_in(self):
        if self.parent.current_page is not None and self.parent.zoom_percentage > 0:
            self.parent.zoom_percentage += 10 #This line set the zoom level
            self.parent.show_page(self.parent.current_page_number)
            # self.parent.zoom_page() #This line refreshes the zoom

    def zoom_out(self):
        if self.parent.current_page is not None and self.parent.zoom_percentage > 0:
            self.parent.zoom_percentage -= 10
            self.parent.show_page(self.parent.current_page_number)

    def apply_zoom(self):
        zoom_text = self.zoom_input.text()
        try:
            self.parent.zoom_percentage = int(zoom_text)
            self.parent.show_page(self.parent.current_page_number)
            # self.parent.zoom_page() #This was duplicate. Use show page instead.
        except ValueError:
            pass







    def compute_expression(self):
        # Get the expression from the input field
        expression = self.expression_input.text()
        
        try:
            # Evaluate the expression and display the result
            result = str(eval(expression))
            self.result_display.setText(result)
        except Exception as e:
            # Display an error message if the expression is invalid
            QMessageBox.critical(self.parent, "Error", f"Error in expression: {str(e)}")




    def copy_result(self):
        result_text = self.result_display.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(result_text)