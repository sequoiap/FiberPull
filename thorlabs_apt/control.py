import thorlabs_apt as apt
import time
import numpy as np
from cmd import Cmd

class Device:
    def __init__(self, serial, name=None):
        self.name = name
        self.serial = serial
        self.motor = apt.Motor(serial)
        self.motor.set_hardware_limit_switches(2,2)
        self.motor.set_motor_parameters(512,67)
        self.motor.set_stage_axis_info(0.0,25.0,1,1.0)
        self.motor.set_move_home_parameters(2,1,2.3,0.3)
        self.motor.set_velocity_parameters(1.0,1.0,1.0)

class StageControl(Cmd):
    prompt = '>>> '
    intro = "PYTHON STAGE CONTROLLER. Type ? to list commands."

    def __init__(self):
        super().__init__()
        self.devices = []

    def do_enroll(self, input):
        '''Adds a device with the given serial number to the list of devices.

        Usage: enroll [serial number] [device-name]'''
        args = input.split()
        print(args)
        if len(args) < 2:
            print("enroll takes two arguments (fewer given)")
            return
        else:
            dev = Device(int(args[0]), args[1])
        print("Adding device with serial number \'{:8d}\' to active devices.".format(dev.serial))
        self.devices.append(dev)

    def do_list(self, input):
        '''Lists all enrolled devices'''
        print("{:<6s} {:<10s} {:<20s}".format("Order", "Serial #", "Name"))
        print("{:=<6} {:=<10} {:=<20}".format("", "", ""))
        i = 0
        for device in self.devices:
            print("{:<6d} {:<10d} {:<20s}".format(i, device.serial, device.name))
            i += 1

    def do_moveto(self, input):
        '''Sends command to specified device to move to a specified position.
        
        Usage: moveto [device-name] [position]'''
        args = input.split()
        dev = args[0]
        x = float(args[1])
        for device in self.devices:
            if dev == device.name:
                device.motor.move_to(float(args[1]))
    
    def do_home(self, input):
        '''Homes the selected stage.

        Usage: home [device-name]'''
        for device in self.devices:
            if input == device.name:
                device.motor.move_home()

    def do_exit(self, inp):
        return True

    do_EOF = do_exit

if __name__ == "__main__":
    StageControl().cmdloop()