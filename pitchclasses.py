PC_UNIVERSE = 12


class PitchClasses:
    def _transposed(self, i):
        return [(self.pcs[x] + i) % self.univ for x, _ in enumerate(self.pcs)]

    def _inverted(self, i):
        return [(i - pc) % self.univ for pc in self.pcs]

    def _m_transformed(self, i):
        return [(pc * i) % self.univ for pc in self.pcs]

    def _retrograded(self):
        return self.pcs[::-1]


class Intervals:
    def __init__(self, intervals, univ=0):
        if univ == 0:
            self.univ = PC_UNIVERSE
        else:
            self.univ = univ
        self.intervals = intervals


class PitchClassSet(PitchClasses):
    def __init__(self, pcs, univ=0):
        if univ == 0:
            self.univ = PC_UNIVERSE
        else:
            self.univ = univ
        self.set_pcs(pcs)

    def set_pcs(self, pcs):
        pcs = [pc % self.univ for pc in pcs]
        self.pcs = sorted(set(pcs))
        self.cardinality = len(self.pcs)

    def __repr__(self):
        return "PitchClassSet {}{}".format(self.univ, self.pcs)

    def __sub__(self, pc_set):
        exception = self._check_valid_pitch_class_set(pc_set)
        if exception is not None:
            raise exception
        else:
            difference = set(self.pcs) - set(pc_set.pcs)
            return PitchClassSet(difference)

    def __and__(self, pc_set):
        exception = self._check_valid_pitch_class_set(pc_set)
        if exception is not None:
            raise exception
        else:
            intersection = set(self.pcs) & set(pc_set.pcs)
            return PitchClassSet(intersection)

    def __xor__(self, pc_set):
        exception = self._check_valid_pitch_class_set(pc_set)
        if exception is not None:
            raise exception
        else:
            sym_diff = set(self.pcs) ^ set(pc_set.pcs)
            return PitchClassSet(sym_diff)

    def __or__(self, pc_set):
        exception = self._check_valid_pitch_class_set(pc_set)
        if exception is not None:
            raise exception
        else:
            union = set(self.pcs) | set(pc_set.pcs)
            return PitchClassSet(union)

    def _check_valid_pitch_class_set(self, pc_set):
        if not isinstance(pc_set, PitchClassSet):
            return TypeError("Only a PitchClassSet can be compared to a PitchClassSet")
        elif pc_set.univ != self.univ:
            return ValueError(
                "Cannot compare PitchClassSets with different values of .univ"
            )
        return None

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

    def set_pcs(self, pcs):
        self.pcs = [pc % self.univ for pc in pcs]
        self.length = len(self.pcs)

    def __repr__(self):
        return "PitchClassSequence {}{}".format(self.univ, self.pcs)

    def __add__(self, pc_sequence):
        exception = self._check_valid_pitch_class_sequence(pc_sequence)
        if exception is not None:
            raise exception
        else:
            combined_sequence = self.pcs + pc_sequence.pcs
            return PitchClassSequence(combined_sequence, univ=self.univ)

    def extend(self, pc_sequence):
        exception = self._check_valid_pitch_class_sequence(pc_sequence)
        if exception is not None:
            raise exception
        else:
            combined_sequence = self.pcs + pc_sequence.pcs
            self.set_pcs(combined_sequence)

    def append(self, pc):
        if not isinstance(pc, int):
            raise TypeError('Only an int can be added to a PitchClassSequence')
        else:
            pc_sequence = self.pcs
            pc_sequence.append(pc)
            self.set_pcs(pc_sequence)
        

    def _check_valid_pitch_class_sequence(self, pc_sequence):
        if not isinstance(pc_sequence, PitchClassSequence):
            return TypeError(
                "Only a PitchClassSequence can be compared to a PitchClassSequence"
            )
        elif pc_sequence.univ != self.univ:
            return ValueError(
                "Cannot compare PitchClassSequences with different values of .univ"
            )
        return None

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

    def retrograded(self):
        return PitchClassSequence(self._retrograded(), univ=self.univ)

    def retrograde(self):
        self.set_pcs(self._retrograded())

    def pc_inventory(self):
        inventory = set(self.pcs)
        return PitchClassSet(inventory, self.univ)

    def intervals(self):
        ivals = []
        for i in range(1, self.length):
            ivals.append((self.pcs[i] - self.pcs[i - 1]) % self.univ)
        return IntervalSequence(ivals, self.univ)


class IntervalVector(Intervals):
    def __repr__(self):
        return "IntervalVector {}{}".format(self.univ, self.intervals)


class IntervalSequence(Intervals):
    def __repr__(self):
        return "IntervalSequence {}{}".format(self.univ, self.intervals)

    def melody(self, starting_pc):
        mel = [starting_pc]
        for i in self.intervals:
            mel.append((mel[-1] + i) % self.univ)
        return PitchClassSequence(mel, self.univ)
