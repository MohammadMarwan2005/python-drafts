from experta import *


class Parent(Fact):
    pass


class Gender(Fact):
    pass


class Relationship(Fact):
    pass


class FamilyTree(KnowledgeEngine):

    @DefFacts()
    def seed(self):
        yield Fact(action="infer")

    # Father
    @Rule(Fact(action="infer"), Parent(child=MATCH.c, father=MATCH.f))
    def father(self, c, f):
        self.declare(Relationship(type="father", person=f, of=c))

    # Mother
    @Rule(Fact(action="infer"), Parent(child=MATCH.c, mother=MATCH.m))
    def mother(self, c, m):
        self.declare(Relationship(type="mother", person=m, of=c))

    # Brother
    @Rule(
        Fact(action="infer"),
        Parent(child=MATCH.c1, father=MATCH.f, mother=MATCH.m),
        Parent(child=MATCH.c2, father=MATCH.f, mother=MATCH.m),
        Gender(name=MATCH.c2, gender="male"),
        TEST(lambda c1, c2: c1 != c2),
    )
    def brother(self, c1, c2):
        self.declare(Relationship(type="brother", person=c2, of=c1))

    # Sister
    @Rule(
        Fact(action="infer"),
        Parent(child=MATCH.c1, father=MATCH.f, mother=MATCH.m),
        Parent(child=MATCH.c2, father=MATCH.f, mother=MATCH.m),
        Gender(name=MATCH.c2, gender="female"),
        TEST(lambda c1, c2: c1 != c2),
    )
    def sister(self, c1, c2):
        self.declare(Relationship(type="sister", person=c2, of=c1))

    # Grandfather
    @Rule(
        Relationship(type="father", person=MATCH.p, of=MATCH.c),
        Parent(child=MATCH.p, father=MATCH.gf),
    )
    def grandfather(self, c, gf):
        self.declare(Relationship(type="grandfather", person=gf, of=c))

    # Grandmother
    @Rule(
        Relationship(type="father", person=MATCH.p, of=MATCH.c),
        Parent(child=MATCH.p, mother=MATCH.gm),
    )
    def grandmother(self, c, gm):
        self.declare(Relationship(type="grandmother", person=gm, of=c))

    # Maharem
    @Rule(Relationship(type="mother", person=MATCH.m, of=MATCH.x))
    def mahram_mother(self, m, x):
        self.declare(Relationship(type="mahram", person=m, of=x))

    @Rule(Relationship(type="grandmother", person=MATCH.gm, of=MATCH.x))
    def mahram_grandmother(self, gm, x):
        self.declare(Relationship(type="mahram", person=gm, of=x))

    @Rule(Relationship(type="sister", person=MATCH.s, of=MATCH.x))
    def mahram_sister(self, s, x):
        self.declare(Relationship(type="mahram", person=s, of=x))

    # PRINT
    @Rule(Relationship(type=MATCH.t, person=MATCH.p, of=MATCH.o))
    def print_rel(self, t, p, o):
        print(f"{p} is {t} of {o}")
