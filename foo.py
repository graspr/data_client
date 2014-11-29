def foo():
	global buf
	buf = np.zeros(40, 'f')
	for i in range(40):
	    #print buf
	    val = np.random.uniform(-1, 1)
	    buf = np.roll(buf,step)
	    buf[:step] = val