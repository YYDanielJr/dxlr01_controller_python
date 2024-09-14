<!--
 * @Author: Y.Y. Daniel 626986815@qq.com
 * @Date: 2024-08-10 18:13:33
 * @LastEditors: Y.Y. Daniel 626986815@qq.com
 * @LastEditTime: 2024-08-11 16:46:11
 * @FilePath: /dxlr01_controller_python/README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# DX_LR01 LoRa模块控制器（Python语言）
> 在Python 3.10.12 (Linux arm64) 上测试通过，其他Python版本或操作系统环境可自行测试。
## 运行方式
1. 安装依赖包：
```sh
pip install -r requirements.txt
```
国内环境用户可使用国内镜像源加速：
```sh
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
2. 在Python环境中运行`main.py`。

## 关于DX_LR01模块的AT命令
请注意，所有传入的命令**请以`\r\n`结尾**。<br>
该模块有两种运行模式，分别为数据传输模式和AT模式。<br>
默认启动时，进入数据传输模式。输入的内容会以透明传输形式向外界传送。<br>
在此模式下输入`+++`，可进入AT命令模式。
### 可调整的参数
使用`AT+HELP`命令，可以查看当前LoRa模块的相关配置。一共可以查询到如下的返回内容：
| 响应 | 说明 |
|-|-|
| VERSION=\<version> | \<version>：版本 |
| MODE:\<mode> | \<mode>：数据发送模式 |
| LEVEL:\<level> | \<level>：空中速率配置 |
| SLEEP:\<sleep> | \<sleep>：功耗模式 |
| Frequency:\<frequency> | \<frequency>：工作频率 |
| MAC:\<mac> | \<mac>：设备地址 |
| Bandwidth:\<bandwidth> | \<bandwidth>：射频带宽 |
| Spreading Factor:\<spreading factor> | \<spreading factor>：扩频因子 |
| Coding rate:\<coding rate> | \<coding rate>：射频编码率 |
| CRC:\<crc> | \<crc>：CRC校验 |
| Preamble:\<preamble> | \<preamble>：前导码长度 |
| IQ:\<iq> | \<iq>：IQ信号是否翻转 |
| Power:\<power> | \<power>：发射功率 |

### 传输模式
#### 信道与设备地址的查看与修改
使用`AT+MAC`命令，以查看或修改该模块的设备地址；<br>
使用`AT+CHANNEL`命令，以查看或修改该模块的信道。
#### 透明传输
只要组网的LoRa模块处于同一信道下，并且传输参数配置一致，则可以进行透明传输。不需要额外的操作，向其中一块LoRa模块输入一个字符串，与该设备在同一信道上的其他LoRa模块即可接收到这个字符串。<br>
在传输之前，请确认所有LoRa模块传输参数配置一致，并且处于透明传输模式（MODE0）下：
```
+++
AT+MODE0
+++
```
#### 定点传输
在定点传输模式下，信息仅可被发送给指定信道的指定LoRa模块。<br>
包格式如下（16进制）：
```
00 01 02 11 45 14
```
前两位（00 01）为地址，第三位（02）为信道，之后的为传输内容。此时，在02信道上的地址为0001的LoRa模块将会收到信息。<br>
在传输之前，请确认所有LoRa模块传输参数配置一致，并且处于定点传输模式（MODE1）下：
```
+++
AT+MODE1
+++
```
#### 广播传输
在广播传输模式下，信息会被广播到指定信道上的所有设备上。<br>
包格式如下（16进制）：
```
02 11 45 14
```
第一位（02）为信道，之后的为传输内容。此时，在02信道上的所有设备都将会收到信息。<br>
在传输之前，请确认所有LoRa模块传输参数配置一致，并且处于广播模式（MODE2）下：
```
+++
AT+MODE2
+++
```
