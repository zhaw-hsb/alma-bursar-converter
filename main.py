# imports for tkinter
import tkinter as tk
from tkinter import messagebox, Label

# other imports
#import pandas as pd
from pathlib import Path

import pandas as pd


class PyBursar:
    """
    PyBursar:
        Class needed for the tkinter framework
    """
    ##################################
    # FREQUENTLY USED VARIABLES
    # If slsp sends new types of lists they can be added in the following variables.
    # Do not forget to add a corresponding value in each variable.
    ##################################

    folder_list = ["late_payments",
                   "unsuccessful_payment_reminders",
                   "op_lists"
    ]
    """
    Use:
        Variable that contains a list of all the folders. This list is based on the types of lists slsp send to participating institutions.
    Types:
        Strings only
    Note:
        
    """

    status = ['manual_payment',
              'late_payments',
              'unsuccessful_payment_reminders',
              'op_lists'
    ]
    """
    Use:
        Variable that contains a list of all possible fee types. This list is only needed to set the order of precedence of all the fee types.
    Types:
        Strings only
    Note:
        Order of list items is important! It helps determine which instance of a fee is kept in the deduplication process.
    """

    date_columns_sorting = {
        "late_payments": "Zahlungsdatum", # there should only be one instance of every unique fee, but just to be sure...
        "unsuccessful_payment_reminders": "Abschlussdatum", # there should only be one instance of every unique fee, but just to be sure...
        "op_lists": "Datum Mahnung" # for the main list we only care about the fees that have been closed.
    }
    """
    Use:
        Variable that contains a dictionary defining which date column is used to sort the fees in the deduplication process.
        Ensures that only the most recent instance of a fee is kept.
    Types:
        Dictionary with string only key value pairs
    """

    blocked_users_file = Path('blocked_users.xlsx')
    manual_payments_file = Path("manual_payments.xlsx")
    main_file = Path('main_list.xlsx')

    """
    Use:
        Variable that stores the path for frequently used files.
    Types:
        Must be pathlib object as various methods are used like path.exists
    """


    ##################################
    # CLASS FUNCTIONS
    ##################################

    def __init__(self):
        """
        __init__:
            Initializing of the class. Contains all parameters and functions called upon the initialization of the class.
        """

        # Initialize TkInter instance for root window and its properties
        self.root = tk.Tk()
        self.root.title("PyBursar")
        self.root.geometry("600x300")

        # add app title
        self.title = Label(self.root, text = "PyBursar")
        self.title.config(font=("Courier", 14))
        self.title.pack(pady=20, padx=20)

        # Create a button widget
        self.button = tk.Button(self.root, text="Initial Setup", command=self.initial_setup)
        self.button.pack(pady=20, padx=20)

        self.button = tk.Button(self.root, text="Update Lists", command=self.update_lists)
        self.button.pack(pady=20, padx=20)

        # Run the interface
        self.root.mainloop()

    def initial_setup(self):
        """
        Use:
            Function that sets up the application. It creates the folders and files needed to run the application.
        """

        message = ""
        """
        Use:
            Contains the text of a message
        """

        # Check if the required folders exist. If the folders are missing they are created
        for folder in PyBursar.folder_list:
            path = Path(folder)
            if not path.exists():
                path.mkdir()
                message += (f"Folder '{folder}' created.\n")

        # If the file manual_payments.xlsx does not yet exist, create it.
        if not self.manual_payments_file.exists():
            columns_manual_payments = ["Library Code","Gebührentyp", "UserID", "TransactionID", "Barcode of Item", "Gebührentext", "Gebührenkommentar", "Abgeschlossener Betrag","Zahlungseingang","Zahlungsdatum","Kommentar"]
            df_manual_payments = pd.DataFrame(columns=columns_manual_payments, dtype='str')
            df_manual_payments.index.name = 'UserID'
            df_manual_payments.to_excel('manual_payments.xlsx')
            message += "File manual_payments.xlsx created.\n"

        # If the file blocked_users.xlsx does not yet exist, create it.
        if not self.blocked_users_file.exists():
            columns = ['Blocks', 'Date Blocked', 'Blocked by']
            df = pd.DataFrame(columns=columns, dtype='str')
            df.index.name = 'UserID'
            df.to_excel('blocked_users.xlsx')
            message += "File blocked_users.xlsx created."

        # If no setup was needed the message is set to the following text.
        if len(message) == 0:
            message = "Initial setup has been previously executed. No folders or files have been created."

        # Display message to user
        tk.messagebox.showinfo(title="Initial Setup", message=message)

    ##################################
    # ASSISTING FUNCTIONS
    # These are the functions called by the main function below.
    ##################################

    def combine_csv(self):
        """
        Use:
            Combines all csv files in the folders defined in the variable folder_list
        """
        for folder in PyBursar.folder_list:
            path = Path(folder)
            dataframe_list = []
            for file in path.glob('*.csv'):
                df = pd.read_csv(file, encoding='windows-1252', on_bad_lines='warn', sep=';')
                dataframe_list.append(df)

            # Concatenate all DataFrames into one
            combined_df = pd.concat(dataframe_list, ignore_index=True)

            # save combined csv to excel files
            combined_df['status'] = str(path)
            file_name = str(path) + '_combined.xlsx'
            xlsx_path = path / file_name
            combined_df.to_excel(xlsx_path)

    def update_blocked_users(self):
        """
        Use:
            Checks the main files for users that need to be blocked.
            Those users are added to the file blocked users.
            In a last step the information in the file blocked users is added to the main file
        """

        # read blocked users file and check which users are already blocked
        blocked_users_df = pd.read_excel(self.blocked_users_file, dtype='str')

        # read main file to check which users need to be blocked
        new_blocked_users_df = pd.read_excel(self.main_file, dtype='str')
        new_blocked_users_df = new_blocked_users_df[~new_blocked_users_df['UserID'].isin(blocked_users_df['UserID'])]
        new_blocked_users_df = new_blocked_users_df['UserID']

        # Add users that need to be blocked
        updated_list_blocked_users_df = pd.concat([blocked_users_df, new_blocked_users_df.to_frame('UserID')], ignore_index=True)

        # write results to excel file
        updated_list_blocked_users_df.to_excel(self.blocked_users_file)

    ##################################
    # MAIN FUNCTION
    # This function is the one that is executed when the user clicks on update lists
    ##################################

    def update_lists(self):
        """
        Use:
            Combines all the different list into the main file.
        """

        # Combine all csv files into excel files
        self.combine_csv()
        # combine all the excel files to one master list
        files = Path.cwd().rglob('*_combined.xlsx')
        data_frames = []
        for file in files:
            if not file.match('~$*'):  # ignore temp excel files
                df = pd.read_excel(file)
                try:
                    list = str(file.parents[0])
                    df.sort_values(['TransactionID', self.date_columns_sorting[list]], ascending=False, inplace=True)
                except:
                    df.sort_values(['TransactionID'], ascending=False, inplace=True)
                data_frames.append(df)

        # Read file wit all the manual payments
        manual_payments_df = pd.read_excel(self.manual_payments_file)
        # add manual payments to dataframe for the main list
        data_frames.append(manual_payments_df)

        # combina all the lists for the main file
        combined_df = pd.concat(data_frames, ignore_index=True)
        # Change status column data type to categorical to enable sorting
        combined_df['status'] = pd.Categorical(combined_df['status'], categories=PyBursar.status, ordered=True)
        # Sort by status and remove duplicates
        combined_df.sort_values(['TransactionID', 'status'], ascending=False, inplace=True)
        combined_df.drop_duplicates(subset=['TransactionID'], keep='last', inplace=True)


        # --> We want to drop unwanted columns here.

        # Save results to excel file
        combined_df.to_excel(self.main_file)

        # Update blocked user
        self.update_blocked_users()


##################################
# INITIALIZE CLASS
##################################
PyBursar()
