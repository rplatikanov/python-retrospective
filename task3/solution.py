class Person:
    def __init__(self, name, birth_year, gender, father=None, mother=None):
        self.name = name
        self.birth_year = birth_year
        self.gender = gender
        self.father = father
        self.mother = mother
        self.children_set = set()

        if self.father is not None:
            self.father.children_set.add(self)

        if self.mother is not None:
            self.mother.children_set.add(self)

    def children(self, gender=None):
        children = self.children_set
        result = []

        if gender is not None:
            result = [child for child in children if child.gender == gender]
        else:
            result = list(children)

        result.sort(key=lambda child: child.birth_year)
        return result

    def get_siblings(self, gender=None):
        siblings = set()
        if self.father is not None:
            siblings.update(self.father.children(gender))

        if self.mother is not None:
            siblings.update(self.mother.children(gender))

        if self in siblings:
            siblings.remove(self)

        return list(siblings)

    def get_brothers(self):
        return self.get_siblings(gender='M')

    def get_sisters(self):
        return self.get_siblings(gender='F')

    def is_direct_successor(self, person):
        return person.father is self or person.mother is self
