import os
import matplotlib
from packaging.version import Version


if __name__ == "__main__":
    MPL_VERSION = Version(matplotlib.__version__)
    ftv = matplotlib.ft2font.__freetype_version__.replace(".", "")
    hash_filename = f"mpl{MPL_VERSION.major}{MPL_VERSION.minor}_ft{ftv}.json"
    hash_library = os.path.join("tests", "baseline", "hashes", hash_filename)

    print(f"MPL_VERSION: {MPL_VERSION}")
    print(f"ftv: {ftv}")
    print(f"hash_filename: {hash_filename}")
    print()
    print("** To generate the hash library, please execute the following command. **")
    print(f"poetry run pytest --mpl-generate-hash-library={hash_library}")
