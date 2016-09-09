# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:30:22 2016

@author: emmaflint
"""

import re

def expand_NUM(n):
    if len(n) > 0:
        if n[-1] == 's':
            if len(n) > 1 and n[-2:] == "'s":
                str = ''
                str += expand_NUM(n[:-2])
                str += "'s"
            else:
                str = ''
                if expand_NUM(n[:-1])[-1] == 'y':
                    str += expand_NUM(n[:-1])[:-1]
                    str += 'ies'
                else:
                    str += expand_NUM(n[:-1])
                    str += 's'
            return str
    
    if dec2_pattern.match(n):
        str2 = ''
        str2 += (expand_NUM(dec2_pattern.match(n).group(1)) + " " 
               + expand_NUM(dec2_pattern.match(n).group(2)))
        return str2
    

    """Return n as an cardinal in words."""
    ones_C = [
             "zero", "one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine", "ten", "eleven", "twelve", "thirteen",
             "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
             "nineteen"
             ]

    tens_C = [
             "zero", "ten", "twenty", "thirty", "forty", "fifty", "sixty",
             "seventy", "eighty", "ninety"
             ]

    large = [
              "", "thousand", "million", "billion", "trillion", "quadrillion",
              "quintillion", "sextillion", "septillion", "octillion",
              "nonillion", "decillion", "undecillion", "duodecillion",
              "tredecillion", "quattuordecillion", "sexdecillion",
              "septendecillion", "octodecillion", "novemdecillion",
              "vigintillion"
              ]

    def subThousand(n):
        """Convert a cardinal to words for numbers less than a thousand."""
        if n <= 19:
            return ones_C[n]
        elif n <= 99:
            q, r = divmod(n, 10)
            return tens_C[q] + (" " + subThousand(r) if r else "")
        else:
            q, r = divmod(n, 100)
            return (ones_C[q]
                    + " hundred"
                    + (" and " + subThousand(r) if r else ""))

    def splitByThousands(n):
        "Return reversed digits of n in groups of 3."""
        res = []
        while n:
            n, r = divmod(n, 1000)
            res.append(r)
        return res

    def thousandUp(n):
        """Return cardinal greater than a thousand in words."""
        list1 = []
        for i, z in enumerate(splitByThousands(n)):
            if i and z:
                list1.insert(0, subThousand(z) + " " + large[i])
            elif z:
                    list1.insert(0, subThousand(z))
        return ", ".join(list1)

    def decimal(n):
        """Returns pronounced words with n as rhs of a decimal"""
        out = ' point'
        for lt in n:
            out += ' {}'.format(ones_C[int(lt)])
        return out

    n_clean = ''
    for i in range(len(n)):
        if not i:
            if n[i].isdigit() or n[i] == '-':
                n_clean += n[i]
        else:
            if n[i].isdigit() or n[i] == '.':
                n_clean += n[i]
    if '.' in n_clean:
        dot = n_clean.find('.')
        whole, part = n_clean[:dot], n_clean[dot+1:]
        return expand_NUM(whole) + decimal(part)
    num = int(n_clean)
    if num == 0:
        return "zero"
    else:
        w = ("minus " if num < 0 else "") + thousandUp(abs(num))
        if len(n) < 4:
            return w
        else:
            if n[-3] == '0' and n[-1] != '0':
                ind = w.rfind(" ")
                return w[:ind-1] + " and" + w[ind:]
            else:
                return w


def expand_NRANGE(n):
    m = range_pattern.match(n)
    str = ''
    str += expand_NUM(m.group(1))
    if m.group(2) in ['/', '-', '–']:
        str += ' to '
    str += expand_NUM(m.group(3))
    return str


