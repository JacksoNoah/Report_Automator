import os
import pandas as pd
import numpy as np
import tkinter as tk
from datetime import date
from tkinter import filedialog, Text

root = tk.Tk()


# by running the following method, data for orders will be parsed and written to
# a new file containing needed data
def getAndFormat(userFile):
    # getting current working directory to use for creating file path to order data
    curWorDir = os.getcwd()

    formatted_DF_Columns = ["Licensor", "Date", "Invoice Id", "Item Description", "Item Identifier",
                            "Affinity Product Category", "Affinity Distribution Channel", "Retailer",
                            "Shipping Country", "Number of Units", "Price Per Unit",
                            "Gross Sales", "Royalties", "Licensed_Or_Not"]

    # initialize data frame that will hold formatted data
    formatted_Order_DataFrame = pd.DataFrame(index=np.arange(1000), columns=formatted_DF_Columns)

    # read data from user specified file path which should be order data
    df = pd.read_csv(userFile)
    df_columns = df.columns
    column_count = len(df_columns)
    row_count = df.shape[0]

    i = 0
    while i < row_count - 1:
        j = 0
        while j < column_count:
            # Match each column of data frame with correct data specified by affinity licensing
            if df_columns[j] == "Order Number":
                formatted_Order_DataFrame['Invoice Id'].values[i] = df.loc[i]["Order Number"]

            elif df_columns[j] == "Order Date":
                formatted_Order_DataFrame['Date'].values[i] = df.loc[i]["Order Date"]

            elif df_columns[j] == "Short Description":
                formatted_Order_DataFrame['Item Description'].values[i] = df.loc[i]["Short Description"]

            elif df_columns[j] == "SKU":
                formatted_Order_DataFrame['Item Identifier'].values[i] = df.loc[i]["SKU"]

            elif df_columns[j] == "Category":
                formatted_Order_DataFrame['Affinity Product Category'].values[i] = df.loc[i]["Category"]

            elif df_columns[j] == "Retailer":
                formatted_Order_DataFrame['Retailer'].values[i] = "Greek Clothing Co LLC"

            elif df_columns[j] == "Country Code":
                formatted_Order_DataFrame['Shipping Country'].values[i] = df.loc[i]["Country Code"]

            elif df_columns[j] == "Quantity":
                formatted_Order_DataFrame['Number of Units'].values[i] = df.loc[i]["Quantity"]

            elif df_columns[j] == "Item Cost":
                formatted_Order_DataFrame['Price Per Unit'].values[i] = df.loc[i]["Item Cost"]

            elif df_columns[j] == "Order Item Metadata":
                metaData = df.loc[i][j]

                # parse group name out of products meta data
                parsedMetaData = productMetaDataParser(metaData)

                # check if group is licensed
                checkIfLicensedGroup(parsedMetaData, formatted_Order_DataFrame, i)

                formatted_Order_DataFrame['Licensor'].values[i] = parsedMetaData

            j += 1
        i += 1
    calculate_gross_sales(formatted_Order_DataFrame)
    writeToFile(formatted_Order_DataFrame)


# parse group name from metadata
def productMetaDataParser(metaData):
    # split metadata by its delimiting bar character
    splitList = metaData.split("|")
    splitListLength = len(splitList)

    i = 0
    while i < splitListLength:
        # get all words that have "Greek" but dont have a quotation mark
        if "Greek" in splitList[i]:
            if "\"" not in splitList[i]:
                greekLetters = splitList[i].split(":")
                greekLettersFinal = greekLetters[1].strip()
                return greekLettersFinal

        i += 1
    return "none"


# takes a dataframe and writes it to a file
def writeToFile(formatted_data):
    # get current date for file name
    today = date.today()

    # getting current working directory to use for creating file path for ordered data DataFrame
    curWorDir = os.getcwd()
    # order_data_file = curWorDir + "/" + "Formatted_Order_Data-" + str(today)
    order_data_file = "/home/jacksonoah/Desktop/Work/GreekClothingCo/2020Q3/" + "Formatted_Order_Data-" + str(today)

    # write formatted data to new csv file
    formatted_data.to_csv(order_data_file, sep=',', encoding='utf-8', index=False)
    # formatted_data.to_csv("/home/jacksonoah/Desktop/Work/GreekClothingCo/2020Q3", sep=',', encoding='utf-8', index=False)


