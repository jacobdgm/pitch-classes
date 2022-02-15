import unittest
from pitchclasses import (
    PitchClassSet,
    PitchClassSequence,
    IntervalVector,
    IntervalSequence,
    aggregate,
    maximally_distributed,
)


class PitchClassSetTest(unittest.TestCase):
    def test_init(self):
        test_set = PitchClassSet([0])
        self.assertIsInstance(test_set, PitchClassSet)

    def test_attribute_types(self):
        test_set = PitchClassSet([0])
        self.assertIsInstance(test_set.pcs, list)
        self.assertIsInstance(test_set.univ, int)
        self.assertIsInstance(test_set.cardinality, int)

    def test_set_pcs(self):
        test_set = PitchClassSet([0])
        test_set.set_pcs([1, 0])
        self.assertEqual(test_set.pcs, [0, 1])  # pcs should be sorted
        self.assertEqual(test_set.cardinality, 2)

    def test_magic_sub(self):
        test_set_0 = PitchClassSet([0, 1, 2])
        with self.assertRaises(TypeError):
            test_set_0 - 1
        test_set_1 = PitchClassSet([2, 3])
        returned_0 = test_set_0 - test_set_1
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [0, 1])
        test_set_2 = PitchClassSet([1, 2], univ=4)
        with self.assertRaises(ValueError):
            test_set_0 - test_set_2

    def test_magic_and(self):
        test_set_0 = PitchClassSet([0, 1, 2])
        with self.assertRaises(TypeError):
            test_set_0 & 1
        test_set_1 = PitchClassSet([1, 2, 3])
        returned_0 = test_set_0 & test_set_1
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [1, 2])
        test_set_2 = PitchClassSet([1, 2], univ=4)
        with self.assertRaises(ValueError):
            test_set_0 & test_set_2

    def test_magic_xor(self):
        test_set_0 = PitchClassSet([0, 1, 2])
        with self.assertRaises(TypeError):
            test_set_0 ^ 1
        test_set_1 = PitchClassSet([1, 2, 3])
        returned_0 = test_set_0 ^ test_set_1
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [0, 3])
        test_set_2 = PitchClassSet([1, 2], univ=4)
        with self.assertRaises(ValueError):
            test_set_0 ^ test_set_2

    def test_magic_or(self):
        test_set_0 = PitchClassSet([0, 1, 2])
        with self.assertRaises(TypeError):
            test_set_0 | 1
        test_set_1 = PitchClassSet([1, 2, 3])
        returned_0 = test_set_0 | test_set_1
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [0, 1, 2, 3])
        test_set_2 = PitchClassSet([1, 2], univ=4)
        with self.assertRaises(ValueError):
            test_set_0 | test_set_2

    def test_private_transposed(self):
        test_set = PitchClassSet([0, 1, 2])
        returned_0 = test_set._transposed(1)
        self.assertIsInstance(returned_0, list)
        self.assertEqual(returned_0, [1, 2, 3])
        returned_1 = test_set._transposed(11)
        self.assertEqual(returned_1, [11, 0, 1])  # pcs should not be sorted

    def test_transposed(self):
        test_set = PitchClassSet([0, 1, 2])
        returned_0 = test_set.transposed(1)
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [1, 2, 3])
        returned_1 = test_set.transposed(11)
        self.assertEqual(returned_1.pcs, [0, 1, 11])

    def test_transpose(self):
        test_set = PitchClassSet([0, 1, 2])
        test_set.transpose(1)
        self.assertEqual(test_set.pcs, [1, 2, 3])
        test_set.transpose(10)
        self.assertEqual(test_set.pcs, [0, 1, 11])

    def test_private_inverted(self):
        test_set = PitchClassSet([0, 1, 2])
        returned_0 = test_set._inverted(0)
        self.assertIsInstance(returned_0, list)
        self.assertEqual(returned_0, [0, 11, 10])  # pcs should not be sorted
        returned_1 = test_set._inverted(2)
        self.assertEqual(returned_1, [2, 1, 0])

    def test_inverted(self):
        test_set = PitchClassSet([0, 1, 2])
        returned_0 = test_set.inverted(0)
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [0, 10, 11])  # pcs should be sorted
        returned_1 = test_set.inverted(2)
        self.assertEqual(returned_1.pcs, [0, 1, 2])

    def test_invert(self):
        test_set = PitchClassSet([0, 1, 2])
        test_set.invert(0)
        self.assertEqual(test_set.pcs, [0, 10, 11])
        test_set.invert(10)
        self.assertEqual(test_set.pcs, [0, 10, 11])

    def test_private_m_transformed(self):
        test_set = PitchClassSet([0, 1, 2])
        returned_0 = test_set._m_transformed(5)
        self.assertIsInstance(returned_0, list)
        self.assertEqual(returned_0, [0, 5, 10])
        returned_1 = test_set._m_transformed(11)
        self.assertEqual(returned_1, [0, 11, 10])

    def test_m_transformed(self):
        test_set = PitchClassSet([0, 1, 2])
        returned_0 = test_set.m_transformed(5)
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [0, 5, 10])
        returned_1 = test_set.m_transformed(11)
        self.assertEqual(returned_1.pcs, [0, 10, 11])

    def test_m_transform(self):
        test_set = PitchClassSet([0, 1, 2])
        test_set.m_transform(5)
        self.assertEqual(test_set.pcs, [0, 5, 10])
        test_set.m_transform(11)
        self.assertEqual(test_set.pcs, [0, 2, 7])

    def test_private_as_univ(self):
        test_set = aggregate(5)
        with self.assertRaises(ValueError):
            test_set._as_univ(12)  # default mode should be 'e'
        returned_0 = test_set._as_univ(12, "d")
        self.assertIsInstance(returned_0, list)
        self.assertEqual(returned_0, [0])
        returned_1 = test_set._as_univ(12, "f")
        self.assertEqual(returned_1, [0, 2, 4, 7, 9])
        returned_2 = test_set._as_univ(12, "r")
        self.assertEqual(returned_2, [0, 2, 5, 7, 10])
        returned_3 = test_set._as_univ(12, "c")
        self.assertEqual(returned_3, [0, 3, 5, 8, 10])

    def test_as_univ(self):
        test_set = aggregate(7)
        with self.assertRaises(ValueError):
            test_set._as_univ(12)  # default mode should be 'e'
        returned_0 = test_set.as_univ(12, "d")
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.univ, 12)
        self.assertEqual(returned_0.pcs, [0])
        returned_1 = test_set.as_univ(12, "f")
        self.assertEqual(returned_1.pcs, [0, 1, 3, 5, 6, 8, 10])
        returned_2 = test_set.as_univ(12, "r")
        self.assertEqual(returned_2.pcs, [0, 2, 3, 5, 7, 9, 10])
        returned_3 = test_set.as_univ(12, "c")
        self.assertEqual(returned_3.pcs, [0, 2, 4, 6, 7, 9, 11])

    def test_set_univ(self):
        test_set_0 = aggregate(3)
        test_set_0.set_univ(6)
        self.assertEqual(test_set_0.univ, 6)
        self.assertEqual(test_set_0.pcs, [0, 2, 4])
        test_set_1 = PitchClassSet([0, 4, 7, 10])
        test_set_1.set_univ(6, "d")
        self.assertEqual(test_set_1.pcs, [0, 2, 5])

    def test_complement(self):
        test_set_0 = PitchClassSet([0, 1, 2])
        returned_0 = test_set_0.complement()
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [3, 4, 5, 6, 7, 8, 9, 10, 11])
        test_set_1 = PitchClassSet([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        returned_1 = test_set_1.complement()
        self.assertEqual(returned_1.pcs, [])

    def test_vector(self):
        test_set_0 = PitchClassSet([0, 1, 2])
        returned_0 = test_set_0.vector()
        self.assertIsInstance(returned_0, IntervalVector)
        self.assertEqual(returned_0.intervals, [2, 1, 0, 0, 0, 0])
        test_set_1 = PitchClassSet([0, 2, 4, 5, 7, 9, 11])
        returned_1 = test_set_1.vector()
        self.assertEqual(returned_1.intervals, [2, 5, 4, 3, 6, 1])


class PitchClassSequenceTest(unittest.TestCase):
    def test_init(self):
        test_sequence = PitchClassSequence([0])
        self.assertIsInstance(test_sequence, PitchClassSequence)

    def test_attribute_types(self):
        test_sequence = PitchClassSequence([0])
        self.assertIsInstance(test_sequence.pcs, list)
        self.assertIsInstance(test_sequence.univ, int)

    def test_set_pcs(self):
        test_sequence = PitchClassSequence([0])
        test_sequence.set_pcs([0, 1, 0])
        self.assertEqual(test_sequence.pcs, [0, 1, 0])

    def test_magic_add(self):
        test_sequence_0 = PitchClassSequence([0, 1, 2])
        test_sequence_1 = PitchClassSequence([1, 2])
        returned_0 = test_sequence_0 + test_sequence_1
        self.assertIsInstance(returned_0, PitchClassSequence)
        self.assertEqual(returned_0.pcs, [0, 1, 2, 1, 2])
        returned_1 = test_sequence_1 + test_sequence_0
        self.assertEqual(returned_1.pcs, [1, 2, 0, 1, 2])

    def test_extend(self):
        test_sequence_0 = PitchClassSequence([0, 1, 2])
        test_sequence_1 = PitchClassSequence([1, 2])
        test_sequence_0.extend(test_sequence_1)
        self.assertEqual(test_sequence_0.pcs, [0, 1, 2, 1, 2])

    def test_append(self):
        test_sequence_0 = PitchClassSequence([0, 1, 2])
        test_sequence_0.append(5)
        self.assertEqual(test_sequence_0.pcs, [0, 1, 2, 5])
        with self.assertRaises(TypeError):
            test_sequence_0.append(4.0)

    def test_private_transposed(self):
        test_sequence = PitchClassSequence([0, 1, 0])
        returned_0 = test_sequence._transposed(1)
        self.assertIsInstance(returned_0, list)
        self.assertEqual(returned_0, [1, 2, 1])
        returned_1 = test_sequence._transposed(11)
        self.assertEqual(returned_1, [11, 0, 11])

    def test_transposed(self):
        test_sequence = PitchClassSequence([0, 1, 0])
        returned_0 = test_sequence.transposed(1)
        self.assertIsInstance(returned_0, PitchClassSequence)
        self.assertEqual(returned_0.pcs, [1, 2, 1])
        returned_1 = test_sequence.transposed(11)
        self.assertEqual(returned_1.pcs, [11, 0, 11])

    def test_transpose(self):
        test_sequence = PitchClassSequence([0, 1, 2])
        test_sequence.transpose(1)
        self.assertEqual(test_sequence.pcs, [1, 2, 3])
        test_sequence.transpose(10)
        self.assertEqual(test_sequence.pcs, [11, 0, 1])

    def test_private_inverted(self):
        test_sequence = PitchClassSequence([0, 1, 2])
        returned_0 = test_sequence._inverted(0)
        self.assertIsInstance(returned_0, list)
        self.assertEqual(returned_0, [0, 11, 10])
        returned_1 = test_sequence._inverted(2)
        self.assertEqual(returned_1, [2, 1, 0])

    def test_inverted(self):
        test_sequence = PitchClassSequence([0, 1, 0])
        returned_0 = test_sequence.inverted(0)
        self.assertIsInstance(returned_0, PitchClassSequence)
        self.assertEqual(returned_0.pcs, [0, 11, 0])
        returned_1 = test_sequence.inverted(2)
        self.assertEqual(returned_1.pcs, [2, 1, 2])

    def test_invert(self):
        test_sequence = PitchClassSequence([0, 1, 0])
        test_sequence.invert(0)
        self.assertEqual(test_sequence.pcs, [0, 11, 0])
        test_sequence.invert(10)
        self.assertEqual(test_sequence.pcs, [10, 11, 10])

    def test_private_m_transformed(self):
        test_sequence = PitchClassSequence([0, 2, 0])
        returned_0 = test_sequence._m_transformed(5)
        self.assertIsInstance(returned_0, list)
        self.assertEqual(returned_0, [0, 10, 0])
        returned_1 = test_sequence._m_transformed(11)
        self.assertEqual(returned_1, [0, 10, 0])

    def test_m_transformed(self):
        test_sequence = PitchClassSequence([0, 3, 0])
        returned_0 = test_sequence.m_transformed(5)
        self.assertIsInstance(returned_0, PitchClassSequence)
        self.assertEqual(returned_0.pcs, [0, 3, 0])
        returned_1 = test_sequence.m_transformed(11)
        self.assertEqual(returned_1.pcs, [0, 9, 0])

    def test_m_transform(self):
        test_sequence = PitchClassSequence([0, 4, 0])
        test_sequence.m_transform(5)
        self.assertEqual(test_sequence.pcs, [0, 8, 0])
        test_sequence.m_transform(11)
        self.assertEqual(test_sequence.pcs, [0, 4, 0])

    def test_pc_inventory(self):
        test_sequence = PitchClassSequence([0, 1, 2, 0])
        returned_0 = test_sequence.pc_inventory()
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [0, 1, 2])

    def test_private_retrograded(self):
        test_sequence = PitchClassSequence([0, 1, 2, 0])
        returned_0 = test_sequence._retrograded()
        self.assertIsInstance(returned_0, list)
        self.assertEqual(returned_0, [0, 2, 1, 0])

    def test_retrograded(self):
        test_sequence = PitchClassSequence([0, 1, 3, 0])
        returned_0 = test_sequence.retrograded()
        self.assertIsInstance(returned_0, PitchClassSequence)
        self.assertEqual(returned_0.pcs, [0, 3, 1, 0])

    def test_retrograde(self):
        test_sequence = PitchClassSequence([0, 1, 4, 0])
        test_sequence.retrograde()
        self.assertEqual(test_sequence.pcs, [0, 4, 1, 0])

    def test_private_as_univ(self):
        test_sequence = PitchClassSequence([0, 2, 4, 0])
        returned = test_sequence._as_univ(6)
        self.assertIsInstance(returned, list)
        self.assertEqual(returned, [0, 1, 2, 0])

    def test_as_univ(self):
        test_sequence = PitchClassSequence([0, 1, 2, 0], univ=8)
        returned = test_sequence.as_univ(16)
        self.assertIsInstance(returned, PitchClassSequence)
        self.assertEqual(returned.pcs, [0, 2, 4, 0])

    def test_set_univ(self):
        test_sequence = PitchClassSequence([7, 7, 7, 3])
        test_sequence.set_univ(24)
        self.assertEqual(test_sequence.univ, 24)
        self.assertEqual(test_sequence.pcs, [14, 14, 14, 6])

    def test_intervals(self):
        test_sequence_0 = PitchClassSequence([0, 1, 3])
        returned_0 = test_sequence_0.intervals()
        self.assertIsInstance(returned_0, IntervalSequence)
        self.assertEqual(returned_0.intervals, [1, 2])
        test_sequence_1 = PitchClassSequence([3, 1, 0])
        returned_1 = test_sequence_1.intervals()
        self.assertEqual(returned_1.intervals, [10, 11])


class IntervalSequenceTest(unittest.TestCase):
    def test_melody(self):
        test_sequence_0 = IntervalSequence([1, 2])
        returned_0 = test_sequence_0.melody(0)
        self.assertIsInstance(returned_0, PitchClassSequence)
        self.assertEqual(returned_0.pcs, [0, 1, 3])
        returned_1 = test_sequence_0.melody(11)
        self.assertEqual(returned_1.pcs, [11, 0, 2])

    def test_private_inverted(self):
        test_sequence_0 = IntervalSequence([1, 4])
        returned_0 = test_sequence_0._inverted()
        self.assertIsInstance(returned_0, list)
        self.assertEqual(returned_0, [11, 8])

    def test_inverted(self):
        test_sequence_0 = IntervalSequence([1, 5])
        returned_0 = test_sequence_0.inverted()
        self.assertIsInstance(returned_0, IntervalSequence)
        self.assertEqual(returned_0.intervals, [11, 7])

    def test_invert(self):
        test_sequence_0 = IntervalSequence([1, 6])
        test_sequence_0.invert()
        self.assertEqual(test_sequence_0.intervals, [11, 6])
    def test_private_retrograded(self):
        test_sequence_0 = IntervalSequence([1, 4])
        returned_0 = test_sequence_0._retrograded()
        self.assertIsInstance(returned_0, list)
        self.assertEqual(returned_0, [8, 11])

    def test_retrograded(self):
        test_sequence_0 = IntervalSequence([1, 5])
        returned_0 = test_sequence_0.retrograded()
        self.assertIsInstance(returned_0, IntervalSequence)
        self.assertEqual(returned_0.intervals, [7, 11])

    def test_retrograde(self):
        test_sequence_0 = IntervalSequence([1, 6])
        test_sequence_0.retrograde()
        self.assertEqual(test_sequence_0.intervals, [6, 11])


class FunctionsTest(unittest.TestCase):
    def test_aggregate(self):
        returned_0 = aggregate(12)
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.assertEqual(returned_0.univ, 12)
        returned_1 = aggregate(4)
        self.assertEqual(returned_1.pcs, [0, 1, 2, 3])
        self.assertEqual(returned_1.univ, 4)

    def test_maximally_distributed(self):
        returned_0 = maximally_distributed(7)
        self.assertIsInstance(returned_0, PitchClassSet)
        self.assertEqual(returned_0.pcs, [0, 1, 3, 5, 6, 8, 10])
        returned_1 = maximally_distributed(5)
        self.assertEqual(returned_1.pcs, [0, 2, 4, 7, 9])
        returned_2 = maximally_distributed(3, 7)
        self.assertEqual(returned_2.univ, 7)
        self.assertEqual(returned_2.pcs, [0, 2, 4])


if __name__ == "__main__":
    unittest.main(exit=False)
