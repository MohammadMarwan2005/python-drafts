from experta import * 

mother_side_aunts = [
    "Niimaat",
    "Fatima", 
    "Mariam"
]

father_side_aunts = [
    "Aishah",
    "Huda",
    "Falha"
]

father = "Marwan"
mother = "Sawsan"
father_side_grandfather = "Mostafa"
father_side_grandmother = "Amina"
mother_side_grandfather = "AbdulKareem"
mother_side_grandmother = "Alia"

wife = None # ☹️💔

brothers = [
    "Ahmed",
    "Mostafa",
    "AbdulRahman"
]

sisters = [
    "Lama",
    "Noha",
    "Roaa"
]

class Person(Fact):
    pass

# type, person1, person2
class Relation(Fact):
    pass

def getOpositeGender(gender):
    if gender == "male":
        return "female"
    return "male"


class Family(KnowledgeEngine):
    @DefFacts()
    def initial_data(self):
        
        # -------------------------
        # PEOPLE
        # -------------------------
        yield Person(name="You", gender="male")

        yield Person(name="Marwan", gender="male")
        yield Person(name="Sawsan", gender="female")

        yield Person(name="Ahmed", gender="male")
        yield Person(name="Mostafa", gender="male")
        yield Person(name="AbdulRahman", gender="male")

        yield Person(name="Lama", gender="female")
        yield Person(name="Noha", gender="female")
        yield Person(name="Roaa", gender="female")

        # Grandparents (father side)
        yield Person(name="Mostafa_Sr", gender="male")
        yield Person(name="Amina", gender="female")

        # Grandparents (mother side)
        yield Person(name="AbdulKareem", gender="male")
        yield Person(name="Alia", gender="female")

        # Father's sisters
        yield Person(name="Aishah", gender="female")
        yield Person(name="Huda", gender="female")
        yield Person(name="Falha", gender="female")

        # Mother's sisters
        yield Person(name="Niimaat", gender="female")
        yield Person(name="Fatima", gender="female")
        yield Person(name="Mariam", gender="female")

        # -------------------------
        # PARENT RELATIONSHIPS
        # -------------------------

        # Parents of You + siblings
        for child in ["You", "Ahmed", "Mostafa", "AbdulRahman", "Lama", "Noha", "Roaa"]:
            yield Relation(type="parent", person=child, related="Marwan")
            yield Relation(type="parent", person=child, related="Sawsan")

        # Grandparents → Marwan
        yield Relation(type="parent", person="Marwan", related="Mostafa_Sr")
        yield Relation(type="parent", person="Marwan", related="Amina")

        # Grandparents → Sawsan
        yield Relation(type="parent", person="Sawsan", related="AbdulKareem")
        yield Relation(type="parent", person="Sawsan", related="Alia")

        # Father side aunts (siblings of Marwan)
        for aunt in ["Aishah", "Huda", "Falha"]:
            yield Relation(type="sibling", person="Marwan", related=aunt)

        # Mother side aunts (siblings of Sawsan)
        for aunt in ["Niimaat", "Fatima", "Mariam"]:
            yield Relation(type="sibling", person="Sawsan", related=aunt)
            
        # Fake neice: Aya
        yield Person(name="Aya", gender="female")
        yield Relation(type="parent", person="Aya", related="Ahmed")    
            
    @Rule(
        Person(name = "You"),
        Relation(type = "parent", person = "You", related = MATCH.f),
        Person(name = MATCH.f, gender = "male")
        )
    def find_father(self, f):
        print("Found your father: ", f) 
        
        
    @Rule(
        Person(name = "You"),
        Relation(type = "parent", person = "You", related = MATCH.m),
        Person(name = MATCH.m, gender = "female")
    )
    def find_mother(self, m):
        print("Found your mother: ", m)
        
    @Rule(
        Person(name = "You"),
        Relation(type = "parent", person = "You", related = MATCH.parent),
        Relation(type = "parent", person = MATCH.child, related = MATCH.parent),
        TEST(lambda child: child != "You"),
        NOT(Relation(type="sibling", person="You", related=MATCH.child))
    )
    def inference_siblings(self, child, parent):
        self.declare(Relation(type="sibling", person="You", related=child))        
        # print("Found your sibling: ", child)
    
    
    @Rule(
        Person(name = "You"),
        Relation(type = "parent", person = "You", related = MATCH.parent_name),
        Relation(type = "sibling", person = MATCH.parent_name, related = MATCH.aunt_name),
        Person(name = MATCH.aunt_name, gender = MATCH.aunt_gender),
        TEST(lambda aunt_gender: aunt_gender == "female"),
        NOT(Relation(type = "aunt", person = "You", related = MATCH.aunt_name))
    )
    def inference_aunts(self, aunt_name): 
        self.declare(Relation(type="aunt", person="You", related=aunt_name))
        # print("Found your aunt: ", aunt_name)
        
        
    @Rule(
        Person(name = "You"),
        Relation(type = "parent", person = "You", related = MATCH.parent_name),
        Relation(type = "parent", person = MATCH.parent_name, related = MATCH.grandparent_name),
        NOT(Relation(type = "grandparent", person = "You", related = MATCH.grandparent_name)),
    )
    def inference_grandparents(self, grandparent_name): 
        self.declare(Relation(type="grandparent", person="You", related=grandparent_name))
        # print("Found your grandparent: ", grandparent_name)
    
    @Rule(
        Person(name = "You"),
        Relation(type = "sibling", person = "You", related = MATCH.sibling_name),
        Relation(type = "parent", person = MATCH.niece_name, related = MATCH.sibling_name),
        NOT(Relation(type = "niece", person = "You", related = MATCH.niece_name))
    )
    def inference_nieces(self, niece_name): 
        self.declare(Relation(type="niece", person = "You", related=niece_name))
        # print("niece: ", niece_name)
        
    @Rule(
        Person(name = "You"),
        Relation(type = MATCH.type, person = "You", related = MATCH.related),
        Person(name = MATCH.related, gender = MATCH.gender),
        TEST(lambda gender: gender == "female"),
        OR(
            TEST(lambda type: type == "parent"),
            TEST(lambda type: type == "sibling"),
            TEST(lambda type: type == "aunt"),
            TEST(lambda type: type == "grandparent"),
            TEST(lambda type: type == "niece"),
        )
    )
    def find_mahrim(self, related, type): 
        # maharim = 
        # 1. mom
        # 2. sisters 
        # 3. aunts (both sides)
        # 4. grandparents (both sides)
        # 5. nieces (if any)
        
        print("Found a mahrim: ", related, " - ", type)
        
    

engine = Family()
engine.reset()
engine.run()
        
        
    