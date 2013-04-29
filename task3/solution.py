class Person:
    def __init__(self, name, birth_year, gender, father=None, mother=None):
        self.name = name
        self.birth_year = birth_year
        self.gender = gender
        self.father = father
        self.mother = mother
        self._children = set()

        if self.father is not None:
            self.father._children.add(self)

        if self.mother is not None:
            self.mother._children.add(self)

    def children(self, gender=None):
        children = self._children
        result = []

        if gender is not None:
            result = [child for child in children if child.gender == gender]
        else:
            result = list(children)

        result.sort(key=lambda child: child.birth_year)
        return result

    def _get_siblings(self, gender=None):
        """Returns all the siblings of the person or only the
        brothers/sisters if a gender argument is passed."""

        siblings = set()
        if self.father is not None:
            siblings.update(self.father.children(gender))

        if self.mother is not None:
            siblings.update(self.mother.children(gender))

        if self in siblings:
            siblings.remove(self)

        return list(siblings)

    def get_brothers(self):
        return self._get_siblings(gender='M')

    def get_sisters(self):
        return self._get_siblings(gender='F')

    def is_direct_successor(self, person):
        return person in self._children
