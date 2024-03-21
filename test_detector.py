from bias_detector import get_bias_info
import time

if __name__ == "__main__":

  start = time.time()
  print(get_bias_info("https://www.texastribune.org/2024/03/21/texas-immigration-law-local-enforcement/"))
  end = time.time()
  print("Total time (seconds) is:")
  print(end-start)
