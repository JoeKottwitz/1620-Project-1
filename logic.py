from PyQt6.QtWidgets import *
from gui import *
import csv


class Logic(QMainWindow, Ui_MainWindow):
    '''
    Class to provide functionality to the voting portal gui
    '''

    def __init__(self) -> None:
        '''
        Method to initialize the voting portal gui
        '''
        super().__init__()
        self.setupUi(self)

        self.button_submit.clicked.connect(lambda: self.submit())

    def submit(self) -> None:
        '''
        Method to provide functionality to the voting portal gui by
        verifying all data given and sending the data to be saved
        in the correct location
        '''
        self.label_error.setText('')

        if self.check_NUID(self.entry_nuid.text()):
            self.clear_gui()
            return
        if self.check_voter(self.entry_nuid.text()):
            self.label_error.setText(f"<font color='red'>Already voted. Cannot vote again.</font>")
            self.clear_gui()
            return

        candidate = self.check_candidate()
        if candidate == None:
            self.label_error.setText(f"<font color='red'>Please select a candidate</font>")
            return

        self.record_vote(self.entry_nuid.text(), candidate)
        self.update_vote_count(candidate)

        self.clear_gui()
        self.label_error.setText(f"<font color='green'>You voted for {candidate}. "
                                 f"Your vote has been recorded. Thank you for voting!</font>")

    def check_NUID(self, NUID) -> bool:
        '''
        Method to check if the NUID entered is valid
        :param NUID: User's NUID
        '''
        try:
            if not NUID.isdigit():
                raise TypeError
            if len(NUID) != 8:
                raise ValueError
        except TypeError:
            self.label_error.setText(f"<font color='red'>NUID must contain numerical characters only</font>")
            return True
        except ValueError:
            self.label_error.setText(f"<font color='red'>NUID must be exactly 8 characters</font>")
            return True

    def check_voter(self, NUID) -> bool:
        '''
        Method to check if the user has voted already
        :param NUID: User's NUID
        '''
        voted = False

        with open('votes.csv', 'r') as votes:
            voter = csv.reader(votes)

            for row in voter:
                if NUID == row[0]:
                    voted = True
                    break

        return voted

    def check_candidate(self) -> str:
        '''
        Method to find which candidate is selected
        :return: Selected candidate
        '''
        candidate = None
        if self.radio_candidate1.isChecked():
            candidate = "John"
        elif self.radio_candidate2.isChecked():
            candidate = "Jane"
        elif self.radio_candidate3.isChecked():
            candidate = "Jack"

        return candidate

    def record_vote(self, NUID, candidate) -> None:
        '''
        Method to record voting information to a csv file
        :param NUID: User's NUID
        :param candidate: Selected candidate
        '''
        row = [NUID, candidate]

        with open('votes.csv', 'a', newline='') as votes:
            voting_info = csv.writer(votes)
            voting_info.writerow(row)

    def update_vote_count(self, candidate) -> None:
        '''
        Method to update the number of votes for the selected candidate
        :param candidate: Selected candidate
        '''
        with open('votes.csv', 'r') as votes_list:
            read_names = csv.reader(votes_list)
            data_update = list(read_names)

        for row in range(len(data_update)):
            if data_update[row][0] == candidate:
                data_update[row][1] = int(data_update[row][1]) + 1
                break

        with open('votes.csv', 'w', newline='') as votes:
            vote_count = csv.writer(votes)
            vote_count.writerows(data_update)

    def clear_gui(self) -> None:
        '''
        Method to clear all information out of the gui
        '''
        self.entry_nuid.clear()

        if self.radio_candidate1.isChecked() or self.radio_candidate2.isChecked() or self.radio_candidate3.isChecked():
            self.radio_group.setExclusive(False)
            self.radio_group.checkedButton().setChecked(False)
            self.radio_group.setExclusive(True)
