# -*- coding: utf-8 -*- 

#V11
#########################################################################################
#########################################################################################
#########################################################################################
###### 개발환경 : python 3.7.3									                    ######
######		   discord = 1.0.1											           ######
######		   discord.py = 1.2.3									               ######
######		   gtts = 2.0.3											               ######
###### 모듈설치 : pip install setuptools --upgrade				                    ######
######		   pip install discord								                   ######
######		   pip install discord.py[voice]			                           ######
######		   pip install gtts					                                   ######
######		   pip install pyssml							                       ######
######		   pip install pywin32							                       ######
######		   pip install pyinstaller					                           ######
#########################################################################################
#########################################################################################
#########################################################################################


import sys
import os
import win32con
import win32api
import win32gui
import asyncio
import discord
import datetime
import random
import re
import time
from discord.ext import commands
from gtts import gTTS


if not discord.opus.is_loaded():
	discord.opus.load_opus('opus')

basicSetting = []
bossData = []
fixed_bossData = []

bossNum = 0
fixed_bossNum = 0
chkvoicechannel = 0
chkrelogin = 0
chflg = 0
LoadChk = 0

bossTime = []
tmp_bossTime = []

fixed_bossTime = []

bossTimeString = []
bossDateString = []
tmp_bossTimeString = []
tmp_bossDateString = []

bossFlag = []
bossFlag0 = []
fixed_bossFlag = []
fixed_bossFlag0 = []
bossMungFlag = []
bossMungCnt = []

channel_info = []
channel_name = []
channel_id = []
channel_voice_name = []
channel_voice_id = []
channel_type = []

katalkData = []
InitkatalkData = []
indexBossname = []

client = discord.Client()

#기본 설정 호출 및 초기 설정 셋팅
def init():
	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fixed_bossFlag0
	global bossMungFlag
	global bossMungCnt

	global voice_client1
	
	global channel_info
	global channel_name
	global channel_voice_name
	global channel_voice_id
	global channel_id
	global channel_type
	global LoadChk

	global katalkData
	global InitkatalkData
	global indexBossname
	
	tmp_bossData = []
	tmp_fixed_bossData = []
	katalkData = []
	InitkatalkData = []
	f = []
	fb = []

	inidata = open('test_setting.ini', 'r', encoding = 'utf-8')
	boss_inidata = open('boss.ini', 'r', encoding = 'utf-8')
	fixed_initdata = open('fixed_boss.ini', 'r', encoding = 'utf-8')

	tmp_inputData = inidata.readlines()
	tmp_boss_inputData = boss_inidata.readlines()
	tmp_fixed_inputData = fixed_initdata.readlines()

	inputData = tmp_inputData
	boss_inputData = tmp_boss_inputData
	fixed_inputData = tmp_fixed_inputData

	for i in range(len(inputData)):
		InitkatalkData.append(inputData[i])

	for i in range(len(boss_inputData)):
		katalkData.append(boss_inputData[i])

	del(boss_inputData[0])
	del(fixed_inputData[0])

	index = 0

	for value in katalkData:
		if value.find('bossname') != -1:
			indexBossname.append(index)
		index = index + 1
	
	for i in range(inputData.count('\n')):
		inputData.remove('\n')

	for i in range(boss_inputData.count('\n')):
		boss_inputData.remove('\n')

	for i in range(fixed_inputData.count('\n')):
		fixed_inputData.remove('\n')
	
	############## 보탐봇 초기 설정 리스트 #####################
	basicSetting.append(inputData[0][12:])   #basicSetting[0] : bot_token
	basicSetting.append(inputData[7][15:])   #basicSetting[1] : before_alert
	basicSetting.append(inputData[9][10:])   #basicSetting[2] : mungChk
	basicSetting.append(inputData[8][16:])   #basicSetting[3] : before_alert1
	basicSetting.append(inputData[3][14:16]) #basicSetting[4] : restarttime 시
	basicSetting.append(inputData[3][17:])   #basicSetting[5] : restarttime 분
	basicSetting.append(inputData[4][15:])   #basicSetting[6] : voice채널 ID
	basicSetting.append(inputData[5][14:])   #basicSetting[7] : text채널 ID
	basicSetting.append(inputData[1][16:])   #basicSetting[8] : 카톡챗방명
	basicSetting.append(inputData[2][13:])   #basicSetting[9] : 카톡챗On/Off
	basicSetting.append(inputData[6][16:])   #basicSetting[10] : 사다리 채널 ID
	basicSetting.append(inputData[10][14:])   #basicSetting[11] : !q 표시 보스 수

	for i in range(len(basicSetting)):
		basicSetting[i] = basicSetting[i].strip()
	
	if basicSetting[6] != "":
		basicSetting[6] = int(basicSetting[6])
		
	if basicSetting[7] != "":
		basicSetting[7] = int(basicSetting[7])

	bossNum = int(len(boss_inputData)/6) 

	fixed_bossNum = int(len(fixed_inputData)/5) 
	
	for i in range(bossNum):
		tmp_bossData.append(boss_inputData[i*6:i*6+6])
	
	for i in range(fixed_bossNum):
		tmp_fixed_bossData.append(fixed_inputData[i*5:i*5+5]) 

	for j in range(bossNum):
		for i in range(len(tmp_bossData[j])):
			tmp_bossData[j][i] = tmp_bossData[j][i].strip()

	for j in range(fixed_bossNum):
		for i in range(len(tmp_fixed_bossData[j])):
			tmp_fixed_bossData[j][i] = tmp_fixed_bossData[j][i].strip()

	############## 일반보스 정보 리스트 #####################
	for j in range(bossNum):
		tmp_len = tmp_bossData[j][1].find(':')
		f.append(tmp_bossData[j][0][11:])		 #bossData[0] : 보스명
		f.append(tmp_bossData[j][1][10:tmp_len])  #bossData[1] : 시
		f.append(tmp_bossData[j][2][13:])		 #bossData[2] : 멍/미입력
		f.append(tmp_bossData[j][3][20:])		 #bossData[3] : 분전 알림멘트
		f.append(tmp_bossData[j][4][13:])		 #bossData[4] : 젠 알림멘트
		f.append(tmp_bossData[j][1][tmp_len+1:])  #bossData[5] : 분
		f.append(tmp_bossData[j][5][13:])		 #bossData[6] : 카톡On/Off		
		f.append('')							  #bossData[7] : 메세지
		bossData.append(f)
		f = []
		bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365))
		tmp_bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365))
		bossTimeString.append('99:99:99')
		bossDateString.append('9999-99-99')
		tmp_bossTimeString.append('99:99:99')
		tmp_bossDateString.append('9999-99-99')
		bossFlag.append(False)
		bossFlag0.append(False)
		bossMungFlag.append(False)
		bossMungCnt.append(0)

	tmp_fixed_now = datetime.datetime.now()

	############## 고정보스 정보 리스트 #####################
	for j in range(fixed_bossNum):
		tmp_fixed_len = tmp_fixed_bossData[j][1].find(':')
		fb.append(tmp_fixed_bossData[j][0][11:])			   #fixed_bossData[0] : 보스명
		fb.append(tmp_fixed_bossData[j][1][11:tmp_fixed_len])  #fixed_bossData[1] : 시
		fb.append(tmp_fixed_bossData[j][1][tmp_fixed_len+1:])  #fixed_bossData[2] : 분
		fb.append(tmp_fixed_bossData[j][2][20:])			   #fixed_bossData[3] : 분전 알림멘트
		fb.append(tmp_fixed_bossData[j][3][13:])			   #fixed_bossData[4] : 젠 알림멘트
		fb.append(tmp_fixed_bossData[j][4][13:])			   #fixed_bossData[5] : 카톡On/Off		
		fixed_bossData.append(fb)
		fb = []
		fixed_bossFlag.append(False)
		fixed_bossFlag0.append(False)
		fixed_bossTime.append(tmp_fixed_now.replace(hour=int(fixed_bossData[j][1]), minute=int(fixed_bossData[j][2]), second = int(0)))
		if fixed_bossTime[j] < tmp_fixed_now :
			fixed_bossTime[j] = fixed_bossTime[j] + datetime.timedelta(days=int(1))


	print ('보탐봇 재시작 시간 : ', basicSetting[4], '시 ', basicSetting[5], '분')
	print ('보스젠알림시간1 : ', basicSetting[1])
	print ('보스젠알림시간2 : ', basicSetting[3])
	print ('보스멍확인시간 : ', basicSetting[2])

	inidata.close()
	fixed_initdata.close()

