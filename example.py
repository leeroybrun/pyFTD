from FrenchTorrentDB import FrenchTorrentDB

ftd = FrenchTorrentDB('username', 'password')

if ftd.login():
	print ftd.getRatio()