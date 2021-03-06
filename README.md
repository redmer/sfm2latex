# SFM to LaTeX

This set of Python scripts generates LaTeX files from [SIL's Toolbox](http://www-01.sil.org/computing/toolbox/) SFM files. Licenced under MIT. 

# Requirements
- Python 3.6+ 
	- Earlier versions of Python 3 have not been tested, but probably will work. Python 2 is not supported. 
- `pyuca` Python Unicode Collation Algorithm implementation by James Tauber
	- Install with `$ pip install pyuca`
- `lualatex`
	- Other LaTeX compilers have not been tested, but will probably work. 

# Other sources
- `data/wordlist-haspelmath-tadmor-2009.csv` is taken from *WOLD* edited by Haspelmath, Martin & Tadmor, Uri is licensed under a Creative Commons Attribution 3.0 Germany License. 

# Use

```$ python3 sfm2latex --dictionary Dictionary.txt --corpus Texts.txt```

The file extensions used are not important. This will generate an `output/` folder with two--five files for the dictionary and reverse indices plus a series of folders for the corpus material. For example, the gloss named `AVM.149.004`. Each `\ref` marker will be split on the last period `.`: the part before it becomes a folder, the part after it the file. The file can be then input as `\input{AVM149/004.tex}`, and referred to as `\ref{avm149004}`

# File requirements
`sfm2latex` can transform a dictionary file and a corpus file. 

## The corpus file
```
\ref reference.number (1)
  \mb morphemes (2)
  \ge gloss English (3)
  \ft free translation (4)
  \cmt Comment. (5)
```

- `ref` The reference number cannot contain characters that are disallowed in folder or file names on your platform. The last period will be used seperate the reference number into a first part for a folder, the second part for a file. No more than one gloss can have the same reference number. Linebreaks in `\tx` are not allowed, this will overwrite the previous gloss' value. 
- `mb` Currently, suffixes and unbound morphemes are recognized and parsed correctly. 
- `ge` Glosses are put in the LaTeX source as is, unless there is a CSV file that converts the glossing (abbreviations). This can be harnassed for the extremely nice `Leipzig` package. 
- `ft` The free translation is capitalized and surrounded with single quotation marks. No further punctuation is added. 
- `cmt` The comment is put after the free translation, without any punctuation or modification. 

The LaTeX trailing source comment is made with the reference number (1) in square brackets. The LaTeX `\label{}` is made by removing all periods from the reference number (1). Also see the section above for how the reference number will be used in the file hierarchy. 

## The dictionary file

```
\lx Headword  (N=1)
  \a Alternative forms (N=0+)
  \mb Consists of (N=0+)
  \hm Homophone disambiguation number (N=0..1)
  \ps Part of Speech (N=1+)
    \sn Sense number (N=0..2+)
      \ge Gloss (not used)
      \de (envr) English definition (N=0+)
  	  \re (envr) Reverse index (N=0+)
	  \ht Standard wordlist meaning number (N=0+)
  \ec Etymological comment (N=0..1)
  \es Etymological source (N=0+)
  \nt Note (N=0..1)
  \cf Other headwords
```

- `lx` The headword. 
- `a` Used for variant forms of the headword. These variant forms also appear between the headwords and then refer to the actual headword. 
- `mb` Consists of: seperate a complex headword into its constituent headwords (incl. suffixes) and they can be clickable. 
- `hm` Homophone disambiguation. 
- `ps` Part of speech. If the build setting `"pos_stem_affix"` is used, it will be parsed and if it starts with a value mentioned there, the headword will be suffixed. 
- `ge` This marker is not used in the output files. It is used for the parsers. If the value starts with `$` dollar sign, the parser will skip that entry and continue to the next. The gloss forms for national, vernacular, regional language (`gn gv gr`) are not used. 
- `de` or `dn dv dr` are used in the dictionary and in the reverse indices. For the reverse lookup it is more practical to put any seperate meanings
- `re` or `rn rv rr` are used instead of any definition form **per language** for a reverse index. That means that `\de x \dn y \rn z`, the reverse index for English shows `x` and for National `z`. 
- `ec` There can be no more than one etymological comment per entry. 
- `es` This field can be interpreted. Put `//` around `\\` word that need to be italicized. Special value `Unknown` marks the word as not-inherited. If the first word is `dub`, the field will be suffixed with a question mark. If the first word is `cf`, the field will be prefixed with `cf. `. Any other first word is considered a language name (or language code) and is subject to etymological evaluation via the Build file. 
- `sn` Sense number. Use if more than one sense, in which case you also add `\sn 1`. 
- `cf` Only put in whole headwords to have it link automatically. 

`
## The build file
- `project`: Project name
- `lang_vernacular`: Name of the language under discussion, this will be used as the name of the output file of the vernacular dictionary. 
- `lang_regional`: Name of the regional language, this will be used as the name of an output file of the meanings index. 
- `lang_national`: Name of the national language, this will be used as the name of an output file of the meanings index. 
- `wordlist`: Empty or dictionary. The dictionary links a marker with a wordlist file. The wordlist file has three columns: 1 sorting integer, 2 linking code, referenced in dictionary file after the marker, 3 the definition. 
- `inherited`: used for the language value of the `\es\` field. If this is a language in the `merit` array, the word will be considered inherited. If in the `demerit` array, it will be considered a loan. If the language is not found, no merit or demerit points are given. 

# Known issues
- `sfm2latex` is not very flexible with the text markers it expects. 
