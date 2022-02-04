PC_UNIVERSE = 12


class PitchClasses:
    def _transposed(self, i):
        return [(self.pcs[x] + i) % self.univ for x, _ in enumerate(self.pcs)]

    def _inverted(self, i):
        return [(i - pc) % self.univ for pc in self.pcs]

    def _m_transformed(self, i):
        return [(pc * i) % self.univ for pc in self.pcs]


class PitchClassSet(PitchClasses):
    def __init__(self, pcs, univ=0):
        if univ == 0:
            self.univ = PC_UNIVERSE
        else:
            self.univ = univ
        self.set_pcs(pcs)

    def __repr__(self):
        return "PitchClassSet " + str(self.pcs)

    def set_pcs(self, pcs):
        pcs = [pc % self.univ for pc in pcs]
        self.pcs = sorted(set(pcs))
        self.cardinality = len(self.pcs)

    def transposed(self, i):
        return PitchClassSet(self._transposed(i), univ=self.univ)

    def transpose(self, i):
        self.set_pcs(self._transposed(i))

    def inverted(self, i):
        return PitchClassSet(self._inverted(i), univ=self.univ)

    def invert(self, i):
        self.set_pcs(self._inverted(i))

    def m_transformed(self, i):
        return PitchClassSet(self._m_transformed(i), univ=self.univ)

    def m_transform(self, i):
        self.set_pcs(self._m_transformed(i))

    def complement(self):
        comp = [pc for pc in range(self.univ) if pc not in self.pcs]
        return PitchClassSet(comp, univ=self.univ)

    def vector(self):
        vec = [0] * (self.univ - 1)
        # calculate interval for each pair of notes
        for i, note1 in enumerate(self.pcs):
            for j, note2 in enumerate(self.pcs):
                if j <= i:
                    continue
                else:
                    interval = (note1 - note2) % self.univ
                    vec[interval - 1] += 1
        # invert large intervals
        for i in range(len(vec) // 2):
            vec[i] += vec.pop()
        return IntervalVector(vec, univ=self.univ)


class PitchClassSequence(PitchClasses):
    def __init__(self, pcs, univ=0):
        if univ == 0:
            self.univ = PC_UNIVERSE
        else:
            self.univ = univ
        self.set_pcs(pcs)

    def __repr__(self):
        return "PitchClassSequence " + str(self.pcs)

    def set_pcs(self, pcs):
        self.pcs = [pc % self.univ for pc in pcs]

    def transposed(self, i):
        return PitchClassSequence(self._transposed(i), univ=self.univ)

    def transpose(self, i):
        self.set_pcs(self._transposed(i))

    def inverted(self, i):
        return PitchClassSequence(self._inverted(i), univ=self.univ)

    def invert(self, i):
        self.set_pcs(self._inverted(i))

    def m_transformed(self, i):
        return PitchClassSequence(self._m_transformed(i), univ=self.univ)

    def m_transform(self, i):
        self.set_pcs(self._m_transformed(i))

    def pc_inventory(self):
        inventory = set(self.pcs)
        return PitchClassSet(inventory, self.univ)


class IntervalVector:
    def __init__(self, intervals, univ=0):
        if univ == 0:
            self.univ = PC_UNIVERSE
        else:
            self.univ = univ
        self.intervals = intervals

    def __repr__(self):
        return "IntervalVector " + str(self.intervals)
