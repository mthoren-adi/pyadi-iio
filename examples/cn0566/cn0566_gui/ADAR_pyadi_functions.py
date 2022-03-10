# ADAR_functions.py 

import numpy as np

def ADAR_init(beam):
    # Initialize the ADAR1000
    beam.reset()                       #Performs a soft reset of the device (writes 0x81 to reg 0x00)
    beam._ctrl.reg_write(0x400, 0x55)   #This trims the LDO value to approx. 1.8V (to the center of its range)

    beam.sequencer_enable = False
    beam.beam_mem_enable = False        # RAM control vs SPI control of the beam state, reg 0x38, bit 6.  False sets bit high and SPI control
    beam.bias_mem_enable = False        # RAM control vs SPI control of the bias state, reg 0x38, bit 5.  False sets bit high and SPI control
    beam.pol_state = False              #Polarity switch state, reg 0x31, bit 0. True outputs -5V, False outputs 0V
    beam.pol_switch_enable = False      #Enables switch driver for ADTR1107 switch, reg 0x31, bit 3
    beam.tr_source = 'spi'              #TR source for chip, reg 0x31 bit 2.  'external' sets bit high, 'spi' sets bit low
    beam.tr_spi = 'rx'                  #TR SPI control, reg 0x31 bit 1.  'tx' sets bit high, 'rx' sets bit low
    beam.tr_switch_enable = True        #Switch driver for external switch, reg0x31, bit 4
    beam.external_tr_polarity = True    #Sets polarity of TR switch compared to TR state of ADAR1000.  True outputs 0V in Rx mode

    beam.rx_vga_enable = True           #Enables Rx VGA, reg 0x2E, bit 0.  
    beam.rx_vm_enable = True            #Enables Rx VGA, reg 0x2E, bit 1.  
    beam.rx_lna_enable = True           #Enables Rx LNA, reg 0x2E, bit 2.  
    beam.rx_lna_bias_current = 8        #Sets the LNA bias to the middle of its range
    beam.rx_vga_vm_bias_current = 22    #Sets the VGA and vector modulator bias. 

# Tx is not an option for Phaser ADAR1000, so we can comment this out
#     beam.tx_vga_enable = True           #Enables Tx VGA, reg 0x2F, bit0
#     beam.tx_vm_enable = True            #Enables Tx Vector Modulator, reg 0x2F, bit1
#     beam.tx_pa_enable = True            #Enables Tx channel drivers, reg 0x2F, bit2
#     beam.tx_pa_bias_current = 6         #Sets Tx driver bias current
#     beam.tx_vga_vm_bias_current = 22    #Sets Tx VGA and VM bias.  
    
def ADAR_update_Rx(beam):
    beam.latch_rx_settings()  # Loads Rx vectors from SPI.  Writes 0x01 to reg 0x28.

def ADAR_update_Tx(beam):
    beam.latch_tx_settings()  # Loads Tx vectors from SPI.  Writes 0x02 to reg 0x28.
    
def ADAR_set_mode(beam, mode):
    if mode == "rx":
        # Configure the device for Rx mode
        beam.mode = "rx"   # Mode of operation, bit 5 of reg 0x31. "rx", "tx", or "disabled"
        #print("When TR pin is low, ADAR1000 is in Rx mode.")
        #beam._ctrl.reg_write(0x031, 180)   #Enables T/R switch control.  When TR is low, ADAR1000 is Rx mode
        SELF_BIASED_LNAs = True
        if SELF_BIASED_LNAs:
            beam.lna_bias_out_enable = False    # Allow the external LNAs to self-bias
        else:
            beam.lna_bias_on = -0.7       # Set the external LNA bias
        # Enable the Rx path for each channel
        for channel in beam.channels:
            channel.rx_enable = True  

    # Configure the device for Tx mode -- which is obviously not used on Phaser
    else:
        beam.mode = "tx"   # Mode of operation, bit 5 of reg 0x31. "rx", "tx", or "disabled"
        # Enable the Tx path for each channel and set the external PA bias
        for channel in beam.channels:
            channel.tx_enable = True
            channel.pa_bias_on = -2
        
        
def ADAR_set_Taper(array, Gain1, Gain2, Gain3, Gain4, Gain5, Gain6, Gain7, Gain8):
    array.elements.get(1).rx_gain=Gain1
    array.elements.get(1).rx_attenuator=not bool(Gain1)  #if Gainx=0, then also click in the 20dB attenuator (i.e. set rx_attenuator to True)
    array.elements.get(2).rx_gain=Gain2
    array.elements.get(2).rx_attenuator=not bool(Gain2)
    array.elements.get(3).rx_gain=Gain3
    array.elements.get(3).rx_attenuator=not bool(Gain3)
    array.elements.get(4).rx_gain=Gain4
    array.elements.get(4).rx_attenuator=not bool(Gain4)
    array.elements.get(5).rx_gain=Gain5
    array.elements.get(5).rx_attenuator=not bool(Gain5)
    array.elements.get(6).rx_gain=Gain6
    array.elements.get(6).rx_attenuator=not bool(Gain6)
    array.elements.get(7).rx_gain=Gain7
    array.elements.get(7).rx_attenuator=not bool(Gain7)
    array.elements.get(8).rx_gain=Gain8
    array.elements.get(8).rx_attenuator=not bool(Gain8)
    array.latch_rx_settings()

def ADAR_set_Phase(array, PhDelta, phase_step_size, phase1, phase2, phase3, phase4, phase5, phase6, phase7, phase8):
    step_size = phase_step_size  #2.8125
    array.elements.get(1).rx_phase = ((np.rint(PhDelta*0/step_size)*step_size) + phase1) % 360
    array.elements.get(2).rx_phase = ((np.rint(PhDelta*1/step_size)*step_size) + phase2) % 360
    array.elements.get(3).rx_phase = ((np.rint(PhDelta*2/step_size)*step_size) + phase3) % 360
    array.elements.get(4).rx_phase = ((np.rint(PhDelta*3/step_size)*step_size) + phase4) % 360
    array.elements.get(5).rx_phase = ((np.rint(PhDelta*4/step_size)*step_size) + phase5) % 360
    array.elements.get(6).rx_phase = ((np.rint(PhDelta*5/step_size)*step_size) + phase6) % 360
    array.elements.get(7).rx_phase = ((np.rint(PhDelta*6/step_size)*step_size) + phase7) % 360
    array.elements.get(8).rx_phase = ((np.rint(PhDelta*7/step_size)*step_size) + phase8) % 360
    array.latch_rx_settings()

def load_gain_cal(self, filename='gain_cal_val.pkl'):
    """ Load gain calibrated value, if not calibrated set all channel gain to maximum.
        parameters:
            filename: type=string
                      Provide path of gain calibration file
    """
    try:
        with open(filename, 'rb') as file1:
            self.gcal = pickle.load(file1)  # Load gain cal values
    except:
        print("file not found, loading default (all gain at maximum)")
        self.gcal = [127, 127, 127, 127, 127, 127, 127, 127] # .append(0x7F)

def load_phase_cal(self, filename='phase_cal_val.pkl'):
    """ Load phase calibrated value, if not calibrated set all channel phase correction to 0.
        parameters:
            filename: type=string
                      Provide path of phase calibration file
    """

    try:
        with open(filename, 'rb') as file:
            self.pcal = pickle.load(file)  # Load gain cal values
    except:
        print("file not found, loading default (no phase shift)")
        self.pcal = [0, 0, 0, 0, 0, 0, 0, 0] # .append(0)  # if it fails load default value i.e. 0