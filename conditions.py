import pip

from experta import *

class Test(KnowledgeEngine): 
    @DefFacts()
    def _initial_action(self):
        yield Fact(salary = 700)
        yield Fact(age = 20)
        yield Fact(work_hours_per_week = 14)
        yield Fact(years_of_experience = 2)
        
    # Rules: 
    # Low Salary: salary < 250
    # Mid Salary: salary >= 250 & salary < 600
    # High Salary: salary >= 600



    @Rule(
        Fact(salary = MATCH.s),
        TEST(lambda s: s< 250)
    )
    def low_salary(self, s):
        print("Low Salary:", s)
        
    @Rule(
        Fact(salary = MATCH.s),
        AND(
            TEST(lambda s: s >= 250),
            TEST(lambda s: s < 600)
        )
        )
    def mid_salary(self, s):
        print("Mid Salary:", s)
        
    @Rule(
        Fact(salary = MATCH.s),
        TEST(lambda s: s >= 600)
    )
    def high_salary(self, s):
        print("High Salary, allah yobarik:", s)
        
    
    # IsStudent: work_hours_per_week < 20 | age < 25
    
    @Rule(
        Fact(work_hours_per_week = MATCH.w),
        Fact(age = MATCH.a),
        OR(
            TEST(lambda w: w < 20),
            TEST(lambda a: a < 25)
        ),
        NOT(Fact(is_student = True))
    )
    def isStudent(self): 
        self.declare(Fact(is_student = True))
        print("You're likely a student...")
        
        
    
    
    # IsJunior: years_of_experience < 3 & age < 30
    
    @Rule(
        Fact(years_of_experience = MATCH.y),
        Fact(age = MATCH.a),
        AND(
            TEST(lambda y: y < 3),
            TEST(lambda a: a < 30)
        )
    )
    def isJunior(self):
        print("You're likely a junior...")
    
    # Overworked: work_hours_per_week > 50
    @Rule(
        Fact(work_hours_per_week = MATCH.w),
        TEST(lambda w: w > 50)
    )
    def overworked(self, w):
        print("You're likely overworked with", w, "hours per week.")
        
    # Underpaid: salary < 300 & work_hours_per_week > 40
    @Rule(
        Fact(salary = MATCH.s),
        Fact(work_hours_per_week = MATCH.w),
        AND(
            TEST(lambda s: s < 300),
            TEST(lambda w: w > 40)
        )
    )
    def underpaid(self, s, w):
        print("You're likely underpaid with a salary of", s, "and working", w, "hours per week.")
        

engine = Test()
engine.reset()
engine.run()


# python3 -m venv .venv
# source .venv/bin/activate
# pip install experta

