from experta import *


class neighbor(Fact):
    pass


class holds(Fact):
    pass


class OrderNumber(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield neighbor(left="M.DH", right="M.GH")
        yield neighbor(left="M.GH", right="M.Marwan")
        yield neighbor(left="M.Marwan", right="M.SH")
        yield neighbor(left="M.SH", right="M.JA")
        yield neighbor(left="M.JA", right="M.KA")

        yield holds(person="M.DH", number=82)
        yield holds(person="M.GH", number=29)
        yield holds(person="M.Marwan", number=46)
        yield holds(person="M.SH", number=50)
        yield holds(person="M.JA", number=68)
        yield holds(person="M.KA", number=59)

    @Rule(
        neighbor(left=MATCH.a, right=MATCH.b),
        AS.Ahas << holds(person=MATCH.a, number=MATCH.x),
        AS.Bhas << holds(person=MATCH.b, number=MATCH.y),
        TEST(lambda x, y: y > x),
    )
    def swap(self, Ahas, Bhas, x, y):
        print("Swapping {} and {}".format(Ahas["person"], Bhas["person"]))
        self.modify(Ahas, number=y)
        self.modify(Bhas, number=x)


o_n = OrderNumber()
o_n.reset()
o_n.run()
watch("ACTIVATIONS")

print("\nFinal numbers:")
for fact in o_n.facts.values():
    if isinstance(fact, holds):
        print("  {}: {}".format(fact["person"], fact["number"]))
