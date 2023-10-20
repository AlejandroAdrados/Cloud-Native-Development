from entity.assignment import Assignment, State, Type
from statistics import get_profile


def test_grade_correct_assignment():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    state = State.CORRECT
    assignment = Assignment(content=content, state=state, type=type_)
    grades = get_profile.compute_grades([assignment.get_dict()])
    assert grades[type_.value]["grade"] == 1


def test_grade_multiple_correct_assignments():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    state = State.CORRECT
    a = Assignment(content=content, state=state, type=type_)
    assignments = [a.get_dict() for _ in range(3)]
    grades = get_profile.compute_grades(assignments)
    assert grades[type_.value]["grade"] == 1


def test_grade_incorrect_assignment():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    state = State.INCORRECT
    assignment = Assignment(content=content, state=state, type=type_)
    grades = get_profile.compute_grades([assignment.get_dict()])
    assert grades[type_.value]["grade"] == 5


def test_grade_correct_and_incorrect_assignment():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    state_correct = State.CORRECT
    state_incorrect = State.INCORRECT
    assignment_correct = Assignment(
        content=content, state=state_correct, type=type_
    )
    assignment_incorrect = Assignment(
        content=content, state=state_incorrect, type=type_
    )
    assignments = [assignment_correct, assignment_incorrect]
    grades = get_profile.compute_grades([a.get_dict() for a in assignments])
    assert grades[type_.value]["grade"] == 4


def test_grade_boundary_1_lower():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    correct_assigments = [
        Assignment(State.CORRECT, Type.ADDITION, content).get_dict()
        for i in range(88)
    ]
    incorrect_assignments = [
        Assignment(State.INCORRECT, Type.ADDITION, content).get_dict()
        for i in range(12)
    ]
    grades = get_profile.compute_grades(
        correct_assigments + incorrect_assignments
    )
    assert grades[type_.value]["grade"] == 1


def test_grade_boundary_2_upper():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    correct_assigments = [
        Assignment(State.CORRECT, Type.ADDITION, content).get_dict()
        for i in range(87)
    ]
    incorrect_assignments = [
        Assignment(State.INCORRECT, Type.ADDITION, content).get_dict()
        for i in range(13)
    ]
    grades = get_profile.compute_grades(
        correct_assigments + incorrect_assignments
    )
    assert grades[type_.value]["grade"] == 2


def test_grade_boundary_2_lower():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    correct_assigments = [
        Assignment(State.CORRECT, Type.ADDITION, content).get_dict()
        for i in range(75)
    ]
    incorrect_assignments = [
        Assignment(State.INCORRECT, Type.ADDITION, content).get_dict()
        for i in range(25)
    ]
    grades = get_profile.compute_grades(
        correct_assigments + incorrect_assignments
    )
    assert grades[type_.value]["grade"] == 2


def test_grade_boundary_3_upper():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    correct_assigments = [
        Assignment(State.CORRECT, Type.ADDITION, content).get_dict()
        for _ in range(74)
    ]
    incorrect_assignments = [
        Assignment(State.INCORRECT, Type.ADDITION, content).get_dict()
        for _ in range(26)
    ]
    grades = get_profile.compute_grades(
        correct_assigments + incorrect_assignments
    )
    assert grades[type_.value]["grade"] == 3


def test_grade_boundary_3_lower():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    correct_assigments = [
        Assignment(State.CORRECT, Type.ADDITION, content).get_dict()
        for _ in range(60)
    ]
    incorrect_assignments = [
        Assignment(State.INCORRECT, Type.ADDITION, content).get_dict()
        for _ in range(40)
    ]
    grades = get_profile.compute_grades(
        correct_assigments + incorrect_assignments
    )
    assert grades[type_.value]["grade"] == 3


def test_grade_boundary_4_upper():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    correct_assigments = [
        Assignment(State.CORRECT, Type.ADDITION, content).get_dict()
        for _ in range(59)
    ]
    incorrect_assignments = [
        Assignment(State.INCORRECT, Type.ADDITION, content).get_dict()
        for _ in range(41)
    ]
    grades = get_profile.compute_grades(
        correct_assigments + incorrect_assignments
    )
    assert grades[type_.value]["grade"] == 4


def test_grade_boundary_4_lower():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    correct_assigments = [
        Assignment(State.CORRECT, Type.ADDITION, content).get_dict()
        for _ in range(50)
    ]
    incorrect_assignments = [
        Assignment(State.INCORRECT, Type.ADDITION, content).get_dict()
        for _ in range(50)
    ]
    grades = get_profile.compute_grades(
        correct_assigments + incorrect_assignments
    )
    assert grades[type_.value]["grade"] == 4


def test_grade_boundary_5_upper():
    content = [i for i in range(5)]
    type_ = Type.ADDITION
    correct_assigments = [
        Assignment(State.CORRECT, Type.ADDITION, content).get_dict()
        for _ in range(49)
    ]
    incorrect_assignments = [
        Assignment(State.INCORRECT, Type.ADDITION, content).get_dict()
        for _ in range(51)
    ]
    grades = get_profile.compute_grades(
        correct_assigments + incorrect_assignments
    )
    assert grades[type_.value]["grade"] == 5


def test_grade_multiple_types():
    # 50 addition exercises: 45 correct, 5 incorrect --> grade 1 (0.9 ratio)
    addition_assignments = [
        Assignment(
            State.CORRECT, Type.ADDITION, [i for i in range(5)]
        ).get_dict()
        for _ in range(45)
    ] + [
        Assignment(
            State.INCORRECT, Type.ADDITION, [i for i in range(5)]
        ).get_dict()
        for _ in range(5)
    ]

    # 50 multiplication exercises: 25 c, 25 inc--> grade 4 (0.5 ratio)
    multiplication_assignments = [
        Assignment(
            State.CORRECT, Type.MULTIPLICATION, [i for i in range(5)]
        ).get_dict()
        for _ in range(25)
    ] + [
        Assignment(
            State.INCORRECT, Type.MULTIPLICATION, [i for i in range(5)]
        ).get_dict()
        for _ in range(25)
    ]

    assignments = addition_assignments + multiplication_assignments
    results = get_profile.compute_grades(assignments)
    assert results[Type.ADDITION.value]["grade"] == 1
    assert results[Type.MULTIPLICATION.value]["grade"] == 4


def test_get_grade_a():
    grade = get_profile.get_grade(100, 1)
    assert grade == 1


def test_get_grade_f():
    grade = get_profile.get_grade(1, 100)
    assert grade == 5


def test_get_grad_div_by_one():
    grade = get_profile.get_grade(1, 0)
    assert grade == 1
