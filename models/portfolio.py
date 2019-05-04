class Portfolio:

    def __init__(self, assets, benchmark):
        self._assets = assets
        self._benchmark = benchmark
        self._performance = None

    @property
    def assets(self):
        return self._assets

    @assets.setter
    def assets(self, assets):
        self._assets = assets

    @property
    def benchmark(self):
        return self._benchmark

    @benchmark.setter
    def benchmark(self, benchmark):
        # need to add logic to check that benchmark is in assets
        self._benchmark = benchmark

    @property
    def performance(self):
        return self._performance

    @performance.setter
    def performance(self, performance):
        self._performance = performance
