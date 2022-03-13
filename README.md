# pitch-classes

`pitch-classes` is a library intended to aid in the exploration of different equally-tempered musical tuning systems. It has five classes—``PitchClassSet``, `PitchClassSequence`, `IntervalVector`, `IntervalSequence`, and `SetSequence`—as well as several functions for generating objects. Each of these classes works with any integer "pitch class universe" size greater than 1, i.e. any equal temperament. 

## PitchClassSet
A `PitchClassSet` is a set of pitch classes, that is, a collection of pitches without regard for octave or ordering.

`PitchClassSet`s have methods for transforming themselves in-place—`.transpose()`, `.invert()`, and so on—as well as methods for creating new `PitchClassSet`s—`.transposed()`, `.inverted()`, etc.

`PitchClassSet`s support many of the same methods as Python sets, including comparisons such as `<`, `>`, `==` and so on, and operations such as `&`, `|`, `^` and `-`. When `PitchClassSet`s of different sizes of universe are compared, the objects are scaled to the same size of universe to allow for comparison (for example, an augmented triad is equal to an augmented triad, no matter whether it is expressed in 12-tone equal temperament or 3-tone equal temperament).

## PitchClassSequence
A `PitchClassSequence` is a sequence of pitch classes, that is, a collection of pitches without regard for octave. Like `PitchClassSet`s, `PitchClassSequence`s have methods for in-place transformation and the creation of new `PitchClassSet`s.

`PitchClassSequence`s support some of the operations as Python sets, such as adding, appending and extending.

## IntervalVector
An `IntervalVector` represents the intervals between the pitch classes of a `PitchClassSet`, familiar from the analysis of 12-tone music. It has no methods.

## IntervalSequence
An `IntervalSequence` represents a series of intervals between successive pitch classes in a `PitchClassSequence`. It includes methods for inverting, retrograding and changing of universe size, as well as a method `.melody()` for creating a `PitchClassSequence` from a given `IntervalSequence`.

## SetSequence
A SetSequence is a sequence of `PitchClassSet`s representing, for example, a succession of chords.