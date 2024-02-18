def fibonacci(n):
  """
  计算斐波那契数列

  Args:
    n: 斐波那契数列的长度

  Returns:
    斐波那契数列
  """

  if n <= 1:
    return n
  else:
    return fibonacci(n - 1) + fibonacci(n - 2)


def main():
  """
  主函数
  """

  n = int(input("请输入斐波那契数列的长度："))
  fibs = fibonacci(n)
  print("斐波那契数列为：")
  print(fibs)


if __name__ == "__main__":
  main()