def expand_NORD(n):
    """Return n as an ordinal in words."""
    ones_C = [
             "zero", "one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine", "ten", "eleven", "twelve", "thirteen",
             "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
             "nineteen"
             ]

    ones_O = [
              "zero", "first", "second", "third", "fourth", "fifth", "sixth",
              "seventh", "eighth", "nineth", "tenth", "eleventh", "twelveth",
              "thirteenth", "fourteenth", "fifteenth", "sixteenth",
              "seventeenth", "eighteenth", "nineteenth"
              ]

    tens_C = [
              "zero", "ten", "twenty", "thirty", "forty", "fifty", "sixty",
              "seventy", "eighty", "ninety"
              ]

    tens_O = [
              "zero", "tenth", "twentieth", "thirtieth", "fortieth",
              "fiftieth", "sixtieth", "seventieth", "eightieth", "ninetieth"
              ]

    large = [
             "", "thousand", "million", "billion", "trillion", "quadrillion",
             "quintillion", "sextillion", "septillion", "octillion",
             "nonillion", "decillion", "undecillion", "duodecillion",
             "tredecillion", "quattuordecillion", "sexdecillion",
             "septendecillion", "octodecillion", "novemdecillion",
             "vigintillion"
             ]

    def subThousand_O(n):
        """Convert an ordinal to words for numbers less than a thousand."""
        if n <= 19:
            return ones_O[n]
        elif n <= 99:
            q, r = divmod(n, 10)
            if r == 0:
                return tens_O[q]
            else:
                return tens_C[q] + "-" + ones_O[r]
        else:
            q, r = divmod(n, 100)
            if r == 0:
                return ones_C[q] + " hundredth"
            else:
                return ones_C[q] + " hundred" + " and " + subThousand_O(r)

    def subThousand_C(n):
        """Convert a cardinal to words for numbers less than a thousand."""
        if n <= 19:
            return ones_C[n]
        elif n <= 99:
            q, r = divmod(n, 10)
            return tens_C[q] + ("-" + subThousand_C(r) if r else "")
        else:
            q, r = divmod(n, 100)
            return (ones_C[q] +
                    " hundred" +
                    (" and " + subThousand_C(r) if r else ""))

    def thousandUp(n):
        """Return cardinal greater than a thousand in words."""
        list1 = []
        for i, z in enumerate(splitByThousands(n)):
            if i and z:
                list1.insert(0, subThousand_C(z) + " " + large[i])
            elif z:
                    list1.insert(0, subThousand_C(z))
        return ", ".join(list1)

    def splitByThousands(n):
        "Return reversed digits of n in groups of 3."""
        res = []
        while n:
            n, r = divmod(n, 1000)
            res.append(r)
        return res

    n_clean = ''
    for i in range(len(n)):
        if i == 0:
            if n[i].isdigit() or n[i] == '-':
                n_clean += n[i]
        else:
            if n[i].isdigit():
                n_clean += n[i]
    num = int(n_clean)
    if num == 0:
        return "Zero"
    else:
        w = thousandUp(num)
        if len(n_clean) < 4:
            pen = subThousand_O(num)
        elif n_clean[-3] == '0':
            if n_clean[-2] == '0' and n_clean[-1] != '0':
                ind = w.rfind(" ")
                end_num = int(n_clean[-1])
                f = w[:ind - 1] + " and " + subThousand_O(end_num)
            elif n_clean[-2:] != '00':
                ind = w.rfind(" ")
                end_num = int(n_clean[-2:])
                f = w[:ind - 1] + " and " + subThousand_O(end_num)
            elif n_clean[-3:] == '000':
                ind = w.rfind(" ")
                f = w[:ind - 1]
            else:
                f = w
            while not f[-1].isalpha():
                f = f[:-1]
            pen = f
        elif n_clean[-3] != '0':
            if n_clean[-2] == '0' and n_clean[-1] != '0':
                ind = w.rfind(" ")
                end_num = int(n_clean[-1])
                f = w[:ind] + " " + subThousand_O(end_num)
            elif n_clean[-2:] != '00':
                ind = w.rfind(" ")
                end_num = int(n_clean[-2:])
                f = w[:ind] + " " + subThousand_O(end_num)
            else:
                f = w
            while not f[-1].isalpha():
                f = f[:-1]
            pen = f
        if ' , ' in pen:
            pen2 = re.sub('(?<= ), ', '', pen)
            pen2 = re.sub('  ', ' ', pen2)
            pen = pen2
        if pen[-3:] == 'ion' or pen[-3:] == 'and':
            return pen + "th"
        else:
            return pen