init()

token = basicSetting[0]

channel = ''

async def task():
	await client.wait_until_ready()
	
	global channel

	global basicSetting
	global bossData
	global fixed_bossData

	global bossNum
	global fixed_bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global fixed_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global fixed_bossFlag
	global fixed_bossFlag0
	global bossMungFlag
	global bossMungCnt

	global voice_client1

	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type

	if chflg == 1 : 
		if voice_client1.is_connected() == False :	
			voice_client1 = await client.get_channel(basicSetting[6]).connect(reconnect=True)
			if voice_client1.is_connected() :
				print("명치복구완료!")
				await dbLoad()
				await client.get_channel(channel).send( '<다시 왔습니다.!>', tts=False)
				#await PlaySound(voice_client1, './sound/hello.mp3')

	while True:
		#print ('working')
		endTime = datetime.datetime.now()
		endTime = endTime.replace(hour=int(basicSetting[4]), minute=int(basicSetting[5]), second = int(0))
		now = datetime.datetime.now()
		priv0 = now+datetime.timedelta(minutes=int(basicSetting[3]))
		priv = now+datetime.timedelta(minutes=int(basicSetting[1]))
		aftr = now+datetime.timedelta(minutes=int(0-int(basicSetting[2])))
		
		if channel != '':
			################ 보탐봇 재시작 ################ 
			if endTime == now:
				if basicSetting[2] != '0':
					for i in range(bossNum):
						if bossMungFlag[i] == True:
							bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
							bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
				await dbSave()
				await client.get_channel(channel).send( '<보탐봇 화장실 갔다올 시간! 접속완료 후 명령어 입력 해주세요!>', tts=False)
				os.system('restart.bat')

			################ 고정 보스 확인 ################ 
			for i in range(fixed_bossNum):

				################ before_alert1 ################ 
				if fixed_bossTime[i] <= priv0 and fixed_bossTime[i] > priv:
					if basicSetting[3] != '0':
						if fixed_bossFlag0[i] == False:
							fixed_bossFlag0[i] = True
							await client.get_channel(channel).send("```" + fixed_bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + fixed_bossData[i][3] +' [' +  fixed_bossTime[i].strftime('%H:%M:%S') + ']```', tts=False)
							KakaoSendMSG(basicSetting[8], '보탐봇 : ' + fixed_bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + fixed_bossData[i][3], basicSetting[9], fixed_bossData[i][5])
							await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '알림1.mp3')
				
				################ before_alert ################ 
				if fixed_bossTime[i] <= priv and fixed_bossTime[i] > now:
					if basicSetting[1] != '0' :
						if fixed_bossFlag[i] == False:
							fixed_bossFlag[i] = True
							await client.get_channel(channel).send("```" + fixed_bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + fixed_bossData[i][3] +' [' +  fixed_bossTime[i].strftime('%H:%M:%S') + ']```', tts=False)
							KakaoSendMSG(basicSetting[8], '보탐봇 : ' + fixed_bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + fixed_bossData[i][3], basicSetting[9], fixed_bossData[i][5])
							await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '알림.mp3')

				################ 보스 젠 시간 확인 ################
				if fixed_bossTime[i] <= now :
					fixed_bossTime[i] = fixed_bossTime[i]+datetime.timedelta(days=int(1))
					fixed_bossFlag0[i] = False
					fixed_bossFlag[i] = False
					embed = discord.Embed(
							description= "```" + fixed_bossData[i][0] + '탐 ' + fixed_bossData[i][4] + "```" ,
							color=0x00ff00
							)
					await client.get_channel(channel).send( embed=embed, tts=False)
					KakaoSendMSG(basicSetting[8], '보탐봇 : ' + fixed_bossData[i][0] + '탐 ' + fixed_bossData[i][4], basicSetting[9], fixed_bossData[i][5])
					await PlaySound(voice_client1, './sound/' + fixed_bossData[i][0] + '젠.mp3')

			################ 일반 보스 확인 ################ 
			for i in range(bossNum):

				################ before_alert1 ################ 
				if bossTime[i] <= priv0 and bossTime[i] > priv:
					if basicSetting[3] != '0':
						if bossFlag0[i] == False:
							bossFlag0[i] = True
							await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3] +' [' +  bossTimeString[i] + ']```', tts=False)
							KakaoSendMSG(basicSetting[8], '보탐봇 : ' + bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3], basicSetting[9], bossData[i][6])
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림1.mp3')
				
				################ before_alert ################ 
				if bossTime[i] <= priv and bossTime[i] > now:
					if basicSetting[1] != '0' :
						if bossFlag[i] == False:
							bossFlag[i] = True
							await client.get_channel(channel).send("```" + bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3] +' [' +  bossTimeString[i] + ']```', tts=False)
							KakaoSendMSG(basicSetting[8], '보탐봇 : ' + bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3], basicSetting[9], bossData[i][6])
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림.mp3')
				
				################ 보스 젠 시간 확인 ################ 
				if bossTime[i] <= now :
					#print ('if ', bossTime[i])
					bossMungFlag[i] = True
					tmp_bossTime[i] = bossTime[i]
					tmp_bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
					tmp_bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
					bossTimeString[i] = '99:99:99'
					bossDateString[i] = '9999-99-99'
					bossTime[i] = now+datetime.timedelta(days=365)

					embed = discord.Embed(
							description= "```" + bossData[i][0] + '탐' + bossData[i][4] + "```" ,
							color=0x00ff00
							)
					await client.get_channel(channel).send( embed=embed, tts=False)
					KakaoSendMSG(basicSetting[8], '보탐봇 : ' + bossData[i][0] + '탐 ' + bossData[i][4], basicSetting[9], bossData[i][6])
					await PlaySound(voice_client1, './sound/' + bossData[i][0] + '젠.mp3')

				################ 보스 자동 멍 처리 ################ 
				if bossMungFlag[i] == True:
					if (bossTime[i]+datetime.timedelta(days=-365)) <= aftr:
						#print (bossData[i][0], bossTime[i]+datetime.timedelta(days=-365), aftr)
						if basicSetting[2] != '0':
							################ 미입력 보스 ################ 
							if bossData[i][2] == '0':
								await client.get_channel(channel).send( bossData[i][0] + ' 미입력 됐습니다.', tts=False)
								KakaoSendMSG(basicSetting[8], '보탐봇 : ' + bossData[i][0] + ' 미입력 됐습니다.', basicSetting[9], bossData[i][6])
								await PlaySound(voice_client1, './sound/' + bossData[i][0] + '미입력.mp3')
								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = bossMungCnt[i] + 1
								tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
								tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
								tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
								embed = discord.Embed(
									description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
									color=0xff0000
									)
								await client.get_channel(channel).send( embed=embed, tts=False)
								await dbSave()
							################ 멍 보스 ################ 
							else :
								await client.get_channel(channel).send( bossData[i][0] + ' 멍 입니다.')
								KakaoSendMSG(basicSetting[8], '보탐봇 : ' + bossData[i][0] + ' 멍 입니다.', basicSetting[9], bossData[i][6])
								await PlaySound(voice_client1, './sound/' + bossData[i][0] + '멍.mp3')
								bossFlag[i] = False
								bossFlag0[i] = False
								bossMungFlag[i] = False
								bossMungCnt[i] = bossMungCnt[i] + 1
								tmp_bossTime[i] = bossTime[i] = nextTime = tmp_bossTime[i]+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(bossData[i][5]))
								tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
								tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
								embed = discord.Embed(
									description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
									color=0xff0000
									)
								await client.get_channel(channel).send( embed=embed, tts=False)
								await dbSave()
											
		await asyncio.sleep(1) # task runs every 60 seconds

