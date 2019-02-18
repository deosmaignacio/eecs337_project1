'''Version 0.2'''

import json
import nltk
import re
import itertools
import sys
from heapq import nlargest
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from difflib import SequenceMatcher




OFFICIAL_AWARDS_1315 = ['cecil b. demille award',
                        'best motion picture - drama',
                        'best performance by an actress in a motion picture - drama',
                        'best performance by an actor in a motion picture - drama',
                        'best motion picture - comedy or musical',
                        'best performance by an actress in a motion picture - comedy or musical',
                        'best performance by an actor in a motion picture - comedy or musical',
                        'best animated feature film', 'best foreign language film',
                        'best performance by an actress in a supporting role in a motion picture',
                        'best performance by an actor in a supporting role in a motion picture',
                        'best director - motion picture',
                        'best screenplay - motion picture',
                        'best original score - motion picture',
                        'best original song - motion picture',
                        'best television series - drama',
                        'best performance by an actress in a television series - drama',
                        'best performance by an actor in a television series - drama',
                        'best television series - comedy or musical',
                        'best performance by an actress in a television series - comedy or musical',
                        'best performance by an actor in a television series - comedy or musical',
                        'best mini-series or motion picture made for television',
                        'best performance by an actress in a mini-series or motion picture made for television',
                        'best performance by an actor in a mini-series or motion picture made for television',
                        'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                        'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama',
                        'best motion picture - musical or comedy',
                        'best performance by an actress in a motion picture - drama',
                        'best performance by an actor in a motion picture - drama',
                        'best performance by an actress in a motion picture - musical or comedy',
                        'best performance by an actor in a motion picture - musical or comedy',
                        'best performance by an actress in a supporting role in any motion picture',
                        'best performance by an actor in a supporting role in any motion picture',
                        'best director - motion picture',
                        'best screenplay - motion picture',
                        'best motion picture - animated',
                        'best motion picture - foreign language',
                        'best original score - motion picture',
                        'best original song - motion picture',
                        'best television series - drama',
                        'best television series - musical or comedy',
                        'best television limited series or motion picture made for television',
                        'best performance by an actress in a limited series or a motion picture made for television',
                        'best performance by an actor in a limited series or a motion picture made for television',
                        'best performance by an actress in a television series - drama',
                        'best performance by an actor in a television series - drama',
                        'best performance by an actress in a television series - musical or comedy',
                        'best performance by an actor in a television series - musical or comedy',
                        'best performance by an actress in a supporting role in a series, limited series or motion picture made for television',
                        'best performance by an actor in a supporting role in a series, limited series or motion picture made for television',
                        'cecil b. demille award']

currWinners = {}

