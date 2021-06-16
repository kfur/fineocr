
from enum import Enum

class DocExportType(Enum):
    DOCX = "Docx"
    PDF = "Pdf"
    PDFA = "Pdfa"
    EPUB = "Epub"
    XLSX = "Xlsx"
    TXT = "Text"


class DocLangType(Enum):
    Abkhaz = "Abkhaz"
    Adyghe = "Adyghe"
    Afrikaans = "Afrikaans"
    Agul = "Agul"
    Albanian = "Albanian"
    Altaic = "Altaic"
    Arabic = "Arabic"
    ArmenianEastern = "ArmenianEastern"
    ArmenianGrabar = "ArmenianGrabar"
    ArmenianWestern = "ArmenianWestern"
    Avar = "Avar"
    Aymara = "Aymara"
    Bashkir = "Bashkir"
    Basic = "Basic"
    Basque = "Basque"
    Belarusian = "Belarusian"
    Bemba = "Bemba"
    Blackfoot = "Blackfoot"
    Breton = "Breton"
    Bugotu = "Bugotu"
    Bulgarian = "Bulgarian"
    Buryat = "Buryat"
    CPlusPlus = "CPlusPlus"
    Catalan = "Catalan"
    Cebuano = "Cebuano"
    Chamorro = "Chamorro"
    Chechen = "Chechen"
    ChinesePrc = "ChinesePrc"
    ChineseTaiwan = "ChineseTaiwan"
    Chukchee = "Chukchee"
    Chuvash = "Chuvash"
    Cobol = "Cobol"
    Corsican = "Corsican"
    CrimeanTatar = "CrimeanTatar"
    Croatian = "Croatian"
    Crow = "Crow"
    Czech = "Czech"
    Dakota = "Dakota"
    Danish = "Danish"
    Dargwa = "Dargwa"
    Dungan = "Dungan"
    Dutch = "Dutch"
    DutchBelgian = "DutchBelgian"
    English = "English"
    EskimoCyrillic = "EskimoCyrillic"
    EskimoLatin = "EskimoLatin"
    Esperanto = "Esperanto"
    Estonian = "Estonian"
    Even = "Even"
    Evenki = "Evenki"
    Faroese = "Faroese"
    Fijian = "Fijian"
    Finnish = "Finnish"
    Fortran = "Fortran"
    French = "French"
    Frisian = "Frisian"
    Friulian = "Friulian"
    Gagauz = "Gagauz"
    Galician = "Galician"
    Ganda = "Ganda"
    German = "German"
    GermanGothic = "GermanGothic"
    Greek = "Greek"
    Guarani = "Guarani"
    Hani = "Hani"
    Hausa = "Hausa"
    Hawaiian = "Hawaiian"
    Hebrew = "Hebrew"
    Hungarian = "Hungarian"
    Icelandic = "Icelandic"
    Indonesian = "Indonesian"
    Ingush = "Ingush"
    Interlingua = "Interlingua"
    Irish = "Irish"
    Italian = "Italian"
    Japanese = "Japanese"
    Java = "Java"
    Jingpo = "Jingpo"
    Kabardian = "Kabardian"
    Kalmyk = "Kalmyk"
    KarachayBalkar = "KarachayBalkar"
    Karakalpak = "Karakalpak"
    Kasub = "Kasub"
    Kawa = "Kawa"
    Kazakh = "Kazakh"
    Khakass = "Khakass"
    Khanty = "Khanty"
    Kikuyu = "Kikuyu"
    Kirghiz = "Kirghiz"
    Kongo = "Kongo"
    Korean = "Korean"
    KoreanHangul = "KoreanHangul"
    Koryak = "Koryak"
    Kpelle = "Kpelle"
    Kumyk = "Kumyk"
    Kurdish = "Kurdish"
    Kyrgyz = "Kyrgyz"
    Latin = "Latin"
    Latvian = "Latvian"
    LatvianGothic = "LatvianGothic"
    Lezgi = "Lezgi"
    Lithuanian = "Lithuanian"
    Luba = "Luba"
    Macedonian = "Macedonian"
    Malagasy = "Malagasy"
    Malay = "Malay"
    Malinke = "Malinke"
    Maltese = "Maltese"
    Mansi = "Mansi"
    Maori = "Maori"
    Mari = "Mari"
    Maya = "Maya"
    Miao = "Miao"
    Minangkabau = "Minangkabau"
    Mohawk = "Mohawk"
    Moldavian = "Moldavian"
    Mongol = "Mongol"
    Mordvin = "Mordvin"
    Nahuatl = "Nahuatl"
    Nenets = "Nenets"
    Nivkh = "Nivkh"
    Nogay = "Nogay"
    NorwegianBokmal = "NorwegianBokmal"
    Numbers = "Numbers"
    Nyanja = "Nyanja"
    Occidental = "Occidental"
    Occitan = "Occitan"
    Ojibway = "Ojibway"
    Ossetian = "Ossetian"
    Papiamento = "Papiamento"
    Pascal = "Pascal"
    Polish = "Polish"
    Quechua = "Quechua"
    RhaetoRomance = "RhaetoRomance"
    Romanian = "Romanian"
    Romany = "Romany"
    Rundi = "Rundi"
    Russian = "Russian"
    Rwanda = "Rwanda"
    Sami = "Sami"
    Samoan = "Samoan"
    ScottishGaelic = "ScottishGaelic"
    Selkup = "Selkup"
    SerbianCyrillic = "SerbianCyrillic"
    SerbianLatin = "SerbianLatin"
    Shona = "Shona"
    Slovak = "Slovak"
    Slovenian = "Slovenian"
    Somali = "Somali"
    Sorbian = "Sorbian"
    Sotho = "Sotho"
    Spanish = "Spanish"
    Sunda = "Sunda"
    Swahili = "Swahili"
    Swazi = "Swazi"
    Swedish = "Swedish"
    Tabasaran = "Tabasaran"
    Tagalog = "Tagalog"
    Tahitian = "Tahitian"
    Tajik = "Tajik"
    Tatar = "Tatar"
    Thai = "Thai"
    TokPisin = "TokPisin"
    Tongan = "Tongan"
    Tswana = "Tswana"
    Turkish = "Turkish"
    TurkmenCyrillic = "TurkmenCyrillic"
    TurkmenLatin = "TurkmenLatin"
    Tuvinian = "Tuvinian"
    Udmurt = "Udmurt"
    UighurCyrillic = "UighurCyrillic"
    UighurLatin = "UighurLatin"
    Ukrainian = "Ukrainian"
    UzbekCyrillic = "UzbekCyrillic"
    UzbekLatin = "UzbekLatin"
    Vietnamese = "Vietnamese"
    Welsh = "Welsh"
    Wolof = "Wolof"
    Xhosa = "Xhosa"
    Yakut = "Yakut"
    Yiddish = "Yiddish"
    Zapotec = "Zapotec"
    Zulu = "Zulu"
