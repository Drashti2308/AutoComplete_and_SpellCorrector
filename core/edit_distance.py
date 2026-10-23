def levenshtein_distance(word1, word2):
    """
    Calculate the minimum number of insertions, deletions,
    and substitutions needed to transform word1 into word2.
    """

    word1 = word1.lower()
    word2 = word2.lower()

    m = len(word1)
    n = len(word2)

    # Create a DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Transforming a word into an empty string requires deletions
    for i in range(m + 1):
        dp[i][0] = i

    # Transforming an empty string into a word requires insertions
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,       # Deletion
                dp[i][j - 1] + 1,       # Insertion
                dp[i - 1][j - 1] + cost # Match or substitution
            )

    return dp[m][n]