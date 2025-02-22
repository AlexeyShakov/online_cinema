async def prepare_data_after_elastic(data: dict, pagination_data: dict) -> dict:
    """
    Избавляемся от лишней вложенности(_source) и добавляем информацию о метаданных
    """
    result = {"meta": {"pagination": pagination_data}}
    if data:
        result["data"] = [el["_source"] for el in data]
    else:
        result["data"] = []
    return result