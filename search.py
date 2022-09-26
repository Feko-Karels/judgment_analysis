from datetime import date
from itertools import count
import re
import os
import argparse
import logging

LISTE_DATEIEN = "all.txt"  #Bei Bedarf ändern in zB hits.txt

# zum benutzen der Suche Parameter -w String benuten
# Zum Beispiel
# $python search.py -w Volkswagen

#treffer werden in hits.txt gespeichert

# logging.basicConfig(level=logging.disable())  # <- deaktiviert
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

VERSION = "1.0"

counter_found = 0

counter_failed = 0

dateinamen_hit = []

def get_parser() -> argparse.ArgumentParser:
    """
    Create a command line parser.
    Returns:
        argparse.ArgumentParser: Created parser
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-w",
        "--word",
        type=str,
        required=False,
        help="the word to search for"
    )

    parser.add_argument(
        "-v",
        "--version",
        required=False,
        action="store_true",
        help="show the version"
    )

    return parser


def find_word(search_tearm: str):
    """
    Open a textfile and search for the given word.
    Show the number of words found.
    Show the total.
    Args:
        search_tearm:
            The word to search for
    """

    global counter_failed
    global counter_found
    global dateinamen_hit

    # It is good practice to use the with keyword when dealing with file objects.
    with open(FILE_NAME) as file_handle:

        try:
            for line in file_handle:
                line = line.rstrip()
                text_line = re.findall(
                    search_tearm + "[^ ]*", line  # <- define your regex here
                )

                for w in text_line:
                    found_words[w] = found_words.get(w, 0) + 1
                    logger.debug(found_words)
        except:
            counter_failed = counter_failed + 1 

    word_count = 0
    total = 0
    for word, count in found_words.items():
        print(f"Searched word: {word}\n Count: {count}")
        word_count += 1
        total += count
    
    if(total > 0):
        counter_found += 1
        dateinamen_hit.append(FILE_NAME)
        print("Total number: {0}".format(total))


def main():
    """
    Invoke the parser and evaluate the result.
    """
    parser = get_parser()
    args = parser.parse_args()

    if args.word:
        find_word(args.word)
    elif args.version:
        print(f"Koalitionsvertrag - Version: {VERSION}")
    else:
        parser.print_help()


if __name__ == "__main__":
    # Create an empty dict for the words found

    txt_name = LISTE_DATEIEN

    with open(txt_name) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    dateien = lines

    FILE_NAME = "Txts/BGH_Anwaltsenat_LE_2000-02-14_NA_AnwZB_9_99_NA_NA_0.txt"  # <- Enter your file here.

    for file in dateien:
        FILE_NAME = file    
        #print(FILE_NAME)
        found_words = dict()
        main()
    
    print("Anzahl Dateien mit Wort:")
    print(counter_found)
    print("Fahlerhafte Datein")
    print(counter_failed)
    #print("Dateinamen")
    #print(dateinamen_hit)

    with open('hits.txt', 'w') as temp_file:
        for item in dateinamen_hit:
            temp_file.write("%s\n" % item)
