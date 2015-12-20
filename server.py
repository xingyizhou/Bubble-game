import socket
import json
import MySQLdb
import random

class_image = [[] for i in range(201)]
label_file = open('image_class_labels.txt', 'r')
for line in label_file:
    s = line.split(' ')
    class_image[int(s[1])].append(int(s[0]))
label_file.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind(('localhost', 8001))
sock.listen(5)
while True:
	connection, address = sock.accept()
	try :
		connection.settimeout(5)
		buf = ''
		while True:
			tmp = connection.recv(1024)
			buf = buf + tmp
			if buf[-3:] == 'END':
				buf = buf[:-3]
				break;

		js = json.loads(buf)
		user_name = js['user_name']
		image_id = js['image_id']
		bubble_num = js['bubble_num']
		point = js['point']

		db = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '', db = 'bubble')
		cur = db.cursor()
		for i in range(bubble_num):
			x = js['x{:d}'.format(i)]
			y = js['y{:d}'.format(i)]
			r = js['r{:d}'.format(i)]
			s = 'insert into bubble values("{:s}", {:d}, {:d}, {:d}, {:d})'.format(user_name, image_id, x, y, r)
			cur.execute(s)

		s = 'select score from user where user_name = "{:s}"'.format(user_name)
		cur.execute(s)
		res = cur.fetchall()
		if len(res) == 0:
			score = point
			s = 'insert into user values("{:s}", {:d})'.format(user_name, point)
		else :
			score = res[0][0] + point
			s = 'update user set score = score + {:d} where user_name = "{:s}"'.format(point, user_name)

		cur.execute(s)

		db.commit()
		cur.close()
		db.close()

		cls1 = random.randint(1, 200)
		cls2 = random.randint(1, 200)
		while cls1 == cls2:
			cls2 = random.randint(1, 200)

		img_id_1 = class_image[cls1][random.randint(0,len(class_image[cls1]) - 1)]
		img_id_2 = class_image[cls2][random.randint(0,len(class_image[cls2]) - 1)]

		bubble_id = class_image[cls1][random.randint(0,len(class_image[cls1]) - 1)]
		while bubble_id == img_id_1:
			bubble_id = class_image[cls1][random.randint(0,len(class_image[cls1]) - 1)]
		
		ans = 1
		if random.randint(0, 1) == 1:
			tmp = img_id_1
			img_id_1 = img_id_2
			img_id_2 = tmp
			ans = 2

		js = {'img_id_1': img_id_1, 'img_id_2': img_id_2, 'bubble_id': bubble_id, 'ans': ans, 'score':score}
		connection.send(json.dumps(js))
	except socket.timeout:
		print 'time out'
	connection.close()