scurr_dict = {'$': 'dollar', 'Y': 'yen', '€': 'euro',
              '£': 'pound', 'HK$': 'Hong Kong Dollar',
              'US$': 'U S Dollar'}
scurr_dict_pl = {'$': 'dollars', 'Y': 'yen', '€': 'euros',
                 '£': 'pounds', 'HK$': 'Hong Kong Dollars',
                 'US$': 'U S Dollars'}
end_dict = {'k': 'thousand', 'm': 'million', 'b': 'billion'}
ecurr_dict = {
                     "US$": "U S Dollar",
                     "AFN": "Afghanistan Afghani",
                     "ALL": "Albanian Lek",
                     "DZD": "Algerian Dinar",
                     "AOA": "Angolan Kwanza",
                     "ARS": "Argentine Peso",
                     "AMD": "Armenian Dram",
                     "AWG": "Aruban Florin",
                     "AUD": "Australian Dollar",
                     "AZN": "Azerbaijan New Manat",
                     "BSD": "Bahamian Dollar",
                     "BHD": "Bahraini Dinar",
                     "BDT": "Bangladeshi Taka",
                     "BBD": "Barbados Dollar",
                     "BYR": "Belarusian Ruble",
                     "BZD": "Belize Dollar",
                     "BMD": "Bermudian Dollar",
                     "BTN": "Bhutan Ngultrum",
                     "BOB": "Bolivian Boliviano",
                     "BAM": "Bosnian Mark",
                     "BWP": "Botswana Pula",
                     "BRL": "Brazilian Real",
                     "BND": "Brunei Dollar",
                     "BGN": "Bulgarian Lev",
                     "BIF": "Burundi Franc",
                     "XOF": "CFA Franc BCEAO",
                     "XAF": "CFA Franc BEAC",
                     "XPF": "CFP Franc",
                     "KHR": "Cambodian Riel",
                     "CAD": "Canadian Dollar",
                     "CHF": "Swiss Franc",
                     "CVE": "Cape Verde Escudo",
                     "KYD": "Cayman Islands Dollar",
                     "CLP": "Chilean Peso",
                     "CNY": "Chinese Yuan",
                     "COP": "Colombian Peso",
                     "KMF": "Comoros Franc",
                     "CDF": "Congolese Franc",
                     "CRC": "Costa Rican Colon",
                     "HRK": "Croatian Kuna",
                     "CUC": "Cuban Convertible Peso",
                     "CUP": "Cuban Peso",
                     "CYP": "Cyprus Pound",
                     "CZK": "Czech Koruna",
                     "DKK": "Danish Krone",
                     "DJF": "Djibouti Franc",
                     "DOP": "Dominican Republic Peso",
                     "XCD": "East Caribbean Dollar",
                     "EGP": "Egyptian Pound",
                     "SVC": "El Salvador Colon",
                     "EEK": "Estonian Kroon",
                     "ETB": "Ethiopian Birr",
                     "EUR": "Euro",
                     "FKP": "Falkland Islands Pound",
                     "FJD": "Fiji Dollar",
                     "GMD": "Gambian Dalasi",
                     "GEL": "Georgian Lari",
                     "GHS": "Ghanaian New Cedi",
                     "GIP": "Gibraltar Pound",
                     "XAU": "Gold (oz)",
                     "GTQ": "Guatemalan Quetzal",
                     "GNF": "Guinea Franc",
                     "GYD": "Guyanese Dollar",
                     "HTG": "Haitian Gourde",
                     "HNL": "Honduran Lempira",
                     "HKD": "Hong Kong Dollar",
                     "HUF": "Hungarian Forint",
                     "ISK": "Iceland Krona",
                     "INR": "Indian Rupee",
                     "IDR": "Indonesian Rupiah",
                     "IRR": "Iranian Rial",
                     "IQD": "Iraqi Dinar",
                     "ILS": "Israeli New Shekel",
                     "JMD": "Jamaican Dollar",
                     "JPY": "Japanese Yen",
                     "JOD": "Jordanian Dinar",
                     "KZT": "Kazakhstan Tenge",
                     "KES": "Kenyan Shilling",
                     "KWD": "Kuwaiti Dinar",
                     "KGS": "Kyrgyzstanian Som",
                     "LAK": "Lao Kip",
                     "LVL": "Latvian Lats",
                     "LBP": "Lebanese Pound",
                     "LSL": "Lesotho Loti",
                     "LRD": "Liberian Dollar",
                     "LYD": "Libyan Dinar",
                     "LTL": "Lithuanian Litas",
                     "MOP": "Macau Pataca",
                     "MKD": "Macedonian Denar",
                     "MGA": "Malagasy Ariary",
                     "MWK": "Malawi Kwacha",
                     "MYR": "Malaysian Ringgit",
                     "MVR": "Maldive Rufiyaa",
                     "MTL": "Maltese Lira",
                     "MRO": "Mauritanian Ouguiya",
                     "MUR": "Mauritius Rupee",
                     "MXN": "Mexican Peso",
                     "MDL": "Moldovan Leu",
                     "MNT": "Mongolian Tugrik",
                     "MAD": "Moroccan Dirham",
                     "MZN": "Mozambique New Metical",
                     "MMK": "Myanmar Kyat",
                     "ANG": "NL Antillian Guilder",
                     "NAD": "Namibia Dollar",
                     "NPR": "Nepalese Rupee",
                     "NZD": "New Zealand Dollar",
                     "NIO": "Nicaraguan Cordoba Oro",
                     "NGN": "Nigerian Naira",
                     "KPW": "North Korean Won",
                     "NOK": "Norwegian Krone",
                     "OMR": "Omani Rial",
                     "PKR": "Pakistan Rupee",
                     "PAB": "Panamanian Balboa",
                     "PGK": "Papua New Guinea Kina",
                     "PYG": "Paraguay Guarani",
                     "PEN": "Peruvian Nuevo Sol",
                     "PHP": "Philippine Peso ",
                     "PLN": "Polish Zloty",
                     "QAR": "Qatari Rial",
                     "RON": "Romanian New Leu",
                     "RUB": "Russian Rouble",
                     "RWF": "Rwandan Franc",
                     "WST": "Samoan Tala",
                     "STD": "Sao Tome/Principe Dobra",
                     "SAR": "Saudi Riyal",
                     "RSD": "Serbian Dinar",
                     "SCR": "Seychelles Rupee",
                     "SLL": "Sierra Leone Leone",
                     "XAG": "Silver oz",
                     "SGD": "Singapore Dollar",
                     "SKK": "Slovak Koruna",
                     "SIT": "Slovenian Tolar",
                     "SBD": "Solomon Islands Dollar",
                     "SOS": "Somali Shilling",
                     "ZAR": "South African Rand",
                     "KRW": "South-Korean Won",
                     "LKR": "Sri Lanka Rupee",
                     "SHP": "St Helena Pound",
                     "SDG": "Sudanese Pound",
                     "SRD": "Suriname Dollar",
                     "SZL": "Swaziland Lilangeni",
                     "SEK": "Swedish Krona",
                     "CHF": "Swiss Franc",
                     "SYP": "Syrian Pound",
                     "TWD": "Taiwan Dollar",
                     "TZS": "Tanzanian Shilling",
                     "THB": "Thai Baht",
                     "TOP": "Tonga Pa'anga",
                     "TTD": "Trinidad/Tobago Dollar",
                     "TND": "Tunisian Dinar",
                     "TRY": "Turkish New Lira",
                     "TMM": "Turkmenistan Manat",
                     "USD": "US Dollar",
                     "UGX": "Uganda Shilling",
                     "UAH": "Ukraine Hryvnia",
                     "UYU": "Uruguayan Peso",
                     "AED": "United Arab Emir Dirham",
                     "VUV": "Vanuatu Vatu",
                     "VEB": "Venezuelan Bolivar",
                     "VND": "Vietnamese Dong",
                     "YER": "Yemeni Rial",
                     "ZMK": "Zambian Kwacha",
                     "ZWD": "Zimbabwe Dollar",
                     "£": "pound",
                     "$": "dollar",
                     "€": "euro"
                     }
