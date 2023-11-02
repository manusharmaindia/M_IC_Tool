import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QLabel, QScrollArea, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PyQt5.QtCore import QRectF, QSettings,Qt, QEvent
# from PyQt5.QtPrintSupport import QPdfWidget

from search_pdf import SearchDialog #Search Dialog is in another class
from toolbars import Toolbar #Import the toolbar class from toolbar (Delete this if you dont want to import)
from menubar import MenuBar

from PyQt5.QtWidgets import QAction, QFileDialog

from PyQt5.QtWidgets import (
    QLineEdit, QPushButton, QApplication, QGraphicsView, QGraphicsTextItem
)
from PyQt5.QtGui import QTextCursor, QColor
from PyQt5.QtCore import Qt, QEvent

from PyQt5.QtWidgets import QApplication



class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()




        #Comment Option Code

        # self.comment_mode = False  # Flag to track comment mode
        # self.comment_text = "Hi Hello"     # Store comment text

        # self.original_pdf_path = ""  # Store the original PDF file path











    def initUI(self):
        self.setWindowTitle("PDF Viewer with Toolbar")
        self.setGeometry(100, 100, 1200, 900)

        # Create a central widget for the PDF viewer
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(self.central_widget)

        # Create a scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Create a widget for the scroll area
        scroll_widget = QWidget()
        self.scroll_area.setWidget(scroll_widget)

        # Create a layout for the scroll widget
        scroll_layout = QVBoxLayout(scroll_widget)



        # # Create a widget for the scroll area
        # scroll_widget = QWidget()
        # self.scroll_area.setWidget(scroll_widget)

        # # Add the QPdfWidget to the scroll area
        # self.pdf_widget = QPdfWidget(scroll_widget)



        # Create a label to display the PDF pages as images
        self.pdf_label = QLabel()
        scroll_layout.addWidget(self.pdf_label) # Add label to scroll area.

        layout.addWidget(self.scroll_area)

        # Create a menu bar instance and add it to the main window
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Create a toolbar with an object name
        self.toolbar = Toolbar(self)  # Pass self as the parent to Toolbar
        self.toolbar.setObjectName("PDFViewerToolbar")  # Assign an object name
        self.addToolBar(self.toolbar)  # Add the toolbar to the main window

        # Initialize the PDF document and page variables
        self.pdf_document = None
        self.current_page = None
        self.current_page_number = None
        self.zoom_percentage = 100  # Default zoom

        # Load the last opened PDF file path from settings
        try:
            settings = QSettings("MyCompany", "MyPDFViewer")  # Change to your organization and application names
            last_opened_pdf = settings.value("LastOpenedPDF", "", type=str)
            if last_opened_pdf:
                self.open_pdf_from_path(last_opened_pdf)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while loading settings: {str(e)}")

    def open_search_dialog(self):
        self.search_dialog = SearchDialog(self.pdf_document, self)
        self.search_dialog.show() #Make it modaless
    


    # Modify the open_pdf_from_path method to store the original file path

    def open_pdf_from_path(self, pdf_path):
        try:
            self.original_pdf_path = pdf_path  # Store the original file path
            self.pdf_document = fitz.open(pdf_path)
            self.current_page_number = 0
            self.show_page(self.current_page_number)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while opening the PDF: {str(e)}")


    def open_pdf(self):
        options = QFileDialog.Options()
        pdf_file, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf)", options=options)

        if pdf_file:
            self.open_pdf_from_path(pdf_file)

            # Save the current PDF file as the last opened PDF
            try:
                settings = QSettings("MyCompany", "MyPDFViewer")  # Change to your organization and application names
                settings.setValue("LastOpenedPDF", pdf_file)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving settings: {str(e)}")

    def show_page(self, page_number):
        if self.pdf_document is not None and page_number >= 0 and page_number < len(self.pdf_document):
            try:


                self.current_page_number = page_number # Sets the current page number.

                self.current_page = self.pdf_document.load_page(page_number)
                # self.rotate_page()  # Apply page rotation
                pixmap = self.get_page_pixmap(self.current_page)
                self.pdf_label.setPixmap(pixmap)

                # Calculate the scroll position to keep the center of the PDF in view
                scroll_x = max(0, (self.current_page.rect.width * self.zoom_percentage / 100 - self.scroll_area.width()) / 2)
                self.scroll_area.horizontalScrollBar().setValue(int(scroll_x))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while displaying the page: {str(e)}")

    def get_page_pixmap(self, page):
        zoom = self.zoom_percentage / 100.0  # Adjust the zoom level
        mat = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        return QPixmap.fromImage(QImage(mat.samples, mat.width, mat.height, mat.stride, QImage.Format_RGB888))


    # def highlight_text(self, line_number):
    #     if self.current_page is not None:
    #         try:
    #             text = self.current_page.get_text()
    #             lines = text.split('\n')
    #             if 0 <= line_number < len(lines):
    #                 line = lines[line_number]
    #                 pixmap = self.get_page_pixmap_with_highlight(line)
    #                 self.pdf_label.setPixmap(pixmap)
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", f"An error occurred while highlighting text: {str(e)}")

    # def get_page_pixmap_with_highlight(self, highlight_text):
        # zoom = self.zoom_percentage / 100.0
        # mat = self.current_page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))

        # image = QImage(mat.samples, mat.width, mat.height, mat.stride, QImage.Format_RGB888)
        # painter = QPainter(image)
        # pen = QPen(QColor(255, 0, 0))  # Red highlight color
        # pen.setWidth(2)
        # painter.setPen(pen)

        # # Find the position of the highlighted text and draw a rectangle around it
        # for block in self.current_page.get_text_blocks():
        #     if highlight_text in block[4]:  # Check if the block contains the highlight_text
        #         x0, y0, x1, y1, _ = block[:5]
        #         # Scale the coordinates based on the zoom level
        #         x0 *= zoom
        #         y0 *= zoom
        #         x1 *= zoom
        #         y1 *= zoom
        #         rect = QRectF(x0, y0, x1 - x0, y1 - y0)
        #         painter.drawRect(rect)

        # painter.end()
        # return QPixmap.fromImage(image)



    # def highlight_text(self, line_number):
    #     if self.current_page is not None:
    #         try:
    #             text = self.current_page.get_text()
    #             lines = text.split('\n')
    #             if 0 <= line_number < len(lines):
    #                 line = lines[line_number]

    #                 zoom = self.zoom_percentage / 100.0
    #                 mat = self.current_page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    #                 image = QImage(mat.samples, mat.width, mat.height, mat.stride, QImage.Format_RGB888)

    #                 painter = QPainter(image)
    #                 pen = QPen(QColor(255, 0, 0))  # Red highlight color
    #                 pen.setWidth(2)
    #                 painter.setPen(pen)

    #                 for block in self.current_page.get_text_blocks():
    #                     if line in block[4]:  # Check if the block contains the line
    #                         x0, y0, x1, y1, _ = block[:5]
    #                         x0 *= zoom
    #                         y0 *= zoom
    #                         x1 *= zoom
    #                         y1 *= zoom
    #                         rect = QRectF(x0, y0, x1 - x0, y1 - y0)
    #                         painter.drawRect(rect)

    #                 painter.end()
    #                 pixmap = QPixmap.fromImage(image)
    #                 self.pdf_label.setPixmap(pixmap)

    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", f"An error occurred while highlighting text: {str(e)}")


    def highlight_text(self, line_number):
        """
        Highlight the specific line of text on the current page.

        Args:
        line_number (int): The line number to be highlighted.

        Returns:
        None

        This function highlights the specific line of text on the current page. It retrieves the text from the current page,
        splits it into lines, and then checks if the provided line number is within the range of the lines. If the line number
        is valid, it gets the specific line and proceeds to create a highlight effect. It does so by adjusting the zoom level,
        obtaining the pixmap of the current page, creating an image, and using a QPainter to draw a rectangle around the
        identified text block. The final highlighted pixmap is then set as the label's pixmap for display. If any errors occur
        during this process, it raises a critical message box displaying the encountered error.

        """
        if self.current_page is not None:
            try:
                # Get the text of the current page and split it into lines
                text = self.current_page.get_text()
                lines = text.split('\n')
                
                # Check if the provided line number is within the valid range
                if 0 <= line_number < len(lines):
                    line = lines[line_number]

                    # Calculate zoom and obtain the pixmap of the current page
                    zoom = self.zoom_percentage / 100.0
                    mat = self.current_page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
                    image = QImage(mat.samples, mat.width, mat.height, mat.stride, QImage.Format_RGB888)

                    # Create a QPainter to draw the highlight effect
                    painter = QPainter(image)
                    pen = QPen(QColor(255, 0, 0))  # Red highlight color
                    pen.setWidth(2)
                    painter.setPen(pen)

                    # Iterate through each text block to identify the specific line and draw a rectangle around it
                    for block in self.current_page.get_text_blocks():
                        if line in block[4]:  # Check if the block contains the line
                            x0, y0, x1, y1, _ = block[:5]
                            x0 *= zoom
                            y0 *= zoom
                            x1 *= zoom
                            y1 *= zoom
                            rect = QRectF(x0, y0, x1 - x0, y1 - y0)
                            painter.drawRect(rect)

                    painter.end()

                    # Convert the modified image to a pixmap and set it as the label's pixmap for display
                    pixmap = QPixmap.fromImage(image)
                    self.pdf_label.setPixmap(pixmap)

            except Exception as e:
                # If an error occurs during the highlighting process, display the error message in a critical message box
                QMessageBox.critical(self, "Error", f"An error occurred while highlighting text: {str(e)}")





















    # #Comment Option Code
    # def eventFilter(self, source, event):
    #     if self.comment_mode and source is self.scroll_area.viewport() and event.type() == QEvent.MouseButtonPress:
    #         # Create a comment annotation at the click location with the stored comment text
    #         self.create_comment(event.pos(), self.comment_text)
    #         self.comment_mode = False  # Disable comment mode
    #         return True
    #     return super(PDFViewer, self).eventFilter(source, event)

    # def create_comment(self, position, text):
    #     if self.current_page is not None:
    #         page = self.current_page
    #         zoom = self.zoom_percentage / 100.0
    #         position /= zoom  # Adjust the position based on the current zoom

    #         rect = fitz.Rect(position.x(), position.y(), position.x() + 100, position.y() + 20)
    #         page.insert_textbox(rect, text, fontsize=8, color=(1, 0, 0))










    # Modify the save_pdf method to use the original file path

    # def save_pdf(self):
    #     if self.pdf_document is not None and self.original_pdf_path:
    #         try:
    #             for page in self.pdf_document:
    #                 # Add your code to add annotations to pages as needed here
    #                 # For example, you can use page.insert_textbox(...) to add text annotations

    #             # Save the original PDF document with the new annotations incrementally
    #                 self.pdf_document.save(self.original_pdf_path, incremental=True)
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", f"An error occurred while saving the PDF: {str(e}")
    #         else:
    #             QMessageBox.warning(self, "Warning", "No original file path available. Please open a PDF first.")








if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())
