import os
import matplotlib.pyplot as plt
import sqlite3

def create_voting_pie_chart(total, voted):
    # Calculate the percentage of people who voted
    percent_voted = voted / total * 100
    percent_not_voted = 100 - percent_voted

    # Create a pie chart
    labels = ['Voted', 'Did not vote']
    sizes = [percent_voted, percent_not_voted]
    colors = ['#1f77b4', '#ff7f0e']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    # Save the pie chart as an image in the "static" directory
    directory = 'static'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, 'votechart.png')
    plt.savefig(filepath)



def get_voting_data():
    # Open a connection to the database
    conn = sqlite3.connect('./instance/usersdata.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Query the database to get the number of people who have voted
    numpplvoted = cursor.execute("SELECT COUNT(*) FROM userdata WHERE voted='Y'").fetchone()[0]
    print(numpplvoted)

    # Query the database to get the total number of people
    total_count = cursor.execute("SELECT COUNT(*) FROM userdata").fetchone()[0]

    # Create a pie chart with the voting data
    create_voting_pie_chart(total_count, numpplvoted)

    # Determine the number of people who have voted
    if numpplvoted == 0:
        pplvoted = "Voting hasn't started yet!"
    else:
        pplvoted = f"{numpplvoted} people have voted!"

    # Close the connection to the database
    conn.close()
    
    return pplvoted
def hello():
    return 0