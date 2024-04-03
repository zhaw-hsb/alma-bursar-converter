# How does it work
This application helps libraries deal with all the lists SLSP sends the libraries participating
in the bursar service.

The application containes the code to generate executable files. Wen executing this executable file it
providesw an user interface with several options.

To generate the executable files the python library PyInstaller was used, however, any similar python library should work as well.
Instructions on how to use PyInstaller: https://datatofish.com/executable-pyinstaller/

# How to use it
You can download the executable python file for windows.
If you want to change the code or use it on any other operationg system you would need to genreate a new executable file. With the existing code.


## Create folders
This option creates all the folders where the files can be stored. The application heavily on these folders.
Please make sure to create these folders before executing the following steps. The command creates three different folders:

- OP-Lists: These lists contain all the current fees in ALMA.
- Unsuccesfull payment reminders: These lists contain all the fees that have been closed after the user has failed to pay the fees.
- Late payments: These lists contain all the late payments of fees that have already been closed.

## Update Lists
Important notice! The lists are newly generated after each execution of the command.
Any changes to those lists will be lost. Please use the list "manual payments" to add any payments not refected in the lists.
Please check the relevant sections for further information.

When you click on the button "update lists" all the lists in the folders are combines in an Excel file. 
In a first step all the files in each folder are combined. Those files are stored in their respective folders and can be identified by the suffix "_combined".

In a second step all the combined files are processed and a master file is created that contains the most
recent status of any fee.

# Master List
In this file every fee is listed with it's status. The status is detemined by the following logic:

Any fee only listed is considered "open".
Any fee from the lists "late payments" is considered "payed".
Any fee from the lists "manual payments" is considered "payed".

Any fee from the lists "unsuccesfull payment reminders" is considered "closed"

In addition all the fees from the "OP List" that either without reminders or that has not been added to the list 
"unsuccesfull payment reminders" after 41 respectively will be considered "likely payed".

# Blocked Users
When ths lists are updated the list of the blocked users is also updated. This list contains
All the Users that would need to be blocked. In the additional columns you can enter the date and the name of the librarian
that blocked the user. If the user is blocked the information from this list will be added to the master list. for each of the fees.

Unlike the other lists, this list is not deleted and can be edited. If information in any of the provided columns
this information will be added to the master list. This allows you to filter the list by blocked users.

# Manual Payments
The application provides a list where you can enter late payments by any user. The will be added in the master list and the status of any such fee will be set to
"payed". This list is provided for any cases where you allow the user to pay fees directly to the library instead of the bursar service.
This information only needs to be entered for fees with the status "closed".