invariant_plural_curr = ['JPY', 'CNY', 'THB', 'ZAR']
irregular_plural_curr = {'SEK': 'Swedish Kronor', 'NOK': 'Norwegian Kroner',
                         'DKK': 'Danish Kroner', 'ISK': 'Iceland Kronur',
                         'BRL': 'Brazilian Reais', 'LTL': 'Litai',
                         'LVL': 'Latu', 'RON': 'Lei'}


def expand_MONEY(n):
    """Return number and currency of input in words."""
    scurr = ''
    ecurr = ''
    end = ''
    num = ''
    if len(n) <= 3:
        if not n[0].isdigit():
            scurr += n[0]
            num += n[1:]
        else:
            num += n[0]
            ecurr += n[1:]
    else:
        for i in range(len(n)-3):
            if not n[i].isdigit():
                scurr += n[i]
            else:
                num = n[i:-3]
                break
        if n[-3].isalpha():
               ecurr += n[-3:]
        elif n[-1].isalpha():
            num += n[-3:-1]
            end += n[-1]
        else:
            num += n[-3:]
 
    exp_num = expand_NUM(num)
    if num == '1' and not end:
        if ecurr:
            currency = ecurr_dict[ecurr]
        elif scurr:
            currency = scurr_dict[scurr]
        else:
            currency = ''
    else:
        if ecurr:
            if ecurr in invariant_plural_curr:
                currency = ecurr_dict[ecurr]
            elif ecurr in irregular_plural_curr:
                currency = irregular_plural_curr[ecurr]
            else:
                currency = ecurr_dict[ecurr] + 's'
        elif scurr:
            currency = scurr_dict_pl[scurr]

        else:
            currency = ''
    if end:
        large = end_dict[end.lower()]
    else:
        large = ''
    items = [exp_num]
    if large:
        items.append(large)
    items.append(currency)

    return ' '.join(items)


