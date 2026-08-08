"""Conversation-first, English-supported isiXhosa A1 sprint.

The course deliberately teaches useful chunks before grammar terminology.  Each
day contains only three new phrases, a short model conversation, and a cultural
or pronunciation note.  The UI reveals these one at a time and then prompts
retrieval from memory.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuidedPhrase:
    text: str
    translation: str
    chunks: str
    usage: str


@dataclass(frozen=True)
class GuidedDialogueLine:
    speaker: str
    text: str
    translation: str


@dataclass(frozen=True)
class GuidedDay:
    day: int
    unit_id: str
    lesson_type: str
    title: str
    xhosa_title: str
    goal: str
    phrases: tuple[GuidedPhrase, GuidedPhrase, GuidedPhrase]
    dialogue: tuple[GuidedDialogueLine, ...]
    coach_note: str
    grammar_refs: tuple[str, ...]


def _p(text: str, translation: str, chunks: str, usage: str) -> GuidedPhrase:
    return GuidedPhrase(text, translation, chunks, usage)


def _line(speaker: str, text: str, translation: str) -> GuidedDialogueLine:
    return GuidedDialogueLine(speaker, text, translation)


GUIDED_XHOSA_A1_DAYS: tuple[GuidedDay, ...] = (
    GuidedDay(
        1,
        "a1-unit-1",
        "listening",
        "Your first isiXhosa conversation",
        "Incoko yakho yokuqala",
        "Greet one person, ask how they are, and answer politely.",
        (
            _p("Molo!", "Hello! (to one person)", "Mo·lo", "Use Molo when greeting one person."),
            _p("Unjani?", "How are you? (one person)", "Un·ja·ni", "Ask this after saying hello."),
            _p(
                "Ndiphilile, enkosi.",
                "I am well, thank you.",
                "Ndi·phi·li·le · en·ko·si",
                "A warm, polite answer to Unjani?",
            ),
        ),
        (
            _line("Lwazi", "Molo!", "Hello!"),
            _line("You", "Molo!", "Hello!"),
            _line("Lwazi", "Unjani?", "How are you?"),
            _line("You", "Ndiphilile, enkosi.", "I am well, thank you."),
        ),
        "In isiXhosa, greeting someone and asking about their wellbeing matters. Do not rush straight into your request.",
        ("xh-singular-plural-greetings",),
    ),
    GuidedDay(
        2,
        "a1-unit-1",
        "vocabulary",
        "Greeting people and saying goodbye",
        "Ukubulisa nokuvalelisa",
        "Greet a group and choose the right goodbye.",
        (
            _p(
                "Molweni!",
                "Hello! (to a group)",
                "Mo·lwe·ni",
                "Use Molweni for two or more people.",
            ),
            _p("Ninjani?", "How are you all?", "Nin·ja·ni", "The plural partner of Unjani?"),
            _p(
                "Hamba kakuhle.",
                "Go well.",
                "Ham·ba · ka·ku·hle",
                "Say this to the person who is leaving. If you are leaving, say Sala kakuhle.",
            ),
        ),
        (
            _line("You", "Molweni!", "Hello, everyone!"),
            _line("Group", "Molo!", "Hello!"),
            _line("You", "Ninjani?", "How are you all?"),
            _line("Group", "Siyaphila, enkosi.", "We are well, thank you."),
            _line("You", "Hamba kakuhle.", "Go well."),
        ),
        "One person: Molo / Unjani? More than one person: Molweni / Ninjani?",
        ("xh-singular-plural-greetings",),
    ),
    GuidedDay(
        3,
        "a1-unit-2",
        "grammar",
        "Names and introductions",
        "Amagama nokuzazisa",
        "Say your name, ask another person's name, and close the introduction warmly.",
        (
            _p(
                "Igama lam nguLwazi.",
                "My name is Lwazi.",
                "I·ga·ma · lam · ngu·Lwa·zi",
                "Replace Lwazi with your own name.",
            ),
            _p(
                "Ngubani igama lakho?",
                "What is your name?",
                "Ngu·ba·ni · i·ga·ma · la·kho",
                "A direct, useful way to ask someone's name.",
            ),
            _p(
                "Ndiyavuya ukukwazi.",
                "Nice to meet you.",
                "Ndi·ya·vu·ya · u·ku·kwa·zi",
                "Say this after exchanging names.",
            ),
        ),
        (
            _line("You", "Molo! Igama lam nguSam.", "Hello! My name is Sam."),
            _line("Aphiwe", "Molo Sam. Igama lam nguAphiwe.", "Hello Sam. My name is Aphiwe."),
            _line("You", "Ndiyavuya ukukwazi.", "Nice to meet you."),
        ),
        "The small word ngu links a person to a name: Igama lam ngu… Learn the whole phrase as one useful block.",
        ("xh-copulative-ngu", "xh-possessives"),
    ),
    GuidedDay(
        4,
        "a1-unit-2",
        "listening",
        "Where you come from and live",
        "Apho uvela khona nalapho uhlala khona",
        "Say where you come from, ask where someone comes from, and say where you live.",
        (
            _p(
                "Ndivela eKapa.",
                "I come from Cape Town.",
                "Ndi·ve·la · e·Ka·pa",
                "Replace eKapa with your place.",
            ),
            _p("Uvela phi?", "Where do you come from?", "U·ve·la · phi", "Use phi for 'where'."),
            _p(
                "Ndihlala eKapa.",
                "I live in Cape Town.",
                "Ndi·hla·la · e·Ka·pa",
                "Use this for where you live now.",
            ),
        ),
        (
            _line("Aphiwe", "Uvela phi?", "Where do you come from?"),
            _line("You", "Ndivela eGqeberha.", "I come from Gqeberha."),
            _line("Aphiwe", "Uhlala phi?", "Where do you live?"),
            _line("You", "Ndihlala eKapa.", "I live in Cape Town."),
        ),
        "Many place names take e-: eKapa, eGqeberha, eMthatha. Learn each place as part of the phrase.",
        ("xh-question-words", "xh-locatives"),
    ),
    GuidedDay(
        5,
        "a1-unit-3",
        "listening",
        "When you do not understand",
        "Xa ungaqondi",
        "Stay in the conversation when you do not understand.",
        (
            _p(
                "Uxolo, andiqondi.",
                "Sorry, I do not understand.",
                "U·xo·lo · an·di·qo·ndi",
                "Use this immediately instead of pretending to understand.",
            ),
            _p(
                "Ithetha ukuthini?",
                "What does it mean?",
                "I·the·tha · u·ku·thi·ni",
                "Point to a word or repeat it before asking.",
            ),
            _p("Andazi.", "I do not know.", "An·da·zi", "A short, honest answer."),
        ),
        (
            _line("Lwazi", "Ivenkile iphaya.", "The shop is over there."),
            _line("You", "Uxolo, andiqondi.", "Sorry, I do not understand."),
            _line("You", "Ithetha ukuthini 'ivenkile'?", "What does 'ivenkile' mean?"),
            _line("Lwazi", "Ivenkile yi-shop.", "Ivenkile means shop."),
        ),
        "The q in andiqondi begins with a firm central click, like the pop of a cork. Press Listen and copy the whole word.",
        ("xh-negation", "xh-clicks"),
    ),
    GuidedDay(
        6,
        "a1-unit-3",
        "grammar",
        "Ask someone to repeat or slow down",
        "Cela ukuphindwa nokuthetha kancinci",
        "Ask for repetition, slower speech, or the isiXhosa word you need.",
        (
            _p(
                "Ndicela uphinde.",
                "Please repeat.",
                "Ndi·ce·la · u·phin·de",
                "Your most useful rescue phrase.",
            ),
            _p(
                "Ndicela uthethe kancinci.",
                "Please speak slowly.",
                "Ndi·ce·la · u·the·the · kan·ci·nci",
                "Use when you recognise words but the speech is too fast.",
            ),
            _p(
                "Ndiyithetha njani ngesiXhosa?",
                "How do I say it in isiXhosa?",
                "Ndi·yi·the·tha · nja·ni · nge·si·Xho·sa",
                "Point to the thing or say the English word first.",
            ),
        ),
        (
            _line("Aphiwe", "Uhlala phi ngoku?", "Where do you live now?"),
            _line("You", "Ndicela uphinde.", "Please repeat."),
            _line("Aphiwe", "Uhlala phi?", "Where do you live?"),
            _line("You", "Ndihlala eKapa.", "I live in Cape Town."),
        ),
        "The c in ndicela is a light dental click, like a single 'tsk'. The x in isiXhosa is released at the side of the tongue.",
        ("xh-polite-requests", "xh-clicks"),
    ),
    GuidedDay(
        7,
        "a1-unit-4",
        "vocabulary",
        "Friends and family",
        "Abahlobo nosapho",
        "Introduce a friend and give one simple fact about your family.",
        (
            _p(
                "Lo ngumhlobo wam.",
                "This is my friend.",
                "Lo · ngu·mhlo·bo · wam",
                "Use this while introducing a friend.",
            ),
            _p(
                "Usapho lwam lukhulu.",
                "My family is big.",
                "U·sa·pho · lwam · lu·khu·lu",
                "A simple way to describe your family.",
            ),
            _p(
                "Ndinobhuti omnye.",
                "I have one brother.",
                "Ndi·no·bhu·ti · o·mnye",
                "Change the family word and number as you learn more.",
            ),
        ),
        (
            _line("You", "Lo ngumhlobo wam, uLwazi.", "This is my friend, Lwazi."),
            _line("Aphiwe", "Molo Lwazi!", "Hello Lwazi!"),
            _line("Lwazi", "Molo! Ndiyavuya ukukwazi.", "Hello! Nice to meet you."),
        ),
        "Family terms are also respectful forms of address. Sisi and bhuti can be used for people around your age.",
        ("xh-noun-classes", "xh-possessives"),
    ),
    GuidedDay(
        8,
        "a1-unit-5",
        "vocabulary",
        "Order a drink politely",
        "Cela isiselo ngembeko",
        "Order water or coffee and decline politely.",
        (
            _p(
                "Ndicela amanzi.",
                "Water, please.",
                "Ndi·ce·la · a·man·zi",
                "Ndicela makes a request polite.",
            ),
            _p(
                "Ndicela ikofu enye.",
                "One coffee, please.",
                "Ndi·ce·la · i·ko·fu · e·nye",
                "Put the item after Ndicela.",
            ),
            _p("Hayi, enkosi.", "No, thank you.", "Ha·yi · en·ko·si", "A polite way to decline."),
        ),
        (
            _line("Server", "Molo, ufuna ntoni?", "Hello, what would you like?"),
            _line("You", "Ndicela ikofu enye.", "One coffee, please."),
            _line("Server", "Ufuna iswekile?", "Would you like sugar?"),
            _line("You", "Hayi, enkosi.", "No, thank you."),
        ),
        "A request with Ndicela is both useful and respectful. You do not need a long grammar explanation to start using it.",
        ("xh-polite-requests",),
    ),
    GuidedDay(
        9,
        "a1-unit-5",
        "listening",
        "Prices and food",
        "Amaxabiso nokutya",
        "Ask a price, understand a simple amount, and compliment food.",
        (
            _p(
                "Yimalini?",
                "How much is it?",
                "Yi·ma·li·ni",
                "Ask this after pointing to the item.",
            ),
            _p(
                "Ziirandi ezilishumi.",
                "It is ten rand.",
                "Zii·ran·di · e·zi·shu·mi",
                "Listen for ishumi, ten.",
            ),
            _p(
                "Ukutya kumnandi.",
                "The food is delicious.",
                "U·ku·tya · kum·nan·di",
                "A warm compliment after eating.",
            ),
        ),
        (
            _line("You", "Uxolo, yimalini?", "Excuse me, how much is it?"),
            _line("Seller", "Ziirandi ezilishumi.", "It is ten rand."),
            _line("You", "Kulungile, enkosi.", "Okay, thank you."),
        ),
        "Numbers change form with different nouns. For now, learn prices as complete phrases and focus on recognising the amount.",
        ("xh-question-words", "xh-polite-requests"),
    ),
    GuidedDay(
        10,
        "a1-unit-6",
        "reading",
        "Ask for directions",
        "Buza indlela",
        "Ask where a place is and thank the person who helps you.",
        (
            _p(
                "Uxolo, iphi ivenkile?",
                "Excuse me, where is the shop?",
                "U·xo·lo · i·phi · i·ven·ki·le",
                "Begin with Uxolo to get someone's attention politely.",
            ),
            _p("Ikude?", "Is it far?", "I·ku·de", "A useful one-word follow-up question."),
            _p(
                "Ndiyabulela ngoncedo lwakho.",
                "Thank you for the help.",
                "Ndi·ya·bu·le·la · ngo·nce·do · lwa·kho",
                "Say this after receiving directions.",
            ),
        ),
        (
            _line("You", "Uxolo, iphi ivenkile?", "Excuse me, where is the shop?"),
            _line("Lwazi", "Ivenkile iphaya.", "The shop is over there."),
            _line("You", "Ikude?", "Is it far?"),
            _line("Lwazi", "Hayi, ikufuphi.", "No, it is nearby."),
            _line("You", "Ndiyabulela ngoncedo lwakho.", "Thank you for the help."),
        ),
        "In a real conversation, pointing and context do a lot of the work. Use the short phrases confidently.",
        ("xh-question-words", "xh-locatives"),
    ),
    GuidedDay(
        11,
        "a1-unit-6",
        "listening",
        "Use a taxi or bus",
        "Sebenzisa iteksi okanye ibhasi",
        "Find transport, check its destination, and ask to stop.",
        (
            _p(
                "Iphi iteksi?",
                "Where is the taxi?",
                "I·phi · i·te·ksi",
                "Swap iteksi for ibhasi when you need a bus.",
            ),
            _p(
                "Iya eKapa?",
                "Does it go to Cape Town?",
                "I·ya · e·Ka·pa",
                "Use this to confirm the destination.",
            ),
            _p(
                "Ndicela ume apha.",
                "Please stop here.",
                "Ndi·ce·la · u·me · a·pha",
                "Say this before your stop.",
            ),
        ),
        (
            _line("You", "Uxolo, iphi iteksi?", "Excuse me, where is the taxi?"),
            _line("Driver", "Iphaya.", "It is over there."),
            _line("You", "Iya eKapa?", "Does it go to Cape Town?"),
            _line("Driver", "Ewe.", "Yes."),
            _line("You", "Ndicela ume apha.", "Please stop here."),
        ),
        "Taxi routes can be highly local. Confirm the destination with a person before boarding.",
        ("xh-question-words", "xh-locatives", "xh-polite-requests"),
    ),
    GuidedDay(
        12,
        "a1-unit-7",
        "listening",
        "Simple everyday plans",
        "Izicwangciso zemihla ngemihla",
        "Ask what someone is doing today, answer, and arrange to meet again.",
        (
            _p(
                "Wenza ntoni namhlanje?",
                "What are you doing today?",
                "Wen·za · nto·ni · nam·hla·nje",
                "A natural small-talk question.",
            ),
            _p(
                "Ndiyasebenza namhlanje.",
                "I am working today.",
                "Ndi·ya·se·ben·za · nam·hla·nje",
                "Replace the action as your vocabulary grows.",
            ),
            _p(
                "Sibonane ngomso.",
                "See you tomorrow.",
                "Si·bo·na·ne · ngo·mso",
                "A friendly way to close the conversation.",
            ),
        ),
        (
            _line("Aphiwe", "Wenza ntoni namhlanje?", "What are you doing today?"),
            _line("You", "Ndiyasebenza namhlanje. Wena?", "I am working today. And you?"),
            _line("Aphiwe", "Nam ndiyasebenza.", "I am also working."),
            _line("You", "Sibonane ngomso.", "See you tomorrow."),
        ),
        "Wena? is an easy way to return almost any question and keep the conversation going.",
        ("xh-present-tense", "xh-conversation-turns"),
    ),
    GuidedDay(
        13,
        "a1-unit-8",
        "review",
        "Keep a conversation going",
        "Qhuba incoko",
        "Combine greeting, introduction, a question, and a rescue phrase.",
        (
            _p(
                "Ndithetha isiXhosa kancinci.",
                "I speak a little isiXhosa.",
                "Ndi·the·tha · i·si·Xho·sa · kan·ci·nci",
                "Say this early so the other person knows to slow down.",
            ),
            _p(
                "Kulungile.",
                "Okay / all right.",
                "Ku·lun·gi·le",
                "Use this to show that you understand.",
            ),
            _p(
                "Wena?",
                "And you?",
                "We·na",
                "Return the question and invite the other person to speak.",
            ),
        ),
        (
            _line("You", "Molo! Igama lam nguSam.", "Hello! My name is Sam."),
            _line("Lwazi", "Molo Sam. Unjani?", "Hello Sam. How are you?"),
            _line("You", "Ndiphilile, enkosi. Wena?", "I am well, thank you. And you?"),
            _line("Lwazi", "Nam ndiphilile.", "I am also well."),
            _line("You", "Ndithetha isiXhosa kancinci.", "I speak a little isiXhosa."),
        ),
        "A successful beginner conversation is not one without mistakes. It is one you can repair and continue.",
        ("xh-conversation-turns", "xh-present-tense", "xh-clicks"),
    ),
    GuidedDay(
        14,
        "completion-test",
        "review",
        "Your two-minute conversation",
        "Incoko yakho yemizuzu emibini",
        "Use what you know without reading a script from beginning to end.",
        (
            _p(
                "Molo! Unjani?", "Hello! How are you?", "Mo·lo · Un·ja·ni", "Open the conversation."
            ),
            _p(
                "Igama lam nguSam.",
                "My name is Sam.",
                "I·ga·ma · lam · ngu·Sam",
                "Introduce yourself; use your own name.",
            ),
            _p(
                "Ndiyavuya ukukwazi. Sibonane!",
                "Nice to meet you. See you!",
                "Ndi·ya·vu·ya · u·ku·kwa·zi · Si·bo·na·ne",
                "Close warmly.",
            ),
        ),
        (
            _line("You", "Molo! Unjani?", "Hello! How are you?"),
            _line("Partner", "Ndiphilile, enkosi. Wena?", "I am well, thank you. And you?"),
            _line("You", "Nam ndiphilile. Igama lam nguSam.", "I am also well. My name is Sam."),
            _line("Partner", "Ndiyavuya ukukwazi.", "Nice to meet you."),
            _line("You", "Ndiyavuya ukukwazi. Sibonane!", "Nice to meet you. See you!"),
        ),
        "Before revealing each answer, pause and say the isiXhosa phrase from memory. That effort is the test—and the learning.",
        ("xh-conversation-turns", "xh-copulative-ngu", "xh-polite-requests"),
    ),
)


def get_guided_xhosa_a1_day(week: int, day: int) -> GuidedDay | None:
    absolute_day = (week - 1) * 7 + day
    return next((item for item in GUIDED_XHOSA_A1_DAYS if item.day == absolute_day), None)
