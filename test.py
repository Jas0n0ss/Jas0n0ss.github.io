# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import glob

paths = glob.glob(r"./*.md")
print(len(paths))

for f_p in paths:
    print(f_p)
    f = open(f_p, 'r')
    alllines = f.readlines()
    f.close()

    f = open(f_p, 'w+')
    for eachline in alllines:
        if "{% codeblock" in eachline:
            eachline = f"```python"
            f.writelines(eachline)
            f.writelines('\n')
        elif "{% endcodeblock" in eachline:
            eachline = f"```"
            f.writelines(eachline)
            f.writelines('\n')
        else:
            f.writelines(eachline)
    f.close()