# calculate gross sale value for each sale
def calculate_gross_sales(formatted_data):
    row_count = formatted_data.shape[0]
    i = 0
    # for each order
    while i < row_count:
        # multiply quantity by the item price to get gross sale value
        formatted_data['Gross Sales'].values[i] = (
                formatted_data.iloc[i]['Number of Units'] * formatted_data.iloc[i]['Price Per Unit'])
        i += 1


# Set text of user displayed message
textUpdate = tk.StringVar()
textUpdate.set("Updates will be displayed here")

# used to keep track of how many licensed group orders we have
licensedGroupCounter = 0


# user must enter valid file of sales data to be formatted
def checkUserEntry(user_input):
    # if the users input is empty
    if not user_input:
        # set display message of GUI
        textUpdate.set("You did not enter any file. Please enter a file and retry.")
        print("User input is empty")

    # otherwise the user did input something
    else:
        # if it was a valid file path
        if os.path.isfile(user_input):
            textUpdate.set("Valid file. The formatted data should now be in your current working directory.")
            print("valid file, press Format Data button to format the order data")
            getAndFormat(user_input)
        # otherwise invalid file path
        else:
            textUpdate.set("userInput: %s is NOT a REAL file. Please retry." % user_input)
            print("\nuser_input: %s is NOT a REAL file\n" % user_input)


