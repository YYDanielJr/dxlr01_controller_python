'''
Author: Y.Y. Daniel 626986815@qq.com
Date: 2024-08-16 22:58:10
LastEditors: Y.Y. Daniel 626986815@qq.com
LastEditTime: 2024-08-16 23:07:48
FilePath: /dxlr01_controller_python/profile_generator.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json

if __name__ == "__main__":
    jsondict = {}
    while True:
        a = int(input("Mode: [0, 1, 2]"))
        if a == 0 or a == 1 or a == 2:
            jsondict["mode"] = a
            break
        else:
            print("Invalid choose.")
            
    while True:
        a = str(input("Channel: [00 - 1E]"))
        if "00" <= a <= "1E":
            jsondict["channel"] = a
            break
        else:
            print("Invalid choose.")
            
    while True:
        a = int(input("Level: [0 - 7]"))
        if 0 <= a <= 7:
            jsondict["level"] = a
            break
        else:
            print("Invalid choose.")
            
    while True:
        a = int(input("Sleep: [0, 1, 2]"))
        if a == 0 or a == 1 or a == 2:
            jsondict["sleep"] = a
            break
        else:
            print("Invalid choose.")
        
    with open("profile.json", "w") as f:
        json.dump(jsondict, f)