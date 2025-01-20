from uuid import UUID

#all constants are ordered from higher to lower importance
#organization types accepted by the database
ORGANIZATION_TYPES = ["university", "institute", "department"]
ACADEMIC_TITLES = ["Prof.", "DSc", "PhD", "DVM", "MSc", "BSc"]
FULL_ACADEMIC_TITLES = [ "Professor", "Doctor of Science", "Doctor of Philosophy", "Doctor of Veterinary Medicine", "Master of Science", "Bachelor of Science" ]


#namespace for id generation
NAMESPACE_BUT = UUID('348ed230-6578-4a00-96c8-a8caf0251c6d')
