"""Static A1 isiXhosa placement bank."""

from app.data._types import AssessmentQuestion


def _q(
    id_: str,
    skill: str,
    question: str,
    options: list[str],
    correct: str,
    grammar_slug: str | None = None,
) -> AssessmentQuestion:
    return AssessmentQuestion(
        id=id_, skill=skill, difficulty="A1", question=question,
        options=options, correct=correct, grammar_slug=grammar_slug,
    )  # type: ignore[arg-type]


ASSESSMENT_BANK: list[AssessmentQuestion] = [
    _q("g-xh-a1-001", "grammar", "Khetha isibuliso somntu omnye.", ["Molo", "Molweni", "Salani kakuhle", "Ninjani"], "Molo", "xh-singular-plural-greetings"),
    _q("g-xh-a1-002", "grammar", "Gqibezela: Igama lam ___Lindiwe.", ["ngu", "ndi", "si", "ba"], "ngu", "xh-copulative-ngu"),
    _q("g-xh-a1-003", "grammar", "Khetha umbuzo wendawo.", ["Uhlala phi?", "Ungubani?", "Unjani?", "Yintoni?"], "Uhlala phi?", "xh-question-words"),
    _q("g-xh-a1-004", "grammar", "Gqibezela: ___qondi.", ["Ndi", "Andi", "Si", "Ni"], "Andi", "xh-negation"),
    _q("g-xh-a1-005", "grammar", "Khetha isicelo esinembeko.", ["Ndicela amanzi.", "Amanzi!", "Ndinike!", "Hayi amanzi."], "Ndicela amanzi.", "xh-polite-requests"),
    _q("g-xh-a1-006", "grammar", "Khetha isininzi sika-'umntu'.", ["abantu", "izinto", "amagama", "iilwimi"], "abantu", "xh-noun-classes"),
    _q("g-xh-a1-007", "grammar", "Gqibezela: Ndi___funda.", ["ya", "ba", "ni", "si"], "ya", "xh-present-tense"),
    _q("g-xh-a1-008", "grammar", "Khetha isivakalisi esithetha indawo ohlala kuyo.", ["Ndihlala eKapa.", "Ndivela eKapa.", "Ndiya eKapa.", "Ndicela eKapa."], "Ndihlala eKapa.", "xh-locatives"),
    _q("v-xh-a1-001", "vocabulary", "U-'enkosi' uthetha ukuthini?", ["ukubulela", "ukuvalelisa", "ukubuza", "ukwala"], "ukubulela"),
    _q("v-xh-a1-002", "vocabulary", "Khetha igama elithetha 'water'.", ["amanzi", "isonka", "inyama", "ikofu"], "amanzi"),
    _q("v-xh-a1-003", "vocabulary", "Khetha igama elithetha 'left'.", ["ekhohlo", "ekunene", "phambili", "phaya"], "ekhohlo"),
    _q("v-xh-a1-004", "vocabulary", "Ubuza njani ixabiso?", ["Yimalini?", "Iphi?", "Nini?", "Ngubani?"], "Yimalini?"),
    _q("v-xh-a1-005", "vocabulary", "Khetha igama losapho.", ["umama", "ivenkile", "ibhasi", "imali"], "umama"),
    _q("v-xh-a1-006", "vocabulary", "U-'ngomso' uthetha nini?", ["ngemini elandelayo", "namhlanje", "ngoku", "izolo"], "ngemini elandelayo"),
    _q("v-xh-a1-007", "vocabulary", "Khetha isithuthi.", ["iteksi", "ukutya", "umhlobo", "igama"], "iteksi"),
    _q("v-xh-a1-008", "vocabulary", "U-'phinda' uthetha ntoni?", ["yenza kwakhona", "thetha ngokukhawuleza", "hamba", "hlala"], "yenza kwakhona"),
    _q("r-xh-a1-001", "reading", "Funda: 'Molo, unjani?' Yeyiphi impendulo efanelekileyo?", ["Ndiyaphila, enkosi.", "Yimalini?", "Jika ekhohlo.", "Andityi nyama."], "Ndiyaphila, enkosi."),
    _q("r-xh-a1-002", "reading", "Funda: 'Igama lam nguSipho.' Yintoni igama lomntu?", ["Sipho", "Molo", "Kapa", "Xhosa"], "Sipho"),
    _q("r-xh-a1-003", "reading", "Funda: 'Ndihlala eBhayi.' Uhlala phi?", ["eBhayi", "eKapa", "eMthatha", "apha"], "eBhayi"),
    _q("r-xh-a1-004", "reading", "Funda: 'Uxolo, andiqondi.' Ufuna ntoni lo mntu?", ["ukucaciselwa", "ukutya", "iteksi", "imali"], "ukucaciselwa"),
    _q("r-xh-a1-005", "reading", "Funda: 'Ndicela ikofu enye.' Ucela ntoni?", ["ikofu", "iti", "amanzi", "isonka"], "ikofu"),
    _q("r-xh-a1-006", "reading", "Funda: 'Ivenkile iphaya. Jika ekunene.' Umele ajike phi?", ["ekunene", "ekhohlo", "phambili", "apha"], "ekunene"),
    _q("r-xh-a1-007", "reading", "Funda: 'Ndisithetha kancinci isiXhosa.' Uthetha njani?", ["kancinci", "kakhulu", "hayi", "ngomso"], "kancinci"),
    _q("r-xh-a1-008", "reading", "Funda: 'Sibonane ngomso.' Baza kudibana nini?", ["ngomso", "namhlanje", "ngoku", "kusasa kuphela"], "ngomso"),
]
