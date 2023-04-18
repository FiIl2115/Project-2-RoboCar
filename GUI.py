from tkinter import *
import paho.mqtt.client as mqtt
import webbrowser

class UI:

    def __init__(self, master):
        self.master = master
        master.title("Wrover Console")
    
    #Left Frame and its contents
        self.left_Frame = Frame(master, width=200, height = 800,bg='gray')
        self.left_Frame.grid(row=0, column=0, padx=10, pady=2)
        Label(self.left_Frame, text="Mission Commands:",bg='gray').grid(row=0, column=0, padx=10, pady=2)
        
        self.commandlist = Text( self.left_Frame, width=30, height=5, takefocus=0)
        self.commandlist.grid(row=1, column=0, padx=10, pady=2)

        Label(self.left_Frame, text = "")

    #Right Frame and its contents
        self.rightFrame = Frame(master, width=400, height = 800, bg='gray')
        self.rightFrame.grid(row=0, column=1, padx=10, pady=2)

        self.circleCanvas = Canvas(self.rightFrame, width=800, height=600, bg='black')
        self.circleCanvas.grid(row=0, column=0, padx=10, pady=2)

        self.btnFrame = Frame(self.rightFrame, width=400, height = 400,bg='gray')
        self.btnFrame.grid(row=1, column=0, padx=10, pady=2)
        
        self.AirQualityBtn = Button(self.btnFrame, text="AirQuality", command=self.AirQuality,bg='gray')
        self.AirQualityBtn.grid(row=0, column=5, padx=10, pady=2)

        self.ProgramMissionBtn = Button(self.btnFrame, text="Program Mission", command=self.ProgramMission,bg='gray')
        self.ProgramMissionBtn.grid(row=0, column=1, padx=10, pady=2)

        self.SendMissionBtn = Button(self.btnFrame,text = "Send Mission",command =self.SendMission,bg='gray')
        self.SendMissionBtn.grid(row=0, column=2, padx=10, pady=2)

        self.AbortMissionBtn = Button(self.btnFrame,text = "Abort Mission",command =self.AbortMission,bg='gray')
        self.AbortMissionBtn.grid(row=0, column=3, padx=10, pady=2)

        self.EditMissionBtn = Button(self.btnFrame,text = "Edit Mission",command =self.Showmission,bg='gray')
        self.EditMissionBtn.grid(row=0, column=4, padx=10, pady=2)

    #Low Right Frame
        self.lowFrame = Frame(master, width=400, height = 100, bg='gray')
        self.lowFrame.grid(row=1, column=1, padx=10, pady=2)

    #Camera Browser Open
        url = 'http://10.120.0.87/'
        webbrowser.open(url)

    def AirQuality(self):
        self.commandlist.insert(0.0, "Receiving Sensor Data\n")
        self.Airquality = Text(self.lowFrame, width=20, height=5, takefocus=0, pady=2)
        self.Airquality.grid(row=0, column=1, padx=10, pady=2)
        Label(self.lowFrame, text="Humidity:\n Dust:\n",bg='gray').grid(row=0, column=0, padx=10, pady=2)

        def on_message(client, userdata, message):
            msg = str(message.payload.decode("utf-8"))
            print("message received " , msg)

            f = open("airquality.txt", "w")
            f.write(str(msg) )
            f.write("\n")
        
            f = open ("airquality.txt", "r")
            
            for line in f:
                self.Airquality.insert(0.0, line)
            f.close()

        broker_address="10.120.0.45"
        client = mqtt.Client() 
        client.on_message=on_message 
        client.connect(broker_address) 
        print("Subscribing to topic","MarsWrover/Sensors/#")
        client.subscribe("MarsWrover/Sensors/#")
        client.loop_start()
        client.publish("MarsWrover/Mission","a s")

    def ProgramMission(self):
        self.edit= Text(self.left_Frame, width=30, height=5, takefocus=0, pady=2 , bg='white')
        self.edit.grid(row=3, column=0, padx=10, pady=2)
        self.commandlist.insert(0.0, "Programing Mission\n")
        Label(self.left_Frame, text="Mission Programing: ", bg='gray').grid(row=2,column=0, padx=10, pady=2)
        Label(self.left_Frame, text = "Instruction:\n  Forward: f+distance\n  Back: b+distance\n Left: l+distance\n Right: r+distance", bg='gray').grid(row=4, column=0, padx=10, pady=2)

    def SendMission(self):
        self.commandlist.insert(0.0, "Sending Mission\n")

        f = open("mission.txt", "w")
        inp = self.edit.get(1.0, "end-1c")

        f.write(str(inp) )

        broker_address="10.120.0.45"
        client = mqtt.Client() 
        client.connect(broker_address) 
        print("Subscribing to topic","MarsWrover/Mission")
        client.subscribe("MarsWrover/Mission")
        client.loop_start()
        client.publish("MarsWrover/Mission",inp)
        f.close()

    def AbortMission(self):
        broker_address="10.120.0.45"
        client = mqtt.Client()
        client.connect(broker_address) 
        print("Subscribing to topic","MarsWrover/Mission")
        client.subscribe("MarsWrover/Mission")
        client.loop_start()
        client.publish("MarsWrover/Mission","p s")

    def Showmission(self):
        self.commandlist.insert(0.0, "EditMission\n")
        window3 = Tk()
        window3.wm_title("Window Title")
        window3.config(background = "#808080")
        window3.geometry('320x200')

        self.Editm= Text(window3, width=30, height=5, takefocus=0, pady=2  )
        self.Editm.grid(row=0, column=0, padx=10, pady=2)

        f = open("mission.txt")
        content = f.read()    
        self.Editm.insert(0.0, content)

        def resend():
            f = open("mission.txt", "w")
            inp = self.Editm.get(1.0, "end-1c")

            f.write(str(inp) )

            broker_address="10.120.0.45"
            client = mqtt.Client() 
            client.connect(broker_address) 
            print("Subscribing to topic","MarsWrover/Mission")
            client.subscribe("MarsWrover/Mission")
            client.loop_start()
            client.publish("MarsWrover/Mission",inp)

        self.Editbtn= Button(window3,text = "Send New Mission", width=15, height=2, takefocus=0, pady=2, bg='gray',command =resend )
        self.Editbtn.grid(row=1, column=0, padx=10, pady=2)

        f.close()

root = Tk() 
my_gui = UI(root)
root.config(background = "#808080")
root.mainloop()