# checking if the order belongs to a licensed group or not
def checkIfLicensedGroup(groupName, df, index):
    licensedGroups = ["Acacia", "Alpha Chi Omega", "Alpha Chi Rho", "Alpha Delta Phi", "Alpha Delta Pi",
                      "Alpha Epsilon Phi",
                      "Alpha Epsilon Pi", "Alpha Eta Rho", "Alpha Gamma Delta", "Alpha Gamma Rho",
                      "alpha Kappa Delta Phi",
                      "Alpha Kappa Lambda", "Alpha Kappa Psi", "Alpha Omega Epsilon", "Alpha Omicron Pi", "Alpha Phi",
                      "Alpha Phi Omega", "Alpha Psi Lambda", "Alpha Sigma Alpha", "Alpha Sigma Phi", "Alpha Sigma Tau",
                      "Alpha Tau Omega", "Alpha Xi Delta", "Appalachian State University",
                      "Austin Peay State University",
                      "Beta Chi Theta", "Beta Theta Pi", "California Baptist University", "Chi Omega", "Chi Phi",
                      "Chi Psi",
                      "Chi Sigma Tau", "Chi Upsilon Sigma", "Circle of Sisterhood Foundation", "Delta Chi",
                      "Delta Delta Delta",
                      "Delta Epsilon Psi", "Delta Gamma", "Delta Kappa Alpha", "Delta Kappa Delta",
                      "Delta Kappa Epsilon",
                      "Delta Phi Epsilon", "Delta Phi Lambda", "Delta Sigma Phi", "Delta Sigma Pi", "Delta Tau Delta",
                      "Delta Upsilon", "Delta Zeta", "Epsilon Sigma Alpha", "FarmHouse", "Fort Hays State University",
                      "Furman University", "Gamma Alpha Omega", "Gamma Phi Beta", "Gamma Rho Lambda",
                      "Gamma Sigma Sigma",
                      "Gamma Zeta Alpha", "Georgia State University", "High Point University", "Iota Phi Theta",
                      "Kansas State"
                      "University", "Kappa Alpha Order", "Kappa Alpha Theta", "Kappa Beta Gamma", "Kappa Delta",
                      "Kappa Delta Chi",
                      "Kappa Delta Rho", "Kappa Kappa Gamma", "Kappa Kappa Psi", "Kappa Phi Lambda", "Kappa Psi",
                      "Kappa Sigma",
                      "Kent State University", "Kiwanis International", "Lamar University", "Lambda Alpha Upsilon",
                      "Lambda Chi"
                      "Alpha", "Lambda Kappa Sigma", "Lambda Phi Epsilon", "Lambda Pi Upsilon", "Lambda Sigma Upsilon",
                      "Lambda Theta Alpha", "Lambda Theta Phi", "Moms RUN This Town", "Mortar Board", "Mu Phi Epsilon",
                      "Mu Sigma Upsilon", "National Charity League", "National English Honor Society", "National Junior"
                                                                                                       "College Athletic Association",
                      "National Panhellenic Conference", "North American Interfraternity"
                                                         "Conference", "Omega Delta Phi", "Omega Phi Alpha",
                      "Omega Phi Chi", "Order of Omega", "Phi Alpha Delta",
                      "Phi Beta Sigma", "Phi Chi Theta", "Phi Delta Epsilon", "Phi Delta Theta", "Phi Gamma Delta",
                      "Phi Kappa Psi",
                      "Phi Kappa Sigma", "Phi Kappa Tau", "Phi Kappa Theta", "Phi Mu Delta", "Phi Sigma Kappa",
                      "Phi Sigma Pi",
                      "Phi Sigma Rho", "Phi Sigma Sigma", "Pi Alpha Phi", "Pi Beta Phi", "Pi Delta Psi",
                      "Pi Kappa Alpha",
                      "Pi Kappa Phi", "Pi Sigma Epsilon", "Psi Sigma Phi", "Psi Upsilon", "Red Hat Society",
                      "Sigma Alpha",
                      "Sigma Alpha Epsilon", "Sigma Alpha Iota", "Sigma Alpha Mu", "Sigma Beta Rho", "Sigma Chi",
                      "Sigma Delta Tau",
                      "Sigma Kappa", "Sigma Lambda Beta", "Sigma Lambda Gamma", "Sigma Nu", "Sigma Phi Delta",
                      "Sigma Phi Epsilon",
                      "Sigma Pi", "Sigma Psi Zeta", "Sigma Sigma Sigma", "Sigma Tau Delta", "Sigma Tau Gamma",
                      "Tau Beta Sigma",
                      "Tau Epsilon Phi", "Tau Kappa Epsilon", "The National Society of Collegiate Scholars",
                      "The University"
                      "of New Mexico", "The University of Tulsa", "Theta Chi", "Theta Phi Alpha", "Theta Tau",
                      "Theta Xi", "Triangle",
                      "Troy University", "University of Hawaii", "University of North Texas",
                      "University of South Carolina"
                      "Upstate", "Winthrop University", "Zeta Beta Tau", "Zeta Psi", "Zeta Tau Alpha",
                      "Zeta Tau Alpha Foundation"]

    # Licensed group flag. 0 means not licensed. 1 means licensed.
    flag = 0
    length = len(licensedGroups)

    i = 0
    while i < length:
        # if group is found to be licensed then set flag to 1
        if licensedGroups[i].lower() == groupName.lower():
            global licensedGroupCounter
            licensedGroupCounter += 1
            flag = 1
            #print("\nLicensedGroup: %s\nGroupName: %s\n" % (licensedGroups[i], groupName))
            break

        i += 1

    if flag == 0:
        df['Licensed_Or_Not'].values[index] = "No"

    if flag == 1:
        df['Licensed_Or_Not'].values[index] = "Yes"

# Create GUI
canvas = tk.Canvas(root, height=1000, width=1000, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="gray", bd=10)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# when pressed sales data to user specified file path will be formatted
checkEntryButton = tk.Button(frame, text="Enter File Name", padx=10, pady=10, fg="black", bg="#263D42",
                             command=lambda: checkUserEntry(fileNameEntry.get()))
checkEntryButton.place(relx=0.7, relheight=1, relwidth=0.3)

# Entry for filepath to sales data
fileNameEntry = tk.Entry(frame, font=20, bg="white")
fileNameEntry.place(relwidth=0.65, relheight=1)

lower_frame = tk.Frame(root, bg='black', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.2, anchor='n')

formatDataUpdate = tk.Label(lower_frame, textvariable=textUpdate)
formatDataUpdate.place(relwidth=1, relheight=1)

root.mainloop()
