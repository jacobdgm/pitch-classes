from math import ceil, floor, gcd, lcm

PC_UNIVERSE = 12


class PitchClasses:
    def __init__(self, pcs, univ=0):
        if univ == 0:
            self.univ = PC_UNIVERSE
        else:
            self.univ = univ
        self.set_pcs(pcs)

    def _transposed(self, i):
        return [(self.pcs[x] + i) % self.univ for x, _ in enumerate(self.pcs)]

    def _inverted(self, i):
        return [(i - pc) % self.univ for pc in self.pcs]

    def _m_transformed(self, i):
        return [(pc * i) % self.univ for pc in self.pcs]

    def _retrograded(self):
        return self.pcs[::-1]

    def _as_univ(self, u, mode="e"):
        multiplier = u / self.univ
        new_pcs = [x * multiplier for x in self.pcs]
        if mode == "exception" or mode == "e":
            for pc in new_pcs:
                if int(pc) != pc:
                    err = round(pc / multiplier)
                    raise ValueError(
                        "pitch class {} does not exist in a universe of size {}.".format(
                            err, u
                        )
                    )
            return [int(x) for x in new_pcs]
        elif mode == "drop" or mode == "d":
            return [int(x) for x in new_pcs if x == int(x)]
        elif mode == "ceiling" or mode == "ceil" or mode == "c":
            return [ceil(x) for x in new_pcs]
        elif mode == "round" or mode == "r":
            return [round(x) for x in new_pcs]
        elif mode == "floor" or mode == "f":
            return [floor(x) for x in new_pcs]

    def _minimized_univ(self):
        divisor = gcd(*self.pcs, self.univ)
        new_univ = self.univ // divisor
        return self._as_univ(new_univ, mode="e"), new_univ


class PitchClassSet(PitchClasses):
    def set_pcs(self, pcs):
        pcs = [pc % self.univ for pc in pcs]
        self.pcs = sorted(set(pcs))
        self.cardinality = len(self.pcs)

    def __repr__(self):
        return "PitchClassSet {}{}".format(self.univ, self.pcs)

    def _pcs_in_normalized_univ(self, *pc_sets):
        "return the pitch classes of a collection of pc_sets, scaled so they are all in a pitch class universe of the same size"
        univs = [pc_set.univ for pc_set in pc_sets]
        comp_univ = lcm(*univs)
        return (pc_set._as_univ(comp_univ) for pc_set in pc_sets), comp_univ

    def __lt__(self, pc_set):
        (self_pcs, arg_pcs), _ = self._pcs_in_normalized_univ(self, pc_set)
        return self_pcs < arg_pcs

    def __le__(self, pc_set):
        (self_pcs, arg_pcs), _ = self._pcs_in_normalized_univ(self, pc_set)
        return self_pcs <= arg_pcs

    def __eq__(self, pc_set):
        (self_pcs, arg_pcs), _ = self._pcs_in_normalized_univ(self, pc_set)
        return self_pcs == arg_pcs

    def __ne__(self, pc_set):
        (self_pcs, arg_pcs), _ = self._pcs_in_normalized_univ(self, pc_set)
        return self_pcs != arg_pcs

    def __gt__(self, pc_set):
        (self_pcs, arg_pcs), _ = self._pcs_in_normalized_univ(self, pc_set)
        return self_pcs > arg_pcs

    def __ge__(self, pc_set):
        (self_pcs, arg_pcs), _ = self._pcs_in_normalized_univ(self, pc_set)
        return self_pcs >= arg_pcs

    # def __sub__(self, pc_set):
    #     exception = self._check_valid_pitch_class_set(pc_set)
    #     if exception is not None:
    #         raise exception
    #     else:
    #         difference = set(self.pcs) - set(pc_set.pcs)
    #         return PitchClassSet(difference)

    # def __and__(self, pc_set):
    #     exception = self._check_valid_pitch_class_set(pc_set)
    #     if exception is not None:
    #         raise exception
    #     else:
    #         intersection = set(self.pcs) & set(pc_set.pcs)
    #         return PitchClassSet(intersection)

    # def __xor__(self, pc_set):
    #     exception = self._check_valid_pitch_class_set(pc_set)
    #     if exception is not None:
    #         raise exception
    #     else:
    #         sym_diff = set(self.pcs) ^ set(pc_set.pcs)
    #         return PitchClassSet(sym_diff)

    # def __or__(self, pc_set):
    #     exception = self._check_valid_pitch_class_set(pc_set)
    #     if exception is not None:
    #         raise exception
    #     else:
    #         union = set(self.pcs) | set(pc_set.pcs)
    #         return PitchClassSet(union)

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

    def as_univ(self, u, mode="e"):
        return PitchClassSet(self._as_univ(u, mode=mode), univ=u)

    def set_univ(self, u, mode="e"):
        new_pcs = self._as_univ(u, mode=mode)
        self.univ = u
        self.set_pcs(new_pcs)

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

    def copy(self):
        return PitchClassSet(pcs=self.pcs, univ=self.univ)

    def minimized_univ(self):
        new_pcs, new_univ = self._minimized_univ()
        return PitchClassSet(new_pcs, univ=new_univ)

    def minimize_univ(self):
        new_pcs, new_univ = self._minimized_univ()
        self.univ = new_univ
        self.pcs = new_pcs


