from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")



# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Structure
    Or(AKnave, AKnight),
    Biconditional(AKnave, Not(AKnight)),
    # Information
    Biconditional(AKnight, And(AKnave, AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Structure
    Or(AKnave, AKnight),
    Implication(AKnave, Not(AKnight)),
    Implication(AKnight, Not(AKnave)),

    Or(BKnave, BKnight),
    Implication(BKnave, Not(BKnight)),
    Implication(BKnight, Not(BKnave)),

    # Information given
    Implication(Not(And(AKnave, AKnight)), BKnight),
    Implication(BKnight, AKnave),
    Implication(And(AKnave, AKnight), AKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # structure
    Or(AKnave, AKnight),
    Implication(AKnave, Not(AKnight)),
    Implication(AKnight, Not(AKnave)),

    Or(BKnave, BKnight),
    Implication(BKnave, Not(BKnight)),
    Implication(BKnight, Not(BKnave)),
    # Information given
    Implication(Not(And(AKnight, BKnight)), BKnight),
    Biconditional(BKnight, AKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Structure
    Or(AKnave, AKnight),
    Implication(AKnave, Not(AKnight)),
    Implication(Not(AKnight), AKnight),

    Or(BKnave, BKnight),
    Implication(BKnave, Not(BKnight)),
    Implication(BKnight, Not(BKnave)),

    Or(CKnave, CKnight),
    Implication(CKnave, Not(CKnight)),
    Implication(CKnight, Not(CKnave)),

    # Information given
    Biconditional(AKnight, Or(AKnave, AKnight)),
    Biconditional(CKnight, AKnight),
    Biconditional(AKnight, BKnave),
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