#mp3 파일 생성함수(gTTS 이용, 남성목소리)
async def MakeSound(saveSTR, filename):
	tts = gTTS(saveSTR, lang = 'ko')
	tts.save('./' + filename + '.mp3')

#mp3 파일 재생함수
async def PlaySound(voiceclient, filename):
	source = discord.FFmpegPCMAudio(filename)
	try:
		voiceclient.play(source)
	except discord.errors.ClientException:
		while voiceclient.is_playing():
			await asyncio.sleep(1)
	while voiceclient.is_playing():
		await asyncio.sleep(1)
	voiceclient.stop()
	source.cleanup()

#my_bot.db 저장하기
async def dbSave():
	global bossData
	global bossNum
	global bossTime
	global bossTimeString
	global bossDateString
	global bossMungCnt

	for i in range(bossNum):
		for j in range(bossNum):
			if bossTimeString[i] and bossTimeString[j] != '99:99:99':
				if bossTimeString[i] == bossTimeString[j] and i != j:
					tmp_time1 = bossTimeString[j][:6]
					tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
					if tmp_time2 < 10 :
						tmp_time22 = '0' + str(tmp_time2)
					elif tmp_time2 == 60 :
						tmp_time22 = '00'
					else :
						tmp_time22 = str(tmp_time2)
					bossTimeString[j] = tmp_time1 + tmp_time22

	datelist1 = bossTime

	datelist = list(set(datelist1))

	information1 = '----- 보스탐 정보 -----\n'

	for timestring in sorted(datelist):
		for i in range(bossNum):
			if timestring == bossTime[i]:
				if bossTimeString[i] != '99:99:99' :
					if bossData[i][2] == '0' :
						information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][7] + '\n'
					else : 
						information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (멍 ' + str(bossMungCnt[i]) + '회)' + ' * ' + bossData[i][7] + '\n'
		
	file = open("my_bot.db", 'w')
	file.write(information1)
	file.close()

#my_bot.db 불러오기
async def dbLoad():
	global LoadChk
	try:
		file = open('my_bot.db', 'r')
		beforeBossData = file.readlines()
		
		for i in range(len(beforeBossData)-1):
			for j in range(bossNum):
				startPos = beforeBossData[i+1].find('-')
				endPos = beforeBossData[i+1].find('(')
				if beforeBossData[i+1][startPos+2:endPos] == bossData[j][0] :
					tmp_mungcnt = 0
					
					tmp_len = beforeBossData[i+1].find(':')
					tmp_datelen = beforeBossData[i+1].find('@')
					tmp_msglen = beforeBossData[i+1].find('*')
					
					years1 = beforeBossData[i+1][tmp_datelen+2:tmp_datelen+6]
					months1 = beforeBossData[i+1][tmp_datelen+7:tmp_datelen+9]
					days1 = beforeBossData[i+1][tmp_datelen+10:tmp_datelen+12]
					
					hours1 = beforeBossData[i+1][tmp_len+2:tmp_len+4]
					minutes1 = beforeBossData[i+1][tmp_len+5:tmp_len+7]
					seconds1 = beforeBossData[i+1][tmp_len+8:tmp_len+10]
					
					now2 = datetime.datetime.now()
					tmp_now = now2

					tmp_now = tmp_now.replace(year = int(years1), month = int(months1), day = int(days1), hour=int(hours1), minute=int(minutes1), second = int(seconds1))

					if tmp_now < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[j][1]), minutes = int(bossData[j][5]))
						while now2 > tmp_now :
							tmp_now = tmp_now + deltaTime
							tmp_mungcnt = tmp_mungcnt + 1
					
					now2 = tmp_now

					tmp_bossTime[j] = bossTime[j] = now2
					tmp_bossTimeString[j] = bossTimeString[j] = bossTime[j].strftime('%H:%M:%S')
					tmp_bossDateString[j] = bossDateString[j] = bossTime[j].strftime('%Y-%m-%d')

					bossData[j][7] = beforeBossData[i+1][tmp_msglen+2:len(beforeBossData[i+1])-1]
					if beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3] != 0 and beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] == ' ':
						bossMungCnt[j] = int(beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3]) + tmp_mungcnt
					elif beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] != ' ':
						bossMungCnt[j] = int(beforeBossData[i+1][tmp_msglen-5:tmp_msglen-4] + beforeBossData[i+1][tmp_msglen-4:tmp_msglen-3]) + tmp_mungcnt
					else:
						bossMungCnt[j] = 0


		LoadChk = 0
					
		file.close()
		LoadChk = 0
		print ("<불러오기 완료>")
	except IOError:
		LoadChk = 1
		print ("보스타임 정보가 없습니다.")

#음성채널 입장
async def JointheVC(VCchannel, TXchannel):
	global chkvoicechannel
	global voice_client1

	#print (VCchannel, '   ', TXchannel)
	#print (type(VCchannel), '   ', type(TXchannel))
	if VCchannel is not None:
		if chkvoicechannel == 0:
			voice_client1 = await VCchannel.connect(reconnect=True)
			if voice_client1.is_connected():
				await voice_client1.disconnect()
				voice_client1 = await VCchannel.connect(reconnect=True)
			chkvoicechannel = 1
			await PlaySound(voice_client1, './sound/hello.mp3')
		else :
			await voice_client1.disconnect()
			voice_client1 = await VCchannel.connect(reconnect=True)
			await PlaySound(voice_client1, './sound/hello.mp3')
	else:
		await TXchannel.send('음성채널에 먼저 들어가주세요.', tts=False)

#사다리함수
async def LadderFunc(number, ladderlist, channelVal):
	if number < len(ladderlist):
		result_ladder = random.sample(ladderlist, number)
		result_ladderSTR = ','.join(map(str, result_ladder))
		embed = discord.Embed(
			title = "----- 당첨! -----",
			description= '```' + result_ladderSTR + '```',
			color=0xff00ff
			)
		await channelVal.send(embed=embed, tts=False)
	else:
		await channelVal.send('```추첨인원이 총 인원과 같거나 많습니다. 재입력 해주세요```', tts=False)

#카톡메세지
def KakaoSendMSG(ChatRoom, SendMSG, allSend, bossSend):
	if int(allSend) == 1 and int(bossSend) == 1:
		kakao = win32gui.FindWindow(None, ChatRoom)
		kakaoED = win32gui.FindWindowEx(kakao, None, "RichEdit20W", None)
		if kakao != None:	
			win32gui.SendMessage(kakaoED, win32con.WM_SETTEXT, 0, SendMSG)
			win32gui.PostMessage(kakaoED, win32con.WM_KEYDOWN, win32con.VK_RETURN, None)
			win32gui.PostMessage(kakaoED, win32con.WM_KEYUP, win32con.VK_RETURN, None)

#카톡알림설정저장
def KakaoAlertSave(saveBossName, AlertStatus):
	global katalkData
	global indexBossname

	for value in indexBossname:
		if katalkData[value].find(saveBossName) != -1:
			katalkData[value + 5] = 'kakaoOnOff = '+ AlertStatus + '\n'

	outputkatalkData = open('boss.ini', 'w', encoding = 'utf-8')
	outputkatalkData.writelines(katalkData)
	outputkatalkData.close()

def handle_exit():
	#print("Handling")
	client.loop.run_until_complete(client.logout())

	for t in asyncio.Task.all_tasks(loop=client.loop):
		if t.done():
			#t.exception()
			try:
				#print ('try :   ', t)
				t.exception()
			except asyncio.CancelledError:
				#print ('cancel :   ', t)
				continue
			continue
		t.cancel()
		try:
			client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
			t.exception()
		except asyncio.InvalidStateError:
			pass
		except asyncio.TimeoutError:
			pass
		except asyncio.CancelledError:
			pass

