from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import pandas as pd
import random
import os

# Flask app and bootstrap
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)


def decks():
    # read in the Excel file
    excel_file = pd.ExcelFile('data/data_norma_NTC.xlsx')  # Download Excel file then add path

    # create an empty dictionary to hold the dataframes
    dfs = {}

    # loop through each sheet in the Excel file
    for sheet_name in excel_file.sheet_names:
        # create a dataframe for the sheet
        df = excel_file.parse(sheet_name)
        # add the dataframe to the dictionary using the sheet name as the key
        dfs[sheet_name] = df

# Deck for each sheet
    system_deck = dfs['Términos Relativos al Sistema']
    require_deck = dfs['Términos Relativos a los Requis']
    auditory_deck = dfs['Términos Relativos a la Auditor']
    deck_list = [system_deck, require_deck, auditory_deck]
    return deck_list


decks_list = decks()


# Function for success or failure
def drop_card(deck, term):  # takes as parameter the dataframe for each sheet
    deck.drop(deck.loc[deck['Término'] == term].index, inplace=True)
    deck.reset_index(drop=True, inplace=True)


def game(deck, name, route, req_method, guess, index):
    if len(deck) == 0:
        return render_template('congratz.html')
    if req_method == 'POST':
        if guess == 'correct':
            drop_card(deck, deck['Término'][index])
            return redirect(url_for(name))
        else:
            return redirect(url_for(name))
    elif req_method is None:
        rand_num = random.randint(0, len(deck['Término']) - 1)
        return render_template(f'{name}.html', card_info=deck, index=rand_num, route=route)


@app.route('/', methods=['GET'])
def home():
    global decks_list
    decks_list = decks()
    return render_template('index.html')


@app.route('/terminos-relativos-al-sistema', methods=['GET', 'POST'])
def sistema():
    global decks_list
    method = request.args.get('method')
    guess = request.args.get('guess')
    index = request.args.get('index')
    if index is not None:
        index = int(index)
    # Run game
    return game(decks_list[0],
                'sistema',
                route='/terminos-relativos-al-sistema',
                req_method=method,
                guess=guess,
                index=index)


@app.route('/terminos-relativos-a-los-requisitos', methods=['GET', 'POST'])
def requisitos():
    global decks_list
    method = request.args.get('method')
    guess = request.args.get('guess')
    index = request.args.get('index')
    if index is not None:
        index = int(index)
    # Run game
    return game(decks_list[1],
                'requisitos',
                route='/terminos-relativos-a-los-requisitos',
                req_method=method,
                guess=guess,
                index=index)


@app.route('/terminos-relativos-a-la-auditoria', methods=['GET', 'POST'])
def auditoria():
    global decks_list
    method = request.args.get('method')
    guess = request.args.get('guess')
    index = request.args.get('index')
    if index is not None:
        index = int(index)
    # Run game
    return game(decks_list[2],
                'auditoria',
                route='/terminos-relativos-a-la-auditoria',
                req_method=method,
                guess=guess,
                index=index)


if __name__ == '__main__':
    app.run(debug=True)


