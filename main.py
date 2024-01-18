import subprocess
import os
import tkinter as tk
from tkinter import filedialog
import ctypes

# 解决高DPI显示屏下的模糊问题
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# 在全局范围内初始化 fp
fp = None

def select_file():
    # 使用文件对话框选择rar文件
    file_path = filedialog.askopenfilename(filetypes=[("RAR files", "*.rar")])
    if file_path:
        # 更新标签以显示文件名和路径
        filename_label.config(text="文件名: " + file_path.split('/')[-1])
        filepath_label.config(text="路径: " + file_path)
        global fp
        fp = file_path
        #print(fp)


# 破解主体
def run_main():
    key_label.config(text=f"密码为:解密中")
    hashkey = None
    # 删除output.txt
    if os.path.exists('hashcat-6.2.6\\output.txt'):
        os.remove('hashcat-6.2.6\\output.txt')

    def find_hashkey():
        folder_path0 = 'john-1.9.0-jumbo-1-win64\\run'
        command = f'rar2john.exe "{fp}"'
        # 切换到指定的文件夹
        os.chdir(folder_path0)
        # 执行命令
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 获取命令执行的输出和错误
        stdout, stderr = process.communicate()
        os.chdir('../..')  # 返回到上两级目录
        # 返回输出和错误
        return stdout, stderr


    output0, error0 = find_hashkey()

    if output0:
        #print(output0.decode())
        # 分割输出为行
        lines = output0.decode().split('\n')
        # 保留的行第一行
        selected_line = lines[0]
        # 在选定的行上进行你的操作
        hashkey = selected_line.split(':')[2]
        print('输出:', hashkey)
    #弹出错误对话框
    if error0:
        ctypes.windll.user32.MessageBoxW(0, error0.decode(), "错误", 0)
        #print('错误:', error.decode())

    def find_key():
        # 删除缓存文件
        if os.path.exists('hashcat-6.2.6\\hashcat.log' or 'hashcat-6.2.6\\hashcat.potfile' ):
            os.remove('hashcat-6.2.6\\hashcat.log' or 'hashcat-6.2.6\\hashcat.potfile' )
        #print("Current working directory:", os.getcwd())
        folder_path1 = 'hashcat-6.2.6'
        command = f'hashcat.exe -m 13000 -a 3 {hashkey} -o output.txt'
        #在指定的文件夹中执行命令
        os.chdir(folder_path1)
        # 执行命令且无需输出结果错误
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 获取命令执行的输出和错误
        stdout, stderr = process.communicate()
        os.chdir('..')  # 返回到上两级目录
        # 返回输出和错误
        return stdout, stderr

    output1, error1 = find_key()
    # if output1:
    #     print(output1.decode())
    # if error1:
    #     print(error1.decode())

    if os.path.exists('hashcat-6.2.6\\output.txt'):
        with open('hashcat-6.2.6\\output.txt', 'r') as f:
            key = f.read().split(':')[1]
            #print('key:', key)
            key_label.config(text=f"密码为:{key}" )

#复制密码
def copy_key():
    key = key_label.cget("text").split(':')[1]
    root.clipboard_clear()
    root.clipboard_append(key)
    root.update()

# 创建主窗口
root = tk.Tk()
root.title("加密RAR文件破解器")
root.iconbitmap('ico.ico')

# 获取屏幕尺寸以设置窗口大小
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width // 4  # 窗口宽度为屏幕宽度的三分之一
window_height = screen_height // 4  # 窗口高度为屏幕高度的四分之一

# 计算窗口的位置，使其位于屏幕中央
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 设置窗口的大小和位置
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# 创建选择文件的按钮，大小自适应
button_height = 2  # 按钮高度
button_width = 20  # 按钮宽度
select_button0 = tk.Button(root, text="选择RAR文件", command=select_file, height=button_height, width=button_width)
select_button0.pack(pady=10)

# 创建标签以显示文件名和路径
filename_label = tk.Label(root, text="文件名: 未选择", wraplength=window_width - 20)
filename_label.pack()
filepath_label = tk.Label(root, text="路径: 未选择", wraplength=window_width - 20)
filepath_label.pack()

# 创建开始破解的按钮，大小自适应
button_height = 2  # 按钮高度
button_width = 20  # 按钮宽度
select_button1 = tk.Button(root, text="开始破解", command=run_main, height=button_height, width=button_width)
select_button1.pack(pady=10)

# 创建一个新的Frame作为容器
key_frame = tk.Frame(root)
key_frame.pack()

# 在新的Frame中显示key标签
key_label = tk.Label(key_frame, text=f"密码为：未开始 ", wraplength=window_width - 20)
key_label.pack(side=tk.LEFT)

# 在key_label右侧添加复制按钮
copy_button = tk.Button(key_frame, text="复制", command=copy_key)
copy_button.pack(side=tk.RIGHT)
# 创建著作权声明标签
copyright_label = tk.Label(root, text="© 2023 LinSSS. All rights reserved.\nEmail:linshanyangcc77@gmail.com", wraplength=window_width - 20)
copyright_label.pack(side=tk.BOTTOM)
# 创建版本号标签
version_label = tk.Label(root, text="版本号: 1.0.0", wraplength=window_width - 20)
version_label.pack(side=tk.BOTTOM)
# 运行主循环
root.mainloop()




