class Project():
    def __init__(self, total_steps=4, levers=4, current_step=0):
        self.levers = levers
        self.current_step=0
        self.sequence={}
        self.total_steps=total_steps
    
    def get_sequence(self, step):
        return self.sequence[step]
    
    def get_next_sequence(self):
        self.current_step = self.current_step+1
        if self.current_step == self.total_steps:
            self.current_step = 0
        return self.sequence[self.current_step]
    
    def get_previous_sequence(self):
        self.current_step = self.current_step-1
        if self.current_step < 0:
            self.current_step = self.total_steps-1
        return self.sequence[self.current_step]
    
    def initialize(self):
        for step in range(self.total_steps):
            self.sequence[step] = [0 for x in range(self.levers)]