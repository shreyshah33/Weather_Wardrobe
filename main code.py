# Made during the 24 hour HowdyHack Hackathon.
# Team Members - Shrey Shah, Pablo Say, Cameron Brock, Davis Kirchhofer
# 2 emails - system_email and server_email are used. All IFTTT are from the system email account.

from tkinter import *
import tkinter.font
import tkinter.messagebox
import urllib.request
import json
import requests
import smtplib
import imaplib
import email

from email.mime.text import MIMEText

global a

#api token for Weather API
api_token = "your_token_here"
api_url_base = "https://api.darksky.net/forecast/"

#get_coordinates gets the latitutde and longitude from the address you provide
def get_coordinates(address):
    address_str = address.replace(' ', '+')
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    key = '&key=your_key_here'

    url = url + address_str + key
    json_str = urllib.request.urlopen(url).read()

    parsed_json = json.loads(json_str)
    try:
        loc = parsed_json['results'][0]['geometry']['location']
    except:
         loc = parsed_json['results'][0]['location']

    lat = loc['lat']
    lng = loc['lng']

    return [lat, lng]

#Weather API JSON Parsing Wrapper which then gives the required output
class DarkSkyWrapper:
    
    def __init__(self, url, token, latitude, longitude, excludes = ""):
        api_request = url + token + "/" + latitude + "," + longitude
        if(excludes is not ""):
            api_request = api_request + "?exclude=" + excludes
        response = requests.get(api_request)
        if(response.status_code is not 200):
            raise requests.exceptions.HTTPError("Bad response")
        self.data = response.content
        self.json_data = response.json()
        
    def currently_setup(self):
        self.currently = self.json_data["currently"]

    def create_advice_letters(self):
        self.advice_list = []
        
        
        #Temperature decided
        if(self.currently["temperature"]>80): #H for hot
            self.advice_list.append("H") #shorts and short tshirt
        elif(self.currently["temperature"]>50): #W for warm; can have U for humid, L for cloudy
            self.advice_list.append("W") #shorts and tshirt if humid, pants and tshirt if not
        elif(self.currently["temperature"]>32): #C for cold
            self.advice_list.append("C") #long tshirt, pants, jackets
        else: #F for freezing
            self.advice_list.append("F") #long tshirt, pants, coat
            
        if(self.currently["precipProbability"]<0.1): #D for dry
            self.advice_list.append("D")
        elif(self.currently["precipProbability"]<0.8): #G for good chance of percipitation
            self.advice_list.append("G")
        else: #P for percipitation
            self.advice_list.append("P")    
            
        #humidity decider 
        if(self.currently["humidity"] > 0.5): #U for humid
            self.advice_list.append("U")
            
        #cloudiness decider
        if(self.currently["cloudCover"] > 0.5):
            self.advice_list.append("L")
        elif(self.currently["cloudCover"] < 0.2):
            self.advice_list.append("S")

        #windiness decider
        if(self.currently["windSpeed"] > 5):
            self.advice_list.append("I")

        while(len(self.advice_list)<5):
            self.advice_list.append("X")

        #print(self.advice_list)
        
    def choose_clothes(self):
        self.clothes = ""

        if (self.advice_list[1] == "P"): # If it will precipitate
            self.clothes += "Poncho\nUmbrella\n"
        elif (self.advice_list[1] == "G"): # If there is a good chance of precipitation
            if (self.advice_list[4] == "I"): # If it will be windy
                self.clothes += "Poncho\n"
            else: #If there is a good chance of precipitation but it will not be windy
                self.clothes += "Umbrella\n"
        
        if(self.advice_list[0] == "H"): #If it will be hot
            self.clothes += "Shorts\nShort sleeved t-shirt\n"
        elif (self.advice_list[0] == "W"): #If it will be warm
            self.clothes += "Short sleeved t-shirt\n"
            if (self.advice_list[2] == "U" or self.advice_list[1] == "S"): #If it is humid or sunny
                self.clothes += "Shorts\n"
            else: # If it will be warm but neither humid nor sunny
                self.clothes += "Pants\n"
        else: # If it will be neither hot nor warm
            self.clothes += "Long sleeved t-shirt\nPants\nJacket"
            if (self.advice_list[0] == "C"): # If it will be neither hot nor warm, but it will be cold
                self.clothes += "Boots\nGloves"
    
        if (self.advice_list[1] == "S"): # If it will not be cloudy
            self.clothes += "Sunglasses"
        
    def test_output(self):
        if(self.currently["precipProbability"] > 0.5):
            self.test = "R"
        elif(self.currently["temperature"] > 60):
            self.test = "W"
        else:
            self.test = "C"

        msg = MIMEText("this is text")
        msg['From'] = "server_email"
        msg['To'] = "system_email"
        msg['Subject'] = ''.join(self.advice_list)
        sent_from = "server_email"  
        to = "system_email" 
        body = ''.join(self.advice_list)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login("server_email", "password")
        s.send_message(msg)
        s.close()
        print('Email sent!')
        return(self.test)

    



