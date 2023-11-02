from PyQt5.QtWidgets import (
    QListWidgetItem,
    QDialog, QPushButton, QMessageBox
)
from num2words import num2words
from PyQt5 import uic

class SearchDialog(QDialog):
    def __init__(self, pdf_document, pdf_viewer):
        super().__init__()
        self.pdf_document = pdf_document
        self.pdf_viewer = pdf_viewer
        self.initUI()

    def initUI(self):
        uic.loadUi("search_dialog.ui", self)

        # self.setWindowTitle("Search Text in PDF")
        self.setGeometry(1320, 100, 500, 600)

        #Connect the signals to appropriate slots
        #self.case_sensitive_checkbox.stateChanged.connect(self.search_text)
        self.search_results.itemClicked.connect(self.item_clicked)

        # Manually connect the search button to the search_text function
        search_button = self.findChild(QPushButton, "search_button")
        if search_button:
            search_button.clicked.connect(self.search_text)

        # Automatically update the similar search terms when the search text changes
        self.search_input.textChanged.connect(self.update_similar_search_terms)

        # Connect the case-sensitive checkbox state change to trigger the search
        self.case_sensitive_checkbox.stateChanged.connect(self.search_text)
    


        # Create a button to close the modeless dialog
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        self.layout().addWidget(close_button)

    def closeEvent(self, event):
        self.hide()  # Hide the dialog instead of closing it
        event.ignore()  # Ignore the close event to keep the dialog modeless


    def update_similar_search_terms(self):
        search_text = self.search_input.text()
        formatted_similar_search_text = self.format_similar_search_text(search_text)
        self.similar_search_input.setText(formatted_similar_search_text)

    def format_similar_search_text(self, text):
        try:
            for char in [",", "$"," "]: #Replaces comma and $
                text = text.replace(char, "")

            number = float(text)
            formats = [
                f"{number:,.0f}",  # with comma and zero decimal
                f"{number:,.2f}",  # in 2 decimal places
                f"{number:,.3f}",  # in 3 decimal places
                f"{number/1000:,.2f} thousand",  # in thousands
                f"{number/1000:,.3f} thousand",  # in thousands
                f"{number/1000000:,.2f} million",  # in millions
                f"{number/1000000:,.3f} million",  # in millions
                f"{number/1000000000:.2f} billion",  # in billions Ex 111,555 shown as 0.01
                f"{number/1000000000:.3f} billion",  # in billions Ex 111,555 shown as 0.012
                num2words(number, lang = "en") #Amount in words
            ]
            formatted_similar_search_text = " | ".join(formats)
            return formatted_similar_search_text
        except ValueError:
            return text


    def search_text(self):
        self.search_results.clear()  # Clear previous search results

        if self.pdf_document is None: #This conditional check verifies that a PDF document has been loaded. If self.pdf_document is None, it means that there is no PDF document to search within. In such a case, the function returns early, and no search is performed.
            return

        search_terms = []

        
        if self.search_input.text():
            search_terms = [self.search_input.text()]  # Treat the main input as a single search term

        if self.similar_search_input.text():
            similar_search_text = self.similar_search_input.text()
            similar_search_terms = similar_search_text.split(" | ")

            # Use a list comprehension to clean and filter the search terms
            similar_search_terms = [term.strip() for term in similar_search_terms if term.strip()]
            # Extend the search_terms list with similar search terms
            search_terms.extend(similar_search_terms)



        if search_terms == []:
            QMessageBox.warning(self,"No Text Entered","Please Enter a Text")
            return
        


        case_sensitive = self.case_sensitive_checkbox.isChecked()

        #The function then iterates through each page of the PDF document using a for loop. It uses enumerate to get both.
        for page_number, page in enumerate(self.pdf_document):
            text = page.get_text()
            lines = text.split('\n')

            #The function uses nested loops to iterate through each line of text and each search term.
            for line_number, line in enumerate(lines):
                for term in search_terms:  # Iterate through each term
                    if (case_sensitive and term in line) or (not case_sensitive and term.lower() in line.lower()):
                        item_text = f"Page {page_number + 1} | Line {line_number + 1} - {line.strip()}"
                        item = QListWidgetItem(item_text)
                        item.page_number = page_number
                        item.line_number = line_number
                        self.search_results.addItem(item)




    def item_clicked(self, item):
        page_number = item.page_number
        line_number = item.line_number



        if page_number < len(self.pdf_document):
            self.pdf_viewer.show_page(page_number)
            self.pdf_viewer.highlight_text(line_number)
