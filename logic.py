from PyQt6.QtWidgets import *

from gui import *
import os

#this code will allow user to enter an id and be able to choose a candidate using radio buttons.
#they will then click a submit button which will make a confirmation text appear and show the vote counts and write it to a file
#it will record user id to prevent user from using the same id
class Logic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # store votes file
        self.vote_file = "votes.txt"

        # vote data
        self.voted_ids = set()
        self.john_votes = 0
        self.jake_votes = 0

        # Load existing votes
        self.load_votes()

        # Submit button
        self.ui.Submit_button.clicked.connect(self.submit_vote)

    def load_votes(self):
        #Load existing votes from the file.
        if os.path.exists(self.vote_file):
            with open(self.vote_file, "r") as file:
                for line in file:
                    id_number, candidate = line.strip().split(",")
                    self.voted_ids.add(id_number)
                    if candidate == "John":
                        self.john_votes += 1
                    elif candidate == "Jake":
                        self.jake_votes += 1

    def submit_vote(self):
        #Handle vote submission.
        id_number = self.ui.ID_input.text().strip()
        if self.ui.John_radio.isChecked():
            candidate = "John"
        elif self.ui.jake_radio.isChecked():
            candidate = "Jake"
        else:
            candidate = None

        # Validate the input
        if not id_number.isdigit():
            self.display_message("Invalid ID. Only numbers are allowed.", "red")
            return
        if id_number in self.voted_ids:
            self.display_message("ID already used. You have already voted.", "red")
            return
        if candidate is None:
            self.display_message("Please select a candidate.", "red")
            return

        # Record the vote
        self.voted_ids.add(id_number)
        if candidate == "John":
            self.john_votes += 1
        elif candidate == "Jake":
            self.jake_votes += 1

        self.save_vote(id_number, candidate)
        self.display_message(f"You voted for {candidate}.", "green")
        self.update_totals()

    def save_vote(self, id_number, candidate):
        #Save the vote to the file.
        with open(self.vote_file, "a") as file:
            file.write(f"{id_number},{candidate}\n")

    def update_totals(self):
        #Update vote totals
        self.ui.VoteTotals_label.setText(
            f"John: {self.john_votes} votes, Jake: {self.jake_votes} votes"
        )

    def display_message(self, message, color):
        """Display a message with a specific color."""
        self.ui.VoteConfirmation_label.setText(message)
        self.ui.VoteConfirmation_label.setStyleSheet(f"color: {color};")