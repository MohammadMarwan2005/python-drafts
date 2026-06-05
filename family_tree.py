from experta import *

# ============================================================
# FACT TYPES
# ============================================================


class Parent(Fact):
    """Parent(child=..., father=..., mother=...)"""

    pass


class Gender(Fact):
    """Gender(name=..., gender='male' | 'female')"""

    pass


class Relationship(Fact):
    """Relationship(type=..., person=..., of=...)
    Read as: <person> is <type> of <of>."""

    pass


# ============================================================
# KNOWLEDGE ENGINE
# ============================================================


class FamilyTree(KnowledgeEngine):

    # ---- Direct parents -----------------------------------
    @Rule(Parent(child=MATCH.c, father=MATCH.f))
    def father(self, c, f):
        self.declare(Relationship(type="father", person=f, of=c))

    @Rule(Parent(child=MATCH.c, mother=MATCH.m))
    def mother(self, c, m):
        self.declare(Relationship(type="mother", person=m, of=c))

    # ---- Siblings (same father AND same mother) -----------
    @Rule(
        Parent(child=MATCH.c1, father=MATCH.f, mother=MATCH.m),
        Parent(child=MATCH.c2, father=MATCH.f, mother=MATCH.m),
        Gender(name=MATCH.c2, gender="male"),
        TEST(lambda c1, c2: c1 != c2),
    )
    def brother(self, c1, c2):
        self.declare(Relationship(type="brother", person=c2, of=c1))

    @Rule(
        Parent(child=MATCH.c1, father=MATCH.f, mother=MATCH.m),
        Parent(child=MATCH.c2, father=MATCH.f, mother=MATCH.m),
        Gender(name=MATCH.c2, gender="female"),
        TEST(lambda c1, c2: c1 != c2),
    )
    def sister(self, c1, c2):
        self.declare(Relationship(type="sister", person=c2, of=c1))

    # ---- Grandparents (chained on the inferred "father") --
    @Rule(
        Relationship(type="father", person=MATCH.p, of=MATCH.c),
        Parent(child=MATCH.p, father=MATCH.gf),
    )
    def grandfather(self, c, gf):
        self.declare(Relationship(type="grandfather", person=gf, of=c))

    @Rule(
        Relationship(type="father", person=MATCH.p, of=MATCH.c),
        Parent(child=MATCH.p, mother=MATCH.gm),
    )
    def grandmother(self, c, gm):
        self.declare(Relationship(type="grandmother", person=gm, of=c))

    # ---- Mahram (mother, grandmother, or sister) ----------
    @Rule(Relationship(type="mother", person=MATCH.m, of=MATCH.x))
    def mahram_mother(self, m, x):
        self.declare(Relationship(type="mahram", person=m, of=x))

    @Rule(Relationship(type="grandmother", person=MATCH.gm, of=MATCH.x))
    def mahram_grandmother(self, gm, x):
        self.declare(Relationship(type="mahram", person=gm, of=x))

    @Rule(Relationship(type="sister", person=MATCH.s, of=MATCH.x))
    def mahram_sister(self, s, x):
        self.declare(Relationship(type="mahram", person=s, of=x))

    # ---- Print every relationship the engine infers -------
    @Rule(Relationship(type=MATCH.t, person=MATCH.p, of=MATCH.o))
    def print_rel(self, t, p, o):
        print(f"{p} is {t} of {o}")


# ============================================================
# FACTS (the family)
# ============================================================

engine = FamilyTree()
engine.reset()

# --- Children of Marwan & Sawsan ---
engine.declare(Gender(name="Mohammad", gender="male"))
engine.declare(Gender(name="Ahmed", gender="male"))
engine.declare(Gender(name="Lama", gender="female"))

engine.declare(Parent(child="Mohammad", father="Marwan", mother="Sawsan"))
engine.declare(Parent(child="Ahmed", father="Marwan", mother="Sawsan"))
engine.declare(Parent(child="Lama", father="Marwan", mother="Sawsan"))

# --- Parents ---
engine.declare(Gender(name="Marwan", gender="male"))
engine.declare(Gender(name="Sawsan", gender="female"))

# --- Grandparents (father's side) ---
engine.declare(Gender(name="Mostafa", gender="male"))
engine.declare(Gender(name="Amina", gender="female"))
engine.declare(Parent(child="Marwan", father="Mostafa", mother="Amina"))

# --- Grandparents (mother's side) ---
engine.declare(Gender(name="AbdulKareem", gender="male"))
engine.declare(Gender(name="Alia", gender="female"))
engine.declare(Parent(child="Sawsan", father="AbdulKareem", mother="Alia"))

engine.run()
