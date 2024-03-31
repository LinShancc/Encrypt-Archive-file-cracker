import subprocess
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ctypes
import re
import threading

# 解决高DPI显示屏下的模糊问题
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# 在全局范围内初始化 fp
fp = None


def select_file():
    # 初始化
    if os.path.exists('hashcat-6.2.6\\output.txt'):
        os.remove('hashcat-6.2.6\\output.txt')
    if os.path.exists('hashcat-6.2.6\\hashcat.log'):
        os.remove('hashcat-6.2.6\\hashcat.log')
    if os.path.exists('hashcat-6.2.6\\hashcat.potfile'):
        os.remove('hashcat-6.2.6\\hashcat.potfile')
    # 使用文件对话框选择rar或zip文件
    file_path = filedialog.askopenfilename(title="选择RAR/ZIP/7z文件", filetypes=[("RAR、ZIP", "*.rar *.zip")])
    if file_path:
        # 更新标签以显示文件名和路径
        filename_label.config(text="文件名: " + file_path.split('/')[-1])
        filepath_label.config(text="路径: " + file_path)
        global fp
        fp = file_path


# 破解主体
def run_main():
    if fp == None:
        # 弹出错误提示
        messagebox.showerror(title='错误', message='未选择文件！')
        return

    # 更新key_label以显示解密中
    key_label.config(text=f"密码为:解密中...")
    #开始后禁用run_button1且变灰,直到解密完成
    run_button1.config(state='disable', bg='grey')

    def find_hashkey(command):
        folder_path0 = 'john-1.9.0-jumbo-1-win64\\run'
        # 切换到指定的文件夹
        os.chdir(folder_path0)
        # 执行命令
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 获取命令执行的输出和错误
        stdout, stderr = process.communicate()
        os.chdir('../..')  # 返回到上两级目录
        # 返回输出和错误
        return stdout, stderr

    def rar():
        command = f'rar2john.exe "{fp}"'
        output, error = find_hashkey(command)
        # 分割输出为行(压缩包多个文件hash时，保留一个hash）
        lines = output.decode().split('\n')
        # 保留的行第一行
        selected_line = lines[0]
        # 寻找标志$RAR3$或者$rar5$，并保留标志和其后的字符串，区分大小写
        pattern = re.compile(r'\$RAR3\$.*|\$rar5\$.*')
        hashkey = pattern.findall(selected_line)[0]

        folder_path1 = 'hashcat-6.2.6'
        # 如果是rar3或rar5，执行不同的命令
        if hashkey.startswith('$RAR3$'):
            command = f'hashcat.exe -m 12500 -a 3 {hashkey} -o output.txt'
        elif hashkey.startswith('$rar5$'):
            command = f'hashcat.exe -m 13000 -a 3 {hashkey} -o output.txt'
        # 在指定的文件夹中执行命令
        os.chdir(folder_path1)
        # 执行命令
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 获取命令执行的输出和错误
        stdout, stderr = process.communicate()
        os.chdir('..')
        if os.path.exists('hashcat-6.2.6\\output.txt'):
            with open('hashcat-6.2.6\\output.txt', 'r') as f:
                out = f.read().split(':')[1]
        else:
            print(stderr.decode())
        return out

    def zip():
        out = None
        command = f'zip2john.exe "{fp}"'
        output, error = find_hashkey(command)
        output = output.decode(errors='ignore')
        zip2 = r'\$zip2\$(.*?)\$/zip2\$'
        pkzip2 = r'\$pkzip2\$(.*?)\$/pkzip2\$'
        # 在output中查找匹配的值
        match_zip2 = re.search(zip2, output)
        match_pkzip2 = re.search(pkzip2, output)
        # 提取匹配的值放入hashkey中
        if match_zip2:
            hashkey = f"$zip2${match_zip2.group(1)}$/zip2$"
            command = f'hashcat.exe -m 13600 -a 3 {hashkey} -o output.txt'

        elif match_pkzip2:
            hashkey = '$pyzip2$'+match_pkzip2.group(1)+'$/pyzip2$'
            command = f'hashcat.exe -m 17200 -a 3 {hashkey} -o output.txt'

        folder_path1 = 'hashcat-6.2.6'
        # 在指定的文件夹中执行命令
        os.chdir(folder_path1)
        # 执行命令
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 获取命令执行的输出和错误
        stdout, stderr = process.communicate()
        os.chdir('..')

        if os.path.exists('hashcat-6.2.6\\output.txt'):
            with open('hashcat-6.2.6\\output.txt', 'r') as f:
                out = f.read().split(':')[1]
        return out

    def decrypt_process():
        if fp.endswith('.rar'):
            key = rar()
            key_label.config(text=f"密码为:{key}")
        elif fp.endswith('.zip'):
            key = zip()
            key_label.config(text=f"密码为:{key}")

        # 恢复run_button1
        run_button1.config(state='normal', bg='SystemButtonFace')

    # 创建并启动新的线程来执行解密过程
    decrypt_thread = threading.Thread(target=decrypt_process)
    decrypt_thread.start()


# 复制密码
def copy_key():
    key = key_label.cget("text").split(':')[1]
    root.clipboard_clear()
    root.clipboard_append(key)
    root.update()


# 创建主窗口
root = tk.Tk()
root.title("加密压缩包文件破解器")
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
select_button0 = tk.Button(root, text="选择文件", command=select_file, height=button_height, width=button_width)
select_button0.pack(pady=10)

# 创建标签以显示文件名和路径
filename_label = tk.Label(root, text="文件名: 未选择", wraplength=window_width - 20)
filename_label.pack()
filepath_label = tk.Label(root, text="路径: 未选择", wraplength=window_width - 20)
filepath_label.pack()

# 创建开始破解的按钮，大小自适应
button_height = 2  # 按钮高度
button_width = 20  # 按钮宽度
run_button1 = tk.Button(root, text="开始破解", command=run_main, height=button_height, width=button_width)
run_button1.pack(pady=10)

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
copyright_label = tk.Label(root, text="by LinSSS.", wraplength=window_width - 20)
copyright_label.pack(side=tk.BOTTOM)
# 创建版本号标签
version_label = tk.Label(root, text="版本号: 1.1.0", wraplength=window_width - 20)
version_label.pack(side=tk.BOTTOM)
# 运行主循环
root.mainloop()
