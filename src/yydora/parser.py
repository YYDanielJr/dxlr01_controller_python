import binascii

packageCutLength = 512
packageCount = 0

# 生成报文编号
def getPackageCount() -> int:
    global packageCount
    packageCount = packageCount + 1
    if packageCount >= 10000:
        packageCount = 0
    return packageCount

def generateShortPackage(text: str) -> str:
    headMagicNumber = "1145"
    tailMagicNumber = "1919"
    ret = headMagicNumber
    ret = ret + "0"
    ret = ret + "{:0>4d}".format(getPackageCount()) + "0000" + text + tailMagicNumber
    return ret

def yydoraParser(text: str) -> bytes:
    if len(text) <= packageCutLength:
        packageStr = generateShortPackage(text)
        packageLength = "{:0>3d}".format(len(packageStr))
        packageStr = packageLength + packageStr
        package = packageStr.encode()
        package = package + str(binascii.crc32(package)).encode()
        return package