# Encrypt-RAR-file-cracker
*简单化操作hashcat进行对加密rar的密码破解。*

<img width="322" alt="image" src="https://github.com/LinShancc/Encrypt-RAR-file-cracker/assets/129955394/8c1a5d58-e132-4e95-a817-e99a82d2714b">


可以近乎吃满显卡性能对加密rar文件快速解密，实测4位密码加密在RTX3060 6G Loptop解密时长在50s左右。

## 依赖
  ### 1.9.0-jumbo-1（文件中所包含的为64位）
官网地址：https://www.openwall.com/john/

利用其获得加密rar文件的hash值。

  ### hashcat（文件中已包含）
官网地址：https://hashcat.net/hashcat/

利用所获hash值进行解密核心。解密速度取决于电脑显卡性能。

## 未来展望
后续可延申至各种加密文件的破解。

## 已知问题
1.在进行解密过程中程序会出现无响应的状态，但这是正常的，等解密完成就正常。

**2.rar文件名包含中文（繁、简）会无法进行解密。**

