#!/usr/bin/python2.7
# _*_ coding: utf-8 _*_
import matplotlib.pyplot as plt
 
month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
sales = [112, 105, 111, 109, 103, 110, 113, 112, 108, 106, 111, 114]
 
plt.plot(month,sales,'o')
 
plt.show()