from lab3.bbs import Bbs


class Fips140_2TestsFor20kElemSeries:
    VALID_SERIES = {1: (2315, 2685),
                    2: (1114, 1386),
                    3: (527, 723),
                    4: (240, 384),
                    5: (103, 209),
                    6: (103, 209)}

    @staticmethod
    def single_bits(series: list[bool]) -> (bool, int):
        assert len(series) == 20000

        ones = len(list(filter(lambda a: a, series)))

        return 9725 < ones < 10275, ones

    @staticmethod
    def series(series: list[bool]) -> (bool, dict[int, int]):
        assert len(series) == 20000

        results = {i: 0 for i in range(1, 7)}

        counter = 0
        streak = False

        for elem in series:
            if elem:
                streak = True
                counter += 1

            elif streak and not elem:
                results[counter if counter < 6 else 6] += 1
                streak = False
                counter = 0

        for (key, value) in Fips140_2TestsFor20kElemSeries.VALID_SERIES.items():
            if results[key] < value[0] or value[1] < results[key]:
                return False, results

        return True, results

    @staticmethod
    def long_series(series: list[bool]) -> bool:
        assert len(series) == 20000

        last = series[0]
        counter = 0

        for elem in series:
            if elem == last:
                counter += 1

                if counter >= 26:
                    return False

            else:
                last = elem
                counter = 1

        return True

    @staticmethod
    def poker(series: list[bool]) -> (bool, float):
        assert len(series) == 20000

        numbers = {k: 0 for k in range(16)}
        bit_summer = []

        for (i, elem) in enumerate(series):
            bit_summer.append(elem)

            if i % 4 == 3:
                sum_value = int(''.join(['1' if e is True else '0' for e in bit_summer]), 2)
                numbers[sum_value] += 1
                bit_summer.clear()

        value = 16 / 5000 * sum([e ** 2 for e in numbers.values()]) - 5000

        return 2.16 < value < 46.17, value

    @staticmethod
    def test(series: list[bool]) -> None:
        assert Fips140_2TestsFor20kElemSeries.single_bits(series)[0] and \
               Fips140_2TestsFor20kElemSeries.series(series)[0] and \
               Fips140_2TestsFor20kElemSeries.long_series(series) and \
               Fips140_2TestsFor20kElemSeries.poker(series)[0], "one of the tests didn't pass"

    @staticmethod
    def visualize(series: list[bool]) -> None:
        style = lambda e: '.' if elem else '0'

        for (i, elem) in enumerate(series):
            if i % 200 == 0:
                print(style(elem))

            else:
                print(style(elem), end='')


if __name__ == '__main__':
    series = Bbs.generate(20000)

    c1, v1 = Fips140_2TestsFor20kElemSeries.single_bits(series)
    c2, v2 = Fips140_2TestsFor20kElemSeries.series(series)
    c3 = Fips140_2TestsFor20kElemSeries.long_series(series)
    c4, v4 = Fips140_2TestsFor20kElemSeries.poker(series)

    print(f'Single bits  = {c1} => {v1}')
    print(f'Series       = {c2} => {v2}')
    print(f'Long series  = {c3}')
    print(f'Poker        = {c4} => {v4}')

    Fips140_2TestsFor20kElemSeries.visualize(series)

    Fips140_2TestsFor20kElemSeries.test(series)
