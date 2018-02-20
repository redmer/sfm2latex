#!/usr/bin/python3

import json
import sys
import re
from pyuca import Collator
from typing import List

from .WordlistHeader import WordlistHeader
from .Entry import Entry
from .PartOfSpeech import PartOfSpeech
from .Image import Image
from .See import See
from .EtymologySource import EtymologySource
from .Sense import Sense
from .WordlistItem import WordlistItem
from .utils import fix_orthography

# We use a Unicode collator, best sorting algorithm
c = Collator()

# Configuration options
LX_TEX_TEMPLATE = r'\hwentry[{homonym}]{{{headword}}}[{alternatives}]{{{pos}}}{{{desc}}}[{sc}][{nt}][{ec}][{cf}]'
HT_FILE_NAME = 'data/wordlist-haspelmath-tadmor-2009.csv'

headers_file = open('data/language-headings.json')
JSON_HEADERS = json.load(headers_file)
headers_file.close()


def headers_for(lang='english'):
    answer = list()

    for obj in JSON_HEADERS:
        if obj['lang'] == lang:
            if 'sortkey' in obj:
                for idx, val in enumerate(obj['headers']):
                    answer.append(
                        WordlistHeader(level='vernacular', sk=obj['sortkey'][idx], desc=val)
                    )
            else:
                for idx, val in enumerate(obj['headers']):
                    answer.append(
                        WordlistHeader(level='reverse', desc=val)
                    )

    return answer


def items_in_file(in_file):
    lexemes = list()
    current_lexeme = None
    not_added_lexemes = list()
    skip_until_next_lx = False

    es_certainty_regex = re.compile(r'.+\(cert=(.+)\)')

    for line in in_file.read().splitlines():
        if '' == line:  # skip empty lines
            continue

        try:
            marker, markervalue = line.split(' ', 1)
        except ValueError:
            continue  # with the iteration

        if skip_until_next_lx and marker != r'\lx':
            # print('Skipped\t' + marker + '\t' + markervalue)
            continue

        markervalue = fix_orthography(markervalue)

        if r'\lx' == marker:  # we have a new word
            skip_until_next_lx = False

            if current_lexeme is not None:
                lexemes.append(current_lexeme)

            current_lexeme = Entry(markervalue)

        if r'\a' == marker:  # alternative hw forms
            current_lexeme.alts.append(markervalue)

        elif r'\ps' == marker:  # pos
            if len(current_lexeme.parts_of_speech[-1].pos):
                current_lexeme.parts_of_speech.append(PartOfSpeech())

            current_lexeme.parts_of_speech[-1].pos = markervalue

        elif r'\mr' == marker:
            current_lexeme.mr += markervalue.split(' ')

        elif r'\de' == marker:  # add an english sense
            current_lexeme.parts_of_speech[-1].senses[-1].de.append(markervalue)

        elif r'\dn' == marker:
            current_lexeme.parts_of_speech[-1].senses[-1].dn.append(markervalue)

        elif r'\re' == marker:
            current_lexeme.parts_of_speech[-1].senses[-1].re.append(markervalue)

        elif r'\rn' == marker:
            current_lexeme.parts_of_speech[-1].senses[-1].rn.append(markervalue)

        elif r'\ge' == marker:
            if '$' == markervalue[0]:
                not_added_lexemes.append('"' + markervalue + '"\t"' + current_lexeme.hw + '"')
                skip_until_next_lx = True  # Start skipping other markers (\dt)
                current_lexeme = None  # Don't add the \lx with a $ \ge

        elif r'\sn' == marker:  # extra sense
            if int(markervalue) > 1:
                current_lexeme.parts_of_speech[-1].senses.append(Sense())

        elif r'\ht' == marker:
            current_lexeme.parts_of_speech[-1].senses[-1].ht.append(markervalue)  # there can be multiple

        elif r'\sc' == marker:
            current_lexeme.parts_of_speech[-1].senses[-1].sc = markervalue

        elif r'\nt' == marker:
            current_lexeme.parts_of_speech[-1].senses[-1].nt = markervalue

        elif r'\es' == marker:
            cert_hits = es_certainty_regex.match(markervalue)

            if cert_hits is not None:
                delete_cert = len(r'(cert=)') + len(cert_hits.group(1))
                markervalue = markervalue[:-delete_cert]
                cert = cert_hits.group(1)
            else:
                cert = ''

            values = markervalue.split(' ', 1)

            if 'Unknown' in values:
                # Unknown provenance, so inform the renderer.
                lang = ' '
                ety = 'No cognates'
                current_lexeme.inherited = -500
            elif len(values) == 1:
                # Only no spaces in the \es marker, so only a language value.
                lang = values[0]
                ety = ''
            else:
                # There is both a language mentioned and a meaning, form, etc.
                #
                lang = values[0]
                ety = values[1]

            current_lexeme.inherited += 50 if is_ancestor_language(lang) and cert is not 'cf' else 1
            current_lexeme.inherited -= 26 if is_not_ancestor_language(lang) and cert is not 'cf' else 1

            current_lexeme.es.append(EtymologySource(
                lang=lang,
                value=ety,
                cert=cert,
            ))

        elif r'\ec' == marker:
            current_lexeme.ec = markervalue

        elif r'\cf' == marker:
            current_lexeme.cfs.append(markervalue)

        elif r'\hm' == marker:
            current_lexeme.hm = markervalue

        elif r'\pc' == marker:
            src, attrib = markervalue.split('|', 1)

            lexemes.append(Image(
                hw=current_lexeme.hw,
                img_src=src.replace('"', ''),
                img_attrib=attrib,
            ))

            current_lexeme.parts_of_speech[-1].senses[-1].img_src = src
            current_lexeme.parts_of_speech[-1].senses[-1].img_attrib = attrib

    # print('Warning: several words were skipped as they had no English definition: \n\t' + '\n\t'.join(not_added_lexemes))

    for item in lexemes:
        if item.type == 'entry':
            if item.parts_of_speech[-1].pos[0] == 'v':
                suffix = '-'  # y
            elif item.parts_of_speech[-1].pos == 'amb':
                suffix = '='  # (y)
            else:
                suffix = ''

            item.hw += suffix

            for i in range(0, len(item.alts)):
                item.alts[i] += suffix
                lexemes.append(See(
                    instead_look_at=[item.hw],  # challwa (correct)
                    if_you_look_at=item.alts[i],  # challuwa (incorrect)
                ))

    return lexemes


