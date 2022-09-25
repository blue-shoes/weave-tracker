class Project():
    def __init__(self, total_steps, levers=4, current_step=0):
        self.levers = levers
        self.current_step=0
        self.sequence=[]
        self.total_steps=total_steps
    
    def add_sequence(self, seq):
        self.sequence.append(seq)
    
    def get_sequence(self, step):
        self.sequence[step]
    
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