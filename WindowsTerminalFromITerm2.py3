from os.path import basename, splitext
import json
import sys
import xml.etree.ElementTree as ET

colorMapping = {
	"Ansi 0 Color": "black",
	"Ansi 1 Color": "red",
	"Ansi 2 Color": "green",
	"Ansi 3 Color": "yellow",
	"Ansi 4 Color": "blue",
	"Ansi 5 Color": "purple",
	"Ansi 6 Color": "cyan",
	"Ansi 7 Color": "white",
	"Ansi 8 Color": "brightBlack",
	"Ansi 9 Color": "brightRed",
	"Ansi 10 Color": "brightGreen",
	"Ansi 11 Color": "brightYellow",
	"Ansi 12 Color": "brightBlue",
	"Ansi 13 Color": "brightPurple",
	"Ansi 14 Color": "brightCyan",
	"Ansi 15 Color": "brightWhite",
	"Cursor Color": "cursorColor",
	"Cursor Text Color": "!cursorTextColor",
	"Bold Color": "!boldColor",
	"Selected Text Color": "!selectionForeground",
	"Selection Color": "selectionBackground",
	"Background Color": "background",
	"Foreground Color": "foreground",
}
def real2hex(real):
	return '%02X' % int( float(real) * 255 )

def rgb2hex(R, G, B):
	return '#%02X%02X%02X' % (R, G, B)

def parseXML(xmlfile, printfn=print):
	keyToHexColor = {}
	winTermOut = {
		'name': splitext(basename(xmlfile))[0],
	}
	tree = ET.parse(xmlfile)
	root = tree.getroot()
	keys = root.findall('./dict/key')
	valkeys = root.findall('./dict/dict/key')
	valreals = root.findall('./dict/dict/real')
	for i, key in enumerate(keys):
		printfn(key.text)
		R,G,B = [0, 0, 0]
		for j in range(3):
			vktext = valkeys[i*3+j].text
			vrtext = valreals[i*3+j].text
			printfn('', vktext, '{:20}'.format(vrtext),
				real2hex(vrtext), sep='\t')
			if vktext.startswith('R'):
				R = int( float(vrtext) * 255 )
			elif vktext.startswith('G'):
				G = int( float(vrtext) * 255 )
			elif vktext.startswith('B'):
				B = int( float(vrtext) * 255 )
		hexColor = rgb2hex(R, G, B)
		printfn(key.text, 'is\t' + hexColor)
		keyToHexColor[key.text] = hexColor
		outKey = colorMapping[key.text]
		if not outKey.startswith('!'):
			winTermOut[outKey] = hexColor
	print(json.dumps(winTermOut, sort_keys=False, indent=4))

def main():
	for xmlfile in sys.argv[1:]:
		parseXML(xmlfile, lambda *args, **kw: None)

if __name__ == "__main__":
	main()

