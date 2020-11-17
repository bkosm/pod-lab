from lab3.fips_tests import Fips140_2TestsFor20kElemSeries as Fips
from lab3.bbs import BBS
from lab6.rsa import RSA

if __name__ == '__main__':
    phi = RSA.generate_keys(extract_phi=True)
    series = BBS.generate(20000, preseed=phi)

    Fips.test_visual(series)
    Fips.visualize(series)
