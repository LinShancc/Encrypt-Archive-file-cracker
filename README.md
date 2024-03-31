# 加密压缩文件破解器 Encrypt-Archive-file-cracker v1.1.0
*图形用户界面化操作hashcat进行对加密rar、zip的密码破解。*

*GUI operation of hashcat for cracking the password of encrypted RAR files.*

![image](https://github.com/LinShancc/Encrypt-Archive-file-cracker/assets/129955394/a712b310-192d-4f65-82ed-5b8909dea9a3)

## 目前版本1.1.0,支持RAR、ZIP

可以近乎吃满显卡性能对加密rar、zip文件快速解密，实测4位密码加密在RTX3060 6G Loptop解密时长在50s左右。

It can nearly fully utilize the graphics card's performance for rapid decryption of encrypted RAR files. In practical tests, a 4-digit password encrypted file took about 50 seconds to decrypt on an RTX 3060 6G Laptop.

## 已知问题 known issues
1.在进行解密过程中程序会出现无响应的状态，但这是正常的，等解密完成就正常。
During the decryption process, the program may become unresponsive, but this is normal. It will return to normal once the decryption is complete.

**2.文件名包含中文（繁、简）会无法进行解密。**
**If the RAR file name includes Chinese characters (traditional or simplified), decryption cannot be performed.**

**3.ZIP文件中若包含一些特殊文件（如word文件等）会造成hach值过长而无法破解的问题.**
**If the ZIP file contains some special files (such as word files, etc.), it will cause the problem that the hach value is too long to crack.**

## 依赖 dependency
  ### 1.9.0-jumbo-1（文件中所包含的为64位）
官网地址：https://www.openwall.com/john/

利用其获得加密rar文件的hash值。

Utilize it to obtain the hash value of the encrypted RAR file.

  ### hashcat（文件中已包含）
官网地址：https://hashcat.net/hashcat/

利用所获hash值进行解密核心。解密速度取决于电脑显卡性能。

Use the obtained hash value for the decryption core. The decryption speed depends on the computer's graphics card performance.

## 未来展望 future outlook
后续可延申至各种加密文件的破解。
Subsequently, it can be extended to the cracking of various types of encrypted files.