class PitchClassSequence(PitchClasses):
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
            raise TypeError("Only an int can be added to a PitchClassSequence")
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

    def as_univ(self, u, mode="e"):
        return PitchClassSequence(self._as_univ(u, mode=mode), univ=u)

    def set_univ(self, u, mode="e"):
        new_pcs = self._as_univ(u, mode=mode)
        self.univ = u
        self.set_pcs(new_pcs)

    def pc_inventory(self):
        inventory = set(self.pcs)
        return PitchClassSet(inventory, self.univ)

    def intervals(self):
        ivals = []
        for i in range(1, self.length):
            ivals.append((self.pcs[i] - self.pcs[i - 1]) % self.univ)
        return IntervalSequence(ivals, self.univ)

    def copy(self):
        return PitchClassSequence(pcs=self.pcs, univ=self.univ)

    def minimized_univ(self):
        new_pcs, new_univ = self._minimized_univ()
        return PitchClassSequence(new_pcs, univ=new_univ)

    def minimize_univ(self):
        new_pcs, new_univ = self._minimized_univ()
        self.univ = new_univ
        self.pcs = new_pcs


class IntervalVector:
    def __init__(self, intervals, univ=0):
        if univ == 0:
            self.univ = PC_UNIVERSE
        else:
            self.univ = univ
        self.intervals = intervals

    def __repr__(self):
        return "IntervalVector {}{}".format(self.univ, self.intervals)


class IntervalSequence:
    def __init__(self, intervals, univ=0):
        if univ == 0:
            self.univ = PC_UNIVERSE
        else:
            self.univ = univ
        self.intervals = intervals

    def __repr__(self):
        return "IntervalSequence {}{}".format(self.univ, self.intervals)

    def melody(self, starting_pc):
        mel = [starting_pc]
        for i in self.intervals:
            mel.append((mel[-1] + i) % self.univ)
        return PitchClassSequence(mel, self.univ)

    def _inverted(self):
        return [(0 - i) % self.univ for i in self.intervals]

    def inverted(self):
        return IntervalSequence(self._inverted(), univ=self.univ)

    def invert(self):
        self.intervals = self._inverted()

    def _retrograded(self):
        inverted = self._inverted()  # intervals flip when reversed
        return inverted[::-1]

    def retrograded(self):
        return IntervalSequence(self._retrograded(), univ=self.univ)

    def retrograde(self):
        self.intervals = self._retrograded()

    def _as_univ(self, u):
        multiplier = u / self.univ
        new_intervals = [x * multiplier for x in self.intervals]
        for i in new_intervals:
            if int(i) != i:
                err = round(i / multiplier)
                raise ValueError(
                    "interval {} does not exist in a universe of size {}.".format(
                        err, u
                    )
                )
        return [int(x) for x in new_intervals]

    def as_univ(self, u):
        return IntervalSequence(self._as_univ(u), univ=u)

    def set_univ(self, u):
        self.intervals = self._as_univ(u)
        self.univ = u

    def copy(self):
        return IntervalSequence(intervals=self.intervals, univ=self.univ)


class SetSequence:
    def __init__(self, pc_sets, univ=12):
        self.univ = univ
        self.pc_sets = self._parse_sets(pc_sets)

    def __repr__(self):
        sets_repr = []
        for s in self.pc_sets:
            if s.cardinality == 1:
                sets_repr.append(s.pcs[0])
            else:
                sets_repr.append(s.pcs)
        return "SetSequence {}{}".format(sets_repr, self.univ)

    def _parse_sets(self, input):
        sequence = []
        if not (isinstance(input, list) or isinstance(input, tuple)):
            t = type(input)
            message = "pc_sets must be of type list or tuple; received {}".format(t)
            raise TypeError(message)
        for element in input:
            if isinstance(element, PitchClassSet):
                sequence.append(element.copy())
            elif (
                isinstance(element, list)
                or isinstance(element, tuple)
                or isinstance(element, set)
            ):
                sequence.append(PitchClassSet(element, univ=self.univ))
            elif isinstance(element, int):
                sequence.append(PitchClassSet([element], univ=self.univ))
            else:
                t = type(element)
                message = "All elements of pc_sets must be of type PitchClassSet, list, tuple, set, or int; received {}".format(
                    t
                )
                raise TypeError(message)
        return sequence


def aggregate(univ=PC_UNIVERSE):
    return PitchClassSet([x for x in range(univ)], univ=univ)


def maximally_distributed(i, univ=PC_UNIVERSE):
    pc_set = aggregate(i)
    pc_set.set_univ(univ, "f")
    return pc_set
