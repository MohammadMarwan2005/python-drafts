from experta import *


class Answer(Fact):
    pass


class question(Fact):
    pass


class need_answer(Fact):
    pass


class DiagnosticExpert(KnowledgeEngine):

    def recommend_action(self, action):
        # "Give final instructions to the user"
        print("I recommend that you " + action + "\n")

    @DefFacts()
    def init(self, **kwargs):
        yield question(
            ident="hardware",
            Type="multi",
            valid=["x86", "Macintosh", "other"],
            text="What kind of hardware is it?",
        )

        yield question(
            ident="sound",
            Type="multi",
            valid=["yes", "no"],
            text="Does the computer make any sound?",
        )

        yield question(
            ident="plugged-in",
            Type="multi",
            valid=["yes", "no"],
            text="Is the computer plugged in?",
        )

        yield question(
            ident="seek",
            Type="multi",
            valid=["yes", "no"],
            text='Does the disk make "seeking" sounds?',
        )

        yield question(
            ident="does-beep",
            Type="multi",
            valid=["yes", "no"],
            text="Does the computer beep?",
        )

        yield question(
            ident="how-many-beeps",
            Type="number",
            valid="0",
            text="How many times does it beep",
        )

        yield question(
            ident="loose-ram",
            Type="multi",
            valid=["yes", "no"],
            text="Are any of the memory modules loose?p",
        )

        yield question(
            ident="boot-begins",
            Type="multi",
            valid=["yes", "no"],
            text="Does the computer begin to boot?",
        )

    @Rule(NOT(Answer(ident=L("hardware"))), NOT(Fact(ask=L("hardware"))))
    def supply_answer_hw(self):
        self.declare(Fact(ask="hardware"))

    @Rule(Answer(ident=L("hardware"), text=~L("x86")))
    def false_architecture(self):
        self.recommend_action("consult a human expert")
        self.halt()

    @Rule(Answer(ident=L("hardware"), text=L("x86")))
    def right_architecture(self):
        self.declare(Fact(ask="seek"))

    @Rule(
        Answer(ident=L("sound"), text=L("no")),
        Answer(ident=L("plugged-in"), text=L("no")),
    )
    def not_plugged_in(self):
        self.recommend_action("plug in the computer")
        self.halt()

    @Rule(
        Answer(ident=L("sound"), text=L("no")),
        Answer(ident=L("plugged-in"), text=L("yes")),
    )
    def power_supply_broken(self):
        self.recommend_action("repair or replace power supply")
        self.halt()

    @Rule(Answer(ident="sound"), NOT(Answer(ident="plugged-in")))
    def supply_answer_plugged_in(self):
        self.declare(Fact(ask="plugged-in"))

    @Rule(Answer(ident="seek", text="yes"), NOT(Answer(ident="boot-begins")))
    def supply_answer_boot_begin(self):
        self.declare(Fact(ask="boot-begins"))

    @Rule(Answer(ident="seek", text="no"), NOT(Answer(ident="does-beep")))
    def supply_answer_does_beep(self):
        self.declare(Fact(ask="does-beep"))

    @Rule(Answer(ident="boot-begins", text="yes"), NOT(Answer(ident="sound")))
    def supply_answer_make_sound(self):
        self.declare(Fact(ask="sound"))

    @Rule(
        Answer(ident="seek", text="no"),
        Answer(ident="does-beep", text="yes"),
    )
    def how_many_beeps(self):
        # "Ask a question and assert the answer""
        self.declare(Fact(ask="how-many-beeps"))

    @Rule(
        Answer(ident="seek", text="no"),
        Answer(ident="does-beep", text="yes"),
        Answer(ident="how-many-beeps", text=MATCH.t),
        TEST(lambda t: int(t) < 3),
    )
    def check_ram(self):
        self.declare(Fact(ask="loose-ram"))

    def ask_user(self, question, Type, valid=None):
        # "Ask a question, and return the answer"
        answer = ""
        while not (self.is_of_type(answer, Type, valid)):
            print(question)
            if Type == "multi":
                print("Valid answers are ")
                for item in valid:
                    print(str(item) + " ")
                print("\n")
            answer = input()
        return answer

    def is_a_number(self, answer):
        try:
            int(answer)
            return True
        except:
            return False

    def is_of_type(self, answer, Type, valid):
        # "Check that the answer has the right form"
        if Type == "multi":
            for item in valid:
                if answer == item:
                    return True
            return False
        if Type == "number":
            return self.is_a_number(answer)
        return len(answer) > 0

    @Rule(
        question(ident=MATCH.id, text=MATCH.text, valid=MATCH.valid, Type=MATCH.Type),
        NOT(Answer(ident=MATCH.id)),
        AS.ask << Fact(ask=MATCH.id),
    )
    def ask_question_by_id(self, ask, id, text, valid, Type):
        # "Ask a question and assert the answer""
        self.retract(ask)
        answer = self.ask_user(text, Type, valid)
        self.declare(Answer(ident=id, text=answer))

    ##############################333

    @Rule(
        Answer(ident="sound", text="yes"),
        Answer(ident="seek", text="no"),
        Answer(ident="does-beep", text="yes"),
        Answer(ident="how-many-beeps", text=MATCH.t),  # GE(3)
        TEST(lambda t: int(t) >= 3),
    )
    def motherboard_or_keyboard(self, ask, id, text, valid, Type):
        # "Ask a question and assert the answer""
        self.recommend_action("check keyboard and motherboard")
        self.halt()

    #####################################3
    @Rule(
        Answer(ident="seek", text="no"),
        Answer(ident="does-beep", text="yes"),
        Answer(ident="how-many-beeps", text=MATCH.t),
        Answer(ident="loose-ram", text="yes"),
        TEST(lambda t: int(t) < 3),
    )
    def is_ram_loose(self):
        self.recommend_action("remove and reseat memory modules")
        self.halt()

    @Rule(
        Answer(ident="seek", text="no"),
        Answer(ident="does-beep", text="yes"),
        Answer(ident="how-many-beeps", text=MATCH.t),
        Answer(ident="loose-ram", text="no"),
        TEST(lambda t: int(t) < 3),
    )
    def isnot_ram_loose(self):
        self.recommend_action("replace memory module ony by one")
        self.halt()

    @Rule(
        Answer(ident="sound", text="yes"),
        Answer(ident="seek", text="no"),
        Answer(ident="does-beep", text="no"),
    )
    def unknown_sound(self):
        self.recommend_action("consult a human expert")
        self.halt()

    @Rule(
        Answer(ident="sound", text="yes"),
        Answer(ident="seek", text="yes"),
        Answer(ident="boot-begins", text="no"),
    )
    def no_boot_start(self):
        self.recommend_action("check keyboard, RAM, motherboard, and power supply")
        self.halt()

    @Rule(
        Answer(ident="sound", text="yes"),
        Answer(ident="seek", text="yes"),
        Answer(ident="boot-begins", text="yes"),
    )
    def boot_start(self):
        self.recommend_action("consult a software expert")
        self.halt()


engine = DiagnosticExpert()
engine.reset()
engine.run()