def reverse_index(lexemes):
    # we hebben ht->hw, en->hw, es->hw
    dict_national = {}
    dict_english = {}
    dict_ht = {}

    for item in lexemes:
        if item.type == 'entry':
            if item.hw[0:1] == '-':
                continue
            else:
                for meaning in item.parts_of_speech:
                    for sense in meaning.senses:
                        index_term_english = sense.re if len(sense.re) else sense.de
                        index_term_national = sense.rn if len(sense.rn) else sense.dn
                        suffix = Entry.LX_WORD_INHERITED_SYMBOL if item.inherited > 0 else Entry.LX_WORD_LOAN_SYMBOL
                        target = item.hw + suffix

                        for english_entry in index_term_english:
                            if english_entry.startswith(' \\'):
                                break  # this is a gloss

                            if english_entry in dict_english:
                                dict_english[english_entry].append(target)
                            else:
                                dict_english[english_entry] = [target]

                        for national_entry in index_term_national:
                            if national_entry in dict_national:
                                dict_national[national_entry].append(target)
                            else:
                                dict_national[national_entry] = [target]

                        for ht in sense.ht:
                            if ht in dict_ht:
                                dict_ht[ht].append(target)
                            elif len(ht):
                                dict_ht[ht] = [target]

    output_index_national = list()
    output_index_english = list()

    for national_hw, qul_hws in dict_national.items():
        output_index_national.append(See(
            instead_look_at=qul_hws,  # yaykuy <-- normal hw
            if_you_look_at=national_hw,  # waykuy <-- alt hw
            sort_as_vernacular=False,
        ))

    for english_hw, qul_hws in dict_english.items():
        output_index_english.append(See(
            instead_look_at=qul_hws,  # yaykuy <-- normal hw
            if_you_look_at=english_hw,  # waykuy <-- alt hw
            sort_as_vernacular=False,
        ))

    return {
        'national': output_index_national,
        'english': output_index_english,
        'ht': dict_ht,
    }


