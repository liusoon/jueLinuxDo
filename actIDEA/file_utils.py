import os
from ui_utils import show_message

def modify_vmoptions_files(paths, absolute_path):
    for path in paths:
        # 将\转换为/，拼接/bin
        path = path.replace('\\', '/') + '/bin'
        show_message(f"JetBrains 软件路径: {path}")
        # 获取path路径下所有文件名列表
        file_list = os.listdir(path)
        # 获取以vmoptions结尾且文件名不包含client的文件并修改，在文件末尾添加
        # --add-opens=java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED
        # --add-opens=java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED
        #
        # -javaagent:C:/Users/xiaoy/Desktop/jh/ja-netfilter/ja-netfilter.jar 该路径为ja-netfilter.jar的绝对路径
        for file in file_list:
            if file.endswith('.vmoptions') and 'client' not in file:
                file_path = os.path.join(path, file)
                with open(file_path, 'r+') as f:
                    lines = f.readlines()
                    # 检查文件中是否已经有这两行
                    if not any('--add-opens=java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED' in line for line in lines) and \
                       not any('--add-opens=java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED' in line for line in lines):
                        f.write(
                            '\n--add-opens=java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED\n'
                            '--add-opens=java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED\n\n'
                            f'-javaagent:{absolute_path}\n'
                        )
                        show_message(f"修改文件: {file} 成功")
                        break
                    else:
                        # 删除所有带有javaagent的行
                        f.seek(0)
                        lines = [line for line in lines if '-javaagent:' not in line]
                        f.truncate(0)
                        f.writelines(lines)
                        # 添加新的javaagent行
                        f.write(f'-javaagent:{absolute_path}\n')
                        show_message(f"修改文件: {file} 成功")
                        break
