class AuthenticationError(Exception):
    """인증 실패 예외"""
    def __init__(self, message="인증이 필요합니다."):
        self.message = message
        super().__init__(self.message)

class AuthorizationError(Exception):
    """권한 부족 예외"""
    def __init__(self, message="권한이 없습니다."):
        self.message = message
        super().__init__(self.message)

class DatabaseConnectionError(Exception):
    """데이터베이스 연결 실패"""
    def __init__(self, message="데이터베이스 연결에 실패했습니다."):
        self.message = message
        super().__init__(self.message)

class DataNotFoundError(Exception):
    """데이터가 존재하지 않을 때"""
    def __init__(self, message="데이터를 찾을 수 없습니다."):
        self.message = message
        super().__init__(self.message)

class DataConflictError(Exception):
    """중복 데이터 존재"""
    def __init__(self, message="이미 존재하는 데이터입니다."):
        self.message = message
        super().__init__(self.message)

class ValidationError(Exception):
    """입력값 유효성 검사 실패"""
    def __init__(self, message="입력값이 잘못되었습니다."):
        self.message = message
        super().__init__(self.message)

class FileUploadError(Exception):
    """파일 업로드 실패"""
    def __init__(self, message="파일 업로드에 실패했습니다."):
        self.message = message
        super().__init__(self.message)

class InvalidFileFormatError(Exception):
    """잘못된 파일 포맷"""
    def __init__(self, message="지원하지 않는 파일 형식입니다."):
        self.message = message
        super().__init__(self.message)

class InvalidJsonFormatError(Exception):
    """잘못된 JSON 포맷"""
    def __init__(self, message="잘못된 JSON 형식입니다. JSON 객체를 보내주세요."):
        self.message = message
        super().__init__(self.message)