@client.event
async def on_ready():
	global channel
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type
	
	global chkvoicechannel
	global chflg
			
	print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
	print(client.user.name)
	print(client.user.id)
	print("===========")

	all_channels = client.get_all_channels()
	
	for channel1 in all_channels:
		channel_type.append(str(channel1.type))
		channel_info.append(channel1)
	
	for i in range(len(channel_info)):
		if channel_type[i] == "text":
			channel_name.append(str(channel_info[i].name))
			channel_id.append(str(channel_info[i].id))
			
	for i in range(len(channel_info)):
		if channel_type[i] == "voice":
			channel_voice_name.append(str(channel_info[i].name))
			channel_voice_id.append(str(channel_info[i].id))

	await dbLoad()

	if basicSetting[6] != "" and basicSetting[7] != "" :
		await JointheVC(client.get_channel(basicSetting[6]), client.get_channel(basicSetting[7]))
		channel = basicSetting[7]
		await client.get_channel(basicSetting[7]).send('< 텍스트채널 [' + client.get_channel(basicSetting[7]).name + '] 접속완료>', tts=False)
		await client.get_channel(basicSetting[7]).send('< 음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>', tts=False)
		await client.get_channel(basicSetting[7]).send('< 보탐봇 재시작 설정시간 ' + basicSetting[4] + '시 ' + basicSetting[5] + '분입니다. >', tts=False)
		chflg = 1
	
	# 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
	# 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
	await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="열일중", type=1))


