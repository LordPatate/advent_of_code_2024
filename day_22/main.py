from pathlib import Path


def parse_input():
    with Path("./input").open(mode="rt", encoding="utf-8") as input_file:
        line = input_file.readline()
        while line:
            yield int(line)
            line = input_file.readline()


def main():
    print(maximize_sells(parse_input(), 2000, 4))


def maximize_sells(initial_numbers, n, sequence_size):
    total_bananas_per_seq = {}
    max_bananas = 0
    for number in initial_numbers:
        income_of_each_seq = get_number_of_bananas_per_seq(n, number, sequence_size)
        for seq, bananas in income_of_each_seq.items():
            total = total_bananas_per_seq.get(seq, 0)
            total += bananas
            total_bananas_per_seq[seq] = total
            if total > max_bananas:
                max_bananas = total
    return max_bananas


def get_number_of_bananas_per_seq(n, number, sequence_size):
    bananas_for_first_occurrence_of_seq = {}
    window = RollingHashWindow(sequence_size)
    previous = number
    for _ in range(1, sequence_size):
        secret = guess_next_secret(previous)
        window.push(secret % 10 - previous % 10)
        previous = secret
    for _ in range(sequence_size, n):
        secret = guess_next_secret(previous)
        price = secret % 10
        window.push(price - previous % 10)
        if window.hash not in bananas_for_first_occurrence_of_seq:
            bananas_for_first_occurrence_of_seq[window.hash] = price
        previous = secret
    return bananas_for_first_occurrence_of_seq


def sum_of_final_secrets(initial_numbers):
    return sum(
        get_final_secret(number, 2000)
        for number in initial_numbers
    )


def get_final_secret(initial_secret_number, n):
    secret = initial_secret_number
    for _ in range(n):
        secret = guess_next_secret(secret)
    return secret


class RollingHashWindow:
    def __init__(self, size, min_value=-10, max_value=10):
        self._size = size
        self._buffer = [0] * size
        self._index = 0
        self._hash = 0
        self._base = max_value - min_value
        self._max_power = self._base ** (self._size - 1)
        self._offset = -min(min_value, 0)

    @property
    def hash(self):
        return self._hash

    def __len__(self):
        return self._size

    def push(self, elt):
        positive = elt + self._offset
        self._buffer[self._index] = positive
        self._hash %= self._max_power
        self._hash *= self._base
        self._hash += positive
        self._index += 1
        self._index %= self._size

    def most_recent_first(self):
        i = (self._index or self._size) - 1
        for _ in range(self._size):
            yield self._buffer[i] - self._offset
            i = (i or self._size) - 1

    def seq_from_hash(self, seq_hash):
        seq = []
        for _ in range(self._size):
            seq.append(seq_hash % self._base - self._offset)
            seq_hash //= self._base
        return reversed(seq)


def guess_next_secret(secret):
    secret = mix_and_prune(secret * 64, secret)
    secret = mix_and_prune(secret // 32, secret)
    secret = mix_and_prune(secret * 2048, secret)
    return secret


def mix_and_prune(result, secret):
    mixed = result ^ secret
    pruned = mixed % 16777216
    return pruned


if __name__ == "__main__":
    main()
