from bias_detector import get_bias_info
import time

if __name__ == "__main__":

  start = time.time()
  print(get_bias_info("https://www.breitbart.com/entertainment/2023/10/31/nolte-guardian-whines-about-incels-embracing-fight-club-1999/"))
  end = time.time()
  print("Total time (seconds) is:")
  print(end-start)
