def not_found_exception(obj: str):
	from fastapi import HTTPException
	return HTTPException(status_code=404, detail=f'{obj} not found')
