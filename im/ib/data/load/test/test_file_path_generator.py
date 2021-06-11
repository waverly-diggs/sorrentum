"""
Import as:

import im.ib.data.load.test.test_file_path_generator as tfpgen
"""

import os

import helpers.unit_test as hut
import im.common.data.types as mcdtyp
import im.ib.data.config as midcfg
import im.ib.data.load.ib_file_path_generator as ifpgen


class TestIbFilePathGenerator(hut.TestCase):
    """
    Test correctness of S3 IB paths.
    """

    def setUp(self) -> None:
        super().setUp()
        self._file_path_generator = ifpgen.IbFilePathGenerator()

    def test_get_latest_symbols_file1(self) -> None:
        """
        Get the latest file with the info.
        """
        latest_file = ifpgen.IbFilePathGenerator.get_latest_symbols_file()
        self.assertRegex(latest_file, "^%s" % midcfg.S3_PREFIX)

    def test_generate_file_path1(self) -> None:
        """
        Test path for ESZ21.
        """
        # Generate path to symbol.
        act = self._file_path_generator.generate_file_path(
            symbol="ESZ21",
            frequency=mcdtyp.Frequency.Minutely,
            asset_class=mcdtyp.AssetClass.Futures,
            contract_type=mcdtyp.ContractType.Expiry,
            exchange="GLOBEX",
            currency="USD",
            ext=mcdtyp.Extension.CSV,
        )
        # Compare with expected value.
        S3_BUCKET = os.environ['AM_S3_BUCKET']
        exp = f"s3://{S3_BUCKET}/data/ib/Futures/GLOBEX/USD/minutely/ESZ21.csv.gz"
        self.assert_equal(act, exp)

    def test_generate_file_path2(self) -> None:
        """
        Test path for TSLA.
        """
        # Generate path to symbol.
        act = self._file_path_generator.generate_file_path(
            symbol="TSLA",
            frequency=mcdtyp.Frequency.Minutely,
            asset_class=mcdtyp.AssetClass.Stocks,
            contract_type=mcdtyp.ContractType.Continuous,
            exchange="NSDQ",
            currency="USD",
            ext=mcdtyp.Extension.CSV,
        )
        # Compare with expected value.
        S3_BUCKET = os.environ['AM_S3_BUCKET']
        exp = f"s3://{S3_BUCKET}/data/ib/stocks/NSDQ/USD/minutely/TSLA.csv.gz"
        self.assert_equal(act, exp)

    def test_generate_file_path3(self) -> None:
        """
        Test path for CLH21.
        """
        # Generate path to symbol.
        act = self._file_path_generator.generate_file_path(
            symbol="CLH21",
            frequency=mcdtyp.Frequency.Daily,
            asset_class=mcdtyp.AssetClass.Futures,
            contract_type=mcdtyp.ContractType.Expiry,
            exchange="ECBOT",
            currency="EUR",
            ext=mcdtyp.Extension.CSV,
        )
        # Compare with expected value.
        S3_BUCKET = os.environ['AM_S3_BUCKET']
        exp = f"s3://{S3_BUCKET}/data/ib/Futures/ECBOT/EUR/daily/CLH21.csv.gz"
        self.assert_equal(act, exp)