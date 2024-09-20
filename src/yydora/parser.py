import binascii

packageCutLength = 512
packageCount = 0

class YYDoraParser:
    # 生成报文编号
    def getPackageCount(self) -> int:
        global packageCount
        packageCount = packageCount + 1
        if packageCount >= 10000:
            packageCount = 0
        return packageCount

    def generateShortPackage(self, text: str) -> str:
        headMagicNumber = "1145"
        tailMagicNumber = "1919"
        ret = headMagicNumber
        ret = ret + "0"
        ret = ret + "{:0>4d}".format(self.getPackageCount()) + "0000" + text + tailMagicNumber
        return ret


    def yydoraConfirmParser(self, packageNumber: int, longPackageNumber: int) -> bytes:
        package = "11455"
        packageNumberStr = "{:0>3d}".format(packageNumber)
        longPackageNumberStr = "{:0>3d}".format(longPackageNumber)
        package += packageNumberStr + longPackageNumberStr + "1919"
        return package.encode()

    def yydoraResendRequestParser(self, packageNumber: int, longPackageNumber: int) -> bytes:
        package = "11452"
        packageNumberStr = "{:0>3d}".format(packageNumber)
        longPackageNumberStr = "{:0>3d}".format(longPackageNumber)
        package += packageNumberStr + longPackageNumberStr + "1919"
        return package.encode()

    def yydoraParser(self, text: str) -> bytes:
        if len(text) <= packageCutLength:
            packageStr = self.generateShortPackage(text)
            packageLength = "{:0>3d}".format(len(packageStr))
            packageStr = packageLength + packageStr
            package = packageStr.encode()
            package = package + str(binascii.crc32(package)).encode()
            return package

    def yydoraUnparser(self, text: bytes) -> str:
        text = text.decode()
        packageLength = int(text[0:3])
        # 验算crc32
        crcPart = text[packageLength + 3:]
        packagePart = text[:packageLength + 3]  # 包括最开头的数字部分
        if int(crcPart) == binascii.crc32(packagePart.encode()):
            # 解包
            packageType = int(text[7])
            packageNumber = int(text[8:12])
            longPackageNumber = int(text[12:16])
            mainTextSize = packageLength - 17
            mainText = text[16:(16 + mainTextSize)]
            return mainText
        else:
            return str()
