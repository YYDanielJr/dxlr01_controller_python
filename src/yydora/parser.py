import binascii

packageCutLength = 512
packageCount = 0

class ReceivedPackage:
    def __init__(self, valid: bool, device: int, type: int, number: int, longPackageNumber: int, text: str):
        self.valid = valid
        self.targetDevice = device
        self.packageType = type
        self.packageNumber = number
        self.longPackageNumber = longPackageNumber
        self.text = text

    def isValid(self) -> bool:
        return self.valid

    def getTargetDevice(self) -> int:
        return self.targetDevice

    def getPackageType(self) -> int:
        return self.packageType

    def getPackageNumber(self) -> int:
        return self.packageNumber

    def getLongPackageNumber(self) -> int:
        return self.longPackageNumber

    def getText(self) -> str:
        return self.text


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
    ret = headMagicNumber + "0000"
    ret = ret + "0"
    ret = ret + "{:0>4d}".format(getPackageCount()) + "0000" + text + tailMagicNumber
    return ret

def yydoraConfirmParser(packageNumber: int, longPackageNumber: int) -> bytes:
    package = "114500005"
    packageNumberStr = "{:0>4d}".format(packageNumber)
    longPackageNumberStr = "{:0>4d}".format(longPackageNumber)
    package += packageNumberStr + longPackageNumberStr + "1919"
    return package.encode()

def yydoraResendRequestParser(packageNumber: int, longPackageNumber: int) -> bytes:
    package = "114500002"
    packageNumberStr = "{:0>4d}".format(packageNumber)
    longPackageNumberStr = "{:0>4d}".format(longPackageNumber)
    package += packageNumberStr + longPackageNumberStr + "1919"
    return package.encode()

def yydoraParser(text: str) -> bytes:
    if len(text) <= packageCutLength:
        packageStr = generateShortPackage(text)
        packageLength = "{:0>3d}".format(len(packageStr))
        packageStr = packageLength + packageStr
        package = packageStr.encode()
        package = package + str(binascii.crc32(package)).encode()
        return package

def yydoraUnparser(text: bytes) -> ReceivedPackage:
    text = text.decode()
    try:
        if text.startswith("\r\n"):
            text = text[2:]
    ###
    # print(text)
    ###
        packageLength = int(text[0:3])
    # 验算crc32
        crcPart = text[packageLength + 3:]
        packagePart = text[:packageLength + 3]  # 包括最开头的数字部分
        if int(crcPart) == binascii.crc32(packagePart.encode()):
        # 解包
            targetDevice = int(text[7:11])
            packageType = int(text[11])
            packageNumber = int(text[12:16])
            longPackageNumber = int(text[16:20])
            mainTextSize = packageLength - 21
            mainText = text[20:(20 + mainTextSize)]
            return ReceivedPackage(True, device=targetDevice, type=packageType, number=packageNumber, longPackageNumber=longPackageNumber, text=mainText)
        else:
            return ReceivedPackage(False, 0, 0, 0, "")
    except UnicodeDecodeError:
        return ReceivedPackage(False, 0, 0, 0, "")