# Finds either a single host or 2 hosts (cohosts) in a list of strings
def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    string = 'gg' + str(year) + '.json'
    parse = parsing(string)

    corpus = parse

    hostMentions = {}

    for tweet in corpus:
        if 'monologue' in tweet:
            word = ""
            for w in tweet:
                word += w + " "
            regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", word)

            for match in regex_match:
                if not match in hostMentions:
                    hostMentions[match] = 1
                else:
                    num = hostMentions.get(match)
                    num = num + 1
                    update = {match : num}
                    hostMentions.update(update)
    hosts = nlargest(2, hostMentions, key=hostMentions.get)
    freq1 = hostMentions.get(hosts[0])
    freq2 = hostMentions.get(hosts[1])

    if freq2 / (freq1 + freq2) > .3:
        return hosts
    else:
        return [hosts[0]]

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here

    end_words = ['Drama', 'Musical', 'Film', 'Television', 'Motion Picture']
    key_words = end_words + ['performance', 'comedy', 'series', 'role', 'Performance', 'Comedy', 'Series', 'Role']

    # Parsing

    string = 'gg' + str(year) + '.json'

    try:
        with open(string) as data_file:
            data = json.load(data_file)
    except:
        pass

    #stop_words = stopwords.words('english')
    stop_words =['The', 'Variety', 'This', 'Globe', 'RT', 'CNNshowbiz', 'http', 'Golden', 'Globes', 'GoldenGlobes', 'Goldenglobes', 'Goldenglobe', 'gg','golden globes', 'golden globe', 'goldenglobe','goldenglobes','gg2015','gg15','goldenglobe2015','goldenglobe15','goldenglobes2015','goldenglobes15', 'gg2013','gg13','goldenglobe2013','goldenglobe13','goldenglobes2013','goldenglobes13', 'rt', '2013', '2015' ]

    tknzr = RegexpTokenizer(r'\w+')

    word_list = []
    word_dic = {}

    for tweet in data:
        text = tweet['text']
        id = tweet['id']

        word_list.append((text,id))

    corpus = word_list

    # End of Parsing

    prev_ID = 1
    temp_awards = {}
    count = 0
    for tweet in corpus:
        for endWord in end_words:
            # Extract the segment between 'Best' and one of the end_words
            match = re.search(r'(?<=\sBest).*(?='+ endWord +')', tweet[0], re.IGNORECASE)
            if match:
                award = 'Best'+ match.group(0) + endWord

                # Remove duplicate segments from the same teweet
                if prev_ID == tweet[1]:
                    continue
                prev_ID = tweet[1]

                # Remove stopwords from the segment
                words = tknzr.tokenize(award)
                for w in words:
                    if w in stop_words:
                        award = award.replace(w, '')

                if (len(words) >= 4) :
                    if endWord not in temp_awards:
                        temp_awards[endWord] = [award]
                    else:
                        temp_awards[endWord].append(award)
                    count = count + 1

    result = []
    for k in temp_awards:
        dic = {}
        p = 0
        while p < len(temp_awards[k]):
            tweet = temp_awards[k][p]
            if tweet in dic:
                dic[tweet] = dic[tweet] + 1
            else:
                dic[tweet] = 1
            p = p+1

        dic_list= sorted(dic.items(), key=lambda x:x[1], reverse = True)
        #stackoverflow.com/questions/16772071/sort-dic-by-value-python

        # dic_list is acutally a list of tuple!!!!!
        dic_list = dic_list[:15]
        # (dic)
        # ('\n\n')

        award_list = []

        for item in dic_list:
            award_list.append(item[0])


        # (award_list)

        remove_list = []

        i = 0
        for tweet1 in award_list:
            j = i + 1

            while j < len(award_list):
                tweet2 = award_list[j]
                sim = SequenceMatcher(None, tweet1, tweet2).ratio()

                if sim > 0.85 and (('actor' not in tweet1 and 'actor' not in tweet2) or ('actress' not in tweet2 and 'actress' not in tweet1)):
                    if (dic[tweet1] > dic[tweet2]):
                        #award_list.remove(tweet2)
                        remove_list.append(tweet2)
                    else:
                        #award_list.remove(tweet1)
                        remove_list.append(tweet1)

                j = j + 1
            i = i + 1

        remove_list = set(remove_list)
        for tweet in award_list:
            if tweet in remove_list:
                award_list.remove(tweet)


        # (award_list)
        # ('\n\n')
        result.append(award_list)

    result[0] = result[0][:6]
    result[1] = result[1][:6]
    result[2] = result[2][:5]
    result[3] = result[3][:6]
    result[4] = result[4][:2]

    awards = []
    for i in result:
        for j in i:
            (j.lower())
            awards.append(j.lower())

    # (sorted(sim_dic.items(), key=lambda x:x[1], reverse = True))
    # (count)
    #awards = sorted(sim_dic, key = sim_dic.get, reverse = True)

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = {}

    #Need to make new condensed awards list


    award_stopList = ['drama', '-', 'by', 'an', 'a', 'in', 'made', 'for', 'role', 'or', 'b.', 'series,', 'performance', 'best']

    personName = {}

    string = 'gg' + str(year) + '.json'
    try:
        parse = parsing(string)
    except:
        pass

    corpus = parse
    if year == 2013 or year == 2015:
        real_awards = OFFICIAL_AWARDS_1315
    else:
        real_awards = OFFICIAL_AWARDS_1819

    tknzr = RegexpTokenizer(r'\w+')
    award_words = ['cecil', 'TV', 'Cecil', 'award', 'Award', 'Movie', 'movie', 'best', 'motion picture', 'drama', 'performance', 'actress', 'actor', 'comedy', 'feature', 'film', 'foreign', 'language', 'musical', 'animated', 'supporting', 'role', 'director', 'screenplay', 'original', 'score', 'song', 'television', 'series', 'mini-series', 'miniseries', 'Best', 'Motion', 'picture', 'motion', 'Picture', 'Drama', 'Performance', 'Actress', 'Actor', 'Comedy', 'Feature', 'Film', 'Foreign', 'Language', 'Musical', 'Animated', 'Supporting', 'Role', 'Director', 'Screenplay', 'Original', 'Score', 'Song', 'Television', 'Series', 'Mini-series', 'Miniseries']
    nominee = ['nominee', 'nominees', 'Nominees', 'Nominee']
    filteredTweets = []
    filteredTweetsTV = []
    TVtweets = ['TV']
    debug = ['best', 'performance', 'actor', 'drama']
    award_stopwords = ['by', 'an', 'in', 'a', 'or', 'made', 'for', 'best']
    for tweet in corpus:
        if len(set(award_words).intersection(set(tweet))) >= 2:
            if len(set(nominee).intersection(set(tweet))) >= 0:
                index = 0
                try:
                    index = 0 #tweet.index('for')
                except:
                    index = 0
                if index > 0:
                    tweet = tweet[0:index]
                # (tweet)
                filteredTweets.append(tweet)
                if len(set(TVtweets).intersection(set(tweet))) >= 1:
                    filteredTweetsTV.append(tweet)

    peopleAwards = ['director', 'actor', 'actress', 'cecil', 'Director', 'Actor', 'Actress', 'Cecil']
    TvAwards = ['TV']
    ignore = ['Supporting', 'Actress', 'Actor', 'Series', 'Nshowbiz', 'Best', 'Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    count = 0
    for award in real_awards:
        personName = {}
        award_parse = award.split(' ')
        for stop in award_stopList:
            while stop in award_parse:
                award_parse.remove(stop)
        if 'television' in award_parse:
            award_parse.remove('television')
            award_parse.append('TV')
        if 'mini-series' in award_parse:
            award_parse.remove('mini-series')
            award_parse.append('series')
        if len(award_parse) >=5:
            while 'motion' in award_parse:
                award_parse.remove('motion')
            while 'picture' in award_parse:
                award_parse.remove('picture')

        key = len(award_parse)
        if len(set(peopleAwards).intersection(set(award_parse))) >= 1:
            for tweet in filteredTweets:
                if 'TV' in award_parse and 'TV' not in tweet:
                    continue
                if 'TV' not in award_parse and 'TV' in tweet:
                    continue
                if 'actor' in award_parse and 'actor' not in tweet:
                    continue
                if 'actress' in award_parse and 'actress' not in tweet:
                    continue
                if 'supporting' in award_parse and 'supporting' not in tweet:
                    continue
                if 'supporting' not in award_parse and 'supporting' in tweet:
                    continue
                if 'director' in award_parse and 'director' not in tweet:
                    continue
                if len(set(award_parse).intersection(set(tweet))) >= key - 1:
                    tweetText = ""
                    for w in tweet:
                        tweetText += w + " "
                    # (tweetText)
                    if award == '':
                         (tweetText)

                    regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", tweetText)

                    for match in regex_match:
                        if match not in ignore:
                            if not match in personName:
                                personName[match] = 1
                            else:
                                num = personName.get(match)
                                num = num + 1
                                update = {match : num}
                                personName.update(update)
            nomineeName = nlargest(5, personName, key=personName.get)
            nominees[real_awards[count]] = nomineeName
        else:
            for tweet in filteredTweets:
                if 'TV' in award_parse and 'TV' not in tweet:
                    continue
                if 'TV' not in award_parse and 'TV' in tweet:
                    continue
                if 'score' in award_parse and 'score' not in tweet:
                    continue
                if 'screenplay' in award_parse and 'screenplay' not in tweet:
                    continue
                if len(set(award_parse).intersection(set(tweet))) >= key - 1:
                    #tweet[:] = [x for x in tweet if x not in ignore]
                    tweetText = ""
                    for w in tweet:
                        tweetText += w + " "


                    regex_match = re.findall("[A-Z][a-z]*", tweetText)

                    for match in regex_match:
                        if match not in ignore:
                            if not match in personName:
                                personName[match] = 1
                            else:
                                num = personName.get(match)
                                num = num + 1
                                update = {match : num}
                                personName.update(update)

                    regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", tweetText)

                    for match in regex_match:
                        if match not in ignore:
                            if not match in personName:
                                personName[match] = 1
                            else:
                                num = personName.get(match)
                                num = num + 1.1
                                update = {match : num}
                                personName.update(update)
            nomineeName = nlargest(5, personName, key=personName.get)
            (nomineeName)
            (real_awards[count])
            nominees[real_awards[count]] = nomineeName
        count = count + 1
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    ##Going to try individually for awards, hard to generalize
    winners = {}

    #Need to make new condensed awards list

    condenseAwards = ['cecil demille award',
                        'best motion picture drama',
                        'best performace actress drama',
                        'best performace actor drama',
                        'best motion picture comedy musical',
                        'actress comedy musical performance',
                        'actor comedy musical performace',
                        'animated feature film',
                        'foreign language film',
                        'supporting actress best',
                        'best supporting actor',
                        'best director',
                        'best screenplay',
                        'best score',
                        'best original song',
                        'best TV series',
                        'actress TV series',
                        'actor TV series',
                        'TV series comedy musical',
                        'actress TV mucial comedy',
                        'actor TV musical comedy',
                        'TV mini series picture',
                        'actress mini picture TV',
                        'actor mini picture TV',
                        'actress supporting TV series',
                        'actor supporting TV series']

    award_stopList = ['drama', '-', 'by', 'an', 'a', 'in', 'made', 'for', 'role', 'or', 'b.', 'series,', 'performance', 'best']

    personName = {}

    string = 'gg' + str(year) + '.json'
    try:
        parse = parsing(string)
    except:
        pass

    corpus = parse
    if year == 2013 or year == 2015:
        real_awards = OFFICIAL_AWARDS_1315
    else:
        real_awards = OFFICIAL_AWARDS_1819
    tknzr = RegexpTokenizer(r'\w+')
    award_words = ['cecil', 'TV', 'Cecil', 'award', 'Award', 'Movie', 'movie', 'best', 'motion picture', 'drama', 'performance', 'actress', 'actor', 'comedy', 'feature', 'film', 'foreign', 'language', 'musical', 'animated', 'supporting', 'role', 'director', 'screenplay', 'original', 'score', 'song', 'television', 'series', 'mini-series', 'miniseries', 'Best', 'Motion', 'picture', 'motion', 'Picture', 'Drama', 'Performance', 'Actress', 'Actor', 'Comedy', 'Feature', 'Film', 'Foreign', 'Language', 'Musical', 'Animated', 'Supporting', 'Role', 'Director', 'Screenplay', 'Original', 'Score', 'Song', 'Television', 'Series', 'Mini-series', 'Miniseries']
    nominee = ['nominee', 'nominees', 'Nominees', 'Nominee']
    filteredTweets = []
    filteredTweetsTV = []
    TVtweets = ['TV']
    debug = ['best', 'performance', 'actor', 'drama']
    award_stopwords = ['by', 'an', 'in', 'a', 'or', 'made', 'for', 'best']
    for tweet in corpus:
        if len(set(award_words).intersection(set(tweet))) >= 2:
            #Not using this part yet
            if len(set(nominee).intersection(set(tweet))) >= 0:
                index = 0
                try:
                    index = 0 #tweet.index('for')
                except:
                    index = 0
                if index > 0:
                    tweet = tweet[0:index]
                # (tweet)
                filteredTweets.append(tweet)
                if len(set(TVtweets).intersection(set(tweet))) >= 1:
                    filteredTweetsTV.append(tweet)




    peopleAwards = ['director', 'actor', 'actress', 'cecil', 'Director', 'Actor', 'Actress', 'Cecil']
    TvAwards = ['TV']
    ignore = ['Supporting', 'Actress', 'Actor', 'Series', 'Nshowbiz', 'Best', 'Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    #award_words.extend(ignore)
    count = 0
    for award in real_awards:
        personName = {}
        award_parse = award.split(' ')
        for stop in award_stopList:
            while stop in award_parse:
                award_parse.remove(stop)
        if 'television' in award_parse:
            award_parse.remove('television')
            award_parse.append('TV')
        if 'mini-series' in award_parse:
            award_parse.remove('mini-series')
            award_parse.append('series')
        if len(award_parse) >=5:
            while 'motion' in award_parse:
                award_parse.remove('motion')
            while 'picture' in award_parse:
                award_parse.remove('picture')

        # (award_parse)
        key = len(award_parse)
        if len(set(peopleAwards).intersection(set(award_parse))) >= 1:
            for tweet in filteredTweets:
                if 'TV' in award_parse and 'TV' not in tweet:
                    continue
                if 'TV' not in award_parse and 'TV' in tweet:
                    continue
                if 'actor' in award_parse and 'actor' not in tweet:
                    continue
                if 'actress' in award_parse and 'actress' not in tweet:
                    continue
                if 'supporting' in award_parse and 'supporting' not in tweet:
                    continue
                if 'supporting' not in award_parse and 'supporting' in tweet:
                    continue
                if 'director' in award_parse and 'director' not in tweet:
                    continue
                if len(set(award_parse).intersection(set(tweet))) >= key - 1:
                    #(award_parse)
                    #tweet[:] = [x for x in tweet if x not in ignore]
                    tweetText = ""
                    for w in tweet:
                        tweetText += w + " "
                    # (tweetText)
                    if award == '':
                         (tweetText)


                    regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", tweetText)

                    for match in regex_match:
                        if match not in ignore:
                            if not match in personName:
                                personName[match] = 1
                            else:
                                num = personName.get(match)
                                num = num + 1
                                update = {match : num}
                                personName.update(update)
            awardWinner = nlargest(1, personName, key=personName.get)
            (awardWinner)
            (real_awards[count])
            winners[real_awards[count]] = awardWinner[0]
        else:
            for tweet in filteredTweets:
                if 'TV' in award_parse and 'TV' not in tweet:
                    continue
                if 'TV' not in award_parse and 'TV' in tweet:
                    continue
                if 'score' in award_parse and 'score' not in tweet:
                    continue
                if 'screenplay' in award_parse and 'screenplay' not in tweet:
                    continue
                if len(set(award_parse).intersection(set(tweet))) >= key - 1:
                    #(award_parse)
                    #tweet[:] = [x for x in tweet if x not in ignore]
                    tweetText = ""
                    for w in tweet:
                        tweetText += w + " "
                    # (tweetText)


                    regex_match = re.findall("[A-Z][a-z]*", tweetText)

                    for match in regex_match:
                        if match not in ignore:
                            if not match in personName:
                                personName[match] = 1
                            else:
                                num = personName.get(match)
                                num = num + 1
                                update = {match : num}
                                personName.update(update)

                    regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", tweetText)

                    for match in regex_match:
                        if match not in ignore:
                            if not match in personName:
                                personName[match] = 1
                            else:
                                num = personName.get(match)
                                num = num + 1.1
                                update = {match : num}
                                personName.update(update)
            awardWinner = nlargest(1, personName, key=personName.get)
            (awardWinner)
            (real_awards[count])
            try:
                winners[real_awards[count]] = awardWinner[0]
            except:
                winners[real_awards[count]] = ""
        count = count + 1

    currWinners = winners
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    string = 'gg' + str(year) + '.json'
    parse = parsing(string)
    corpus = parse

    presenters = {}
    triggerWords = ['present', 'presented', 'presenters', 'Present', 'Presented', 'Presenters', 'presenting', 'Presenting', 'awarded', 'Awarded']
    unwantedWords = ['congrats', 'yeah', 'wow', 'why', 'win', 'present', 'award']
    awardList = []
    winners = currWinners
    winnerFilms = []

    if year in [2013, 2015]:
        awardList = OFFICIAL_AWARDS_1315
    elif year in [2018, 2019]:
        awardList = OFFICIAL_AWARDS_1819

    for award in awardList:
        presenters[award] = []

    for award, winner in winners.items():
        if award not in ['performance', 'cecil', 'director', 'screenplay']:
            winnerFilms.append(winner)

    for entry in corpus:
        if any(triggerWord in entry for triggerWord in triggerWords) and 'represent' not in entry and ('best' in entry or 'Best' in entry or 'cecil' in entry or 'Cecil' in entry):
            hostName = ""
            award = ""
            awardGuesses = []
            entryListIndex = 0
            while entryListIndex < len(entry):
                word = entry[entryListIndex]
                if word.lower() in ["best"]:
                    currAwardGuess = "best"
                    while True:
                        entryListIndex += 1
                        if entryListIndex < len(entry):
                            currAwardGuess = (entry[entryListIndex]).lower()
                            # for TV awards, must replacae "tv" for "television" in order for this to work
                            if currAwardGuess in ["tv"]:
                                currAwardGuess = "television"
                                entry[entryListIndex] = "television"
                            tempAwardGuesses = [currAward for awardIndex, currAward in enumerate(awardList) if currAwardGuess in currAward]
                            awardGuesses += tempAwardGuesses
                            if len(tempAwardGuesses) == 0:
                                entryListIndex = entryListIndex - 1
                                break
                        else:
                            break
                elif word[0].isupper() and word[1:].islower(): # this would be place to correct "Sacha Baron Cohen Tarantino"
                    hostName += word + " "
                elif word in ["and", "And", "&"]:
                    hostName += "and "
                entryListIndex += 1

            if len(awardGuesses) > 0:
                data = Counter(awardGuesses)
                award = max(awardGuesses, key=data.get)
                if award in awardList:
                    presenters[award] = presenters[award] + [hostName]

    for award, guesses in presenters.items():
        newGuesses = []
        for guess in guesses:
            splitGuess = (guess.lower()).split()
            try:
                winner = (winners[award]).split()
            except:
                winner = []
            matches = list(set(splitGuess).intersection(set(winner)))
            if len(matches) > 0:
                for match in matches:
                    toRemove = difflib.get_close_matches(match, guess.split())
                    for removeWord in toRemove:
                        guess = (guess.replace(removeWord, '')).strip()

            splitGuess = guess.split()
            # a bit more processing, more specific and somewhat case based
            # 1. Make sure no movie name is in guesses
            for film in winnerFilms:
                filmLower = film.lower()
                guessLower = guess.lower()
                if filmLower in guessLower:
                    filmIndex = guessLower.index(filmLower)
                    guess = guess[0:filmIndex] + guess[(filmIndex + len(filmLower)):]
                    splitGuess = guess.split()
            # 2. Remove entries with unwanted words
            for unwantedWord in unwantedWords:
                lowerGuess = guess.lower()
                if unwantedWord in lowerGuess:
                    wordIndex = lowerGuess.index(unwantedWord)
                    guess = guess[0:wordIndex] + guess[(wordIndex + len(unwantedWord)):]
            # 3. If we have an 'and' in our guess, then we must have two presenters
            if "and" in splitGuess: # 2 presenters so want 5 words [firstName lastName and firstName lastName]
                andIndex = guess.index("and")
                guess = guess[0:andIndex] + guess[(andIndex + 3):]
            # 4. If we don't have an and but we have two names, then we need to insert an and
            elif len(splitGuess) == 4: # then we need an "and" inserted, since we have two names (double-checking this):
                checker = True  # making sure all words are actually names
                for firstLastName in splitGuess:
                    if firstLastName[0].islower():
                        checker = False
                        break
                if checker:
                    guess = str(splitGuess[0]).strip() + " " + str(splitGuess[1]).strip() + " and " + str(splitGuess[2]).strip() + " " + str(splitGuess[3]).strip()
            # 5. Remove all 2-character words
            splitGuess = guess.split()
            wordNumber = 0
            while wordNumber < len(splitGuess):
                word = splitGuess[wordNumber]
                if len(word) < 3:
                    wordIndex = guess.index(word)
                    guess = guess[0:wordIndex] + guess[(wordIndex + len(word)):]
                    splitGuess = guess.split()
                    wordNumber = 0
                else:
                    wordNumber+= 1

            if len(guess.split()) > 1:
                newGuesses.append(guess.strip())
        presenters[award] = newGuesses

        # How to decide between options that survived all of the above? So awards with more than one presenter guess
        numberOfGuesses = len(newGuesses)
        # if we have 0 or 1 guess, do nothing
        moreCheckNeeded = False # used if a guess enters the two following if statements but needs more processing
        if numberOfGuesses == 1:
            presenters[award] = newGuesses[0]
        if numberOfGuesses == 2:
            firstGuess = newGuesses[0]
            secondGuess = newGuesses[1]
            # There are two presenters for this award, so see if we have structure of firstName lastName and firstName lastName in one of them but not in another
            # Logic here is that if we have one entry with structure firstName and another with firstName lastName and firstName lastName, since we can have two Presenters
            # but can't have two winners (in fact, must have only one winner), then one is winner and the other is presenters
            if len(firstGuess.split()) == 5 and 'and' in firstGuess and len(secondGuess.split()) < 5:
                presenters[award] = firstGuess
            elif len(secondGuess.split()) == 5 and 'and' in secondGuess and len(firstGuess.split()) < 5:
                presenters[award] = secondGuess
            else:
                moreCheckNeeded = True
        # if more than two options, then unclear if we have one or two presenters
        # Finally, find the most common pair of consecutive words
        # Structure (firstName lastName, frequency, index)
        # We then check if the two most frequent entries have similar freqs and if they occur many times on same index
        if numberOfGuesses > 2 or moreCheckNeeded:
            structArray = []
            namesArray = []
            # if type(newGuesses) is not  list:
            #     newGuesses = [newGuesses]
            for guessIndex in range(len(newGuesses)):
                guessContents = (newGuesses[guessIndex]).split()
                if len(guessContents) > 1:
                    for wordIndex in range(len(guessContents) - 1):
                        word1 = (guessContents[wordIndex]).strip()
                        word2 = (guessContents[wordIndex + 1]).strip()
                        if 'and' not in [word1, word2]:
                            completeName = str(word1) + " " + str(word2)
                            if completeName not in namesArray:
                                nameStruct = (completeName, 1, guessIndex)
                                structArray.append(nameStruct)
                                namesArray.append(completeName)
                            elif completeName in namesArray:
                                nameIndex = namesArray.index(completeName)
                                name, freq, index = structArray[nameIndex]
                                newNameStruct = (name, freq + 1, index)
                                structArray[nameIndex] = newNameStruct

            # Now, find two most common entries (structs)
            # If similar freqs (within similarityTolerance % of each other) then we have 2 presenters
            structArray.sort(key=lambda tup: tup[1], reverse=True)
            maxFreq = structArray[0][1]
            maxStruct = structArray[0]
            secondMaxStruct = structArray[0]
            structIndex = 0
            while structIndex < len(structArray):
                secondMaxStructNames = (structArray[structIndex][0]).split()
                if len(secondMaxStructNames) == 1:
                    if secondMaxStructNames[0] in maxStruct[0]:
                        structIndex += 1
                    else:
                        secondMaxStruct = structArray[structIndex]
                        break
                elif len(secondMaxStructNames) > 1:
                    firstName = secondMaxStructNames[0]
                    if firstName in maxStruct[0]:
                        structIndex += 1
                    else:
                        secondMaxStruct = structArray[structIndex]
                        break

            secondMaxFreq = secondMaxStruct[1]
            name1, freq1, index1 = maxStruct
            similarityTolerance = 0.90
            if year == 2013:
                similarityTolerance = 0.70
            if secondMaxFreq > (similarityTolerance * maxFreq):
                name2, freq2, index2 = secondMaxStruct
                presenters[award] = name1.strip() + " and " + name2.strip()
            else:
                presenters[award] = name1.strip()

    return presenters

def get_bestDressed(year):
    '''Best Dressed is list of a strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here

    string = 'gg' + str(year) + '.json'
    try:
        parse = parsing(string)
    except:
        pass

    corpus = parse

    bestDressed = {}

    keys = ['best', 'dressed', 'Best', 'Dressed', 'Red', 'Carpet', 'red', 'carpet', 'amazing', 'Amazing', 'dress', 'Dress', 'stunning', 'Stunning']

    for tweet in corpus:
        if len(set(tweet).intersection(set(keys))) >= 4:
            # (tweet)
            word = ""
            tweet[:] = [x for x in tweet if x not in keys]
            for w in tweet:
                word += w + " "
            regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", word)

            for match in regex_match:
                if not match in bestDressed:
                    bestDressed[match] = 1
                else:
                    num = bestDressed.get(match)
                    num = num + 1
                    update = {match : num}
                    bestDressed.update(update)
    person = nlargest(1, bestDressed, key=bestDressed.get)
    # (bestDressed)

    return person

def get_worstDressed(year):
    '''Best Dressed is list of a strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here

    string = 'gg' + str(year) + '.json'
    try:
        parse = parsing(string)
    except:
        pass

    corpus = parse

    worstDressed = {}

    keys = ['ugly', 'dress']

    for tweet in corpus:
        if len(set(tweet).intersection(set(keys))) >= 2:
            # (tweet)
            word = ""
            tweet[:] = [x for x in tweet if x not in keys]
            for w in tweet:
                word += w + " "
            regex_match = re.findall("[A-Z][a-z]* [A-Z][a-z]*", word)

            for match in regex_match:
                if not match in worstDressed:
                    worstDressed[match] = 1
                else:
                    num = worstDressed.get(match)
                    num = num + 1
                    update = {match : num}
                    worstDressed.update(update)
    person = nlargest(1, worstDressed, key=worstDressed.get)
    # (worstDressed)

    return person

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    year = int(list(sys.argv)[1])

    # Hosts
    print("Hosts: ")
    hosts = get_hosts(year)
    for hostIndex in range(len(hosts)):
        if hostIndex == len(hosts) - 1:
            print(hosts[hostIndex])
        else:
            print(hosts[hostIndex] + ", ")
    print('\n')

    # Awards
    print("Awards: ")
    awards = get_awards(year)
    for award in awards:
        print(award)
    print('\n')

    # Nominees
    print("Nominees: ")
    nominees = get_nominees(year)
    for award, names in nominees.items():
        print('\n')
        print(award + ": ")
        for nameIndex in range(len(names)):
            if nameIndex == len(names) - 1:
                print(names[nameIndex])
            else:
                print(names[nameIndex] + ", ")
    print('\n')

    # Winners
    print("Winners: ")
    winners = get_winner(year)
    for award, name in winners.items():
        print(award + ": " + name)
    print('\n')

    # Presenters
    print("Presenters: ")
    presenters = get_presenters(year)
    for award, presenter in presenters.items():
        print(str(award) + ": " + str(presenter))
    print('\n')

    # Best Dressed
    bestDressed = get_bestDressed(year)
    print("Best Dressed: " + bestDressed[0])
    print('\n')

    # Worst Dressed
    worstDressed = get_worstDressed(year)
    print("Worst Dressed: " + worstDressed[0])
    print('\n')

    return

def parsing(filename):
    with open(filename) as data_file:
        data = json.load(data_file)

    #If you want to remove stop words, do so inside the function call
    #stop_words = stopwords.words('english')
    stop_words =['The', 'Variety', 'This', 'Globe', 'RT', 'CNNshowbiz', 'http', 'Golden', 'Globes', 'GoldenGlobes', 'gg','golden globes', 'golden globe', 'goldenglobe','goldenglobes','gg2015','gg15','goldenglobe2015','goldenglobe15','goldenglobes2015','goldenglobes15', 'gg2013','gg13','goldenglobe2013','goldenglobe13','goldenglobes2013','goldenglobes13', 'rt' ]
    #stop_words.extend(track)
    tknzr = RegexpTokenizer(r'\w+')

    word_list = []

    for tweet in data:
        text = tweet['text']
        words = tknzr.tokenize(text)
        tweetText = []
        for w in words:
            if w not in stop_words:
                tweetText.append(w)
        word_list.append(tweetText)
    return word_list

if __name__ == '__main__':
    main()
