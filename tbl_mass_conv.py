
import re
import os.path
import base64
import codecs


class Text_2_TBL:
	
	def t_text(self, dirpath):
		name = dirpath + 't_text.txt'

		file = open(name, 'rb+')
		new = dirpath + 't_text.tbl'
		fn = open(new, 'wb+')
		array = file.readlines()
		head = 429
		head = head.to_bytes(2, byteorder='little')
		fn.write(head)
		a = 0
		b = len(array)
		zero = b'\x00'

		REPLACEMENT_MAP = {15:17, 16:18, 17:19, 18:20, 19:21, 20:22, 21:23, 22:24, 23:25, 24:26, 25:27, 26:28, 27:15, 28:16, 165:419, 166:420, 167:421, 168:422, 169:423, 170:424, 171:425, 172:426, 173:165, 174:166, 175:167, 176:168, 177:169, 178:170, 179:171, 180:172, 181:173, 182:174, 183:175, 184:176, 185:177, 186:178, 187:179, 188:180, 189:181, 190:182, 191:183, 192:184, 193:185, 194:236, 195:237, 196:238, 197:239, 198:240, 199:241, 200:242, 201:243, 202:244, 203:245, 204:246, 205:247, 206:248, 207:249, 208:250, 209:251, 210:252, 211:253, 212:254, 213:255, 214:256, 215:257, 216:258, 217:259, 218:260, 219:261, 220:262, 221:263, 222:264, 223:265, 224:266, 225:267, 226:268, 227:269, 228:270, 229:271, 230:272, 231:273, 232:274, 233:275, 234:276, 235:277, 236:278, 237:279, 238:280, 239:281, 240:282, 241:283, 242:284, 243:285, 244:286, 245:287, 246:288, 247:289, 248:186, 249:187, 250:188, 251:189, 252:190, 253:191, 254:192, 255:193, 256:194, 257:195, 258:196, 259:197, 260:198, 261:199, 262:200, 263:201, 264:202, 265:203, 266:204, 267:205, 268:206, 269:207, 270:208, 271:209, 272:211, 273:212, 274:213, 275:214, 276:215, 277:216, 278:217, 279:218, 280:219, 281:220, 282:221, 283:222, 284:223, 285:224, 286:225, 287:226, 288:227, 289:228, 290:229, 291:230, 292:231, 293:232, 294:233, 295:234, 296:235, 297:290, 298:291, 299:302, 300:303, 301:304, 302:305, 303:306, 304:307, 305:308, 306:309, 307:310, 308:311, 309:312, 310:292, 311:293, 312:294, 313:295, 314:296, 315:297, 316:298, 317:299, 318:300, 319:301, 320:313, 321:314, 322:315, 323:316, 324:317, 325:318, 326:319, 327:320, 328:321, 329:322, 330:323, 331:324, 332:325, 333:326, 334:327, 335:328, 336:329, 337:330, 338:331, 339:332, 340:333, 341:334, 342:335, 343:336, 344:337, 345:338, 346:339, 347:340, 348:341, 349:342, 350:343, 351:344, 352:345, 353:346, 354:347, 355:348, 356:349, 357:350, 358:351, 359:352, 360:353, 361:354, 362:355, 363:356, 364:357, 365:358, 366:359, 367:360, 368:361, 369:362, 370:363, 371:364, 372:365, 373:366, 374:367, 375:368, 376:369, 377:370, 378:371, 379:372, 380:373, 381:374, 382:375, 383:376, 384:377, 385:378, 386:379, 387:380, 388:381, 389:382, 390:383, 391:384, 392:385, 393:386, 394:387, 395:388, 396:389, 397:390, 398:391, 399:392, 400:393, 401:394, 402:395, 403:396, 404:397, 405:398, 406:399, 407:400, 408:401, 409:402, 410:403, 411:404, 412:405, 413:406, 414:407, 415:408, 416:409, 417:410, 418:411, 419:412, 420:413, 421:414, 422:415, 423:416, 424:417, 425:418, 426:427, 427:428, 428:429}

		for i in range(0, b):
			fn.write(bytes('TextTableData', encoding='utf-8'))
			fn.write(zero)
			d1 = len(array[i]) + 2
			fn.write(d1.to_bytes(2, byteorder='little'))
			
			if a in REPLACEMENT_MAP.keys():
				new_a = REPLACEMENT_MAP[a]
			else:
				new_a = a
				
			d2 = new_a.to_bytes(2, byteorder='little')
			fn.write(d2)
			a += 1
			print(array[i])
			fn.write(array[i][:-2]+zero)
			
	def t_item(self, dirpath):
		pass
		
class TBL_2_text:

	def t_text(self, dirpath):
		name = dirpath + 't_text.tbl'

		file = open(name, 'rb+')
		new = dirpath + 't_text.txt'
		fn = open(new, 'w+')

		count = file.read(2)
		count = int.from_bytes(count, byteorder='little')

		for i in range(count):
			file.seek(14, 1)
			strSize = file.read(2)
			strSize = int.from_bytes(strSize, byteorder='little') - 3
			file.seek(2, 1)
			string = file.read(strSize)
			fn.write(str(string)+'\n')
			file.seek(1, 1)

		file.close()
		fn.close()
		
	def t_place(self, dirpath):
		pass
		
	def t_item(self, dirpath):
		name = dirpath + 't_item.tbl'

		file = open(name, 'rb+')
		new = dirpath + 't_item.txt'
		fn = open(new, 'w+')
		new_d = dirpath + 't_item_data.txt'
		fnd = open(new_d, 'w+')

		count = file.read(2)
		count = int.from_bytes(count, byteorder='little')

		for i in range(count):
			item = file.read(5)
			allsize = file.read(2)
			allsize = int.from_bytes(allsize, byteorder='little')
			data = file.read(allsize)
			try:
				data1 = data.split(b'\xff\xff')
			except IndexError:
				data1 = [data]
			try:
				strings = data1[1].split(b'\x00')
			except IndexError:
				strings = ['', '']
			if len(strings) == 1:
				sss = strings[0]
				strings = [sss, '']
			fnd.write(str(i) + '\t' + str(data1[0]) + '\n')
			fn.write(str(i) + '\t' + str(strings[0])[2:-1] + '\t' + str(strings[1])[2:-1] + '\n')
			print(str(i) + '\t' + str(data1[0]))
			print(str(strings[0])[2:-1])
			print(str(strings[1])[2:-1] + '\n')
			
		file.close()
		fn.close()
		fnd.close()
			
				
	
conv = TBL_2_text()
conv.t_item('C:/Users/40pja/Desktop/fl/tl/')

input('Press ENTER')










