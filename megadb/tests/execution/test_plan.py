import unittest
from megadb.execution.plan import *
from megadb.algebra.plan import Comparison

class SchemaTestCase(unittest.TestCase):
    def test_load(self):
        schema = Schema()
        schema.load()

        self.assertTrue(len(schema.relations) > 0)

class PlanTestCase(unittest.TestCase):
    def setUp(self):
        self.schema = Schema()
        self.schema.load()

        print "Schema is ready..."

    def test_relation(self):
        alpha = Relation(None, 'Alpha', self.schema.relations['Alpha'])

        with alpha:
            it = alpha.iterate()
            for s in it:
                print s

    def test_projection(self):
        fields = [name for (name, type) in self.schema.relations['Alpha'][0:2]]
        projection = Projection(None, fields)
        alpha = Relation(projection, 'Alpha', self.schema.relations['Alpha'])

        with projection:
            it = projection.iterate()
            for t in it:
                print t

    def test_selection_one_cond(self):
        selection = Selection(None, [Comparison('a1', '3', '=')])
        alpha = Relation(selection, 'Alpha', self.schema.relations['Alpha'])

        with selection:
            it = selection.iterate()
            for t in it:
                print t

    def test_selection_two_cond(self):
        selection = Selection(None, [Comparison('a1', '3', '='), Comparison('a2', 'cc', '=')])
        alpha = Relation(selection, 'Alpha', self.schema.relations['Alpha'])

        with selection:
            it = selection.iterate()
            for t in it:
                print t

    def test_selection_then_projection(self):
        fields = [name for (name, type) in self.schema.relations['Alpha'][1:]]
        projection = Projection(None, fields)
        selection = Selection(projection, [Comparison('a1', '3', '=')])
        alpha = Relation(selection, 'Alpha', self.schema.relations['Alpha'])

        with projection:
            it = projection.iterate()
            for t in it:
                print t

    def test_cross_join_then_selection(self):
        selection = Selection(None, [Comparison('a1', '3', '=')])
        cross_join = CrossJoin(selection)
        alpha = Relation(cross_join, 'Alpha', self.schema.relations['Alpha'])
        beta = Relation(cross_join, 'Beta', self.schema.relations['Beta'])

        with selection:
            it = selection.iterate()
            for t in it:
                print t


