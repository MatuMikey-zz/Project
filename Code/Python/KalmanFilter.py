

class KalmanFilter:
    
    def __init__(self, errorMeasurement, errorEstimate, q):
        self.errorMeasurement = errorMeasurement
        self.errorEstimate = errorEstimate
        self.q = q #covariance error
        self.lastEstimate = 25.0 
        self.currentEstimate = 25.0
        
    def updateEstimate(self,measurement):
        kGain = self.errorEstimate/(self.errorEstimate+self.errorMeasurement)
        self.currentEstimate = self.lastEstimate + kGain*(measurement-self.lastEstimate)
        self.errorEstimate = (1.0-kGain)*self.errorEstimate + abs(self.lastEstimate-self.currentEstimate)*self.q
        self.lastEstimate=self.currentEstimate
        return self.currentEstimate
    
    def setLastEstimate(self,val):
        self.lastEstimate = val
        self.currentEstimate = val