while True:
	@client.event
	async def on_message(msg):
		if msg.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
			return None #동작하지 않고 무시합니다.

		global channel
		
		global basicSetting
		global bossData
		global fixed_bossData

		global bossNum
		global fixed_bossNum
		global chkvoicechannel
		global chkrelogin

		global bossTime
		global tmp_bossTime

		global fixed_bossTime

		global bossTimeString
		global bossDateString
		global tmp_bossTimeString
		global tmp_bossDateString

		global bossFlag
		global bossFlag0
		global bossMungFlag
		global bossMungCnt
		
		global voice_client1
		
		global channel_info
		global channel_name
		global channel_id
		global channel_voice_name
		global channel_voice_id
		global channel_type
		
		global chflg
		global LoadChk

		global katalkData
		global InitkatalkData
		global indexBossname
		
		id = msg.author.id

		if chflg == 0 :
			channel = int(msg.channel.id) #메세지가 들어온 채널 ID

			print ('[ ', basicSetting[7], ' ]')
			print ('] ', client.get_channel(channel).name, ' [')
			
			if basicSetting[7] == "":
				inidata_text = open('test_setting.ini', 'r', encoding = 'utf-8')
				inputData_text = inidata_text.readlines()
				inidata_text.close()
			
				inidata_text = open('test_setting.ini', 'w', encoding = 'utf-8')				
				for i in range(len(inputData_text)):
					if inputData_text[i] == 'textchannel = \n':
						inputData_text[i] = 'textchannel = ' +str(channel) + '\n'
						basicSetting[7] = channel
				
				inidata_text.writelines(inputData_text)
				inidata_text.close()
				
			await client.get_channel(channel).send('< 텍스트채널 [' + client.get_channel(channel).name + '] 접속완료>', tts=False)
			
			if basicSetting[6] != "":
				await JointheVC(client.get_channel(basicSetting[6]), client.get_channel(channel))
				await client.get_channel(channel).send('< 음성채널 [' + client.get_channel(basicSetting[6]).name + '] 접속완료>', tts=False)

			await client.get_channel(channel).send('< 보탐봇 재시작 설정시간 ' + basicSetting[4] + '시 ' + basicSetting[5] + '분입니다. >', tts=False)
			chflg = 1
			
		if client.get_channel(channel) != msg.channel :
			if basicSetting[10] != "":
				if msg.channel.id == int(basicSetting[10]):
					message = await msg.channel.fetch_message(msg.id)
					################ 사다리 특정 채널에서 하기 ################ 
					if message.content.startswith('!사다리'):
						ladder = []
						ladder = message.content[5:].split(" ")
						num_cong = int(ladder[0])
						del(ladder[0])
						await LadderFunc(num_cong, ladder, msg.channel)

					##################################
				else :
					return None
			else:
				return None
		else :
			message = await client.get_channel(channel).fetch_message(msg.id) #디코에 입력된 메세지 저장
			
			################ 서버 채널 확인 ################ 

			if message.content  == '!채널확인':
				ch_information = ''
				for i in range(len(channel_name)):
					ch_information += '[' + channel_id[i] + '] ' + channel_name[i] + '\n'

				ch_voice_information = ''
				for i in range(len(channel_voice_name)):
					ch_voice_information += '[' + channel_voice_id[i] + '] ' + channel_voice_name[i] + '\n'
				print (ch_information)
				print (ch_voice_information)
				embed = discord.Embed(
					title = "----- 채널 정보 -----",
					description= '',
					color=0xff00ff
					)
				embed.add_field(
					name="< 택스트 채널 >",
					value= '```' + ch_information + '```',
					inline = False
					)
				embed.add_field(
					name="< 보이스 채널 >",
					value= '```' + ch_voice_information + '```',
					inline = False
					)
				await client.get_channel(channel).send( embed=embed, tts=False)

			################ 텍스트 채널 이동 ################ 

			if message.content.startswith('!채널이동'):
				tmp_sayMessage1 = message.content
				
				for i in range(len(channel_name)):
					if  channel_name[i] == str(tmp_sayMessage1[6:]):
						channel = int(channel_id[i])
				
				print ('[ ', client.get_channel(basicSetting[7]).name, ' ]에서')
				print ('] ', client.get_channel(channel).name, ' [이동')
						
				if basicSetting[7] != channel:
					inidata_text = open('test_setting.ini', 'r', encoding = 'utf-8')
					inputData_text = inidata_text.readlines()
					inidata_text.close()
					
					inidata_text = open('test_setting.ini', 'w', encoding = 'utf-8')
					for i in range(len(inputData_text)):
						if inputData_text[i] == 'textchannel = ' + str(basicSetting[7]) + '\n':
							inputData_text[i] = 'textchannel = ' + str(channel) + '\n'
							basicSetting[7] = channel
								
					inidata_text.writelines(inputData_text)
					inidata_text.close()
								
				await client.get_channel(channel).send( '< ' + client.get_channel(channel).name + ' 이동완료>', tts=False)
			
			hello = message.content

			################ 보스 컷처리 ################ 

			for i in range(bossNum):
				if message.content.startswith(bossData[i][0] +'컷'):
					if hello.find('  ') != -1 :
						bossData[i][7] = hello[hello.find('  ')+2:]
						hello = hello[:hello.find('  ')]
					else:
						bossData[i][7] = ''

					tmp_msg = bossData[i][0] +'컷'
									
					if len(hello) > len(tmp_msg) + 3 :
						if hello.find(':') != -1 :
							chkpos = hello.find(':')
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos+1:chkpos+3]
							now2 = datetime.datetime.now()
							tmp_now = datetime.datetime.now()
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							chkpos = len(hello)-2
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos:chkpos+2]	
							now2 = datetime.datetime.now()
							tmp_now = datetime.datetime.now()
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						now2 = datetime.datetime.now()
						tmp_now = now2
						
					bossFlag[i] = False
					bossFlag0[i] = False
					bossMungFlag[i] = False
					bossMungCnt[i] = 0

					if tmp_now > now2 :
						tmp_now = tmp_now + datetime.timedelta(days=int(-1))
						
					if tmp_now < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
						while now2 > tmp_now :
							tmp_now = tmp_now + deltaTime
							bossMungCnt[i] = bossMungCnt[i] + 1
						now2 = tmp_now
						bossMungCnt[i] = bossMungCnt[i] - 1
					else :
						now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
								
					tmp_bossTime[i] = bossTime[i] = nextTime = now2
					tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
					tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
					embed = discord.Embed(
							description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
							color=0xff0000
							)
					await client.get_channel(channel).send( embed=embed, tts=False)
					await dbSave()

			################ 보스 멍 처리 ################ 
				if message.content.startswith(bossData[i][0] +'멍'):
					if hello.find('  ') != -1 :
						bossData[i][6] = hello[hello.find('  ')+2:]
						hello = hello[:hello.find('  ')]
					else:
						bossData[i][6] = ''
						
					tmp_msg = bossData[i][0] +'멍'
					tmp_now = datetime.datetime.now()

					if len(hello) > len(tmp_msg) + 3 :
						if hello.find(':') != -1 :
							chkpos = hello.find(':')
							hours1 = hello[chkpos-2:chkpos] 
							minutes1 = hello[chkpos+1:chkpos+3]					
							temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							chkpos = len(hello)-2
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos:chkpos+2]					
							temptime = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						
						nextTime = temptime + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))

						bossMungCnt[i] = 0
						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = bossMungCnt[i] + 1

						if nextTime > tmp_now :
							nextTime = nextTime + datetime.timedelta(days=int(-1))

						if nextTime < tmp_now :
							deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							while tmp_now > nextTime :
								nextTime = nextTime + deltaTime
								bossMungCnt[i] = bossMungCnt[i] + 1
						else :
							nextTime = nextTime

						tmp_bossTime[i] = bossTime[i] = nextTime				

						tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
						tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
						embed = discord.Embed(
								description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
								color=0xff0000
								)
						await client.get_channel(channel).send(embed=embed, tts=False)
						await dbSave()
					else:
						if tmp_bossTime[i] < tmp_now :

							nextTime = tmp_bossTime[i] + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))

							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False
							bossMungCnt[i] = bossMungCnt[i] + 1

							tmp_bossTime[i] = bossTime[i] = nextTime				

							tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
							embed = discord.Embed(
									description= '```다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.```',
									color=0xff0000
									)
							await client.get_channel(channel).send(embed=embed, tts=False)
							await dbSave()
						else:
							await client.get_channel(channel).send('```' + bossData[i][0] + '탐이 아직 안됐습니다. 다음 ' + bossData[i][0] + '탐 [' + tmp_bossTimeString[i] + '] 입니다```', tts=False)
				
			################ 예상 보스 타임 입력 ################ 

				if message.content.startswith(bossData[i][0] +'예상'):
					if hello.find('  ') != -1 :
						bossData[i][7] = hello[hello.find('  ')+2:]
						hello = hello[:hello.find('  ')]
					else:
						bossData[i][7] = ''
					
					tmp_msg = bossData[i][0] +'예상'
					if len(hello) > len(tmp_msg) + 3 :
						if hello.find(':') != -1 :
							chkpos = hello.find(':')
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos+1:chkpos+3]
							now2 = datetime.datetime.now()
							tmp_now = datetime.datetime.now()
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							chkpos = len(hello)-2
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos:chkpos+2]
							now2 = datetime.datetime.now()
							tmp_now = datetime.datetime.now()
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))

						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
						bossMungCnt[i] = 0

						if tmp_now < now2 :
							tmp_now = tmp_now + datetime.timedelta(days=int(1))
									
						tmp_bossTime[i] = bossTime[i] = nextTime = tmp_now
						tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
						tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
						embed = discord.Embed(
								description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
								color=0xff0000
								)
						await client.get_channel(channel).send(embed=embed, tts=False)
						await dbSave()
					else:
						await client.get_channel(channel).send(bossData[i][0] + ' 예상 시간을 입력해주세요.')
					
			################ 보스타임 삭제 ################ 
					
				if message.content.startswith(bossData[i][0] +'삭제'):
					bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365)
					tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365)
					bossTimeString[i] = '99:99:99'
					bossDateString[i] = '9999-99-99'
					tmp_bossTimeString[i] = '99:99:99'
					tmp_bossDateString[i] = '9999-99-99'
					bossFlag[i] = (False)
					bossFlag0[i] = (False)
					bossMungFlag[i] = (False)
					bossMungCnt[i] = 0
					await client.get_channel(channel).send('<' + bossData[i][0] + ' 삭제완료>', tts=False)
					await dbSave()
					print ('<' + bossData[i][0] + ' 삭제완료>')

			################ 전체 카톡 켬 ################ 

				if message.content.startswith(bossData[i][0] +'카톡끔'):
					bossData[i][6] = '0'
					KakaoAlertSave(bossData[i][0], bossData[i][6])
					await client.get_channel(channel).send('< ' + bossData[i][0] + ' 카톡 보내기 끔>', tts=False)

				if message.content.startswith(bossData[i][0] +'카톡켬'):
					bossData[i][6] = '1'
					KakaoAlertSave(bossData[i][0], bossData[i][6])
					await client.get_channel(channel).send('< ' + bossData[i][0] + ' 카톡 보내기 켬>', tts=False)

			################ 전체 카톡 끔 ################ 

			if message.content == '!카톡끔':
				basicSetting[9] = '0'
				InitkatalkData[2] = 'kakaoOnOff = ' + basicSetting[9] +'\n'
				tmp_katalkData = open('test_setting.ini', 'w', encoding = 'utf-8')
				tmp_katalkData.writelines(InitkatalkData)
				tmp_katalkData.close()
				await client.get_channel(channel).send('<카톡 보내기 끔>', tts=False)

			if message.content == '!카톡켬':
				basicSetting[9] = '1'
				InitkatalkData[2] = 'kakaoOnOff = ' + basicSetting[9] +'\n'
				tmp_katalkData = open('test_setting.ini', 'w', encoding = 'utf-8')
				tmp_katalkData.writelines(InitkatalkData)
				tmp_katalkData.close()
				await client.get_channel(channel).send('<카톡 보내기 켬>', tts=False)
			
			################ ?????????????? ################ 
						
			if message.content.startswith('!오빠'):
				await PlaySound(voice_client1, './sound/오빠.mp3')
			if message.content.startswith('!언니'):
				await PlaySound(voice_client1, './sound/언니.mp3')
			if message.content.startswith('!형'):
				await PlaySound(voice_client1, './sound/형.mp3')

			################ 분배 결과 출력 ################ 

			if message.content.startswith('!분배'):
				separate_money = []
				separate_money = message.content[4:].split(" ")
				num_sep = int(separate_money[0])
				cal_tax1 = int(float(separate_money[1])*0.05)
				real_money = int(int(separate_money[1]) - cal_tax1)
				cal_tax2 = int(real_money/num_sep) - int(float(int(real_money/num_sep))*0.95)
				if num_sep == 0 :
					await client.get_channel(channel).send('분배 인원이 0입니다. 재입력 해주세요.', tts=False)
				else :
					await client.get_channel(channel).send('1차세금 : ' + str(cal_tax1) + '\n1차 수령액 : ' + str(real_money) + '\n분배자 거래소등록금액 : ' + str(int(real_money/num_sep)) + '\n2차세금 : ' + str(cal_tax2) + '\n인당 실수령액 : ' + str(int(float(int(real_money/num_sep))*0.95)), tts=False)

			################ 사다리 결과 출력 ################ 

			if message.content.startswith('!사다리'):
				ladder = []
				ladder = message.content[5:].split(" ")
				num_cong = int(ladder[0])
				del(ladder[0])
				await LadderFunc(num_cong, ladder, client.get_channel(channel))

			################ 보탐봇 메뉴 출력 ################ 	

			if message.content == '!메뉴':
				embed = discord.Embed(
						title = "----- 메뉴 -----",
						description= '```!설정확인\n!카톡확인\n!채널확인\n!채널이동 [채널명]\n!소환\n!불러오기\n!초기화\n!재시작\n!명치\n!미예약\n!분배 [인원] [금액]\n!사다리 [뽑을인원수] [아이디1] [아이디2] ...\n!보스일괄 00:00 또는 !보스일괄 0000\n!카톡켬\n!카톡끔\n!ㅂ,ㅃ,q\n!k,ㅏ (할말)\n\n[보스명]컷\n[보스명]컷 00:00 또는 [보스명]컷 0000\n[보스명]멍\n[보스명]멍 00:00 또는 [보스명]멍 0000\n[보스명]예상 00:00 또는 [보스명]예상 0000\n[보스명]카톡켬\n[보스명]카톡끔\n[보스명]삭제\n보스탐\n!카톡보스\n!보스탐\n!리젠```',
						color=0xff00ff
						)
				embed.add_field(
						name="----- 추가기능 -----",
						value= '```(보스명)컷/멍/예상  (할말) : 보스시간 입력 후 빈칸 두번!! 메모 가능```'
						)
				await client.get_channel(channel).send( embed=embed, tts=False)

			################ 미예약 보스타임 출력 ################ 

			if message.content == '!미예약':
				temp_bossTime2 = []
				for i in range(bossNum):
					if bossTimeString[i] == '99:99:99' :
						temp_bossTime2.append(bossData[i][0])

				if len(temp_bossTime2) != 0:
					temp_bossTimeSTR1 = ','.join(map(str, temp_bossTime2))
					temp_bossTimeSTR1 = '```fix\n' + temp_bossTimeSTR1 + '\n```'
				else:
					temp_bossTimeSTR1 = '``` ```'
						
				embed = discord.Embed(
						title = "----- 미예약보스 -----",
						description= temp_bossTimeSTR1,
						color=0x0000ff
						)
				await client.get_channel(channel).send( embed=embed, tts=False)

			################ 음성파일 생성 후 재생 ################ 		
				
			if message.content.startswith('!v') or message.content.startswith('!ㅍ'):
				tmp_sayMessage = message.content
				sayMessage = tmp_sayMessage[3:]
				await MakeSound(message.author.display_name +'님이' + sayMessage, './sound/say')
				await client.get_channel(channel).send( "```< " + msg.author.display_name + " >님이 \"" + sayMessage + "\"```", tts=False)
				await PlaySound(voice_client1, './sound/say.mp3')

			################ 카톡으로 메세지 보내기 ################ 
						
			if message.content.startswith('!k') or message.content.startswith('!ㅏ'): 
				tmp_sayMessage = message.content
				sayMessage = tmp_sayMessage[3:]
				KakaoSendMSG(basicSetting[8], message.author.display_name + ' : ' + sayMessage, basicSetting[9], '1')

			################ 보탐봇 재시작 ################ 

			if message.content == '!재시작':
				if basicSetting[2] != '0':
					for i in range(bossNum):
						if bossMungFlag[i] == True:
							bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
							bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
				await dbSave()
				await client.get_channel(channel).send( '<보탐봇 재시작 중! 접속완료 후 명령어 입력 해주세요!>', tts=False)
				os.system('restart.bat')
				#sys.exit()
				
			################ 보탐봇 음성채널 소환 ################ 

			if message.content == '!소환':
				if message.author.voice == None:
					await client.get_channel(channel).send('음성채널에 먼저 들어가주세요.', tts=False)
				else:
					voice_channel = message.author.voice.channel
					
					print ('< ', basicSetting[6], ' >')
					print ('> ', client.get_channel(voice_channel.id).name, ' <')
					
					if basicSetting[6] == "":
						inidata_voice = open('test_setting.ini', 'r', encoding = 'utf-8')
						inputData_voice = inidata_voice.readlines()
						inidata_voice.close()
					
						inidata_voice = open('test_setting.ini', 'w', encoding = 'utf-8')				
						for i in range(len(inputData_voice)):
							if inputData_voice[i] == 'voicechannel = \n':
								inputData_voice[i] = 'voicechannel = ' + str(voice_channel.id) + '\n'
								basicSetting[6] = int(voice_channel.id)
								#print ('======', inputData_voice[i])
						
						inidata_voice.writelines(inputData_voice)
						inidata_voice.close()
						
					elif basicSetting[6] != int(voice_channel.id):
						inidata_voice = open('test_setting.ini', 'r', encoding = 'utf-8')
						inputData_voice = inidata_voice.readlines()
						inidata_voice.close()
						
						inidata_voice = open('test_setting.ini', 'w', encoding = 'utf-8')
						for i in range(len(inputData_voice)):
							if inputData_voice[i] == 'voicechannel = ' + str(basicSetting[6]) + '\n':
								inputData_voice[i] = 'voicechannel = ' + str(voice_channel.id) + '\n'
								basicSetting[6] = int(voice_channel.id)
								#print ('+++++++', inputData_voice[i])
									
						inidata_voice.writelines(inputData_voice)
						inidata_voice.close()

					await JointheVC(voice_channel, channel)
					await client.get_channel(channel).send( '< 음성채널 [' + client.get_channel(voice_channel.id).name + '] 접속완료>', tts=False)

			
			################ 저장된 정보 초기화 ################ 
						
			if message.content == '!초기화':
				basicSetting = []
				bossData = []

				bossTime = []
				tmp_bossTime = []

				fixed_bossTime = []

				bossTimeString = []
				bossDateString = []
				tmp_bossTimeString = []
				tmp_bossDateString = []

				bossFlag = []
				bossFlag0 = []
				fixed_bossFlag = []
				fixed_bossFlag0 = []
				bossMungFlag = []
				bossMungCnt = []

				katalkData = []
				InitkatalkData = []
				indexBossname = []
				
				init()

				await dbSave()

				await client.get_channel(channel).send( '<초기화 완료>', tts=False)
				print ("<초기화 완료>")

			################ 보스타임 일괄 설정 ################ 
			
			if message.content.startswith('!보스일괄'):
				for i in range(bossNum):
					tmp_msg = '!보스일괄'
					if len(hello) > len(tmp_msg) + 3 :
						if hello.find(':') != -1 :
							chkpos = hello.find(':')
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos+1:chkpos+3]
							now2 = datetime.datetime.now()
							tmp_now = datetime.datetime.now()
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
						else:
							chkpos = len(hello)-2
							hours1 = hello[chkpos-2:chkpos]
							minutes1 = hello[chkpos:chkpos+2]
							now2 = datetime.datetime.now()
							tmp_now = datetime.datetime.now()
							tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					else:
						now2 = datetime.datetime.now()
						tmp_now = now2
						
					bossFlag[i] = False
					bossFlag0[i] = False
					bossMungFlag[i] = False
					bossMungCnt[i] = 1

					if tmp_now > now2 :
						tmp_now = tmp_now + datetime.timedelta(days=int(-1))
						
					if tmp_now < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
						while now2 > tmp_now :
							tmp_now = tmp_now + deltaTime
							bossMungCnt[i] = bossMungCnt[i] + 1
						now2 = tmp_now
						bossMungCnt[i] = bossMungCnt[i] - 1
					else :
						now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
								
					tmp_bossTime[i] = bossTime[i] = nextTime = now2
					tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
					tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')

				await dbSave()
				await dbLoad()
				await dbSave()
				
				await client.get_channel(channel).send( '<보스 일괄 입력 완료>', tts=False)
				print ("<보스 일괄 입력 완료>")

			################ 보탐봇 기본 설정확인 ################ 

			if message.content == '!설정확인':			
				setting_val = '보탐봇 재시작 설정시간 : ' + basicSetting[4] + '시 ' + basicSetting[5] + '분\n' + '보스젠알림시간1 : ' + basicSetting[1] + ' 분 전\n' + '보스젠알림시간2 : ' + basicSetting[3] + ' 분 전\n' + '보스멍확인시간 : ' + basicSetting[2] + ' 분 후\n'
				embed = discord.Embed(
						title = "----- 설정내용 -----",
						description= setting_val,
						color=0xff00ff
						)
				await client.get_channel(channel).send( embed=embed, tts=False)
				print ('보스젠알림시간1 : ', basicSetting[1])
				print ('보스젠알림시간2 : ', basicSetting[3])
				print ('보스멍확인시간 : ', basicSetting[2])

			################ 카톡 설정 확인 ################ 
			
			if message.content == '!카톡확인':	
				katalkInformation = ''
				if basicSetting[9] == '0' :
					katalkInformation = '전체카톡 : 꺼짐\n'
				else : 
					katalkInformation = '전체카톡 : 켜짐\n'
				

				katalkInformation += '---------------------\n'

				for i in range(bossNum):
					for j in range(bossNum):
						if bossTimeString[i] and bossTimeString[j] != '99:99:99':
							if bossTimeString[i] == bossTimeString[j] and i != j:
								tmp_time1 = bossTimeString[j][:6]
								tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
								if tmp_time2 < 10 :
									tmp_time22 = '0' + str(tmp_time2)
								elif tmp_time2 == 60 :
									tmp_time22 = '00'
								else :
									tmp_time22 = str(tmp_time2)
								bossTimeString[j] = tmp_time1 + tmp_time22

				datelist2 = bossTime

				datelist = list(set(datelist2))
				
				for timestring in sorted(datelist):
					for i in range(bossNum):
						if timestring == bossTime[i]:
							if bossTimeString[i] != '99:99:99' :
								if 	bossData[i][6] == '0':
									katalkInformation += bossData[i][0] + " 카톡 : 꺼짐\n"
								else :
									katalkInformation += bossData[i][0] + " 카톡 : 켜짐\n"
				embed = discord.Embed(
						title = "----- 카톡설정내용 -----",
						description= katalkInformation,
						color=0xff00ff
						)
				await client.get_channel(channel).send( embed=embed, tts=False)

			################ my_bot.db에 저장된 보스타임 불러오기 ################ 

			if message.content == '!불러오기':
				await dbLoad()

				if LoadChk == 0:
					await client.get_channel(channel).send( '<불러오기 완료>', tts=False)
				else:
					await client.get_channel(channel).send( '<보스타임 정보가 없습니다.>', tts=False)
			
			################ 가장 근접한 보스타임 출력 ################ 

			if message.content == '!ㅂ' or message.content == '!q' or message.content == '!ㅃ' or message.content == '!Q':
				await dbLoad()

				checkTime = datetime.datetime.now() + datetime.timedelta(days=1)

				sorted_datelist = []

				datelist = bossTime
				
				tmp_sorted_datelist = sorted(datelist)

				for i in range(len(tmp_sorted_datelist)):
					if checkTime > tmp_sorted_datelist[i]:
						sorted_datelist.append(tmp_sorted_datelist[i])
					
				if len(sorted_datelist) == 0:
					await client.get_channel(channel).send( '<보스타임 정보가 없습니다.>', tts=False)
				else : 
					result_lefttime = ''
					
					
					if len(sorted_datelist) > int(basicSetting[11]):
						for j in range(int(basicSetting[11])):
							for i in range(bossNum):
								if sorted_datelist[j] == bossTime[i]:
									leftTime = bossTime[i] - datetime.datetime.now()

									total_seconds = int(leftTime.total_seconds())
									hours, remainder = divmod(total_seconds,60*60)
									minutes, seconds = divmod(remainder,60)

									result_lefttime += '다음 ' + bossData[i][0] + '탐까지 %02d:%02d:%02d 남았습니다. ' % (hours,minutes,seconds) + '[' +  bossTimeString[i] + ']\n'
					else :
						for j in range(len(sorted_datelist)):
							for i in range(bossNum):						
								if sorted_datelist[j] == bossTime[i]:
									leftTime = bossTime[i] - datetime.datetime.now()

									total_seconds = int(leftTime.total_seconds())
									hours, remainder = divmod(total_seconds,60*60)
									minutes, seconds = divmod(remainder,60)

									result_lefttime += '다음 ' + bossData[i][0] + '탐까지 %02d:%02d:%02d 남았습니다. ' % (hours,minutes,seconds) + '[' +  bossTimeString[i] + ']\n'
									#result_lefttime += bossData[i][0] + '탐[' +  bossTimeString[i] + ']까지 ' + '%02d:%02d:%02d 남았습니다.\n' % (hours,minutes,seconds)

					embed = discord.Embed(
						description= result_lefttime,
						color=0xff0000
						)
					await client.get_channel(channel).send( embed=embed, tts=False)

					datelist = []

			################ 보스타임 출력 ################ 

			if message.content == '보스탐' or message.content == '/?' or message.content == '/보스' :
				
				datelist = []
				datelist2 = []
				temp_bossTime1 = []
				ouput_bossData = []
				aa = []
				
				for i in range(bossNum):
					if bossMungFlag[i] == True :
						datelist2.append(tmp_bossTime[i])
					else :
						datelist2.append(bossTime[i])

				for i in range(fixed_bossNum):
					if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours= 3):
						datelist2.append(fixed_bossTime[i])

				datelist = list(set(datelist2))

				for i in range(bossNum):
					if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
						temp_bossTime1.append(bossData[i][0])
					else :
						aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
						if bossMungFlag[i] == True :
							aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
							aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00)
							aa.append('-')	                                 #output_bossData[3] : -
						else :
							aa.append(bossTime[i])                           #output_bossData[1] : 시간
							aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00)
							aa.append('+')	                                 #output_bossData[3] : +
						aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
						aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
						aa.append(bossData[i][7])	                         #output_bossData[6] : 메세지
						ouput_bossData.append(aa)
						aa = []

				for i in range(fixed_bossNum):
					aa.append(fixed_bossData[i][0])                      #output_bossData[0] : 보스명
					aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
					aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : 시간(00:00:00)
					aa.append('@')                                       #output_bossData[3] : @
					aa.append(0)                                         #output_bossData[4] : 멍/미입력 보스
					aa.append(0)                                         #output_bossData[5] : 멍/미입력횟수
					aa.append("")                                        #output_bossData[6] : 메세지
					ouput_bossData.append(aa)
					aa = []

				if len(temp_bossTime1) != 0:
					temp_bossTimeSTR1 = ','.join(map(str, temp_bossTime1))
					temp_bossTimeSTR1 = '```fix\n' + temp_bossTimeSTR1 + '\n```'
				else:
					temp_bossTimeSTR1 = '``` ```'
							
				information = ''
				for timestring in sorted(datelist):
					for i in range(len(ouput_bossData)):
						if timestring == ouput_bossData[i][1]:
							if ouput_bossData[i][4] == '0' :
								if ouput_bossData[i][5] == 0 :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
								else :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
							else : 
								if ouput_bossData[i][5] == 0 :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
								else :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
			
				if len(information) != 0:
					information = "```diff\n" + information + "\n```"
				else :
					information = '``` ```'

				embed = discord.Embed(
						title = "----- 보스탐 정보 -----",
						description= information,
						color=0x0000ff
						)
				embed.add_field(
						name="----- 미예약보스 -----",
						value= temp_bossTimeSTR1,
						inline = False
						)

				
				await client.get_channel(channel).send( embed=embed, tts=False)

				await dbSave()

			################ 보스타임 출력(고정보스포함) ################ 

			if message.content == '!보스탐':

				datelist = []
				datelist2 = []
				temp_bossTime1 = []
				ouput_bossData = []
				aa = []
				
				for i in range(bossNum):
					if bossMungFlag[i] == True :
						datelist2.append(tmp_bossTime[i])
					else :
						datelist2.append(bossTime[i])

				datelist = list(set(datelist2))

				for i in range(bossNum):
					if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
						temp_bossTime1.append(bossData[i][0])
					else :
						aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
						if bossMungFlag[i] == True :
							aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
							aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00)
							aa.append('-')	                                 #output_bossData[3] : -
						else :
							aa.append(bossTime[i])                           #output_bossData[1] : 시간
							aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00)
							aa.append('+')	                                 #output_bossData[3] : +
						aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
						aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
						aa.append(bossData[i][7])	                         #output_bossData[6] : 메세지
						ouput_bossData.append(aa)
						aa = []

				fixed_information = ''
				for i in range(fixed_bossNum):
						tmp_timeSTR = fixed_bossTime[i].strftime('%H:%M:%S')
						fixed_information += tmp_timeSTR + ' : ' + fixed_bossData[i][0] + '\n'

				if len(fixed_information) != 0:
					fixed_information = "```" + fixed_information + "```"
				else :
					fixed_information = '``` ```'

				temp_bossTime1 = []
				for i in range(bossNum):
					if bossTimeString[i] == '99:99:99' :
						temp_bossTime1.append(bossData[i][0])

				if len(temp_bossTime1) != 0:
					temp_bossTimeSTR1 = ','.join(map(str, temp_bossTime1))
					temp_bossTimeSTR1 = '```fix\n' + temp_bossTimeSTR1 + '\n```'
				else:
					temp_bossTimeSTR1 = '``` ```'
							
				information = ''
				for timestring in sorted(datelist):
					for i in range(len(ouput_bossData)):
						if timestring == ouput_bossData[i][1]:
							if ouput_bossData[i][4] == '0' :
								if ouput_bossData[i][5] == 0 :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
								else :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
							else : 
								if ouput_bossData[i][5] == 0 :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
								else :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
			
				if len(information) != 0:
					information = "```diff\n" + information + "\n```"
				else :
					information = '``` ```'

				embed = discord.Embed(
						title = "----- 고 정 보 스 -----",
						description= fixed_information,
						color=0x0000ff
						)
				embed.add_field(
						name="----- 보스탐 정보 -----",
						value=information,
						inline = False
						)
				embed.add_field(
						name="----- 미예약보스 -----",
						value= temp_bossTimeSTR1,
						inline = False
						)
				
				await client.get_channel(channel).send( embed=embed, tts=False)

				await dbSave()

			################ 현재시간 확인 ################ 

			if message.content == '!현재시간':
				await client.get_channel(channel).send( datetime.datetime.now().strftime('%H:%M:%S'), tts=False)

			################ 보스타임 출력 ################ 

			if message.content == '!카톡보스':

				datelist = []
				datelist2 = []
				temp_bossTime1 = []
				ouput_bossData = []
				aa = []
				
				for i in range(bossNum):
					if bossMungFlag[i] == True :
						datelist2.append(tmp_bossTime[i])
					else :
						datelist2.append(bossTime[i])

				for i in range(fixed_bossNum):
					if fixed_bossTime[i] < datetime.datetime.now() + datetime.timedelta(hours= 3):
						datelist2.append(fixed_bossTime[i])

				datelist = list(set(datelist2))

				for i in range(bossNum):
					if bossTimeString[i] == '99:99:99' and bossMungFlag[i] != True :
						temp_bossTime1.append(bossData[i][0])
					else :
						aa.append(bossData[i][0])		                     #output_bossData[0] : 보스명
						if bossMungFlag[i] == True :
							aa.append(tmp_bossTime[i])                       #output_bossData[1] : 시간
							aa.append(tmp_bossTime[i].strftime('%H:%M:%S'))  #output_bossData[2] : 시간(00:00:00)
							aa.append('-')	                                 #output_bossData[3] : -
						else :
							aa.append(bossTime[i])                           #output_bossData[1] : 시간
							aa.append(bossTime[i].strftime('%H:%M:%S'))      #output_bossData[2] : 시간(00:00:00)
							aa.append('+')	                                 #output_bossData[3] : +
						aa.append(bossData[i][2])                            #output_bossData[4] : 멍/미입력 보스
						aa.append(bossMungCnt[i])	                         #output_bossData[5] : 멍/미입력횟수
						aa.append(bossData[i][7])	                         #output_bossData[6] : 메세지
						ouput_bossData.append(aa)
						aa = []

				for i in range(fixed_bossNum):
					aa.append(fixed_bossData[i][0])                      #output_bossData[0] : 보스명
					aa.append(fixed_bossTime[i])                         #output_bossData[1] : 시간
					aa.append(fixed_bossTime[i].strftime('%H:%M:%S'))    #output_bossData[2] : 시간(00:00:00)
					aa.append('@')                                       #output_bossData[3] : @
					aa.append(0)                                         #output_bossData[4] : 멍/미입력 보스
					aa.append(0)                                         #output_bossData[5] : 멍/미입력횟수
					aa.append("")                                        #output_bossData[6] : 메세지
					ouput_bossData.append(aa)
					aa = []

				if len(temp_bossTime1) != 0:
					temp_bossTimeSTR1 = ','.join(map(str, temp_bossTime1))
					temp_bossTimeSTR1 = '```' + temp_bossTimeSTR1 + '```'
				else:
					temp_bossTimeSTR1 = '``` ```'
							
				information = ''
				for timestring in sorted(datelist):
					for i in range(len(ouput_bossData)):
						if timestring == ouput_bossData[i][1]:
							if ouput_bossData[i][4] == '0' :
								if ouput_bossData[i][5] == 0 :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
								else :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (미 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
							else : 
								if ouput_bossData[i][5] == 0 :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' ' + ouput_bossData[i][6] + '\n'
								else :
									information += ouput_bossData[i][3] + ' ' + ouput_bossData[i][2] + ' : ' + ouput_bossData[i][0] + ' (멍 ' + str(ouput_bossData[i][5]) + '회)' + ' ' + ouput_bossData[i][6] + '\n'
							
				if len(information) != 0:
					KakaoSendMSG(basicSetting[8], information, basicSetting[9], '1')
					#await client.get_channel(channel).send(information)
				else :
					KakaoSendMSG(basicSetting[8], '보스타임 정보가 없습니다.', basicSetting[9], '1')
					#await client.get_channel(channel).send(information)

			################ 보스타임 출력 ################ 

			if message.content == '!리젠':
				embed = discord.Embed(
						title='----- 리스폰 보스 -----',
						description= ' ')
				embed.add_field(name='2시간반', value='브래카', inline=False)
				embed.add_field(name='3시간', value='펠리스,템페스트,체르투바', inline=False)
				embed.add_field(name='3시간반', value='판나로드', inline=False)
				embed.add_field(name='4시간', value='바실라,엔쿠라,메두사,릴리', inline=False)
				embed.add_field(name='5시간', value='켈소스,사르카,탈라킨', inline=False)
				embed.add_field(name='6시간', value='판드라이드,여왕개미,베히모스', inline=False)
				embed.add_field(name='7시간', value='카탄', inline=False)
				embed.add_field(name='8시간', value='티미트리스,크루마,오염된크루마', inline=False)
				embed.add_field(name='10시간', value='카탄,코어수스켑터', inline=False)
				embed.add_field(name='12시간', value='사반,드래곤비스트', inline=False)
				await client.get_channel(channel).send(embed=embed, tts=False)

			################ 명존쎄 ################ 

			if message.content == '!명치':
				await client.get_channel(channel).send( '<보탐봇 명치 맞고 숨 고르기 중! 잠시만요!>', tts=False)
				print("명치!")
				for i in range(bossNum):
					if bossMungFlag[i] == True:
						bossTimeString[i] = tmp_bossTime[i].strftime('%H:%M:%S')
						bossDateString[i] = tmp_bossTime[i].strftime('%Y-%m-%d')
						bossFlag[i] = False
						bossFlag0[i] = False
						bossMungFlag[i] = False
				await dbSave()
				await voice_client1.disconnect()
				#client.clear()
				raise SystemExit

			
	client.loop.create_task(task())
	try:
		client.loop.run_until_complete(client.start(token))
	except SystemExit:
		handle_exit()
	except KeyboardInterrupt:
		handle_exit()
		#client.loop.close()
		#print("Program ended")
		#break

	print("Bot restarting")
	client = discord.Client(loop=client.loop)
