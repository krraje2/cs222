from network.service import AbstractService


class GpaService(AbstractService):
    def validate_input(self, year, semester, subjectCode, courseNumber, crn):
        if year < 2004:
            raise ValueError("year must be > 2004 for CIS Data Explorer")
    