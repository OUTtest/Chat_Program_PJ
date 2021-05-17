string = "Python"
print("bytearray: {} ".format(bytearray(string, "utf-8")))
print("map : {}".format(map(bin, bytearray(string, "utf-8"))))
binary_converted = ' '.join(map(bin, bytearray(string, "utf-8")))
print("The Binary Represntation is:", binary_converted)