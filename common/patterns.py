import re

sentence_with_monadic_predicates_pattern = re.compile('([a-zA-Z0-9]+)\(([A-Z]\d*)\)')
sentence_with_non_monadic_predicates_pattern = re.compile(r'([a-zA-Z0-9]+)\((([A-Z]\d*),([A-Z]\d*,*)*)\)')
