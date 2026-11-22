"""Logiken för hemlig tomte. Ingen input eller print här, så den går att testa."""
import random


def draw(names, rng, forbidden=()):
    """Lottar vem som ger present till vem och returnerar {givare: mottagare}.

    Regler: ingen drar sig själv, och ett par i `forbidden` får inte dra varandra (i någon riktning).
    Lyfter ValueError om reglerna gör det omöjligt.
    """
    names = list(names)
    if len(names) < 2:
        raise ValueError("Det behövs minst två deltagare")
    if len(set(names)) != len(names):
        raise ValueError("Namnen måste vara unika")

    not_together = {frozenset(pair) for pair in forbidden}

    def allowed(giver, receiver):
        return giver != receiver and frozenset((giver, receiver)) not in not_together

    order = names[:]
    rng.shuffle(order)  # slumpa ordningen så att lottningen inte blir lika varje gång
    result = {}

    def solve(i, left):
        if i == len(order):
            return True
        giver = order[i]
        candidates = [r for r in left if allowed(giver, r)]
        rng.shuffle(candidates)
        for receiver in candidates:
            result[giver] = receiver
            if solve(i + 1, [r for r in left if r != receiver]):
                return True
        result.pop(giver, None)
        return False

    if not solve(0, names[:]):
        raise ValueError("Det går inte att lotta med de här reglerna")
    return result


def is_valid(assignment, forbidden=()):
    """Kontrollerar en färdig lottning. Används av testerna, och av dig om du bygger vidare."""
    not_together = {frozenset(pair) for pair in forbidden}
    everyone_gives = set(assignment)
    everyone_gets = set(assignment.values())
    return (
        everyone_gives == everyone_gets
        and len(everyone_gets) == len(assignment)
        and all(g != r and frozenset((g, r)) not in not_together for g, r in assignment.items())
    )


def share_valid_random_shuffles(n, trials, rng):
    """Hur stor andel av helt slumpade blandningar av n personer där ingen drar sig själv?"""
    people = list(range(n))
    ok = 0
    for _ in range(trials):
        shuffled = people[:]
        rng.shuffle(shuffled)
        if all(a != b for a, b in zip(people, shuffled)):
            ok += 1
    return ok / trials
