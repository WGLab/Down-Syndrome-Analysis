import os
import sys
for root, dirs, files in os.walk(sys.argv[1]):
    for i, f in enumerate(files):
        # if i>10:
            # quit()
        print (os.path.relpath(os.path.join(root, f), "."))
