#!/usr/bin/env python3
"""6.009 Lab 6 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS

def update_formula(formula, variable, value):
    
    """
    Takes in a cnf formula, a variable in that formula, and a value.
    Returns a new formula after updating the input variable to be the input value.
    """
    result = []
    for clause in formula: 
            if (variable, not value) in clause:
                if len(clause) == 1:
                    return None  
                else:
                    clause_copy = clause.copy() 
                    clause_copy.remove((variable, not value))
                    result.append(clause_copy)
                continue
            elif (variable, value) not in clause:
                result.append(clause)  
    return result
        
def find_variables(formula):
    """ 
    takes in a formula and returns all the variables in that formula.
    """
    variables = set() 
    for clause in formula:
        for literal in clause:
            variables.add(literal[0])
    
    return list(variables) 

def find_combinations(students, capacity, result=None):
   """ 
   Takes in a list of (student_room names, False) tuples and returns a list containing
   all combinations of the former list of students for the capacity of the room.
   """

   if result == None:
       result = []
       
   if len(result) == capacity:  
       return [result]
   
   combinations = []
   for index, student in enumerate(students):
       new_result = result.copy()
       new_result.append(student)
       combinations += find_combinations(students[index+1:], capacity, new_result)
       
   return combinations
    
def create_name(student_name, room_name):
    """  Takes in a student name and a room name returns a student_room name.
    """
    return str(student_name) + "_" + str(room_name) 

def generate_rule1(preferences_map, capacities_map):
    """ Takes in student preferences and room capacities to return a formula
        meeting the 'all students are in a room of their preference' constraint.
    """
    
    formula = []
    for student in preferences_map.keys():
        clause = []
        for room in capacities_map.keys():
            if room in preferences_map[student]:
                clause.append((create_name(student, room), True))
        formula.append(clause)
        
    return formula

def generate_rule2(preferences_map, capacities_map):
    """ Takes in student preferences and room capacities to return a formula
        meeting the 'all students are in at most one room' constraint.
    """
    
    formula = []
    for student in preferences_map.keys():
        prev = list(capacities_map.keys())[len(list(capacities_map.keys())) - 1]
        for room in capacities_map.keys():
            formula.append([(create_name(student, room), False), (create_name(student, prev), False)])
            prev = room 
            
    return formula

def generate_rule3(preferences_map, capacities_map):
    """ Takes in student preferences and room capacities to return a formula
        meeting the 'no room has more students than the allowed capacity' constraint.
    """
    
    formula = []
    for room in capacities_map.keys():    
        students = []
        for student in preferences_map.keys():
            students.append((create_name(student, room), False)) 
        if capacities_map[room] < len(preferences_map):
            for i in range(capacities_map[room] + 1, len(preferences_map) + 1):
               formula += find_combinations(students, i) 
    return formula

def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """ 
    out = {}
    
    if formula == None:
        return None
    if formula == []:
        return {} 
    
    variables = find_variables(formula)
    for variable in variables: 
        if variable not in out.keys():
            out[variable] = False
            
    for clause in formula:
        if len(clause) == 1:
            variable = clause[0][0]
            value = clause[0][1]
            if variable in variables:
                variables.remove(variable)
                out[variable] = value
                formula = update_formula(formula, variable, value)
                if variables == []:
                    return None
                if formula == None:
                    return None
            
    variable = variables[0]
    
    if update_formula(formula, variable, True) == []:
        if out != {}:
            out[variable] = True
            return out
        else:
            return {variable: True}
    if update_formula(formula, variable, False) == []:
        if out != {}:
            out[variable] = False
            return out
        else:
            return {variable: False}
    
    new_formula = update_formula(formula, variable, True)
    assignment = satisfying_assignment(new_formula)
    
    if assignment is not None:
        out[variable] = True
        out.update(assignment)
        return out
    
    new_formula = update_formula(formula, variable, False) 
    assignment = satisfying_assignment(new_formula)
    
    if assignment is not None:
        out[variable] = False
        out.update(assignment)
        return out 
    
    return None
    

def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                     for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up

    We assume no student or room names contain underscores.
    """
    rule1 = generate_rule1(student_preferences, room_capacities)
    rule2 = generate_rule2(student_preferences, room_capacities)
    rule3 = generate_rule3(student_preferences, room_capacities)
    
    return rule1 + rule2 + rule3


if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
