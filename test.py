
def insert_print_statements():
    try:
        # 读取原始文件内容
        with open('测试.md', encoding='utf-8') as f:
            original_content = f.read()
        
        # 生成5000行print语句
        print_statements = '\n'.join([f'print("任意内容{i+1}")' for i in range(50000)])
        
        # 将print语句插入到文件末尾
        new_content = original_content + '\n\n# 以下是Python代码\n' + print_statements
        
        # 写入文件
        with open('测试.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("成功向测试.md文件中插入了5000行print语句")
        print(f"文件总行数: {len(new_content.splitlines())}")
        
    except FileNotFoundError:
        print("错误: 找不到测试.md文件")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    insert_print_statements()
