# Apriori-association
The code is implementing the Apriori algorithm for generating association rules from transaction data in a Pandas DataFrame.

The algorithm starts by reading in the transaction data from an Excel file and building a transaction dictionary that holds the relationships between the items in each transaction.

The ```apriori()``` function then prompts the user to enter the minimum support and minimum confidence for generating association rules.

The ```get_item_list()``` function uses recursion to generate a list of item sets of increasing size, where each set contains items that occur together in at least min_supp_count transactions.

The ```generate_association_rules()``` function generates all possible combinations of items and their corresponding remaining items to form association rules.

Finally, the ```calc_support_confidence()``` function calculates the support and confidence for each association rule, using a cache to speed up the process.

The output is a list of association rules with their corresponding support and confidence values, sorted by confidence.
