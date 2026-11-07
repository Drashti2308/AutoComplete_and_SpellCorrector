def levenshtein_distance(word1, word2, max_distance=None):
    """
    Calculate Levenshtein distance using optimized
    banded dynamic programming.

    If max_distance is provided, calculations stop
    when the distance exceeds that threshold.
    """

    word1 = word1.lower()
    word2 = word2.lower()

    m = len(word1)
    n = len(word2)

    # Length difference gives a lower bound on edit distance.
    if max_distance is not None:
        if abs(m - n) > max_distance:
            return max_distance + 1

    # Keep the shorter word as the second dimension.
    if n > m:
        word1, word2 = word2, word1
        m, n = n, m

    if max_distance is None:
        previous = list(range(n + 1))

        for i in range(1, m + 1):
            current = [i] + [0] * n

            for j in range(1, n + 1):
                cost = 0 if word1[i - 1] == word2[j - 1] else 1

                current[j] = min(
                    previous[j] + 1,
                    current[j - 1] + 1,
                    previous[j - 1] + cost
                )

            previous = current

        return previous[n]

    # Initialize banded DP.
    infinity = max_distance + 1

    previous = [infinity] * (n + 1)

    for j in range(min(n, max_distance) + 1):
        previous[j] = j

    # Calculate only cells inside the allowed distance band.
    for i in range(1, m + 1):

        current = [infinity] * (n + 1)

        if i <= max_distance:
            current[0] = i

        start = max(1, i - max_distance)
        end = min(n, i + max_distance)

        for j in range(start, end + 1):

            cost = 0 if word1[i - 1] == word2[j - 1] else 1

            current[j] = min(
                previous[j] + 1,
                current[j - 1] + 1,
                previous[j - 1] + cost
            )

        # Early termination.
        if min(current[start:end + 1]) > max_distance:
            return infinity

        previous = current

    return previous[n]