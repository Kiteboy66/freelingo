"""Practical isiXhosa A1 phrasebook."""

from app.data._types import PhrasebookCategory, PhrasebookEntry


def _phrase(text: str, context: str, unit_ref: str, register: str = "neutral") -> PhrasebookEntry:
    return PhrasebookEntry(text=text, context=context, register=register, unit_ref=unit_ref)  # type: ignore[arg-type]


PHRASEBOOK_CATEGORIES: list[PhrasebookCategory] = [
    PhrasebookCategory(
        id="xh_greetings", level="A1", situation="Imibuliso nokuvalelisa", icon="👋",
        phrases=[
            _phrase("Molo!", "Xa ubulisa umntu omnye", "a1-unit-2"),
            _phrase("Molweni!", "Xa ubulisa abantu abaninzi okanye ngembeko", "a1-unit-2", "formal"),
            _phrase("Unjani?", "Xa ubuza impilo yomntu omnye", "a1-unit-2"),
            _phrase("Ndiyaphila, enkosi. Wena?", "Xa uphendula uze ubuyisele umbuzo", "a1-unit-2"),
            _phrase("Hamba kakuhle.", "Xa ohambayo ingomnye umntu", "a1-unit-2"),
            _phrase("Sala kakuhle.", "Xa inguwe ohambayo", "a1-unit-2"),
        ],
    ),
    PhrasebookCategory(
        id="xh_introductions", level="A1", situation="Ukuzazisa", icon="🙂",
        phrases=[
            _phrase("Igama lam ngu[igama].", "Xa uxela igama lakho", "a1-unit-3"),
            _phrase("Ngubani igama lakho?", "Xa ubuza igama", "a1-unit-3"),
            _phrase("Ndivela e[indawo].", "Xa uxela indawo ovela kuyo", "a1-unit-3"),
            _phrase("Uvela phi?", "Xa ubuza imvelaphi", "a1-unit-3"),
            _phrase("Ndihlala e[indawo].", "Xa uxela indawo ohlala kuyo", "a1-unit-3"),
            _phrase("Kumnandi ukukwazi.", "Emva kokudibana nomntu", "a1-unit-3"),
        ],
    ),
    PhrasebookCategory(
        id="xh_repair", level="A1", situation="Xa ungaqondi", icon="🔁",
        phrases=[
            _phrase("Uxolo, andiqondi.", "Xa ungayiqondi into ethethiweyo", "a1-unit-4"),
            _phrase("Ndicela uphinde.", "Xa ufuna umntu aphinde", "a1-unit-4"),
            _phrase("Ndicela uthethe kancinci.", "Xa umntu ethetha ngokukhawuleza", "a1-unit-4"),
            _phrase("Ithetha ukuthini?", "Xa ubuza intsingiselo", "a1-unit-4"),
            _phrase("Ndiyithetha njani ngesiXhosa?", "Xa ufuna igama lesiXhosa", "a1-unit-4"),
            _phrase("Ndiyazi kancinci isiXhosa.", "Xa uchaza inqanaba lakho", "a1-unit-4"),
        ],
    ),
    PhrasebookCategory(
        id="xh_family", level="A1", situation="Usapho nabantu", icon="🏠",
        phrases=[
            _phrase("Lo ngumhlobo wam.", "Xa wazisa umhlobo", "a1-unit-5"),
            _phrase("Usapho lwakho lunjani?", "Xa ubuza ngosapho", "a1-unit-5"),
            _phrase("Ndinobhuti omnye.", "Xa uchaza usapho", "a1-unit-5"),
            _phrase("Ndinoodade ababini.", "Xa uchaza oodade", "a1-unit-5"),
            _phrase("Uhlala nabani?", "Xa ubuza umntu ahlala naye", "a1-unit-5"),
        ],
    ),
    PhrasebookCategory(
        id="xh_food", level="A1", situation="Ukutya nokusela", icon="🍽️",
        phrases=[
            _phrase("Ndicela amanzi.", "Xa ucela amanzi", "a1-unit-6"),
            _phrase("Ndicela ikofu enye.", "Xa u-odola ikofu", "a1-unit-6"),
            _phrase("Yimalini?", "Xa ubuza ixabiso", "a1-unit-6"),
            _phrase("Andityi nyama.", "Xa uchaza into ongayityiyo", "a1-unit-6"),
            _phrase("Ukutya kumnandi.", "Xa uncoma ukutya", "a1-unit-6"),
            _phrase("Hayi, enkosi.", "Xa wala ngembeko", "a1-unit-6"),
        ],
    ),
    PhrasebookCategory(
        id="xh_directions", level="A1", situation="Ukubuza indlela", icon="🧭",
        phrases=[
            _phrase("Uxolo, iphi ivenkile?", "Xa ubuza indawo yevenkile", "a1-unit-7"),
            _phrase("Ikude?", "Xa ubuza ukuba indawo ikude", "a1-unit-7"),
            _phrase("Hamba uye phambili.", "Xa uxelela umntu aqhubeke", "a1-unit-7"),
            _phrase("Jika ekhohlo.", "Xa uxelela umntu ajike ngasekhohlo", "a1-unit-7"),
            _phrase("Jika ekunene.", "Xa uxelela umntu ajike ngasekunene", "a1-unit-7"),
            _phrase("Ndiyabulela ngoncedo.", "Emva kokuncedwa", "a1-unit-7"),
        ],
    ),
    PhrasebookCategory(
        id="xh_transport", level="A1", situation="Izithuthi", icon="🚕",
        phrases=[
            _phrase("Iphi iteksi?", "Xa ukhangela iteksi", "a1-unit-7"),
            _phrase("Iya eKapa?", "Xa uqinisekisa indawo eya kuyo", "a1-unit-7"),
            _phrase("Ibhasi ifika nini?", "Xa ubuza ixesha lokufika", "a1-unit-7"),
            _phrase("Ndifuna ukuya e[indawo].", "Xa uxela indawo oya kuyo", "a1-unit-7"),
            _phrase("Ndicela ume apha.", "Xa ucela ukwehla", "a1-unit-7"),
        ],
    ),
    PhrasebookCategory(
        id="xh_small_talk", level="A1", situation="Incoko emfutshane", icon="💬",
        phrases=[
            _phrase("Wenza ntoni namhlanje?", "Xa ubuza ngezicwangciso zanamhlanje", "a1-unit-8"),
            _phrase("Ndiyasebenza namhlanje.", "Xa uxela into oyenzayo", "a1-unit-8"),
            _phrase("Uyasithetha isiXhosa?", "Xa ubuza ngolwimi", "a1-unit-8"),
            _phrase("Ndisithetha kancinci.", "Xa uchaza ukuba usithetha kancinci", "a1-unit-8"),
            _phrase("Kulungile, ndiyabulela.", "Xa uvala isihloko", "a1-unit-8"),
            _phrase("Sibonane ngomso.", "Xa nizakudibana ngosuku olulandelayo", "a1-unit-8"),
        ],
    ),
]
