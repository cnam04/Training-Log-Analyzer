import matplotlib.pyplot as plt
import numpy as np

def main():
    print("test")
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4],[4,3,2,1], marker='o', linewidth=2, markersize=12)
    ax.set_title("Title", fontsize='50', color='red')
    plt.show()

if __name__ ==  "__main__":
    main()
