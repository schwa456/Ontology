from owlready2 import *

onto = get_ontology("http://test.o123rg/onto.owl")

# 온톨로지 내에서 코드가 작성됨.
with onto:

# Drug 클래스 생성, 알약당 가격 지정 함수 정의
  class Drug(Thing):
    def get_per_tablet_cost(self):
      return self.cost / self.number_of_tablets

# has_for_cost property 생성, 실수형, FuntionalProperty, Cost name으로 사용
  class has_for_cost(Drug >> float, FunctionalProperty):
    python_name = "cost"

  class has_for_number_of_tablets(Drug >> int, FunctionalProperty):
    python_name = "number_of_tablets"

my_drug = Drug(cost = 10.0, number_of_tablets = 5)
print(my_drug.get_per_tablet_cost())


class has_for_active_principle(Property): pass


with onto:
  class Drug(Thing): pass


  class ActivePrinciple(Thing): pass


  # has_for_active_principle속성 정의, Drug와 ActivePrinciple이 연결됨을 설정
  class has_for_active_principle(Drug >> ActivePrinciple): pass


  # Drug 개념 확장, is_a 제약변수 정의, has_for_active_principle 속성은 하나 이상의 ActivePrinciple과 관련
  class Drug(Thing):  # Extends the previous definition of Drug
    is_a = [has_for_active_principle.some(ActivePrinciple)]


  aspirin = onto.Drug("aspirin")
  acetylsalicylic_acid = onto.ActivePrinciple("acetylsalicylic_acid")
  aspirin.has_for_active_principle = [acetylsalicylic_acid]

  print(f"Drug:{aspirin.name}, activePrinciple:{aspirin.has_for_active_principle[0].name}")

  onto.save(file="my_ontology.owl", format="rdfxml")

  with onto:
    class Drug(Thing):
      pass

Drug.comment = ["A first comment on the Drug class", "A second comment"]

Drug.comment.append("A third comment")

with onto:
  class HealthProblem(Thing):
    pass


  # is_prescribed_for 속성 클래스를 정의, Drug와 HealthProblem이 관련
  class is_prescribed_for(Drug >> HealthProblem):
    pass

acetaminophen = Drug("acetaminophen")
pain = HealthProblem("pain")
acetaminophen.is_prescribed_for.append(pain)

# 관계에 주석 추가하는 anotatedRelation
AnnotatedRelation(acetaminophen, is_prescribed_for, pain).comment = ["A comment on the acetaminophen-pain relation"]