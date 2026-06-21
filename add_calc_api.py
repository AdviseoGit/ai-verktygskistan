import re

with open("/data/workspace/projects/ai-verktygskistan/main.py", "r") as f:
    content = f.read()

if "/api/calc-data" not in content:
    api_code = """
class CalcDataIn(BaseModel):
    employees: int
    salary: int
    industry: str
    saved_value: int

@app.post("/api/calc-data")
async def capture_calc_data(data: CalcDataIn):
    import os
    # Log to a simple file for now to build the data moat
    file_path = "data_moat_calc.csv"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("employees,salary,industry,saved_value\\n")
    with open(file_path, "a") as f:
        f.write(f"{data.employees},{data.salary},{data.industry},{data.saved_value}\\n")
    return {"status": "success"}
"""
    # Insert before the app.mount line
    content = content.replace('app.mount("/static", StaticFiles(directory="static"), name="static")', f'{api_code}\napp.mount("/static", StaticFiles(directory="static"), name="static")')

    with open("/data/workspace/projects/ai-verktygskistan/main.py", "w") as f:
        f.write(content)
    print("Added /api/calc-data endpoint.")
else:
    print("Endpoint already exists.")
