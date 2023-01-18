class Borrower():
    '''
    A Class that manage Library borrower via name id and if it was 
    student or teacher beacuse of diffrent borrow period and cost
    '''
    def __init__(self,name:str , id:int , is_student:bool , \
                                                    is_teacher:bool) -> None:
        self.b_name = name
        self.b_id = id
        self.is_student = is_student
        self.is_teacher = is_teacher
        self.charges = 0 # Added for simplicity
    # a class method that work as constructor for students that borrow a book
    @classmethod
    def borrower_student(cls,name:str , id:int):
        return cls(name,id,True,False)
    # a class method that work as constructor for teachers that borrow a book
    @classmethod
    def borrower_teacher(cls, name: str , id : int):
        return cls(name,id,False,True)
    #Object printer that return a string of all info in every object we create
    def __repr__(self) -> str:
        out_put = f"Borrower Name: {self.b_name}\n"+\
                  f"Borrower ID: {self.b_id}\n"
        if self.is_student:
            out_put += f"Borrower is Student"
        elif self.is_teacher:
            out_put += f"Borrower is Teacher"
        return out_put

    