def build(input_filename, settings={}):
    in_file = open(input_filename)

    # Get the lexemes from the SFM file
    lexemes = items_in_file(in_file)

    # Generate the reverse indices
    indices = reverse_index(lexemes)

    dict_english = search_reverse_index_for_common_prefixes(indices['english'])
    dict_national = search_reverse_index_for_common_prefixes(indices['national'])

    # Sort the dictionaries
    dict_english = sorted(
        dict_english + headers_for(lang='en'),
        key=lambda x: c.sort_key(x.sk())
    )
    dict_national = sorted(
        dict_national + headers_for(lang='es'),
        key=lambda x: c.sort_key(x.sk())
    )
    dict_vernacular = sorted(
        lexemes + headers_for(lang='qul'),
        key=lambda x: c.sort_key(x.sk())
    )
    dict_ht = sorted_ht_list(indices['ht'])

    try:
        file_contents_csv = render_csv(lexemes)
        file_contents_en = render(dict_english)
        file_contents_es = render(dict_national)
        file_contents_ht = render(dict_ht)
        file_contents_qu = render(dict_vernacular)
    except ValueError as e:
        print('An error occurred during processing, check your syntax.', e)
        quit(5)

    # Create the out-files
    out_file_qu = open('output/qul.tex', 'w+')
    out_file_en = open('output/en.tex', 'w+')
    out_file_es = open('output/es.tex', 'w+')
    out_file_ht = open('output/ht.tex', 'w+')
    out_file_csv = open('output/loanwords.csv', 'w+')

    # 03 Write string
    out_file_qu.write(file_contents_qu)
    out_file_en.write(file_contents_en)
    out_file_es.write(file_contents_es)
    out_file_ht.write(file_contents_ht)
    out_file_csv.write(file_contents_csv)

    # 04 Cleanup
    in_file.close()
    out_file_qu.close()
    out_file_en.close()
    out_file_es.close()
    out_file_ht.close()
    out_file_csv.close()


def search_reverse_index_for_common_prefixes(complete_reverse_list):
    # return complete_reverse_list  # added as a paper-saving measure

    items_that_need_heading_term = []

    prefixes = []
    subordinated_prefixes = []

    for see in complete_reverse_list:
        '''
        $see : See()

        (1) village: llaqta
            village, big: hatun llaqta

        (2) brother, to a man: wawqi
            brother, to a woman: tura

        (3) chew: masticar
            chew coca: coquear

            ---  become  ---

        (4) village: llaqta         <-- 'index_mainentry' '✓'
                big: hatun llaqta   <-- 'index_subentry'

        (5) brother                 <-- 'index_mainentry' 'tbd'
                to a man: wawqi     <-- 'index_subentry'
                to a woman: tura    <-- 'index_subentry'

        (6) chew: masticar          <-- 'index_mainentry'
            chew coca: coquear      <-- 'index_mainentry'
        '''
        indexed_term = see.if_you_look_at
        if ', ' in indexed_term:
            prefixes.append(indexed_term.split(', ', 1)[0])

    for prefix in prefixes:
        for see in complete_reverse_list:
            if see.if_you_look_at == prefix:
                # 'village'
                subordinated_prefixes.append(see.if_you_look_at)
                prefixes.remove(prefix)

    print('Prefixes remaining: "' + '", "'.join(prefixes) + '".')

    for see in complete_reverse_list:
        indexed_term = see.if_you_look_at
        if ', ' in indexed_term:
            if indexed_term.split(', ', 1)[0] in subordinated_prefixes:
                see.is_subordinate = True

    return complete_reverse_list + items_that_need_heading_term


WORDLIST_HT_ORIGINALS = dict()
WORDLIST_HT_HEADINGS = list()


def load_ht_file():
    try:
        definition_file = open(HT_FILE_NAME, 'r')
    except FileNotFoundError:
        print(f'File "{HT_FILE_NAME}" is missing. Please re-download it from <https://github.com/redmer/sfm2tex/>.')
        sys.exit(2)

    for line in definition_file.read().splitlines():
        sk, ht_code, title = line.split(',')
        if ht_code[0] is 'h':
            # this is a heading
            WORDLIST_HT_HEADINGS.append(
                WordlistHeader(sk=sk, desc=title, level='ht')
            )
        else:
            WORDLIST_HT_ORIGINALS[ht_code] = {'sk': sk, 'desc': title}


def sk_for_ht(ht_code):
    return WORDLIST_HT_ORIGINALS[ht_code]['sk']


def desc_for_ht(ht_code):
    return WORDLIST_HT_ORIGINALS[ht_code]['desc']


def sorted_ht_list(ht_list):
    load_ht_file()
    final_list = list()

    for ht_code, hws in ht_list.items():
        final_list.append(
            WordlistItem(
                sk=sk_for_ht(ht_code),
                ht_code=ht_code,
                desc=desc_for_ht(ht_code),
                instead_look_at=hws
            )
        )

    return sorted(final_list + WORDLIST_HT_HEADINGS, key=lambda x: int(x.sk()))


def render_csv(lexemes: List[Entry]):
    output = ''

    for item in lexemes:
        if callable(getattr(item, 'csv_render', None)):
            output += item.csv_render() + '\n'

    return output


def render(index):
    output = ''

    for item in index:
        output += item.render() + '\n'

    return output


def is_ancestor_language(language):
    return language in ['PQue', 'PQueAym', 'Que', 'SQue']


def is_not_ancestor_language(language):
    return language in ['Sp', 'Uch', 'Aym', ' ', 'Paym', 'CENAQ']
