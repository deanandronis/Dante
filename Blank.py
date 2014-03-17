        #check and apply slide
        if self.sliding:
            self.arrowkey_enabled = False
            self.xvel -= self.xvel/10
            if abs(self.xvel) < 1.5: 
                self.xvel = 0
                self.sliding = False
                self.arrowkey_enabled = True
                self.can_damage = True
                
        if self.decelerate and not self.sliding:
            if self.sprinting:
                if self.xvel < -0.3:
                        self.xvel += 0.087
                elif self.xvel > 0.3:
                    self.xvel -= 0.087
                else: self.xvel = 0
            else:
                if self.xvel < -0.267:
                        self.xvel += 0.153
                elif self.xvel > 0.267:
                    self.xvel -= 0.153
                else: self.xvel = 0
            
        #calculate acceleration
        if not self.sliding and not self.decelerate and not self.sprinting:
            if self.xvel < 0:
                if self.xvel > -2.67: 
                    self.xvel += self.accel
                    if self.accel < 0: self.accel -= 0.006
                    elif self.accel > 0: self.accel += 0.006
                else: 
                    if self.xvel < -2.67:
                        self.xvel += 0.107
                    else: self.xvel = 0

            elif self.xvel > 0:
                if self.xvel < 2.67: 
                    self.xvel += self.accel
                    if self.accel > 0: self.accel += 0.006
                    elif self.accel < 0: self.accel -= 0.006
                else: 
                    if self.xvel > 2.67:
                        self.xvel -= 0.107
                    else: self.xvel = 0
                        

        if not self.sliding and not self.decelerate and self.sprinting:
            if self.xvel < 0:
                if self.xvel > -5: 
                    self.xvel += self.accel
                    if self.accel < 0: self.accel -= 0.013
                    elif self.accel > 0: self.accel += 0.006
                else: 
                    self.accel = 0
            elif self.xvel > 0:
                if self.xvel < 5: 
                    self.xvel += self.accel
                    if self.accel > 0: self.accel += 0.013
                    elif self.accel < 0: self.accel -= 0.006
                else: 
                    self.accel = 0        