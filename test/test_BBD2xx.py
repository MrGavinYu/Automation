from BBD2xx.BBD import BBD, MoveTimeoutException
import matplotlib.pyplot as plt
import time
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
datefmt = '%Y-%m-%d  %H:%M:%S %a',
filename='logging.txt',
filemode='w',
level=logging.INFO)
logging.info('Start Program')

plt.ion()
start = 150
end = 180
a = BBD()
data = []
a.move_to(start)
plt.figure(1)

while a.get_position() < end:
	data.append(a.get_position())
	print(data[-1])
	if len(data) % 100 == 0:
		plt.plot(range(len(data)-100, len(data)), data[-100:], '.')
		plt.pause(0.5)
		if a.reset_if_stuck(data[-100:]):
			print('Stuck At %f' % data[-1])
			logging.error('Stuck At %f' % data[-1])
			logging.error(str(data[-100:]))
		a.move_to(data[-1])
	try:
		a.move_relative(0.001)
	except MoveTimeoutException as e:
		print('Some Unknown Reason', e)
		raise Exception("Error")