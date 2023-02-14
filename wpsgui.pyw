import tkinter as tk
from wpsutils import atan2f, convert_to_ms, convert_to_meters, convert_to_kt, convert_to_hm, gen_min_conv
from math import degrees, radians, cos, sin
from PIL import Image, ImageTk
from wpsclass import SubScen

LINE_LEN = 70
TORP_LIST = ["G7a-lo", "G7a-md", "G7a-hi", "G7e-st"]

class WpsGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WolfPack Solution V.1.0")
        self.resizable(False, False)
        self.geometry("515x580+100+100")
        self.iconbitmap(r"./media/wps.ico")
        
        # Init the wps module...
        self.wps = SubScen()
        
        # tkinter vars
        # Submarine vars...
        self.sub_hdg = tk.IntVar()
        self.sub_hdg.set(360)
        self.sub_spd = tk.DoubleVar()
        self.sub_spd.set(0.0)
        # Target vars...
        self.rng_scale = tk.IntVar()
        self.rng_scale.set(0)
        self.brg_A = tk.IntVar()
        self.brg_A.set(360)
        self.rng_A = tk.DoubleVar()
        self.rng_A.set(1.0)
        self.brg_B = tk.IntVar()
        self.brg_B.set(360)
        self.rng_B = tk.DoubleVar()
        self.rng_B.set(1.0)
        
        # Torp var...
        self.torps = tk.StringVar()
        self.torps.set(TORP_LIST[0])
        
        # Mark time var...
        self.time_M = tk.StringVar()
        self.time_S = tk.DoubleVar()

        # Image var...
        self.rose_img = None
        
        # Data vars
        self.v_status = tk.StringVar()
        self.v_status.set("---")
        self.v_tar_H = tk.IntVar()
        self.v_tar_H.set(0)
        self.v_tar_S = tk.DoubleVar()
        self.v_tar_S.set(0.0)
        self.v_tar_AOB = tk.IntVar()
        self.v_tar_AOB.set(0)
        self.v_tor_Imp = tk.IntVar()
        self.v_tor_Imp.set(0)
        self.v_tor_Tm = tk.StringVar()
        self.v_tor_Tm.set("0:00")
        self.v_tor_Rng = tk.DoubleVar()
        self.v_tor_Rng.set(0.0)
        self.v_tor_Hdg = tk.IntVar()
        self.v_tor_Hdg.set(0)
        self.v_gyro = tk.IntVar()
        self.v_gyro.set(0)
        
                
        # Startup...
        self.create_widgets()
        self.place_widgets()
        self.initialize_app()
        
        
    def create_widgets(self):
        self.hdg_lbl = tk.Label(        self, text="Sub heading:")
        self.brg_A_lbl = tk.Label(      self, text="Mark A bearing:")
        self.brg_B_lbl = tk.Label(      self, text="Mark B bearing:")
        self.hdg_val = tk.Entry(        self, width=5, bd=2, textvariable=self.sub_hdg, state="readonly", justify=tk.CENTER)
        self.brg_A_val = tk.Entry(      self, width=5, bd=2, textvariable=self.brg_A, state="readonly", justify=tk.CENTER)
        self.brg_B_val = tk.Entry(      self, width=5, bd=2, textvariable=self.brg_B, state="readonly", justify=tk.CENTER)
        self.hdg_canvas = tk.Canvas(    self, 
                                        width=147, 
                                        height=147, 
                                        bg="white", 
                                        bd=2, 
                                        relief=tk.GROOVE, 
                                        cursor="tcross")
                                        
        self.brg_A_canvas = tk.Canvas(  self, 
                                        width=147, 
                                        height=147, 
                                        bg="white", 
                                        bd=2, 
                                        relief=tk.GROOVE, 
                                        cursor="tcross")
                                        
        self.brg_B_canvas = tk.Canvas(  self, 
                                        width=147, 
                                        height=147, 
                                        bg="white", 
                                        bd=2, 
                                        relief=tk.GROOVE, 
                                        cursor="tcross")
                                        
        self.spd_scale = tk.Scale(      self, 
                                        label="Sub speed (kt)", 
                                        from_=0.0, 
                                        to=20.0, 
                                        resolution=0.1, 
                                        length=131, 
                                        repeatdelay=200,
                                        takefocus=True,
                                        variable=self.sub_spd,
                                        orient=tk.HORIZONTAL)
                                        
        self.rng_A_scale = tk.Scale(    self, 
                                        label="Range A (hm)", 
                                        from_=1.0, 
                                        to=80.0, 
                                        resolution=0.1, 
                                        length=131, 
                                        repeatdelay=100,
                                        takefocus=True,
                                        variable=self.rng_A,
                                        orient=tk.HORIZONTAL)
                                        
        self.rng_B_scale = tk.Scale(    self, 
                                        label="Range B (hm)", 
                                        from_=1.0, 
                                        to=80.0, 
                                        resolution=0.1, 
                                        length=131, 
                                        repeatdelay=100,
                                        takefocus=True,
                                        variable=self.rng_B,
                                        orient=tk.HORIZONTAL)
                                        
        self.lr_A_chk = tk.Checkbutton( self, variable=self.rng_scale, text="LR", command=self.change_range)
        
        self.torp_lbl = tk.Label(       self, text="Select Torpedo Type")
        self.torp_opt = tk.OptionMenu(  self, self.torps, *TORP_LIST)
        self.torp_opt.configure(width=15)
        
        self.mark_time = tk.Scale(      self,
                                        label="Mark Time (seconds)",
                                        from_=1,
                                        to=600,
                                        length=131,
                                        repeatdelay=200,
                                        takefocus=True,
                                        variable=self.time_S,
                                        command=self.minute_convert,
                                        orient=tk.HORIZONTAL)
        
        self.min_lbl = tk.Label(        self, text="Mark Time (minutes)")
        self.min_conv = tk.Entry(       self, width=10, bd=2, textvariable=self.time_M, state="readonly", justify=tk.CENTER)
        
        self.exec_btn = tk.Button(      self, text="-- EXECUTE --", 
                                        width=18, 
                                        bg="#FAFFA9",
                                        activebackground="#FFEFA9",
                                        command=self.generate_data)
        
        self.sol_frm = tk.Frame(        self, width=455, height=160, bd=2, bg="white", relief=tk.GROOVE)
        
        self.sol_lbl = tk.Label(        self.sol_frm, bg="white", text="SOLUTION:")
        
        self.tar_hdg_lbl = tk.Label(    self.sol_frm, bg="white", text="Target Heading:")
        self.tar_spd_lbl = tk.Label(    self.sol_frm, bg="white", text="Target Speed (kt):")
        self.tar_aob_lbl = tk.Label(    self.sol_frm, bg="white", text="Target AOB:")
        self.torp_imp_lbl = tk.Label(   self.sol_frm, bg="white", text="Impact Angle:")
        self.torp_tm_lbl = tk.Label(    self.sol_frm, bg="white", text="Torp Run Time:")
        self.torp_rng_lbl = tk.Label(   self.sol_frm, bg="white", text="Torp Run Dist (hm):")
        self.torp_hdg_lbl = tk.Label(   self.sol_frm, bg="white", text="Torp Heading:")
        self.gyro_ang_lbl = tk.Label(   self.sol_frm, bg="white", text="Gyro Angle (rel):")
        
        self.status_val = tk.Entry(     self.sol_frm, 
                                        relief=tk.FLAT, 
                                        width= 15, 
                                        readonlybackground="white", 
                                        state="readonly", 
                                        textvariable=self.v_status, 
                                        justify=tk.LEFT)    # Int
        
        self.tar_hdg_val = tk.Entry(    self.sol_frm, 
                                        relief=tk.FLAT, 
                                        width= 7, 
                                        readonlybackground="white", 
                                        state="readonly", 
                                        textvariable=self.v_tar_H, 
                                        justify=tk.CENTER)    # Int
                                        
        self.tar_spd_val = tk.Entry(    self.sol_frm, 
                                        relief=tk.FLAT, 
                                        width= 7, 
                                        readonlybackground="white", 
                                        state="readonly", 
                                        textvariable=self.v_tar_S, 
                                        justify=tk.CENTER)    # Double
                                        
        self.tar_aob_val = tk.Entry(    self.sol_frm, 
                                        relief=tk.FLAT, 
                                        width= 7, 
                                        readonlybackground="white", 
                                        state="readonly", 
                                        textvariable=self.v_tar_AOB, 
                                        justify=tk.CENTER)  # Int 
                                        
        self.torp_imp_val = tk.Entry(   self.sol_frm, 
                                        relief=tk.FLAT, 
                                        width= 7, 
                                        readonlybackground="white", 
                                        state="readonly", 
                                        textvariable=self.v_tor_Imp, 
                                        justify=tk.CENTER)  # Int
                                        
        self.torp_tm_val = tk.Entry(    self.sol_frm, 
                                        relief=tk.FLAT, 
                                        width= 7, 
                                        readonlybackground="white", 
                                        state="readonly", 
                                        textvariable=self.v_tor_Tm, 
                                        justify=tk.CENTER)   # String
                                        
        self.torp_rng_val = tk.Entry(   self.sol_frm, 
                                        relief=tk.FLAT, 
                                        width= 7, 
                                        readonlybackground="white", 
                                        state="readonly", 
                                        textvariable=self.v_tor_Rng, 
                                        justify=tk.CENTER)  # Int
                                        
        self.torp_hdg_val = tk.Entry(   self.sol_frm, 
                                        relief=tk.FLAT, 
                                        width= 7, 
                                        readonlybackground="white", 
                                        state="readonly", 
                                        textvariable=self.v_tor_Hdg, 
                                        justify=tk.CENTER)  # Int
                                        
        self.gyro_ang_val = tk.Entry(   self.sol_frm, 
                                        relief=tk.FLAT, 
                                        width= 7, 
                                        readonlybackground="white",
                                        state="readonly", 
                                        textvariable=self.v_gyro, 
                                        justify=tk.CENTER)     # Int
        
        # Bindings
        self.hdg_canvas.bind("<Button-1>", self.hdg_canvas_draw)
        self.hdg_canvas.bind("<MouseWheel>", self.hdg_canvas_draw)
        self.brg_A_canvas.bind("<Button-1>", self.brg_A_canvas_draw)
        self.brg_A_canvas.bind("<MouseWheel>", self.brg_A_canvas_draw)
        self.brg_B_canvas.bind("<Button-1>", self.brg_B_canvas_draw)
        self.brg_B_canvas.bind("<MouseWheel>", self.brg_B_canvas_draw)

                                        
    def place_widgets(self):
        # Using place. Future versions may use grid.
        
        self.hdg_lbl.place(x=30, y=11)
        self.brg_A_lbl.place(x=191, y=11)
        self.brg_B_lbl.place(x=352, y=11)
        self.hdg_val.place(x=125, y=11)
        self.brg_A_val.place(x=286, y=11)
        self.brg_B_val.place(x=448, y=11)
        self.hdg_canvas.place(x=20, y=40)
        self.brg_A_canvas.place(x=181, y=40)
        self.brg_B_canvas.place(x=342, y=40)
        self.spd_scale.place(x=30, y=202)
        self.rng_A_scale.place(x=191, y=202)
        self.rng_B_scale.place(x=352, y=202)
        self.lr_A_chk.place(x=285, y=202)
        self.torp_lbl.place(x=30, y=270)
        self.torp_opt.place(x=30, y=300)
        self.mark_time.place(x=191, y=270)
        self.min_lbl.place(x=360, y=272)
        self.min_conv.place(x=390, y=305)
        self.exec_btn.place(x=190, y=350)
        
        self.sol_frm.place(x=30, y=390)
        
        self.sol_lbl.place(x=10, y=8)
                
        self.tar_hdg_lbl.place(x=10, y=35)
        self.tar_spd_lbl.place(x=10, y=65)
        self.tar_aob_lbl.place(x=10, y=95)
        self.torp_imp_lbl.place(x=10, y=125)
        self.torp_tm_lbl.place(x=230, y=35)
        self.torp_rng_lbl.place(x=230, y=65)
        self.torp_hdg_lbl.place(x=230, y=95)
        self.gyro_ang_lbl.place(x=230, y=125)
        
        self.status_val.place(x=80, y=9)
        self.tar_hdg_val.place(x=130, y=35)
        self.tar_spd_val.place(x=130, y=65)
        self.tar_aob_val.place(x=130, y=95)
        self.torp_imp_val.place(x=130, y=125)
        self.torp_tm_val.place(x=350, y=35)
        self.torp_rng_val.place(x=350, y=65)
        self.torp_hdg_val.place(x=350, y=95)
        self.gyro_ang_val.place(x=350, y=125)
        
        
    def initialize_app(self):
        # Initialize...
        self.rose_img = ImageTk.PhotoImage(Image.open(r"./media/rose.png"))
        self.draw_canvas_pointer(self.hdg_canvas, self.sub_hdg.get())
        self.draw_canvas_pointer(self.brg_A_canvas, self.brg_A.get())
        self.draw_canvas_pointer(self.brg_B_canvas, self.brg_B.get())
        self.minute_convert(1)
        
    
    def change_range(self):
        if self.rng_scale.get() == 1: # LR checked...
            self.rng_A_scale.config(from_=60.0, to=200.0)
            self.rng_B_scale.config(from_=60.0, to=200.0)
            self.rng_A_scale.set(60.0)
            self.rng_B_scale.set(60.0)
        else:
            self.rng_A_scale.config(from_=1.0, to=80.0)
            self.rng_B_scale.config(from_=1.0, to=80.0)
            self.rng_A_scale.set(1.0)
            self.rng_B_scale.set(1.0)


    def hdg_canvas_draw(self, event):
        self.canvas_draw(event, self.hdg_canvas, self.sub_hdg)


    def brg_A_canvas_draw(self, event):
        self.canvas_draw(event, self.brg_A_canvas, self.brg_A)

        
    def brg_B_canvas_draw(self, event):
        self.canvas_draw(event, self.brg_B_canvas, self.brg_B)
    

    def canvas_draw(self, event, cnv, var):
        #self.hdg_canvas.delete("all")
        # Note: Event types may look like numbers, but they are really strings.
        if event.type == "38": # MouseWheel
            brg = var.get()
            if event.delta > 0:
                brg = (lambda b: (b + 1) if (b + 1) <= 360 else (b + 1) - 360)(brg)
            else:
                brg = (lambda b: (b - 1) if (b - 1) > 0 else (b - 1) + 360)(brg)
            var.set(brg)
        elif event.type == "4": # MouseButton
            brg = self.get_canvas_angle(event.x, event.y)
            var.set(brg)
                    
        self.draw_canvas_pointer(cnv, brg)
   

    def draw_canvas_pointer(self, cnv, brg):
        cnv.delete("all")
        cnv.create_image(3, 3, anchor=tk.NW, image = self.rose_img)
        rbrg = radians(brg)
        x = (sin(rbrg) * LINE_LEN) + 77
        y = 77 - (cos(rbrg) * LINE_LEN)
        cnv.create_line(77, 77, x, y, width = 2, fill = "red")

    
    def get_canvas_angle(self, x, y):
        x_dist = x - 77
        y_dist = 77 - y
        tbrg = round(degrees(atan2f(x_dist, y_dist)))
        return tbrg if tbrg != 0 else 360
        
        
    def minute_convert(self, sec):
        # Special minute convert for the tkinter variable.
        # This is NOT a general minute converter.
        # wpsutils.py contains that.
        try:
            f_sec = float(sec)
            d_min = f_sec / 60.0
            s_min = f"{int(d_min)}:{round((d_min - int(d_min)) * 60):02}"
        except TypeError:
            s_min = "ERROR"
            
        self.time_M.set(s_min)
    
    
    def generate_data(self):
        # The app works in hectometers and knots, the wps class in meters and meters per second.
        # Be careful with using the correct converters appropriately.
        # Collect Data phase...
        self.wps.get_sub["hdg"] = radians(self.sub_hdg.get())
        self.wps.get_sub["spd"] = convert_to_ms(self.sub_spd.get())
        self.wps.get_state["st_brg_A"] = radians(self.brg_A.get())
        self.wps.get_state["st_rng_A"] = convert_to_meters(self.rng_A.get())
        self.wps.get_state["st_brg_B"] = radians(self.brg_B.get())
        self.wps.get_state["st_rng_B"] = convert_to_meters(self.rng_B.get())
        self.wps.get_state["s_time"] = self.time_S.get() # It is already a float from the scale.
        self.wps.set_torp(self.torps.get())
        # Execute Data phase...
        self.wps.mover(self.wps.get_sub, self.wps.get_state["s_time"], ("nx", "ny"))
        self.wps.plotter()
        self.wps.torp_calculator()
        self.print_out_data()
        
        # DEBUG (raw)
        """
        print(self.wps.get_sub["hdg"])
        print(self.wps.get_sub["spd"])
        print(self.wps.get_state["st_brg_A"])
        print(self.wps.get_state["st_rng_A"])
        print(self.wps.get_state["st_brg_B"])
        print(self.wps.get_state["st_rng_B"])
        print(self.wps.get_state["s_time"])
        print(self.wps.get_torps[self.torps.get()][0])
        print(self.wps.get_torps[self.torps.get()][1])
        """
        # DEBUG
        # Corrected, converted data...
        """
        print("Target Hdg:", round(degrees(self.wps.get_target["hdg"]), 2))
        print("Target Spd:", round(convert_to_kt(self.wps.get_target["spd"]), 2))
        print("Launch AOB:", round(degrees(self.wps.get_state["aob"]), 2))
        print("Torp Hdg:", round(degrees(self.wps.get_weapon["hdg"]), 2))
        print("Torp Rng:", round(self.wps.get_state["wpn_run"], 2))
        print("Torp status:", self.wps.get_state["status"])
        print("Torp time:", self.wps.get_state["torp_time"]) # Seconds
        print("Impact:", round(degrees(self.wps.get_state["impact"]), 2))
        print("Gyro Angle:", round(degrees(self.wps.get_state["gyro_angle"])))
        """
        
    
    def print_out_data(self):
        if self.wps.get_state["status"] == "OUT OF RANGE":
            self.status_val.configure(fg="red")
        elif self.wps.get_state["status"] == "IN RANGE":
            self.status_val.configure(fg="green")
            
        self.v_status.set(self.wps.get_state["status"])                                     # String
        self.v_tar_H.set(int(degrees(self.wps.get_target["hdg"])))                          # Int
        self.v_tar_S.set(round(convert_to_kt(self.wps.get_target["spd"]), 1))               # Double
        self.v_tar_AOB.set(int(degrees(self.wps.get_state["aob"])))                         # Int
        self.v_tor_Imp.set(int(degrees(self.wps.get_state["impact"])))                      # Int
        self.v_tor_Tm.set(str(gen_min_conv(self.wps.get_state["torp_time"])))               # String
        self.v_tor_Rng.set(round(float(convert_to_hm(self.wps.get_state["wpn_run"])),1))    # Double
        self.v_tor_Hdg.set(int(degrees(self.wps.get_weapon["hdg"])))                        # Int
        self.v_gyro.set(int(degrees(self.wps.get_state["gyro_angle"])))                     # Int

    
# Configure for Windows and Initiate Mainloop...       
if __name__ == "__main__":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        Wps = WpsGui()
        Wps.mainloop()
    