"""High-frequency isiXhosa A1 vocabulary for basic conversation."""

from app.data._types import PartOfSpeech, VocabularyEntry, VocabularySet


def _entry(
    word: str,
    pos: PartOfSpeech,
    definition: str,
    example: str,
    ipa: str | None = None,
) -> VocabularyEntry:
    return VocabularyEntry(word=word, pos=pos, definition=definition, example=example, ipa=ipa)


VOCABULARY_SETS: list[VocabularySet] = [
    VocabularySet(
        id="izandi_xh_a1", level="A1", topic="Izandi ezisisiseko", unit_ref="a1-unit-1",
        words=[
            _entry("cela", "verb", "ukucela into", "Ndicela amanzi.", "/ǀɛːla/"),
            _entry("qonda", "verb", "ukuva intsingiselo", "Andiqondi.", "/ǃɔnda/"),
            _entry("Xhosa", "noun", "ulwimi nabantu bamaXhosa", "Ndifunda isiXhosa.", "/ǁʰɔːsa/"),
            _entry("cofa", "verb", "ukucinezela", "Cofa apha.", "/ǀɔfa/"),
            _entry("qala", "verb", "ukuqalisa", "Masiqale.", "/ǃala/"),
            _entry("xelela", "verb", "ukunika ulwazi ngomlomo", "Ndixelele.", "/ǁɛlɛla/"),
        ],
    ),
    VocabularySet(
        id="imibuliso_xh_a1", level="A1", topic="Imibuliso", unit_ref="a1-unit-2",
        words=[
            _entry("Molo", "phrase", "isibuliso kumntu omnye", "Molo, unjani?"),
            _entry("Molweni", "phrase", "isibuliso kubantu abaninzi", "Molweni, ninjani?"),
            _entry("Unjani?", "phrase", "umbuzo wempilo kumntu omnye", "Molo, unjani?"),
            _entry("Ndiyaphila", "phrase", "impendulo ethi uphilile", "Ndiyaphila, enkosi."),
            _entry("Hamba kakuhle", "phrase", "uvalelisa kumntu ohambayo", "Hamba kakuhle, sisi."),
            _entry("Sala kakuhle", "phrase", "uvalelisa kumntu oshiyekayo", "Sala kakuhle, bhuti."),
        ],
    ),
    VocabularySet(
        id="imbeko_xh_a1", level="A1", topic="Imbeko", unit_ref="a1-unit-2",
        words=[
            _entry("enkosi", "phrase", "ukubulela", "Enkosi kakhulu."),
            _entry("ndiyabulela", "phrase", "ukubulela ngokupheleleyo", "Ndiyabulela ngoncedo."),
            _entry("ndicela", "phrase", "ukuqala isicelo ngembeko", "Ndicela undincede."),
            _entry("uxolo", "phrase", "ukucela uxolo okanye ukuvula incoko", "Uxolo, iphi iteksi?"),
            _entry("ewe", "adverb", "ukuvuma", "Ewe, ndiyavuma."),
            _entry("hayi", "adverb", "ukwala", "Hayi, enkosi."),
        ],
    ),
    VocabularySet(
        id="ukuzazisa_xh_a1", level="A1", topic="Ukuzazisa", unit_ref="a1-unit-3",
        words=[
            _entry("igama", "noun", "into umntu abizwa ngayo", "Igama lam nguAphiwe."),
            _entry("ifani", "noun", "igama losapho", "Ifani yam nguDlamini."),
            _entry("hlala", "verb", "ukuba nekhaya kwindawo", "Ndihlala eGqeberha."),
            _entry("vela", "verb", "ukusuka kwindawo", "Ndivela eMthatha."),
            _entry("umhlobo", "noun", "umntu osondeleyo kuwe", "Lo ngumhlobo wam."),
            _entry("funda", "verb", "ukuzuza ulwazi", "Ndifunda isiXhosa."),
        ],
    ),
    VocabularySet(
        id="ukuqonda_xh_a1", level="A1", topic="Ukucela ukucaciselwa", unit_ref="a1-unit-4",
        words=[
            _entry("Andiqondi", "phrase", "ukuxela ukuba awuqondi", "Uxolo, andiqondi."),
            _entry("Andazi", "phrase", "ukuxela ukuba awazi", "Andazi, uxolo."),
            _entry("phinda", "verb", "ukuthetha okanye ukwenza kwakhona", "Ndicela uphinde."),
            _entry("kancinci", "adverb", "ngesantya esiphantsi okanye ngomlinganiselo omncinci", "Thetha kancinci."),
            _entry("thetha", "verb", "ukusebenzisa amazwi", "Ndithetha isiXhosa kancinci."),
            _entry("nceda", "verb", "ukunika uncedo", "Khawuncede undincede."),
        ],
    ),
    VocabularySet(
        id="usapho_xh_a1", level="A1", topic="Usapho", unit_ref="a1-unit-5",
        words=[
            _entry("usapho", "noun", "abantu basekhaya", "Usapho lwam lukhulu."),
            _entry("umama", "noun", "umzali obhinqileyo", "Umama wam usekhaya."),
            _entry("utata", "noun", "umzali oyindoda", "Utata wam uyasebenza."),
            _entry("ubhuti", "noun", "umntakwenu oyindoda", "Ubhuti wam uyafunda."),
            _entry("usisi", "noun", "umntakwenu obhinqileyo", "Usisi wam nguLihle."),
            _entry("umntwana", "noun", "umntu oselula", "Umntwana uyadlala."),
        ],
    ),
    VocabularySet(
        id="abantu_xh_a1", level="A1", topic="Abantu", unit_ref="a1-unit-5",
        words=[
            _entry("umntu", "noun", "isilwanyana esingumntu", "Lo ngumntu olungileyo."),
            _entry("abantu", "noun", "isininzi somntu", "Abantu bayathetha."),
            _entry("umfazi", "noun", "umntu obhinqileyo okanye umfazi otshatileyo", "Umfazi uyasebenza."),
            _entry("indoda", "noun", "umntu oyindoda", "Indoda ihleli apha."),
            _entry("utitshala", "noun", "umntu ofundisayo", "Utitshala uthetha isiXhosa."),
            _entry("umfundi", "noun", "umntu ofundayo", "Ndingumfundi."),
        ],
    ),
    VocabularySet(
        id="ukutya_xh_a1", level="A1", topic="Ukutya nokusela", unit_ref="a1-unit-6",
        words=[
            _entry("amanzi", "noun", "isiselo esicacileyo", "Ndicela amanzi."),
            _entry("ukutya", "noun", "izinto ezityiweyo", "Ukutya kumnandi."),
            _entry("isonka", "noun", "ukutya okubhakiweyo", "Ndicela isonka."),
            _entry("inyama", "noun", "ukutya okuvela kwizilwanyana", "Andityi nyama."),
            _entry("iti", "noun", "isiselo esishushu", "Ndisela iti."),
            _entry("ikofu", "noun", "isiselo sekofu", "Ndicela ikofu enye."),
        ],
    ),
    VocabularySet(
        id="amanani_xh_a1", level="A1", topic="Amanani namaxabiso", unit_ref="a1-unit-6",
        words=[
            _entry("nye", "numeral", "inani u-1", "Ndicela ikofu enye."),
            _entry("mbini", "numeral", "inani u-2", "Ndicela ezimbini."),
            _entry("ntathu", "numeral", "inani u-3", "Sithathu."),
            _entry("ishumi", "numeral", "inani u-10", "Ziirandi ezilishumi."),
            _entry("imali", "noun", "into yokuhlawula", "Ndinayo imali."),
            _entry("Yimalini?", "phrase", "ukubuza ixabiso", "Uxolo, yimalini?"),
        ],
    ),
    VocabularySet(
        id="iindawo_xh_a1", level="A1", topic="Iindawo nendlela", unit_ref="a1-unit-7",
        words=[
            _entry("apha", "adverb", "kule ndawo", "Hlala apha."),
            _entry("phaya", "adverb", "kuloo ndawo", "Ivenkile iphaya."),
            _entry("ekunene", "adverb", "kwicala lesandla sasekunene", "Jika ekunene."),
            _entry("ekhohlo", "adverb", "kwicala lesandla sasekhohlo", "Jika ekhohlo."),
            _entry("phambili", "adverb", "kwicala elingaphambi kwakho", "Hamba uye phambili."),
            _entry("ivenkile", "noun", "indawo yokuthenga", "Iphi ivenkile?"),
        ],
    ),
    VocabularySet(
        id="izithuthi_xh_a1", level="A1", topic="Izithuthi", unit_ref="a1-unit-7",
        words=[
            _entry("iteksi", "noun", "isithuthi esihlawulelwayo", "Iphi iteksi?"),
            _entry("ibhasi", "noun", "isithuthi sabantu abaninzi", "Ibhasi ifika nini?"),
            _entry("imoto", "noun", "isithuthi sendlela", "Imoto iphaya."),
            _entry("hamba", "verb", "ukusuka okanye ukuhamba ngeenyawo", "Hamba kakuhle."),
            _entry("jika", "verb", "ukutshintsha icala", "Jika ekhohlo."),
            _entry("fika", "verb", "ukufikelela kwindawo", "Ifika nini?"),
        ],
    ),
    VocabularySet(
        id="ixesha_xh_a1", level="A1", topic="Ixesha nemini", unit_ref="a1-unit-8",
        words=[
            _entry("namhlanje", "adverb", "ngale mini", "Ndiyasebenza namhlanje."),
            _entry("ngomso", "adverb", "ngemini elandelayo", "Siza kuthetha ngomso."),
            _entry("ngoku", "adverb", "ngeli xesha", "Ndiyahamba ngoku."),
            _entry("kusasa", "adverb", "ngexesha lasekuseni", "Sibonana kusasa."),
            _entry("emva kwemini", "adverb", "ngexesha lasemva kwemini", "Ndiza emva kwemini."),
            _entry("ebusuku", "adverb", "ngexesha lobusuku", "Ulale kamnandi ebusuku."),
        ],
    ),
    VocabularySet(
        id="incoko_xh_a1", level="A1", topic="Incoko yemihla ngemihla", unit_ref="a1-unit-8",
        words=[
            _entry("kulungile", "phrase", "ukuvuma okanye ukubonisa ukuqonda", "Kulungile, enkosi."),
            _entry("wena?", "phrase", "ukubuyisela umbuzo kumntu omnye", "Ndiyaphila. Wena?"),
            _entry("nam", "pronoun", "mna ngokunjalo", "Nam ndiyafunda."),
            _entry("kakhulu", "adverb", "ngomlinganiselo omkhulu", "Enkosi kakhulu."),
            _entry("kumnandi", "adjective", "kuyonwabisa okanye kulungile", "Kumnandi ukukwazi."),
            _entry("sibonane", "phrase", "uvaleliso oluthetha ukudibana kwakhona", "Sibonane ngomso."),
        ],
    ),
]