def expand_NDIG(w):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    num_words = ['oh', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    str2 = ''
    for n in w:
        if n.isdigit():
            str2 += num_words[numbers.index(n)]
            str2 += ' '
        else:
            str2 += ''
    return str2


def expand_NTEL(w):
    str2 = ''
    if w[0] == '+':
        str2 += 'plus '
        str2 += expand_NDIG(w[1:])
    else:
        str2 += expand_NDIG(w)
    return str2
    

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
num_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
numbers1 = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
num_words1 = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
numbers2 = ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
num_words2 = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven']


def expand_NTIME(w):
    str2 = ''
    m = time_pattern.match(w)
    if w in ['0:00' or '00:00']:
        return 'midnight'
    if m.group(1) in numbers:
        str2 += num_words[numbers.index(m.group(1))]
        str2 += ' '
    elif m.group(1) in numbers1:
        str2 += num_words1[numbers1.index(m.group(1))]
        str2 += ' '
    elif m.group(1) in numbers2:
        str2 += num_words2[numbers2.index(m.group(1))]
        str2 += ' '
    if m.group(3) == '00':
        str2 += ''
    elif int(m.group(3)) < 10:
        str2 += expand_NDIG(m.group(3))
    else:
        str2 += expand_NUM(m.group(3))
        str2 += ' '
    if int(m.group(1)) <= 12:
        str2 += 'am'
    else:
        str2 += 'pm'
    return str2
    

def expand_NYER(w):
    if w[-1] == 's':
        if len(w) > 1 and w[-2:] == "'s":
            str = ''
            str += expand_NYER(w[:-2])
            str += "'s"
        else:
            str = ''
            if expand_NYER(w[:-1])[-1] == 'y':
                str += expand_NYER(w[:-1])[:-1]
                str += 'ies'
            else:
                str += expand_NYER(w[:-1])
                str += 's'
        return str


    num_decades = ['00s', '10s', '20s', '30s', '40s', '50s', '60s', '70s', '80s', '90s']
    decades = ['hundreds', 'tens', 'twenties', 'thirties', 'forties', 'fifties',
               'sixties', 'seventies', 'eighties', 'nineties']
    if w[-3:] in num_decades:
        return expand_NUM(w[:2]) + " " + decades[num_decades.index(w[-3:])]
    elif w[1:3] == '00':
        return expand_NUM(w)
    elif w[2:4] == '00':
        for i in range(len(w)):
            a = w[:2]
            return expand_NUM(a) + " " + "hundred"
    else:
        if len(w) == 4:
            for i in range(len(w)):
                a = w[:2]
                b = w[2:]
                return expand_NUM(a) + " " + expand_NUM(b)
        else:
            return expand_NUM(w)


def expand_NDATE(w):
    numbers = ['01', '1', '02', '2', '03', '3', '04', '4', '05', '5', '06', 
               '6', '07', '7', '08', '8', '09', '9', '10', '11', '12']
    months = ['January', 'January', 'February', 'February', 'March', 'March',
              'April', 'April', 'May', 'May', 'June', 'June', 'July', 'July',
              'August', 'August', 'September', 'September', 'October',
              'November', 'December']
    m = date_pattern.match(w)
    str2 = ''
    if m.group(5):
        if int(m.group(1)) > 12:
            str2 += (expand_NORD(m.group(1)) + ' of ' 
                    + months[numbers.index(m.group(3))] 
                    + " " + expand_NYER(m.group(5)))
        elif int(m.group(3)) > 12:
            str2 += (expand_NORD(m.group(3)) + ' of ' 
                    + months[numbers.index(m.group(1))] 
                    + " " + expand_NYER(m.group(5)))
        else:
            str2 += (expand_NORD(m.group(1)) + ' of ' 
                    + months[numbers.index(m.group(3))] 
                    + " " + expand_NYER(m.group(5)))
    else:
        if int(m.group(1)) > 12:
            str2 += (expand_NORD(m.group(1)) + ' of ' 
                    + months[numbers.index(m.group(3))])
        elif int(m.group(3)) > 12:
            str2 += (expand_NORD(m.group(3)) + ' of ' 
                    + months[numbers.index(m.group(1))])
        else:
            str2 += (expand_NORD(m.group(1)) + ' of ' 
                    + months[numbers.index(m.group(3))])
    return str2


def expand_PRCT(w):
    if '.' in w:
        m = percent_pattern2.match(w)
        a = m.group(1)
        b = m.group(3)
        return expand_NUM(a) + " point " + expand_NDIG(b) + "percent"
    else:
        m = percent_pattern1.match(w)
        a = m.group(1)
        return expand_NUM(a) + " percent"


percent_pattern1 = re.compile('''
([0-9]+)
(%)
$
''', re.VERBOSE)

percent_pattern2 = re.compile('''
([0-9]+)
([\.]?)
([0-9]+?)
(%)
$
''', re.VERBOSE)

time_pattern = re.compile('''
([0-9]{1,2})
([\.|:])
([0-9]{2})
$
''', re.VERBOSE)

date_pattern = re.compile('''
([0-9]{1,2})
([\.|-|./])
([0-9]{1,2})
([\.|-|./]?)
([0-9]{0,4})
$
''', re.VERBOSE)

range_pattern = re.compile('''
([0-9]+                 # 1 or more digits
\.?                     # optional '.'
[0-9]*)                 # 0 or more digits
(/|-|–)                   # hyphen or slash
([0-9]+                 # same pattern as lines 1-3
\.?
[0-9]*)
$
''', re.VERBOSE)

dec2_pattern = re.compile('''
([0-9]+)
\.
([0-9]+
\.
[0-9]+)
$
''', re.VERBOSE)