#GUI Code -----------------------------------------------------------------------------------------------------------------#

def address_error():
    tkinter.messagebox.showerror("Error!", "Address is Invalid")

def empty_location():
    tkinter.messagebox.showerror("Error!", "Please fill out all fields")

def zip_error():
    tkinter.messagebox.showerror("Error!", "Zip Code Number Provided invalid")
    

def submit_location():
    userAddress = locationAddress.get()
    userCity = locationCity.get()
    userState = locationState.get()
    userZip = locationZip.get()

    #if user fails to provide a single input, program calls a error function to alert user
    
    if (userAddress == "") | (userCity == "") | (userState == "") | (userZip == ""):
        empty_location()

    #checks for valid zip code
    try: 
        zipNumber = int(userZip)
        if zipNumber < 501 | zipNumber > 99950:
            zip_error()
    except:
        zip_error()
    
    #checks for a valid address
    try: 
        int(userAddress[0])
    except:
        address_error()

    #if there are no errors, then the function will complete
    else:
        fullAddress = userAddress + ", " + userCity + ", " + userState  + ", " + userZip

        
        a = DarkSkyWrapper(api_url_base,api_token,str(get_coordinates(fullAddress)[0]),str(get_coordinates(fullAddress)[1]),"minutely,hourly,daily,alerts,flags")
        a.currently_setup()
        a.create_advice_letters()
        a.choose_clothes()
        a.test_output()

        Label (guiWeather, text = "Suggested Clothes: ", bg = "light sky blue", fg = "white", font = "none 12 bold").grid (row= 1, column =2, sticky=W)
        Label (guiWeather, text = a.clothes, bg = "light sky blue", fg = "white", font = "none 12 bold").grid (row= 2, column =2, sticky=W)

#grabs data from email subject line sent from IFTTT
def okgoogle():
    obj = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    obj.login('server_email', 'password')
    obj.select('inbox')
    type, data = obj.search(None, 'all')
    num = data[0].split()[-1]
    #for num in data[0].split():
    type2, data2 = obj.fetch(num, '(RFC822)' )
    msg2 = email.message_from_bytes(data2[0][1])
    print(msg2['Subject'])
    a = DarkSkyWrapper(api_url_base,api_token,str(get_coordinates(msg2['Subject'])[0]),str(get_coordinates(msg2['Subject'])[1]),"minutely,hourly,daily,alerts,flags")
    a.currently_setup()
    a.create_advice_letters()
    a.choose_clothes()
    a.test_output()

    Label (guiWeather, text = "Suggested Clothes: ", bg = "light sky blue", fg = "white", font = "none 12 bold").grid (row= 1, column =2, sticky=W)
    Label (guiWeather, text = a.clothes, bg = "light sky blue", fg = "white", font = "none 12 bold").grid (row= 2, column =2, sticky=W)
    
  
#creates gui window
guiWeather = Tk()
guiWeather.title("Weather Wear")
myfont = tkinter.font.Font(family = "Arial", size = "12" , weight = "bold")
guiWeather.configure(background = "sky blue")

#text entry box for location
Label (guiWeather, text = "Enter Address", bg = "light sky blue", fg = "white", font = "none 12 bold") . grid(row = 1, column = 0, sticky=W)

locationAddress = Entry(guiWeather, width = 20, bg= "white")
locationAddress.grid(row = 1, column = 1, sticky=W)

#text entry box for city 
Label (guiWeather, text = "Enter City", bg = "light sky blue", fg = "white", font = "none 12 bold") . grid(row = 2, column = 0, sticky=W)
locationCity = Entry(guiWeather, width = 20, bg = "white" )
locationCity.grid(row = 2, column = 1, sticky =W )

#text entry box for state
Label (guiWeather, text = "Enter State Abbriviations (i.e. TX)", bg = "light sky blue", fg = "white", font = "none 12 bold") . grid(row = 3, column = 0, sticky=W)
locationState = Entry (guiWeather,width = 20, bg = "white")
locationState.grid (row=  3, column  =1, sticky = W )

#text entry box for zip code
Label (guiWeather, text = "Enter Zip Code", bg = "light sky blue", fg = "white", font = "none 12 bold") . grid( row = 4, column = 0, sticky = W)
locationZip = Entry (guiWeather,width = 20, bg = "white")
locationZip.grid(row = 4, column = 1, sticky=W)

#submit button that reads in all inputs & concatenates
Button(guiWeather, text= "Enter Location", width = 10, command =submit_location ).grid (row = 5, column = 1, sticky = W)

#runs new function
Button(guiWeather,text = "OK Google", width = 10, command = okgoogle).grid (row=6, column = 1,sticky=W )

#runs window loop
guiWeather.mainloop()