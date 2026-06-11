import json
from pathlib import Path
from bctr_engine.cli import main

if __name__ == "__main__":
    import sys
    sys.argv = ["", "examples/euler_route.json"]
    main()
