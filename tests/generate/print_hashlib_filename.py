import os

import matplotlib
from packaging.version import Version

if __name__ == "__main__":
    MPL_VERSION = Version(matplotlib.__version__)
    ftv = matplotlib.ft2font.__freetype_version__.replace(".", "")
    hash_filename = f"mpl{MPL_VERSION.major}{MPL_VERSION.minor}_ft{ftv}.json"
    hash_library = os.path.join("tests", "baseline", "hashes", hash_filename)

    print(hash_library)
