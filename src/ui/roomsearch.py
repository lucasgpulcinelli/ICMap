from PyQt5.QtWidgets import QLineEdit, QListView, QWidget, QVBoxLayout
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class RoomSearch(QWidget):
    '''
    class RoomSearch defines a widget that shows an interactive search bar with 
    the options given.
    '''

    def __init__(self, options, search_placeholder):
        super().__init__()
        self.options = options

        layout = QVBoxLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText(search_placeholder)

        self.options_list = QListView(self)
        self.model = QStandardItemModel()
        self.options_list.setModel(self.model)

        layout.addWidget(self.search_input)
        layout.addWidget(self.options_list)

        self.setLayout(layout)

        self.search_input.textChanged.connect(self.filterOptions)
        self.search_input.returnPressed.connect(self.selectFirst)
        self.options_list.clicked.connect(self.selectPos)

        self.updateOptions(self.options)

    def updateOptions(self, options):
        '''
        updateOptions updates the options available in the search bar depending
        on the text written.
        '''

        self.model.clear()
        for option in options:
            item = QStandardItem(option)
            self.model.appendRow(item)

    def filterOptions(self, text):
        '''
        fileterOptions runs every time the user writes to the search bar to 
        update the available options.
        '''

        filtered_options = [
            option for option in self.options if text.lower() in option.lower()
        ]

        self.updateOptions(filtered_options)

    def selectFirst(self):
        '''
        selectFirst selects the first match in the options given the search bar 
        text.
        '''

        if self.search_input.text() == "":
            return None

        item = self.model.item(0, 0)
        if item is None:
            self.search_input.setText("")
            return None
        t = item.text()
        self.search_input.setText(t)
        return t

    def selectPos(self):
        '''
        selectPos selects the text the user has clicked on.
        '''

        item = None
        try:
            item = self.options_list.selectedIndexes()[0].data()
        except IndexError:
            return
        self.search_input.setText(item)
