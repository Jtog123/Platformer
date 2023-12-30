            if self.velocity[1] < 0:
                self.can_jump = False
            elif self.velocity[1] == 0:
                self.can_jump = True