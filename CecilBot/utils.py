from typing import List
from pathlib import Path
import re
import xlrd
# Open specified excel file and read data from file.
# Warning: when files are updated and their names get changed, you
#   must update the hard coded file name in DataBuilder.py
def dict_builder(path: Path):
    location = path
    name = path.name.replace(".xls", "")
    book = xlrd.open_workbook(location)
    sheet = book.sheet_by_index(0)
    sheet.cell_value(0, 0)
    data_dictionary = dict()

    for rownum in range(1, sheet.nrows):
        tempdict = dict()
        for cn, values in zip(sheet.row_values(0, 0), sheet.row_values(rownum, 0)):
            if values != "":
                tempdict[cn] = values
        if re.match(r".*Root Table.*", str(location), re.IGNORECASE):
            data_dictionary[str(sheet.cell_value(rownum, 0))] = tempdict
        else:
            data_dictionary[str(sheet.cell_value(rownum, 0)).lower()] = tempdict

    return {name: data_dictionary}

def build_mega_dict(paths: List[Path]):
    data = {}
    for excel_path in paths:
        d = dict_builder(excel_path)
        for k, v in d.items():
            data[k] = v
    return data


def generate_correction(orig_text: str, checklist: dict):

    WORDS = Counter(checklist.keys())

    def P(word, N=sum(WORDS.values())):
        return WORDS[word] / N

    def known(words):
        return {w for w in words if w in WORDS}

    def candidates(word):
        return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]

    def correction(word):
        "Most probably spelling correction for word"
        return max(candidates(word), key=P) or ""

    def edits1(word):
        "All edits that are one edit away from `word`"
        letters = "abcdefghijklmnopqrstuvwxyz"
        symbols = "-.0123456789 "
        letters += letters.upper() + symbols
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(word):
        return (e2 for e1 in edits1(word) for e2 in edits1(e1))

    return correction(orig_text)
