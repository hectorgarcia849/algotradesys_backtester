import sys
import analysis.tests.test_technical_analysis as ta_test


if __name__ == "__main__":
    sys.path.append('C:\\projects\\python\\algorithmic_trading\\')
    print('Setting up tests for Technical Analysis module')
    ta_test.run_tests()

