import re

with open("/data/workspace/projects/ai-verktygskistan/main.py", "r") as f:
    content = f.read()

new_content = content.replace("""class CalcDataIn(BaseModel):
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
    return {"status": "success"}""", """class CalcDataIn(BaseModel):
    employees: int
    salary: int
    industry: str
    saved_value: int

@app.post("/api/calc-data")
async def capture_calc_data(data: CalcDataIn, db: Session = Depends(get_db)):
    from models import CalcData
    new_calc = CalcData(
        employees=data.employees,
        salary=data.salary,
        industry=data.industry,
        saved_value=data.saved_value
    )
    db.add(new_calc)
    db.commit()
    
    import os
    # Fallback log to a simple file as well to build the data moat easily
    file_path = "data_moat_calc.csv"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("employees,salary,industry,saved_value\\n")
    with open(file_path, "a") as f:
        f.write(f"{data.employees},{data.salary},{data.industry},{data.saved_value}\\n")
        
    return {"status": "success"}""")

with open("/data/workspace/projects/ai-verktygskistan/main.py", "w") as f:
    f.write(new_content)
